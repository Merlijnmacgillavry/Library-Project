from flask import Flask, make_response, jsonify, request
from flask import render_template
from flask_cors import CORS, cross_origin
from tfidf import TFIDF
from BM25 import BM25
import time
import json

app = Flask("Library Project Backend")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
tfidf = TFIDF()
bm25Okapi = BM25(bm_type="Okapi")
bm25L = BM25(bm_type="L")
bm25Plus = BM25(bm_type="Plus")

models = ['tfidf', 'bm25Okapi', 'bm25L', 'bm25Plus']
filters = {

}


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
    return search_model(model, page, query)


if __name__ == '__main__':
    app.run()


# TODO:
# Seperate dataframe, preprocessing to seperate file Done
# Make OPENAI class Fuck you
# Make BM25 class Yessir
# Make Comparator class that outputs:
# query, TFIDF, BM25, OPENAI, Current Library
