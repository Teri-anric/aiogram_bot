from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, DeclarativeBase

metadata = MetaData()

Base: DeclarativeBase = declarative_base(metadata=metadata)
