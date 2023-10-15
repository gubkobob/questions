import datetime
from typing import List

import requests
from database import Question
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession


async def post_questions(session: AsyncSession, questions_num: int) -> Question:
    query = await session.execute(select(Question.id_on_site))
    site_ids_in_db = query.scalars().all()

    data = {"count": questions_num}
    response = requests.get("https://jservice.io/api/random", params=data)
    num_dublicates = 0
    last_inserted_question_id = None
    for question in response.json():
        if question["id"] not in site_ids_in_db:
            insert_questions_query = await session.execute(
                insert(Question).values(
                    id_on_site=question["id"],
                    question_text=question["question"],
                    answer_text=question["answer"],
                    create_date=datetime.datetime.strptime(
                        question["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                )
            )
            last_inserted_question_id = insert_questions_query.inserted_primary_key[0]
        else:
            num_dublicates += 1
    await session.commit()
    q = await session.execute(
        select(Question).where(Question.id == last_inserted_question_id)
    )
    last_inserted_question = q.scalars().one_or_none()
    if num_dublicates != 0:
        last_inserted_question = await post_questions(
            session=session, questions_num=num_dublicates
        )
    return last_inserted_question


async def get_questions(session: AsyncSession) -> List[Question]:
    q = await session.execute(select(Question))
    questions = q.scalars().all()
    return questions
