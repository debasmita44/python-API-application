# main.py
from fastapi import FastAPI, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from database import SessionLocal, engine, Base
from models import Item


# --- CREATE TABLES ---
print("⏳ Creating tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables ready")


app = FastAPI(title="Secure Data API on Render")


# --- SECURITY ---
API_KEY = "014dk58dba90olkd4" # You can change this


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(
    x_api_key: Optional[str] = Header(default=None),
    api_key_query: Optional[str] = Query(default=None, alias="api_key"),
):
    key = x_api_key or api_key_query
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True


def item_to_dict(item: Item):
    return {
        "id": item.id,
        "key": item.key,
        "name": item.name,
        "description": item.description,
    }


@app.get("/items", dependencies=[Depends(verify_api_key)])
def get_all_items(db: Session = Depends(get_db)):
    return [item_to_dict(i) for i in db.query(Item).all()]


@app.get("/items/{item_key}", dependencies=[Depends(verify_api_key)])
def get_item_by_key(item_key: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.key == item_key).first()
    if not item:
        raise HTTPException(404, f"Item with key '{item_key}' not found")
    return item_to_dict(item)


@app.post("/items", dependencies=[Depends(verify_api_key)])
def create_item(
    key: str,
    name: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if db.query(Item).filter(Item.key == key).first():
        raise HTTPException(400, f"Item with key '{key}' already exists")

    item = Item(key=key, name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)

    return item_to_dict(item)
