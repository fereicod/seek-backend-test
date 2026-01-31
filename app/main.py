from fastapi import FastAPI
from app.routers import auth, books

app = FastAPI(title="Books API", version="1.0.0")

prefix = "/api/v1"
app.include_router(auth.router, prefix=prefix, tags=["Authentication"])
app.include_router(books.router, prefix=prefix, tags=["Books"])