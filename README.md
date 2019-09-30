# pdf-to-html

The **pdf-to-html** service converts PDF files into HTML. It uses the pdf2htmlEx [1] tool to convert the files.

The service can be executed as a single Python application or within a container.

To execute as a Python application:

    gunicorn --bind 0.0.0.0:5010 --chdir src/main/python wsgi:app

To build or rebuild the Docker image type (the HTTP_PROXY variable must
be set if executed behind a proxy):

    docker build --build-arg http_proxy=$HTTP_PROXY --build-arg https_proxy=$HTTPS_PROXY --build-arg no_proxy=$NO_PROXY -t pdf-to-html .

To run the container as a service:

    docker run --rm -p 6000:6000 --name pdf-to-html pdf-to-html

To run the container interactively:

    docker run -it --rm --entrypoint bash pdf-to-html

How to test if the service is running:

    curl http://localhost:6000/

How to test the upload endpoint:

    curl -F file=@<file>  http://localhost:6000/api/v1.0/documents/convert

## References

Useful references:

* [https://github.com/coolwanglu/pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX)