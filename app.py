from flask import Flask, jsonify, abort, make_response
import os
import scraping
from flask_cors import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/200ok/www/service-account-file.json"

app = Flask(__name__)
CORS(app, supports_credentials = True)

@app.route('/comments/<id>', methods=['GET'])
def get_comments(id):
    data = scraping.comments(id)
    return jsonify({ 'data': data })

@app.route('/searchResIds/<q>', methods=['GET'])
def get_searchResIds(q):
    res = scraping.getSearchResIds(q)
    return jsonify({ 'data': res })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug = True)

