FROM python:3-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# INSTALL THE POSTGRES PYTHON PACKAGE
RUN apk update && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev && \
 apk add postgresql-dev
RUN pip install psycopg2 asyncpg
RUN apk del .build-deps

# INSTALL THE OTHER REQUIREMENTS
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
