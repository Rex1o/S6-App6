import asyncio
from flask import Flask, jsonify, request

app = Flask(__name__)

# POST
@app.route('/exit', methods=['POST'])
def add_exit():
    new_item = request.json
    print(new_item)
    return jsonify(new_item), 201

# POST
@app.route('/enter', methods=['POST'])
def add_entry():
    new_item = request.json
    print(new_item)
    return jsonify(new_item), 201 # Add to database

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

