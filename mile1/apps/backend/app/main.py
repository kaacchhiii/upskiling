"""Simple Flask backend that connects to PostgreSQL."""

import os
import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)

# Database config — comes from environment variables (set in K8s manifest)
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "appdb"),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "changeme"),
}


def get_db():
    """Get a database connection."""
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create the items table if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


# --- Routes ---

@app.route("/health")
def health():
    """Health check — used by Kubernetes probes."""
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "ok"})
    except Exception:
        return jsonify({"status": "error"}), 503


@app.route("/api/items", methods=["GET"])
def list_items():
    """Return all items."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM items ORDER BY id")
    items = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(items)


@app.route("/api/items", methods=["POST"])
def create_item():
    """Create a new item."""
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name) VALUES (%s) RETURNING id, name", (data["name"],))
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": row[0], "name": row[1]}), 201


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Delete an item."""
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return "", 204


# Start the app
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8000)
