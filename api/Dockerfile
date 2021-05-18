FROM python:3-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /

# INSTALL THE BUILD DEP.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -U setuptools wheel

# COPY THE REQUIREMENTS
RUN mkdir /api
COPY ./requirements.txt /api/requirements.txt

# INSTALL PYTHON PACKAGES
RUN pip install --no-cache-dir -r /api/requirements.txt

# COPY APP SOURCE CODE
COPY . /api

# CREATE IMAGES FOLDER
RUN mkdir /images
