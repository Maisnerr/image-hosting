from flask import Flask, render_template, request, jsonify, redirect
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/uploads"

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
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    print(f"Saving file to: {file_path}")
    file.save(file_path)

    return jsonify({"Status": "alr"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
