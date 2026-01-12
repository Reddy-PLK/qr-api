from flask import Flask, send_file, render_template
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "QR Menu API is running"

# ---------------- MENU ----------------
@app.route("/menu")
def menu():
    return render_template("menu.html")

# ---------------- QR ----------------
@app.route("/qr")
def generate_qr():
    menu_url = "https://qr-api-md89.onrender.com/menu"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )

    qr.add_data(menu_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color="black",
        back_color="white"
    ).convert("RGB")

    # ---------- TRY TO ADD LOGO ----------
    logo_path = os.path.join(app.root_path, "static", "logo.png")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path)

        qr_width, qr_height = qr_img.size
        logo_size = qr_width // 4
        logo = logo.resize((logo_size, logo_size))

        pos = (
            (qr_width - logo_size) // 2,
            (qr_height - logo_size) // 2
        )

        qr_img.paste(logo, pos, mask=logo if logo.mode == "RGBA" else None)

    # ---------- SEND IMAGE ----------
    img_io = io.BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run()
