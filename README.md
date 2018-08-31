# pdf-to-html

The **pdf-to-html** module transforms PDF files into HTML. It uses the
pdf2htmlEx [1] tool to convert PDF files.

To build or rebuild the Docker image type (the HTTP_PROXY variable must
be set if executed behind a proxy):

    docker build --build-arg http_proxy=$HTTP_PROXY --build-arg https_proxy=$HTTPS_PROXY --build-arg no_proxy=$NO_PROXY -t pdf-to-html .
    
To run the container as a service:

    docker run --rm -p 5010:6000 --name pdf-to-html pdf-to-html    
 
To run the container interactively:

    docker run -it --rm --entrypoint bash -v <absolute-path-on-host>:/data pdf-to-html
    
How to test if the service is running:

    curl http://localhost:5010/    
    
How to test the upload endpoint:

    curl -F file=@<file>  http://localhost:5010/api/v1.0/documents/convert

[1] https://github.com/coolwanglu/pdf2htmlEX
