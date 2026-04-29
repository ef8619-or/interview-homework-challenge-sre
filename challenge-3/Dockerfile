# We will use the official Python image based on Alpine Linux, 
# which is a minimal and lightweight distribution. This will help us keep our Docker image small and efficient. We will set the working directory to /app, copy our server.py file into the container, expose port 8080 for our server to listen on, and finally, we will specify the command to run our server when the container starts.
FROM python:alpine

# Addition for challenge-5: we need to add a label to be able to push the built image
# to ghcr.io registry. We need to rebuilt the image for challenge-5, but it will not affect the previous challenges.
LABEL org.opencontainers.image.source=https://github.com/ef8619-or/interview-homework-challenge-sre

# A good practice is to use a separate directory for the application
WORKDIR /app

# Next we copy the desired file into the directory in the container
COPY server.py /app/

# Here we will expose the port that the server will be listening on
EXPOSE 8080

# Finally we will use the CMD command to start python and run the
# server.py file when the container starts
CMD ["python", "server.py"]