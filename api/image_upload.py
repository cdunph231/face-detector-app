import boto3
import cv2
import numpy as np

from threading import Thread
import io

class S3Thread(Thread):

    def __init__(self, bucket_name):
        super(S3Thread, self).__init__()
        self.bucket = bucket_name
        self.key = None
        self.data = None
        self.content_type = "image/jpeg"

    def run(self):
        self.upload()

    def upload(self):
        s3Client = boto3.client('s3')
        
        s3Client.upload_fileobj(io.BytesIO(self.data), self.bucket, self.key, ExtraArgs={'ContentType': self.content_type})

    #Representation of the object to be saved to S3
    def withObject(self, key, data, content_type="image/jpeg"):
        self.key = key
        self.data = data
        self.content_type = content_type
        return self

# Function to download result image, given a bucket name and session_id.
# Returns image to be base64 encoded
def download_result_s3(session_id, bucket_name, filename="bounding_box.jpg"):
    s3 = boto3.resource('s3')

    image_bucket = s3.Bucket(bucket_name)

    file_key = session_id + "/" + filename
    img_obj = image_bucket.Object(file_key).get().get('Body').read()
    npimg = cv2.imdecode(np.asarray(bytearray(img_obj)), cv2.IMREAD_COLOR) 

    return npimg


#Method to extract bucket and session information for image upload.
def upload_debug(imageName, imageData, headers):
    if 'bucket' in headers.keys() and headers['bucket'] is not None:
        bucket = headers['bucket']
    
        #Set base path of images to unique_id
        base_path = headers['session']

        uploadImage(bucket, base_path, imageName, imageData)

#Method for uploading images in the background to specified image paths.
def uploadImage(bucket_name, base_path, image_name, image_data):
    if base_path is not None and bucket_name is not None and image_name is not None and image_data is not None:
        key = base_path + '/' + image_name
        uploader = S3Thread(bucket_name)
        #Set to execute in background.
        uploader.daemon = True
        #encode in to Bytes
        _, encoded_image = cv2.imencode(".jpg", image_data)
        uploader.withObject(key, encoded_image).start()


