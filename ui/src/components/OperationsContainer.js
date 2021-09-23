import React from "react";
import "./OperationsContainer.css";

//Component which holds all operations to interact with face detection.

const OperationsContainer = (props) => {

    const blurHandler = () => {
        props.blurIsSet();
    }

    return (
        <div className="operations-container">
            <button onClick={blurHandler}>Blur</button>
        </div>
    )
}

export default OperationsContainer;