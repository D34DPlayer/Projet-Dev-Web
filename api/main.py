from .app import app

from .routers import users


app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
