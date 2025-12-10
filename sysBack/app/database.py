from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends
from app.config import settings

# SINGLETON ENGINES (evita memory leaks)
_engine_rw = None
_engine_ro = None

def get_engine_rw():
    global _engine_rw
    if _engine_rw is None:
        _engine_rw = create_engine(settings.primary_url, pool_pre_ping=True, pool_size=20)
    return _engine_rw

def get_engine_ro():
    global _engine_ro
    if _engine_ro is None:
        _engine_ro = create_engine(settings.readonly_url, pool_pre_ping=True, pool_size=20)
    return _engine_ro

def get_db_rw() -> Session:
    SessionLocal = sessionmaker(bind=get_engine_rw())
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_db_ro() -> Session:
    SessionLocal = sessionmaker(bind=get_engine_ro())
    db = SessionLocal()
    try: yield db
    finally: db.close()
