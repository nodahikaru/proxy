from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres.zqhlbjyljfskhnmwhdcd:y7RFNFX6%kjqUqr@aws-1-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()