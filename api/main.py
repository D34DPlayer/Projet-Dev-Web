from app import app
from db import db


@app.get("/")
async def root():
    return {"message": "Hello World"}
