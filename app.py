from flask import Flask, request, send_file, redirect
import qrcode
import sqlite3
import os
from PIL import Image

app = Flask(__name__)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("qr.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_url TEXT NOT NULL
        )
    """)
    db.commit()
    db.close()

init_db()

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Custom QR API is running 🚀"

# ---------------- CREATE QR ----------------
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

    # 👉 THIS IS YOUR LIVE QR LINK
    qr_data = f"https://qr-api-md89.onrender.com/scan/{qr_id}"

    # --------- QR STYLE SETTINGS (CHANGE HERE) ---------
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color="#blue",  # 🔴 CHANGE COLOR HERE
        back_color="white"
    ).convert("RGBA")

    # --------- ADD LOGO ---------
    logo = Image.open("static/logo.png")

    qr_width, qr_height = img.size
    logo_size = qr_width // 4

    logo = logo.resize((logo_size, logo_size))

    logo_position = (
        (qr_width - logo_size) // 2,
        (qr_height - logo_size) // 2
    )

    img.paste(logo, logo_position, mask=logo)

    img.save("qr.png")

    return send_file("qr.png", mimetype="image/png")

# ---------------- SCAN QR ----------------
@app.route("/scan/<int:qr_id>")
def scan_qr(qr_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT target_url FROM qr_codes WHERE id = ?",
        (qr_id,)
    )
    row = cursor.fetchone()
    db.close()

    if row is None:
        return "QR not found", 404

    return redirect(row["target_url"])

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

