import os
import qrcode
import sqlite3
from flask import Flask, request, send_file, redirect

app = Flask(__name__)

# -------- DATABASE SETUP --------
def get_db():
    return sqlite3.connect("qr.db")

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_url TEXT,
            scan_count INTEGER DEFAULT 0
        )
    """)
    db.commit()
    db.close()

init_db()

# -------- GENERATE QR --------
@app.route("/create")
def create_qr():
    target_url = request.args.get("url")

    if not target_url:
        return "Please provide url", 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO qr_codes (target_url) VALUES (?)",
        (target_url,)
    )
    qr_id = cursor.lastrowid
    db.commit()
    db.close()

   qr_data = f"https://qr-api-md89.onrender.com/scan/{qr_id}"

    img = qrcode.make(qr_data)
    img.save("qr.png")

    return send_file("qr.png", mimetype="image/png")

# -------- SCAN QR --------
@app.route("/scan/<int:qr_id>")
def scan_qr(qr_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT target_url, scan_count FROM qr_codes WHERE id = ?",
        (qr_id,)
    )
    row = cursor.fetchone()

    if not row:
        return "Invalid QR", 404

    target_url, scan_count = row
    cursor.execute(
        "UPDATE qr_codes SET scan_count = ? WHERE id = ?",
        (scan_count + 1, qr_id)
    )

    db.commit()
    db.close()

    return redirect(target_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)






