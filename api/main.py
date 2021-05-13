from api.routers import contact

from .app import app
from .routers import contact, horaire, products, users

app.include_router(users.router)
app.include_router(horaire.router)
app.include_router(products.router)
app.include_router(contact.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
