# Challenge 3: Is it running?

The task was to containerize a simple Python server application and test if it is running in the desired way. Therefore we need to create a Dockerfile.

## Dockerfile

### Base Image

We will use the official Python Alpine image as base image as it sufficient enough to get the
server application running without any hassle. The advantage of the server.py is, that it only
uses dependencies which come with Python itself. Therefore we don't need to run any extra
RUN commands when building the container.

### Workdir & Copy
It is a good practice to use a separate directory where we will put all the necessary application
files into. Regarding the COPY command we also could have used `COPY . /app/` but we want to make
it more clear and choose specific files.

### Port Exposure
As we want to have the server react on requests we need to expose ports so that the container
is able to communicate with the outer world. As we can see in the server.py the application will
use Port 8080 so we are going this specific port.

### Running the application inside the container
Finally we have to use the CMD command to start python and give it the filename (server.py) as an
argument so that our application will start.

## Building and running the container

### Container build

The Dockerfile is our recipe to build a real container. To do so we need to run the following command

```sh
docker build -t <container_image_name> .
```

When the container was successfully built we can go to the next step and run it

### Run the Container

Because we want to communicate with the server application inside the container we need to
explicitly set the `-p` option for the correct port numbers. We will also use the `-d` option
to use the detached mode which means that the shell will not be blocked by docker

Our final command to run the container is

```sh
docker run -p 8080:8080 -d localhost/<container_image_name>
```

## Testing the connection
Our tool of choice is cURL which is a perfect fit to test the responses of the server application.
We will need to use some options of cURL to test against the server with a specific request header

`-i` includes the response headers in the output. This is optional but useful to inspect the HTTP status code
`-H` is used to send a request header to the server. We need to use `-H "Challenge: orcrist.org"``
`-X` will be used to set the request method explicitly. Because we want GET we will use `-X GET``

In the end we need to execute following command in our shell where the container runs on:
```sh
curl -i -H "Challenge: orcrist.org" -X GET http://localhost:8080
``` 

The Response from the server is

```sh
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.14.4
Date: Fri, 24 Apr 2026 13:21:12 GMT
Content-type: text/html

Everything works!%
```