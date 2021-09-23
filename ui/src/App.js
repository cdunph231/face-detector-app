import React, { useState } from 'react';
import { post } from 'axios';
import ImageSubmission from './components/ImageSubmission';
import OperationsContainer from './components/OperationsContainer';
import OriginalImageDisplay from './components/OriginalIMageDisplay';
import ResultImageDisplay from './components/ResultImageDisplay';
import BlurredImageDisplay from './components/BlurredImageDisplay';
import './App.css';

//App Component will handle all get and post requests.
function App() {

  const [imageDataUrl, setImageDataUrl] = useState("");
  const [responseData, setResponseData] = useState("");
  const [resultImage, setResultImage] = useState("");
  const [blurredImg, setBlurredImage] = useState("");
  const [isBlurred, setIsBlurred] = useState(false);


  //TODO provide means of entering URL and getting image that way.
  //TODO provide functionality for drawing landmarks and do some blurring.
  //Dockerize this application
  //If time allows, provide video support
  //Extend API to return count of faces in image.


  //A callback to send response data from posting image to face detector.
  //Sends get request with 2 params: session_id & bucket_name
  const getResultImage = () => {
    const getResultUrl = "http://localhost:5000/api/get_result"

    let session_id = responseData.session_id;
    console.log("Session Id being passed: ", session_id);
    let bucket_name = responseData.bucket_name;
    console.log("Bucket Name being passed: ", bucket_name);

    const data = {
      "sessionId": session_id,
      "bucketName": bucket_name
    }

    post(getResultUrl, data)
      .then(response => setResultImage(response.data))

  }

  //Sets image data Url that is recieved from ImageSubmission.js
  const getImageDataUrlHandler = (enteredImageData) => {
    setImageDataUrl(enteredImageData);
  }

  //function to build a request and return result image from s3
  const getResultImageHandler = (imageData) => {
    const bucketName = "face-detector-app-images"
        
    //strip start of base64 URL
    let base64result = imageData.split(',')[1]

    const findFacesUrl = "http://localhost:5000/api/find_faces_file";
    const headers = {
        "Bucket": bucketName
    }

    const data = {"file": base64result}
    return post(findFacesUrl, data, {headers: headers})
        .then(function (response){
          setResponseData(response.data);
        });

  }

  const retrieveBlurred = () => {

    let session_id = responseData.session_id;
    let bucket_name = responseData.bucket_name;

    let data = {
      "session_id": session_id,
      "bucket_name": bucket_name
    }

    let url ="http://localhost:5000/api/get_blurred"
    post(url, data)
      .then(res => setBlurredImage(res.data));
  }

  const blurredSetter = () => {
    setIsBlurred(true);
  }

  return (
    <div className="App-container">
      <ImageSubmission 
        onFileSelectData={getImageDataUrlHandler}
        onImageSubmit={getResultImageHandler}
        onImageProcess={getResultImage}/>
      <OperationsContainer 
        blurIsClicked={retrieveBlurred}
        blurIsSet= {blurredSetter}/> 
      <div className="image-display__container">
        <div>
          <OriginalImageDisplay imageData={imageDataUrl}/>
        </div>
        {isBlurred ?
        <div> <BlurredImageDisplay blurredImgData={blurredImg} /> </div> : <div><ResultImageDisplay resultImageData={resultImage} /></div>
        }

      </div>
    </div>
  );
}

export default App;
