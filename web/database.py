from typing import Any, Dict

from fastapi import FastAPI
from sqlalchemy import Column, DateTime, Integer, Sequence, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()
engine = create_async_engine("postgresql+asyncpg://admin:admin@db:5432")
Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, Sequence("question_id_seq"), primary_key=True)
    id_on_site = Column(Integer, nullable=False)
    question_text = Column(String(1000), nullable=False)
    answer_text = Column(String(1000), nullable=False)
    create_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"Вопрос номер {self.id_on_site}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
