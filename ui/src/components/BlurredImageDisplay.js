import React from 'react';

const BlurredImageDisplay = (props) => {

    let blurredImage = props.blurredImg;

    return(
        <div>
            <img src={"data:image/jpeg;base64," + blurredImage.blurred_image} alt=""></img>
        </div>
    )
}

export default BlurredImageDisplay;