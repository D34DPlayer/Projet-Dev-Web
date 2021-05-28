from api.app import app
from api.routers import contact, horaire, products, users, comments


app.include_router(users.router)
app.include_router(horaire.router)
app.include_router(products.router)
app.include_router(comments.router)
app.include_router(contact.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
