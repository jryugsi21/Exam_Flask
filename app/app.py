from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "DevOps App")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/")
def home():
    status = "OK"
    try:
        conn = get_connection()
        conn.close()
    except:
        status = "ERROR"

    return jsonify({
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "db_status": status
    })

@app.route("/productos")
def productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    rows = cur.fetchall()

    result = []
    for r in rows:
        result.append({
            "id": r[0],
            "nombre": r[1],
            "precio": r[2],
            "stock": r[3]
        })

    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)