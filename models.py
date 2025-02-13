from sqlalchemy import Column, Integer, Text, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code_snippet = Column(Text, nullable=False)
    suggestion = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
