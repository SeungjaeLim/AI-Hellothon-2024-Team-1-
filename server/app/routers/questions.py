from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database

router = APIRouter()


@router.post("/", response_model=schemas.Question)
def add_question(question: schemas.QuestionCreate, db: Session = Depends(database.get_db)):
    """
    Add a new question to the database.
    """
    existing_question = crud.get_question_by_text(db, text=question.text)
    if existing_question:
        raise HTTPException(status_code=400, detail="Question already exists")

    return crud.create_question(db, question)


@router.get("/", response_model=List[schemas.Question])
def get_all_questions(db: Session = Depends(database.get_db)):
    """
    Retrieve all questions from the database.
    """
    questions = db.query(models.Question).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


@router.get("/{question_id}", response_model=schemas.Question)
def get_question_by_id(question_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a question by its ID.
    """
    question = crud.get_question_by_id(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/record/{record_id}/questions", response_model=List[schemas.Question])
def get_questions_by_record(record_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all questions linked to a specific record.
    """
    record = crud.get_record_by_id(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    questions = crud.get_questions_by_record_id(db, record_id=record_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this record")

    return questions


@router.post("/random", response_model=schemas.Question)
def add_random_question(db: Session = Depends(database.get_db)):
    """
    Add a random question to the database.
    """
    random_questions = [
        "What is your happiest memory?",
        "Can you describe your favorite vacation?",
        "What hobby do you enjoy the most?",
        "Who has had the most influence on your life?",
        "What are you most proud of?"
    ]

    from random import choice
    random_text = choice(random_questions)

    existing_question = crud.get_question_by_text(db, text=random_text)
    if existing_question:
        raise HTTPException(status_code=400, detail="Question already exists")

    question_data = schemas.QuestionCreate(text=random_text)
    return crud.create_question(db, question=question_data)
