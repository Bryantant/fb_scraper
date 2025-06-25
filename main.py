from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import scraper

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

class Scrape(BaseModel):
    url: str

@app.post("/scrape/")
def scrape(scrape: Scrape):
    if not scrape.url:
        raise HTTPException(status_code=400, detail="URL is required")
    result = scraper.scrape(scrape.url)
    return result