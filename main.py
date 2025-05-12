from fastapi import FastAPI
from app.routes import s3_routes

app = FastAPI()

app.include_router(s3_routes.router, prefix="/s3")