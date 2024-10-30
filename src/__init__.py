from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.database.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"is started...")
    await init_db()
    yield
    print(f"server has been stoped")

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A Rest API for book review webservice",
    version=version,
    lifespan=life_span
)

# register route
app.include_router(router=book_router, prefix=f"/api/{version}/books", tags=["books"])
