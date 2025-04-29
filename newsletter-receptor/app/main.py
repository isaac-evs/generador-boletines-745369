from fastapi import FastAPI
from app.routers import newsletter

app = FastAPI(title="Newsletter Service API")

app.include_router(newsletter.router)

@app.get("/")
async def root():
    return {"message": "Newsletter Service API is running"}
