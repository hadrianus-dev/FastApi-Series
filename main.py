from fastapi import FastAPI
from src.books.routes import book_router

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A Rest API for book review webservice",
    version=version,
)

# register route
app.include_router(router=book_router, prefix=f"/api/{version}/books", tags=["books"])
