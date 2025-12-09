# seed_data.py
from database import Base, engine, SessionLocal
from models import Item

def init_db():
    # create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # check if data already exists
        if db.query(Item).first():
            print("Data already exists, skipping seeding.")
            return

        items = [
            Item(key="item1", name="First Item", description="This is the first sample item."),
            Item(key="item2", name="Second Item", description="Another sample item."),
            Item(key="item3", name="Special Item", description="Something special here."),
        ]

        db.add_all(items)
        db.commit()
        print("Sample data inserted successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
