import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from busesdb import models
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

models.base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def home():
    return "Home page"

@app.get("/bus")
async def read_buses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    buses = db.query(models.Bus).offset(skip).limit(limit).all()
    return buses

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)