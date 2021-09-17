from flask import Flask, jsonify, request
from helpers import detect_faces, url_to_img
import numpy as np
import urllib
import cv2
import json


app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return "HELLO WORLD!!"

#Handle images from urls
@app.route("/api/find_faces_url", methods=["POST"])
def find_faces():

    if request.method == "POST":
        data = request.get_json()

        img_url = data["image"]
        image = url_to_img(img_url)

        faces = detect_faces(image)
        #npimg = np.fromfile(data, dtype=np.uint8)
        #image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        height, width = image.shape[:2]

        return jsonify({"faces" : faces})




if __name__ == "__main__":
    app.run(debug=True)