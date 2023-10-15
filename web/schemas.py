"""
schemas.py
----------
Модуль реализует pydantic-схемы для валидации данных

"""
from datetime import datetime

from pydantic import BaseModel


class QuestionSchema(BaseModel):
    """
    Pydantic-схема вопроса

    Parameters
    ----------
    id: int
        Идентификатор вопроса в СУБД
    id_on_site: int
        Идентификатор вопроса в БД на сайте
    question_text: str
        текст вопроса
    answer_text: str
        текст ответа
    create_date: datetime
        дата создания вопроса
    """

    id: int
    id_on_site: int
    question_text: str
    answer_text: str
    create_date: datetime
