import uvicorn
from fastapi import FastAPI
from app.database import SessionLocal, engine
from app import models

app = FastAPI()

busesdb.models.base.metadata.create_all(bind=engine)

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
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    bus = db.query(busesdb.models.Bus).offset(skip).limit(limit).all()
    return bus
