FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /api

# INSTALL THE PYTHON PACKAGES THAT HAVE BUILD DEP.
RUN apk update && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev cargo && \
 apk add postgresql-dev libffi-dev openssl-dev
RUN pip install psycopg2==2.8.6 asyncpg==0.22.0 cryptography==3.4.6 bcrypt==3.2.0 
RUN apk del .build-deps

# INSTALL THE OTHER REQUIREMENTS
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /images
COPY . .
WORKDIR /
