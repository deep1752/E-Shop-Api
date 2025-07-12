from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.config import DATABASE_URL

# Optional extra engine options
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# ✅ Create the SQLAlchemy engine with better MySQL compatibility
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,    # ✅ Auto-check connection health
    pool_recycle=280       # ✅ Optional: Recycle connections after 280s to avoid timeout
)

# Session maker for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
