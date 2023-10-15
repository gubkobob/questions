from typing import List, Union

from database import Base, app, async_session, engine
from schemas import QuestionSchema
from services import get_questions, post_questions


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


@app.post(
    "/questions",
    summary="Публикация вопросов",
    response_description="Последний вопрос",
    response_model=Union[QuestionSchema, None],
    status_code=200,
)
async def insert_questions_handler(questions_num: int) -> Union[QuestionSchema, None]:
    """
    Эндпоинт скачивает указанное количество вопросов с сайта и сохраняет их в БД
    \f
    :param questions_num: int
         количество вопросов для скачивания

    :return: Union[QuestionSchema, None]
        Pydantic-схема с последним вопросом или пустой обьект
    """
    if questions_num < 1:
        return None
    async with async_session() as session:
        last_question = await post_questions(
            session=session, questions_num=questions_num
        )
    return last_question


@app.get(
    "/questions",
    summary="Список всех вопросов",
    response_description="Все вопросы",
    response_model=List[QuestionSchema],
    status_code=200,
)
async def get_questions_handler() -> List[QuestionSchema]:
    """
    Эндпоинт возвращает все вопросы из БД
    \f

    :return: List[QuestionSchema]
        Pydantic-схема со списком всех вопросов БД
    """
    async with async_session() as session:
        result = await get_questions(session=session)
    return result
