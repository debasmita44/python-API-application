# app.py
from fastapi import FastAPI, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from database import SessionLocal, engine, Base
from models import Item

# Make sure tables exist (in case seed not run)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Data API")

# 🔐 Simple API key (in real life, use env vars or a secrets manager)
API_KEY = "014dk58dba90olkd4"  # change this to anything you like


# --- DB DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- SECURITY DEPENDENCY ---
def verify_api_key(
    x_api_key: Optional[str] = Header(default=None),
    api_key_query: Optional[str] = Query(default=None, alias="api_key"),
):
    """
    Accept API key either in:
      - Header: X-API-Key: <key>
      - Query: ?api_key=<key>
    """
    key = x_api_key or api_key_query
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return True


# --- RESPONSE SCHEMA (simple manual dicts) ---
def item_to_dict(item: Item) -> dict:
    return {
        "id": item.id,
        "key": item.key,
        "name": item.name,
        "description": item.description,
    }


# --- ROUTES ---

@app.get("/items", dependencies=[Depends(verify_api_key)])
def get_all_items(db: Session = Depends(get_db)) -> List[dict]:
    items = db.query(Item).all()
    return [item_to_dict(i) for i in items]


@app.get("/items/{item_key}", dependencies=[Depends(verify_api_key)])
def get_item_by_key(item_key: str, db: Session = Depends(get_db)) -> dict:
    item = db.query(Item).filter(Item.key == item_key).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with key '{item_key}' not found",
        )
    return item_to_dict(item)


@app.post("/items", dependencies=[Depends(verify_api_key)])
def create_item(
    key: str,
    name: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
) -> dict:
    # check if key exists
    existing = db.query(Item).filter(Item.key == key).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Item with key '{key}' already exists",
        )

    new_item = Item(key=key, name=name, description=description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return item_to_dict(new_item)
