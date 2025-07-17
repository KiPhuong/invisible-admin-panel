from flask import Flask, request, make_response, render_template, session, send_file
import random
import string
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Required for session management

# Simulated order database
orders = {
    i: {
        "user": f"user_{i}",
        "product": f"Product_{random.randint(100, 999)}",
        "total": f"${random.randint(10, 500)}"
    } for i in range(10, 50)
}

# Admin panel page (hidden)
admin_pages = {
    51: "FLAG{Au7OMAtiN6_cU$tom12ed_4TTaCks}"
}

# List of 5 fixed CAPTCHA texts
CAPTCHA_LIST = ['AB12', 'CD34', 'EF56', 'GH78', 'IJ90']

# Generate CAPTCHA image
def generate_captcha_image(text):
    image = Image.new('RGB', (160, 60), color='white')
    draw = ImageDraw.Draw(image)
    
    # Use default font (Pillow's built-in font)
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 36) 
    except IOError:
        font = ImageFont.load_default()
    
    # Draw text
    draw.text((30, 5), text, fill='black', font=font)
    
    # Add noise (random dots)
    for _ in range(30):
        x = random.randint(0, 99)
        y = random.randint(0, 29)
        draw.point((x, y), fill='gray')
    
    # Save to bytes buffer
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer

# Route to serve CAPTCHA image
@app.route("/captcha/image")
def captcha_image():
    # Select a random CAPTCHA from the list
    captcha_text = random.choice(CAPTCHA_LIST)
    session['captcha_solution'] = captcha_text
    
    # Set CAPTCHA type (retained for compatibility)
    if 'captcha_type' not in session:
        session['captcha_type'] = 'captcha1'
    
    # Generate and return CAPTCHA image
    image_buffer = generate_captcha_image(captcha_text)
    return send_file(image_buffer, mimetype='image/png')

@app.route("/orders/view")
def view_order():
    id_str = request.args.get("id")
    cookie = request.cookies.get("admin")
    captcha_solution = request.args.get("captcha")

    # Validate CAPTCHA: Allow any solution from CAPTCHA_LIST
    if captcha_solution not in CAPTCHA_LIST:
        error = "Invalid CAPTCHA. Please enter the 4-character code from the image."
        return render_template("index.html", id=id_str, captcha=captcha_solution, error=error, show_captcha=True), 401

    # Validate ID input
    try:
        id_num = int(id_str)
    except (TypeError, ValueError):
        return render_template("index.html", id=id_str, captcha=captcha_solution, error="Invalid ID format", show_captcha=True), 400

    # Normal user-visible order IDs
    if id_num in orders:
        result = f"<h3>Order #{id_num}</h3><p>User: {orders[id_num]['user']}<br>Product: {orders[id_num]['product']}<br>Total: {orders[id_num]['total']}</p>"
        session.pop('captcha_solution', None)  # Clear CAPTCHA after success
        return render_template("index.html", id=id_str, captcha=captcha_solution, result=result, show_captcha=True)

    # Hidden admin page: requires cookie check
    elif id_num in admin_pages:
        if cookie == "true":
            result = f"<h1>Welcome Admin!</h1><p>Here is your flag: {admin_pages[id_num]}</p>"
            session.pop('captcha_solution', None)  # Clear CAPTCHA after success
            return render_template("index.html", id=id_str, captcha=captcha_solution, result=result, show_captcha=True)
        else:
            return render_template("index.html", id=id_str, captcha=captcha_solution, error="Admin access required", show_captcha=True), 403

    # Special case for id=52
    elif id_num == 52:
        result = "Correct CAPTCHA! Here is your partial flag: FLAG{CByp4SS_caPtCh@}"
        session.pop('captcha_solution', None)  # Clear CAPTCHA after success
        return render_template("index.html", id=id_str, captcha=captcha_solution, result=result, show_captcha=True)

    # Not found
    else:
        return render_template("index.html", id=id_str, captcha=captcha_solution, error="Order not found", show_captcha=True), 404

@app.route("/login")
def login():
    # Simulate login that sets admin cookie
    resp = make_response(render_template("index.html", result="Logged in as admin (cookie set)", show_captcha=False))
    resp.set_cookie("admin", "true")
    return resp

@app.route("/")
def index():
    return render_template("index.html", show_captcha=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
