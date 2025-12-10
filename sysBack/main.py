from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db_rw, get_db_ro
from sqlalchemy import text

app = FastAPI()

@app.get("/")
async def root():
    return {
        "primary": settings.primary_url.split('@')[1],
        "readonly": settings.readonly_url.split('@')[1]
    }

@app.get("/write", dependencies=[Depends(get_db_rw)])
async def write_test(db: Session = Depends(get_db_rw)):
    result = db.execute(text("SELECT now()"))
    return {"server_time": result.scalar()}

@app.get("/read", dependencies=[Depends(get_db_ro)])
async def read_test(db: Session = Depends(get_db_ro)):
    result = db.execute(text("SELECT version()"))
    return {"pg_version": result.scalar()}
