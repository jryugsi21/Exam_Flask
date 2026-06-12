from flask import Flask, render_template, os, psycopg2

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
    alert_class = "success"
    try:
        conn = get_connection()
        conn.close()
    except Exception as e:
        status = f"ERROR: No se pudo conectar a la base de datos. ({e})"
        alert_class = "danger"

    # Pasamos las variables directamente a la plantilla HTML
    return render_template(
        "home.html",
        app_name=APP_NAME,
        version=APP_VERSION,
        status=status,
        alert_class=alert_class
    )

@app.route("/productos")
def productos():
    try:
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

        cur.close()
        conn.close()
        error = None
    except Exception as e:
        result = []
        error = f"Error al consultar la base de datos: {e}"

    # Pasamos la lista de productos y el error (si existe) al HTML
    return render_template("productos.html", productos=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)