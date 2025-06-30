from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import scraper

app = FastAPI()

origins = [
    "https://a.hicomsystem.com",
    "http://a.hicomsystem.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World", "version": "1.0.1"}

class Scrape(BaseModel):
    url: str

@app.post("/scrape/")
def scrape(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL is required")
    result = scraper.scrape(url)
    return result