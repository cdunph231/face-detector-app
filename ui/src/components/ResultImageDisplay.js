import React from "react";

const ResultImageDisplay = (props) => {

    const textStyle = {
        color: "white",
        textAlign: "center"
    }

    let dataUrl = props.resultImageData.result_image;
    

    return(
        <div>
            <div>
                <img src={"data:image/jpeg;base64," + dataUrl} height="300" width="300" alt=""></img>
            </div>
            <div>
                <h2 style={textStyle}>Result</h2>
            </div>
        </div>
    )
}

export default ResultImageDisplay;