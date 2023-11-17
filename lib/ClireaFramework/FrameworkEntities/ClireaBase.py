from sqlalchemy import Column, DateTime
from datetime import datetime
from ..environment import Base, jst

class ClireaBase(Base):
    __abstract__ = True
    InsertDate = Column(DateTime, default=lambda: datetime.now(jst))
    UpdateDate = Column(DateTime, default=lambda: datetime.now(jst), onupdate=datetime.now(jst))
