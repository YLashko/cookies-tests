from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone


Base = declarative_base()


class TestTable(Base):
    __tablename__ = "test_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc), nullable=False)
