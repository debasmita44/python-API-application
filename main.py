from fastapi import FastAPI
from database import Base, engine, SessionLocal
from models import Item
from seed_data import init_db

app = FastAPI()


# ----------------------------------------
# AUTO-SEED DATABASE ON SERVER START
# ----------------------------------------

def seed_once():
    """
    Seeds database ONLY if it's empty.
    Safe for Render – runs every boot but inserts only once.
    """
    db = SessionLocal()
    try:
        # check for existing data
        item_exists = db.query(Item).first()
        if not item_exists:
            print("No data found — running seed_data.init_db()...")
            init_db()
        else:
            print("Data already present — skipping seeding.")
    except Exception as e:
        print("Seeding error:", e)
    finally:
        db.close()


# Run seeding immediately when Render starts the app
seed_once()

# -----------------------------------------------------
# API ROUTES
# -----------------------------------------------------

@app.get("/")
def home():
    return {"message": "API is running!"}


@app.get("/items")
def get_items():
    db = SessionLocal()
    try:
        items = db.query(Item).all()
        return items
    finally:
        db.close()


@app.get("/items/{key}")
def get_item_by_key(key: str):
    db = SessionLocal()
    try:
        item = db.query(Item).filter(Item.key == key).first()
        if item:
            return item
        return {"error": "Item not found"}
    finally:
        db.close()
