from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db_rw, get_db_ro  # Ajusta tu import
from app.config import settings

app = FastAPI(title="Sistema Contratos API")

@app.get("/")
async def root():
    return {
        "message": "Sistema Contratos OK",
        "env": "LOCAL" if "localhost" in str(settings.primary_url) else "PROD"
    }

@app.get("/write")
async def write_test(db: Session = Depends(get_db_rw)):
    result = db.execute(text("SELECT now()"))
    return {"server_time": result.scalar()}

@app.get("/read")
async def read_test(db: Session = Depends(get_db_ro)):
    result = db.execute(text("SELECT version()"))
    return {"pg_version": result.scalar()}

# 🆕 RUTA 1: ¿Qué DB RW estoy usando?
@app.get("/db-rw-info")
async def db_rw_info(db: Session = Depends(get_db_rw)):
    """Muestra exactamente qué RW (Primary) estás usando"""
    result = db.execute(text("""
        SELECT 
            current_database() as db_name,
            inet_server_addr() as server_ip,
            inet_server_port() as server_port,
            version() as pg_version
    """))
    row = dict(result.fetchone()._mapping)
    
    is_local = "localhost" in str(settings.primary_url)
    row["env"] = "LOCAL" if is_local else "PROD (RW Primary)"
    row["connection_url"] = str(settings.primary_url).split('@')[1][:50] + "..."
    
    return row

# 🆕 RUTA 2: ¿Qué DB RO estoy usando?
@app.get("/db-ro-info")
async def db_ro_info(db: Session = Depends(get_db_ro)):
    """Muestra exactamente qué RO (Réplica) estás usando"""
    result = db.execute(text("""
        SELECT 
            current_database() as db_name,
            inet_server_addr() as server_ip,
            inet_server_port() as server_port,
            version() as pg_version
    """))
    row = dict(result.fetchone()._mapping)
    
    is_local = "localhost" in str(settings.readonly_url)
    row["env"] = "LOCAL" if is_local else "PROD (RO Replica)"
    row["connection_url"] = str(settings.readonly_url).split('@')[1][:50] + "..."
    
    return row

@app.get("/identification-types")
async def identification_types(db: Session = Depends(get_db_ro)):
    result = db.execute(text("""
        SELECT nIdIdentificationType, cCode, cName, nMaxLength, bIsActive 
        FROM s01identification_type ORDER BY nIdIdentificationType
    """))
    return {"types": [dict(row._mapping) for row in result.fetchall()]}

@app.get("/health")
async def health():
    return {"status": "healthy"}
