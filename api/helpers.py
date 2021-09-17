from mtcnn.mtcnn import MTCNN
import urllib.request
import numpy as np
import cv2

def detect_faces(image):
    detector = MTCNN()
    faces = detector.detect_faces(image)
    
    return faces

def url_to_img(url):

    #Mimics browser requesting image using user agent.
    opener = urllib.request.build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
    urllib.request.install_opener(opener)

    data = urllib.request.urlopen(url)
    image = np.asanyarray(bytearray(data.read()), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    return image

