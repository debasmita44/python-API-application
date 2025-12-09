from fastapi import FastAPI, Depends, HTTPException, status, Header, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from database import SessionLocal, Base, engine
from models import Item

# Create tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure Data API")

API_KEY = "014dk58dba90olkd4" # <-- you can replace this


# --- DB DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- SECURITY ---
def verify_api_key(
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    api_key_query: Optional[str] = Query(default=None, alias="api_key")
):
    key = x_api_key or api_key_query
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return True


# --- CONVERTER ---
def item_to_dict(item: Item) -> dict:
    return {
        "id": item.id,
        "key": item.key,
        "name": item.name,
        "description": item.description
    }


# --- ROUTES ---
@app.get("/items", dependencies=[Depends(verify_api_key)])
def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [item_to_dict(i) for i in items]


@app.get("/items/{item_key}", dependencies=[Depends(verify_api_key)])
def get_item(item_key: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.key == item_key).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_to_dict(item)


@app.post("/items", dependencies=[Depends(verify_api_key)])
def create_item(
    key: str,
    name: str,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    existing = db.query(Item).filter(Item.key == key).first()
    if existing:
        raise HTTPException(status_code=400, detail="Key already exists")

    item = Item(key=key, name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item_to_dict(item)
