# face-detector-app
A simple face detector app using the Tensorflow implementation of MTCNN. This is a very basic implementation of a React app with a Flask back end in order to practice concepts in both frameworks. Styling isn't great at the moment but I will work on adding functionality and styling in the near future. This app is tightly integrated with my own AWS count, as I have the AWS SDK configured to a user in IAM, if you wish to use or add to this app, make sure you keep that in mind.

## How to run react app
Navigate to UI folder
`cd ui`

Run the following command
`npm start`

## How to start flask app
Navigate to api folder from face-detector-app and run:
`python app.py`

Alternatively, if you wish to build a docker image, there is a Dockerfile included, navigate to api folder and run:
`docker build -t <PREFERRED NAME FOR IMAGE> .`

