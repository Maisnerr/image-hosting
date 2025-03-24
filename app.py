from flask import Flask, render_template, request, jsonify, redirect
from flask_cors import CORS
from dotenv import load_dotenv
import os
import datetime
import cloudinary.uploader
import cloudinary.api
from PIL import Image
import io
import string
import random
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
SITES = [
    "http://192.168.1.138:5000"
]
CORS(app, resources={r"/*": {"origins": SITES}})
app.config["UPLOAD_FOLDER"] = "static/uploads"

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class Images(db.Model):
    __tablename__ = "images_db"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.Date, nullable=False, default=datetime.date.today)

    large_img = db.Column(db.String(2048), nullable=False)

    name = db.Column(db.String(2048), nullable=False)

    url = db.Column(db.String(2048), nullable=False, unique=True)

def create_url():
    all_urls = Images.query.all()
    characters = string.digits + string.ascii_letters
    url = ""
    while url=="":
        url = ''.join(random.choices(characters, k=10))
        for i in all_urls:
            if url ==  i.url:
                url=""
                break
    return url

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_image", methods=["GET", "POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        img = Image.open(file)

        img.thumbnail((1920,1080))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        url = create_url()

        response = cloudinary.uploader.upload(img_byte_arr, resource_type='image',folder="image_hosting", public_id=url)
        large_url = response["url"]
    except Exception as e:
        print(e)
        return jsonify({"error":"Error"}), 400

    print(url+" : "+large_url)

    new_entry = Images(large_img=large_url, url=url, name=file.filename)

    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"Status": "alr", "image_url":large_url}), 200

@app.route("/image/<url>")
def return_img_url(url):
    all_urls = Images.query.all()
    for i in all_urls:
        if url == i.url:
            return jsonify({"image_url": i.large_img})
    return jsonify({"Error":"Mas spatny url bracho"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5000)
