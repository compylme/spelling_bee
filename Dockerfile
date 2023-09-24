FROM python:3.11

# Set the environment variable for the port
ENV PORT 8080

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-setuptools \
    python3-venv \
    git \
    && apt-get clean

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && \
    apt-get install -y google-cloud-sdk


# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Set the environment variables and working directory
ENV APP_HOME /APP_HOME
WORKDIR $APP_HOME
COPY . .

EXPOSE 8080

# Set environment variables:
ENV GOOGLE_APPLICATION_CREDENTIALS="keys/service-account-key.json"

# Copy the Python script and service account key into the container
COPY keys/service-account-key.json .

RUN gcloud auth activate-service-account --key-file=keys/service-account-key.json

# Start your application
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app