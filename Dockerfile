FROM ubuntu:16.04

LABEL maintainer="david.suarez.fuentes@gmail.com"

# Set environment
ENV LANG C.UTF-8
ENV USER_ID 999
ENV GROUP_ID 999
ENV USER language
ENV USER_HOME /home/$USER
ENV FLASK_APP pdf_to_html_server.py

# Create user's home
RUN mkdir -p $USER_HOME

# Avoid running application as root user
RUN groupadd -g $USER_ID $USER && \
    useradd -r -u $GROUP_ID -g $USER -d $USER_HOME -s /sbin/nologin -c "Docker image user" $USER && \
    chown -R $USER:$USER $USER_HOME

# Install packages and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
  apt-utils \
  python3-setuptools \
  python3-pip \
  ttfautohint \
  poppler-data \
  pdf2htmlex

# Clean up apt when done
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set Python3 as the default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
    && update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Update Python tools
RUN pip install --upgrade pip setuptools wheel

# Install application's packages
COPY requirements.txt /tmp/
RUN pip install --upgrade -r /tmp/requirements.txt

# Avoid running application as root user
USER $USER

# Create application folder
RUN mkdir -p $USER_HOME/app

# Copy resources
WORKDIR $USER_HOME/app
COPY --chown=$USER:$USER /src/main/python src

# Create uploads folder
RUN mkdir -p src/uploads

# Expose the service's port
EXPOSE 6000

# Run the application
WORKDIR $USER_HOME/app/src
CMD ["gunicorn", "-b 0.0.0.0:6000", "-k gevent", "-w 4", "wsgi:app"]