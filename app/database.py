from sqlmodel import SQLModel, create_engine, Session
import os

DB_FILE = os.getenv("GLOSSARY_DB", "./data/glossary.db")
os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

def init_db():
    from .models import Term
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
