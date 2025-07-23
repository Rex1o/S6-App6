import asyncio
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="main_db",
    user="user",
    password="password",
    host="localhost",  # e.g., 'localhost' or an IP address
    port="5432"  # default is 5432
)

# POST
@app.route('/exit', methods=['POST'])
def add_exit():
    new_item = request.json
    if not new_item or "userID" not in new_item or "roomID" not in new_item:
        return jsonify({"message": "Invalid  data"}), 400

    return jsonify(new_item), 201 # Add to database

# POST
@app.route('/enters', methods=['POST'])
def add_entry():
    new_item = request.json
    if not new_item or "userID" not in new_item or "roomID" not in new_item:
        return jsonify({"message": "Invalid  data"}), 400

    return jsonify(new_item), 201 # Add to database

if __name__ == "__main__":
    cur = conn.cursor()
    app.run(debug=True)

