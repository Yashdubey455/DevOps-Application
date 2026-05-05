from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import time

app = Flask(__name__)
CORS(app)

# 🔥 DB CONNECTION WITH RETRY (IMPORTANT)
def connect_db():
    while True:
        try:
            conn = psycopg2.connect(
                host="postgres",      # service name
                database="testdb",
                user="postgres",
                password="postgres"
            )
            print("✅ Connected to DB")
            return conn
        except Exception as e:
            print("⏳ Waiting for DB...", e)
            time.sleep(2)

# connect once at startup
conn = connect_db()
cur = conn.cursor()

# create table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT
)
""")
conn.commit()


# 🔹 GET USERS
@app.route("/users", methods=["GET"])
def get_users():
    cur.execute("SELECT name FROM users")
    users = cur.fetchall()
    return jsonify(users)


# 🔹 ADD USER
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Name required"}), 400

    cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    conn.commit()

    return jsonify({"status": "ok"})


# 🔹 HEALTH CHECK (VERY USEFUL FOR K8s)
@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)