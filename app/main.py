from fastapi import FastAPI
from app.routes.api import router

app = FastAPI()

# Include the API routes
app.include_router(router)