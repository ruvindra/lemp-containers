from flask import Flask, jsonify
import os
import mysql.connector

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )


def ensure_schema():
    """Create the visits counter table/row if they don't exist yet."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INT PRIMARY KEY,
            count INT NOT NULL DEFAULT 0
        )
    """)
    cur.execute("INSERT IGNORE INTO visits (id, count) VALUES (1, 0)")
    conn.commit()
    cur.close()
    conn.close()


@app.get('/api/health')
def health():
    return {'status': 'ok'}


@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Flask!'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message=row[0])


@app.get('/api/time')
def db_time():
    """Read operation: current MySQL server time."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(server_time=str(row[0]))


@app.post('/api/visits')
def record_visit():
    """Write operation: increment and return the persistent visit counter."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE visits SET count = count + 1 WHERE id = 1")
    conn.commit()
    cur.execute("SELECT count FROM visits WHERE id = 1")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(visits=row[0])


ensure_schema()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)