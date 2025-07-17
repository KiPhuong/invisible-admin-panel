from PIL import Image
import pytesseract
import requests
from io import BytesIO

# Lấy ảnh CAPTCHA
cookies = {'session': '...'}  # Thêm cookie nếu cần
resp = requests.get('http://localhost:5000/captcha/image', cookies=cookies)

img = Image.open(BytesIO(resp.content))

# OCR nhận diện CAPTCHA
captcha = pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
captcha = captcha.strip()
print("CAPTCHA:", captcha)
