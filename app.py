from flask import Flask, send_file, render_template
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os

app = Flask(__name__)

# ===============================
# HOME CHECK
# ===============================
@app.route("/")
def home():
    return "QR API is live ✅"

# ===============================
# MENU PAGE (WHAT QR OPENS)
# ===============================
@app.route("/menu")
def menu():
    return render_template("menu.html")

# ===============================
# GENERATE QR CODE
# ===============================
@app.route("/qr")
def generate_qr():
    # 🔗 URL that QR will open
    qr_url = "https://qr-api-md89.onrender.com/menu"

    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,  # REQUIRED for logo
        box_size=12,
        border=4,
    )

    qr.add_data(qr_url)
    qr.make(fit=True)

    # 🎨 CUSTOM QR COLORS (CHANGE HERE)
    qr_img = qr.make_image(
        fill_color="white",   # QR color (black)
        back_color="blue"      # Background
    ).convert("RGBA")

    # ===============================
    # ADD LOGO IN CENTER
    # ===============================
    logo_path = os.path.join(app.root_path, "static", "logo.png")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        qr_width, qr_height = qr_img.size

        # 🔽 Logo size (VERY IMPORTANT)
        logo_size = qr_width // 5
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # ⚪ White padding behind logo
        padding = 20
        bg_size = logo_size + padding

        background = Image.new("RGBA", (bg_size, bg_size), "white")

        pos = ((bg_size - logo_size) // 2, (bg_size - logo_size) // 2)
        background.paste(logo, pos, logo)

        center = (
            (qr_width - bg_size) // 2,
            (qr_height - bg_size) // 2
        )

        qr_img.paste(background, center, background)

    # ===============================
    # SAVE & SEND IMAGE
    # ===============================
    output_path = "qr.png"
    qr_img.save(output_path)

    return send_file(output_path, mimetype="image/png")

# ===============================
# RENDER / GUNICORN ENTRY POINT
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
