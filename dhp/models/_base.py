from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

from dhp import DB_URL

engine = create_engine(DB_URL)
Base = declarative_base()
