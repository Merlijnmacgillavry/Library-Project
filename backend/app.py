from flask import Flask, make_response, jsonify, request
from flask import render_template
from flask_cors import CORS, cross_origin
from libraryProject import BM25, SBERT, TFIDF, PreProcess
from BM25 import BM25
import time
import json
import pandas as pd
from preprocess import lemmatization, remove_stopwords, remove_punctuation
import os

models = ['tfidf', 'bm25Okapi', 'bm25L', 'bm25Plus', 'sbert']
filters = {

}


def data(name):
    return os.path.join(os.path.dirname(__file__), name)


def model(name):
    return os.path.join(os.path.dirname(__file__), 'models', name)


app = Flask("Library Project Backend")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
tfidf = TFIDF(data_name=data('data.csv'), model_name=model('TFIDFmodel.pkl'))
bm25Okapi = BM25(data_name=data('data.csv'),
                 model_name=model('BM25Okapimodel.pkl'))
bm25L = BM25(bm_type="L", data_name=data('data.csv'),
             model_name=model('BM25Lmodel.pkl'))
bm25Plus = BM25(bm_type="Plus", data_name=data('data.csv'),
                model_name=model('BM25Plusmodel.pkl'))
sbert = SBERT()


def success_message(message):
    return render_template('success.html', message=message), 200


def search_model(model, page, query):
    match model:
        case 'bm25Okapi':
            return bm25Okapi.search(query, page)
        case 'bm25L':
            return bm25L.search(query, page)
        case 'bm25Plus':
            return bm25Plus.search(query, page)
        case 'sbert':
            return bm25Plus.search(query, page)
        case _:
            return tfidf.search(query, page)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message=error), 200


@app.route("/", methods=['GET'])
def healthCheck():
    return success_message("Backend is online")


@app.route('/models', methods=['GET'])
def get_models():
    return json.dumps(models)


@app.route('/search', methods=['GET'])
def search():
    model = request.args.get('model', default='tfidf')
    page = request.args.get('page', default=1, type=int)
    query = request.args.get('query')
    query = remove_punctuation(query)
    query = remove_stopwords(query)
    query = lemmatization(query)
    print(query)
    return search_model(model, page, query)


def answer_all(queries):
    tfidf.records_per_page = 5
    bm25Okapi.records_per_page = 5
    bm25L.records_per_page = 5
    bm25Plus.records_per_page = 5

    tfidf_results = []
    bm25Okapi_results = []
    bm25L_results = []
    bm25Plus_results = []

    for query in queries:
        tfidf_results.append(tfidf.search(query, 1))
        bm25Okapi_results.append(bm25Okapi.search(query, 1))
        bm25L_results.append(bm25L.search(query, 1))
        bm25Plus_results.append(bm25Plus.search(query, 1))

    data = {'query': queries, 'tfidf': tfidf_results, 'BM25Okapi': bm25Okapi_results,
            'BM25L_results': bm25L_results, 'BM25Plus_results': bm25Plus_results}

    df = pd.DataFrame(data, columns=[
                      'query', 'tfidf', 'BM25Okapi', 'BM25L_results', 'BM25Plus_results'])

    tfidf.records_per_page = 20
    bm25Okapi.records_per_page = 20
    bm25L.records_per_page = 20
    bm25Plus.records_per_page = 20

    return df


@app.route('/get_results', methods=['POST'])
def get_results():
    data = request.json
    print(data)
    df = answer_all(queries=data['queries'])
    response = make_response(df.to_csv())
    response.headers['Content-Type'] = 'text/csv'
    return response


if __name__ == '__main__':
    app.run()
