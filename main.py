#main.py
from flask import Flask, jsonify, request
from db import fetch_data, add_data

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def songs():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        add_data(request.get_json())
        return 'Song Added'

    return fetch_data()    

if __name__ == '__main__':
    app.run()
