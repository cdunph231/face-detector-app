import React from "react";
import { useState, useEffect } from "react";
import "./ImageSubmission.css";


//Start with form to upload file to api endpoint.
//Display image in component and display result from api in componenet below.

const ImageSubmission = (props) => {

    const [enteredImage, setEnteredImage] = useState(null);
    const [enteredUrl, setEnteredUrl] = useState("")
    //const [isSelected, setIsSelected] = useState(false);

    useEffect(() => {
        console.log(enteredImage);
        props.onFileSelectData(enteredImage);
    }, [enteredImage]);



    const selectFileHandler = (event) => {
        let reader = new FileReader();
        const files = event.target.files;
        console.log(files);
        //base64 representation
        reader.readAsDataURL(files[0]);

        reader.onload = (e) => {
            let dataUrl = e.target.result;
            console.log(dataUrl);
            setEnteredImage(dataUrl);
        }
    }

    const submissionHandler = () => {
        props.onImageSubmit(enteredImage);
    }

    const getResultHandler = () => {
        props.onImageProcess();
    }

    
    return (
        <div className="submission-buttons">    
            <div>
                <h3 style={{color: 'white'}}>Please Select a file</h3>
                <input type="file" name="file" onChange={selectFileHandler} />
                <button onClick={submissionHandler}>Submit</button>
                <button onClick={getResultHandler}>Process image</button>
            </div>
        </div>
    )
}

export default ImageSubmission;