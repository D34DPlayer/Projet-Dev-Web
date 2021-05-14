FROM python:3-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /

# INSTALL THE BUILD DEP.
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -U setuptools wheel

# COPY APP SOURCE CODE
COPY . /api

# INSTAL PYTHON PACKAGES
RUN pip install --no-cache-dir -r /api/requirements.txt

# CREATE IMAGES FOLDER
RUN mkdir /images
