
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# If the DATABASE_URL references asyncpg but async driver is not installed,
# fall back to the synchronous psycopg2 driver so the service can run with
# the existing psycopg2 dependency in requirements.txt.
database_url = settings.database_url
if "+asyncpg" in database_url:
    database_url = database_url.replace("+asyncpg", "+psycopg2")

engine = create_engine(database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


