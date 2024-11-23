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
    기록을 시작할 때 제공하는 노인 친화적 랜덤 질문 제공
    """
    random_questions = [
        "안녕하세요, 오늘 기분은 어떠신가요?",
        "오늘 아침에 드신 음식이 기억나시나요?",
        "최근에 기억에 남는 일이 있으신가요?",
        "오늘 특별히 생각나는 분이 계신가요?",
        "좋아하는 노래가 있다면 어떤 곡인가요?",
        "예전에 가봤던 가장 기억에 남는 장소가 어디인가요?",
        "젊었을 때 하던 취미가 있으셨나요?",
        "오늘은 무엇을 하며 하루를 보내셨나요?",
        "요즘 자주 드는 생각이 있다면 무엇인가요?",
        "가족 중에서 최근에 연락한 사람이 있나요?",
        "요즘 보고 싶은 사람이 있으신가요?",
        "오늘은 무엇을 먹고 싶으신가요?",
        "예전에 즐겨보셨던 영화나 드라마가 있으신가요?",
        "좋아하는 계절이 있다면 어떤 계절인가요?",
        "건강을 위해 요즘 어떤 노력을 하고 계신가요?",
        "친구나 지인들과 어떤 이야기를 나누고 싶으신가요?",
        "가장 좋아하는 추억이 있다면 공유해 주시겠어요?",
        "오늘 마주한 재미있는 일이 있었나요?",
        "어릴 적 자주 가던 곳이 떠오르시나요?",
        "요즘 취미로 즐기고 계신 것이 있나요?",
        "예전과 달라진 점이 있다면 무엇인가요?",
        "오늘은 어떤 이야기를 하고 싶으신가요?",
        "주변 사람들에게 감사하고 싶은 일이 있으신가요?",
        "오늘 특별히 기쁜 일이 있었나요?",
        "요즘 관심이 가는 것이 있다면 무엇인가요?",
        "가장 좋아하는 음식이 무엇인지 말씀해 주시겠어요?",
        "어떤 꿈을 꾸셨는지 기억나시나요?",
        "요즘 자주 생각나는 풍경이 있나요?",
        "어린 시절 자주 하던 놀이가 있었나요?",
        "오늘 하루가 어땠는지 말씀해 주세요."
    ]

    from random import choice
    random_text = choice(random_questions)

    existing_question = crud.get_question_by_text(db, text=random_text)
    if existing_question:
        raise HTTPException(status_code=400, detail="Question already exists")

    question_data = schemas.QuestionCreate(text=random_text)
    return crud.create_question(db, question=question_data)
