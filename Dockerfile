FROM ubuntu:16.04

MAINTAINER David Suárez "david.suarez.fuentes@gmail.com"

# Set environment
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install packages and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-utils \
  python3-dev \
  python3-setuptools \
  python3-pip \
  python3-wheel \
  pdf2htmlex

# Clean up apt when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy resources
WORKDIR /app
COPY /src/main/python .
COPY requirements.txt .
RUN mkdir -p uploads

# Set Python3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Update Python tools
RUN pip install --upgrade pip setuptools wheel
RUN pip install --upgrade -r requirements.txt

# Set environment variables
ENV FLASK_APP=pdf_to_html_server.py

# Expose the service's port
EXPOSE 5010

# Run the application
CMD ["gunicorn", "-b 0.0.0.0:6000", "-w 4", "wsgi:app"]
