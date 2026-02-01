from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routers import auth, books

app = FastAPI(title="Books API", version="1.0.0")

prefix = "/api/v1"
app.include_router(auth.router, prefix=prefix)
app.include_router(books.router, prefix=prefix)

# Enable pagination support
add_pagination(app)