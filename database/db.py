from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite+pysqlite:///:memory:"
engine = create_engine(url, echo=True)
session_factory = sessionmaker(bind=engine)

session = session_factory()

