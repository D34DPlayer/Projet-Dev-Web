from .app import app

from .routers import users, horaire


app.include_router(users.router)
app.include_router(horaire.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
