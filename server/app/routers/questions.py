from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import FileResponse
from app import schemas, crud, database, models
from app.utils.openai_client import generate_follow_up_question, generate_tts, generate_tts_openai
router = APIRouter()


@router.post("/", response_model=schemas.Question)
def add_question(
    question: schemas.QuestionCreate,
    record_id: int,  # Accept record_id as a query parameter
    db: Session = Depends(database.get_db),
):
    """
    Add a question directly and associate it with a record.
    """
    # Validate the record_id
    record = crud.get_record_by_id(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Check if the question already exists
    existing_question = crud.get_question_by_text(db, text=question.text)
    if existing_question:
        raise HTTPException(status_code=400, detail="Question already exists")

    # Create the question
    new_question = crud.create_question(db, question)

    # Create a record-question relationship
    record_question = models.RecordQuestion(
        record_id=record_id,
        question_id=new_question.id,
    )
    db.add(record_question)
    db.commit()

    return new_question


@router.get("/", response_model=List[schemas.Question])
def get_all_questions(db: Session = Depends(database.get_db)):
    """
    모든 질문 받아오기
    """
    questions = db.query(models.Question).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found")
    return questions


@router.get("/{question_id}", response_model=schemas.Question)
def get_question_by_id(question_id: int, db: Session = Depends(database.get_db)):
    """
    question ID로 질문 받아오기
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

    
    question_data = schemas.QuestionCreate(text=random_text)
    return crud.create_question(db, question=question_data)

@router.post(
    "/generate_follow_up",
    response_model=schemas.GenerateFollowUpResponse,
    summary="Generate a Follow-Up Question",
    description="Generate a meaningful follow-up question for an elder using provided question IDs."
)
def generate_follow_up_question_api(
    input_data: schemas.GenerateFollowUpInput,  # Input schema
    db: Session = Depends(database.get_db),
):
    """
    Generate a follow-up question for an elder using provided question IDs.
    """
    # Validate elder existence
    elder = crud.get_elder_by_id(db, elder_id=input_data.elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Validate questions and retrieve answers
    answers_with_questions = crud.get_answers_by_question_ids(
        db, elder_id=input_data.elder_id, question_ids=input_data.question_ids
    )
    if not answers_with_questions:
        raise HTTPException(
            status_code=404, detail="No questions and answers found for the provided IDs"
        )

    # Prepare data for OpenAI
    question_answer_pairs = [
        {"question": question_text, "answer": answer.response}
        for answer, question_text in answers_with_questions
    ]

    # Generate follow-up question using OpenAI
    follow_up_question = generate_follow_up_question(question_answer_pairs)

    # Save the follow-up question in the database
    follow_up_question_data = schemas.QuestionCreate(text=follow_up_question)
    new_question = crud.create_question(db, question=follow_up_question_data)

    # Return the generated follow-up question
    return schemas.GenerateFollowUpResponse(
        generated_question=follow_up_question,
        question_id=new_question.id,
    )

@router.get("/tts/{question_id}", summary="Generate TTS for a Question", description="Generate TTS audio for a specific question by its ID.")
def generate_tts_for_question(question_id: int, db: Session = Depends(database.get_db)):
    """
    Generate TTS for a question by its ID.

    Args:
        question_id (int): ID of the question.

    Returns:
        FileResponse: The generated TTS audio file.
    """
    # Fetch the question from the database
    question = crud.get_question_by_id(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Generate TTS audio using the Elice API
    try:
        tts_file_path = generate_tts_openai(question.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")

    # Return the audio file as a response
    return FileResponse(tts_file_path, media_type="audio/mpeg", filename=f"question_{question_id}.mp3")
