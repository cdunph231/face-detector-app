from copy import Error
import boto3
from botocore.retries import base
from flask import Flask, jsonify, request
from helpers import detect_faces, url_to_img
from image_upload import upload_debug, download_result_s3
import numpy as np
import base64
import cv2
import uuid
import json

#DEFAULT_BUCKET = "face-detector-app-images"

app = Flask(__name__)

#Route to get image from s3 folder.
@app.route("/api/get_result", methods=["POST"])
def get_result():

    resp = {}

    data = request.get_json(force=True)

    sessionId = data["sessionId"]
    bucket_name = data["bucketName"]
    #print(sessionId)
    #bucket_name = request.args.get("bucketName")
    #print(bucket_name)

    
    #Download image from bucket using provided query params.
    image = download_result_s3(sessionId, bucket_name)

    #Base64 encode image and return.
    _, encoded_image = cv2.imencode('.jpg', image)
    baseStr = base64.b64encode(encoded_image)
    resp["result_image"] = baseStr.decode('utf8')
    
    return jsonify(resp)

@app.route("/api/get_blurred", methods=["POST"])
def get_blurred():

    resp = {}

    data = data = request.get_json(force=True)

    sessionId = data["session_id"]
    bucket_name = data["bucket_name"]
    
    #Download image from bucket using provided query params.
    image = download_result_s3(sessionId, bucket_name, filename="original.jpg")

    w, h = image.shape[:2]

    kW = 101
    kH = 91

    '''
    if kW % 2 == 0:
        kW -= 1
    
    if kH % 2 ==0:
        kH -= 1
    '''

    faces = detect_faces(image)
    for face in faces:
        (x, y, w, h) = face['box']
        image[y: y+h, x: x+w] = cv2.GaussianBlur(image[y: y+h, x: x+w], (kH, kW), 0)

    _, encoded_image = cv2.imencode('.jpg', image)
    baseStr = base64.b64encode(encoded_image)

    resp['blurred_img'] = baseStr.decode('utf8')
    
    return jsonify(resp)


#Url data handler. Finds faces and draws bounding boxes.
#Saves image to s3 bucket with unique ID 
@app.route("/api/find_faces_url", methods=["POST"])
def find_faces_url():

    if request.method == "POST":
        data = request.get_json()

        session_id = str(uuid.uuid4())

        session_details = {
            "session": session_id,
            "bucket": request.headers.get("Bucket")
        }

        img_url = data["image"]
        image = url_to_img(img_url)

        faces = detect_faces(image)
        return jsonify({"faces" : faces})

#File upload handler. Finds faces and draws bounding boxes, as well as landmarks.
#Saves image to S3 bucket with unique ID.
@app.route("/api/find_faces_file", methods=["POST"])
def find_faces_file():

    resp = {}
    if request.method == "POST":
        #Unique identifier to refer back to folder where images are stored.
        session_id = str(uuid.uuid4())

        resp['session_id'] = session_id
        bucket_name = request.headers.get("Bucket")

        session_details = {
            "session": session_id,
            "bucket": bucket_name
        }

        resp['bucket_name'] = bucket_name


        data = request.get_json()
        img_string = data['file']

       
        #Decode base64 file string.
        npimg = np.fromstring(base64.b64decode(img_string), dtype=np.uint8)
        image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        try:
            #Upload original image.
            upload_debug("original.jpg", image, session_details)
        except Error as e:
            print("Error uploading image : ", e.message)


        faces = detect_faces(image)

        for face in faces:
            (x, y, w, h) = face['box']
            faceFoundImage = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 5)
            landmarks = face['keypoints']
            for key, point in landmarks.items():
                cv2.circle(image, point, 2, (0, 0, 255), 6)


        resp["faces"] = faces
        #Upload image with bounding box drawn.
        try:
            upload_debug("bounding_box.jpg", faceFoundImage, session_details)
        except Error as e:
            print("Error uploading image: ", e.message)

    return jsonify(resp)


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Bucket')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response



if __name__ == "__main__":
    app.run(debug=True)