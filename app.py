from flask import Flask, render_template, send_file
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import os
import io

app = Flask(__name__)

# ===============================
# MENU DATA (CHANGE ITEMS HERE)
# ===============================
MENU_ITEMS = [
    {"id": 1, "name": "Veg Burger", "price": 120},
    {"id": 2, "name": "Chicken Burger", "price": 180},
    {"id": 3, "name": "Paneer Pizza", "price": 240},
    {"id": 4, "name": "Chicken Pizza", "price": 280},
    {"id": 5, "name": "French Fries", "price": 90},
    {"id": 6, "name": "Veg Momos", "price": 110},
    {"id": 7, "name": "Chicken Momos", "price": 150},
    {"id": 8, "name": "Cold Coffee", "price": 110},
    {"id": 9, "name": "Chocolate Milkshake", "price": 140},
]

GST_RATE = 0.18

# ===============================
# MENU PAGE
# ===============================
@app.route("/")
@app.route("/menu")
def menu():
    return render_template("menu.html", menu=MENU_ITEMS, gst=GST_RATE)

# ===============================
# QR GENERATION (THIS IS YOUR CODE)
# ===============================
@app.route("/qr")
def generate_qr():

    # 🔗 THIS IS THE LINK QR WILL OPEN
    qr_url = "https://qr-api-md89.onrender.com/menu"  
    # 👆 CHANGE THIS AFTER DEPLOY IF NEEDED

    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_H,  # REQUIRED for logo
        box_size=12,
        border=4,
    )

    qr.add_data(qr_url)
    qr.make(fit=True)

    # 🎨 CHANGE QR COLORS HERE
    qr_img = qr.make_image(
        fill_color="white",   # QR dots color
        back_color="#0a3d91"  # Blue background
    ).convert("RGBA")

    # ===============================
    # ADD LOGO IN CENTER
    # ===============================
    logo_path = os.path.join(app.root_path, "static", "logo.png")

    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")

        qr_width, qr_height = qr_img.size

        # 🔽 CHANGE LOGO SIZE HERE
        logo_size = qr_width // 5
        logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

        # ⚪ WHITE BACKGROUND BEHIND LOGO
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
    # RETURN QR IMAGE
    # ===============================
    img_io = io.BytesIO()
    qr_img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)
