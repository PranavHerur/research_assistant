from fastapi import FastAPI
from api.papers import router as papers_router

app = FastAPI()

app.include_router(papers_router)
