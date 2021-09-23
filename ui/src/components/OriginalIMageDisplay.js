import React from "react";

const OriginalImageDisplay = (props) => {

    console.log(props);

    const textStyle = {
        color: "white",
        textAlign: "center"
    }

    return (
        <div>
            <div>
                <img src={props.imageData} height="300" width="300" alt=""></img>
            </div>
            <div>
                <h2 style={textStyle}>Original</h2>
            </div>
        </div>
    )
}

export default OriginalImageDisplay;