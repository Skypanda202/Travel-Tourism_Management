import qrcode
import os

def generate_qr(data, filename):
    if not os.path.exists("static"):
        os.makedirs("static")

    qr = qrcode.make(data)
    qr.save(f"static/{filename}")