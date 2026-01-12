from flask import Flask, send_file, render_template
import qrcode
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "QR Menu App is running"

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/qr")
def generate_qr():

    menu_url = "https://qr-api-md89.onrender.com/menu"

    # 🎨 QR COLORS (CHANGE HERE)
    qr_foreground_color = "white"
    qr_background_color = "blue"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # REQUIRED FOR LOGO
        box_size=12,
        border=4
    )

    qr.add_data(menu_url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=qr_foreground_color,
        back_color=qr_background_color
    ).convert("RGBA")

    # 🖼 CENTER LOGO
    logo_path = os.path.join(app.root_path, "static", "logo.png")

   if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert("RGBA")

    qr_width, qr_height = qr_img.size

    # 🔽 MUCH SMALLER LOGO
    logo_size = qr_width // 6
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # ⚪ White background behind logo
    bg_size = logo_size + 20
    background = Image.new("RGBA", (bg_size, bg_size), "white")

    bg_pos = ((bg_size - logo_size) // 2, (bg_size - logo_size) // 2)
    background.paste(logo, bg_pos, logo)

    pos = (
        (qr_width - bg_size) // 2,
        (qr_height - bg_size) // 2
    )

    qr_img.paste(background, pos, background)


    img_io = io.BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run()

