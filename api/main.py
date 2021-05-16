from .app import app

from .routers import users, horaire, products, comments


app.include_router(users.router)
app.include_router(horaire.router)
app.include_router(products.router)
app.include_router(comments.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
