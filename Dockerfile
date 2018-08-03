FROM ubuntu:16.04

MAINTAINER David Suárez "dsuarezf@indra.es"

RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-utils \
  python3-dev \
  python3-setuptools \
  python3-pip \
  python3-wheel \
  pdf2htmlex

# Clean up apt when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app
ADD . /app

# set python 3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

RUN pip install --upgrade pip setuptools wheel

RUN pip install --upgrade -r /app/requirements.txt

# Set environment variables
ENV FLASK_APP=/app/src/main/python/pdf-to-html-server.py

# Expose the application's port
EXPOSE 5010

# Run the application
CMD ["python", "/app/src/main/python/pdf-to-html-server.py"]