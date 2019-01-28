from flask import Flask, jsonify, abort, make_response
import os
from scraping import comments
from flask_cors import *

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/200ok/www/service-account-file.json"

app = Flask(__name__)
CORS(app, supports_credentials = True)

@app.route('/comments', methods=['GET'])
def get_comments():
    data = comments('韓国 日本')
    return jsonify({ 'data': data })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug = True)

