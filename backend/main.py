from flask import Flask, make_response, jsonify, request
from flask import render_template
from flask_cors import CORS, cross_origin
from tfidf import TFIDF


app = Flask("Library Project Backend")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
tfidf = TFIDF()


def success_message(message):
    return render_template('success.html', message=message), 200


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message=error), 200


@app.route("/", methods=['GET'])
def healthCheck():
    return success_message("Backend is online")


@app.route('/search', methods=['GET'])
def search():
    page = request.args.get('page', default=1, type=int)
    query = request.args.get('query')
    return tfidf.search(query, page)


if __name__ == '__main__':
    app.run()


# TODO:
# Seperate dataframe, preprocessing to seperate file
# Make OPENAI class
# Make BM25 class
# Make Comparator class that outputs:
# query, TFIDF, BM25, OPENAI, Current Library
