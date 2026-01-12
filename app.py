from flask import Flask, send_file, render_template, request
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "QR Menu App is running"

# ---------------- MENU PAGE ----------------
@app.route("/menu")
def menu():
    return render_template("menu.html")

# ---------------- QR GENERATOR ----------------
@app.route("/qr")
def generate_qr():

    # 🔗 THIS IS THE PAGE YOUR QR WILL OPEN
    menu_url = "https://qr-api-md89.onrender.com/menu"

    # 🎨 ===============================
    # 🎨 QR COLORS — CHANGE HERE ONLY
    # 🎨 ===============================
    qr_foreground_color = "red"     # examples: "black", "blue", "#ff5733"
    qr_background_color = "blue"     # examples: "white", "black", "#f2f2f2"

    # Create QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4
    )

    qr.add_data(menu_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=qr_foreground_color,
        back_color=qr_background_color
    ).convert("RGBA")

    # 🖼 ===============================
    # 🖼 LOGO (OPTIONAL)
    # 🖼 ===============================
    logo_path = os.path.join(app.root_path, "static", "logo.png")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))

        position = (
            (qr_width - logo_size) // 2,
            (qr_height - logo_size) // 2
        )

        qr_img.paste(logo, position, mask=logo)

    # 📤 SEND IMAGE
    img_io = io.BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()

