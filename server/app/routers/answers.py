from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database, models
from app.utils.openai_client import transcribe_audio
import os
import uuid
router = APIRouter()


@router.get("/", response_model=List[schemas.Answer])
def get_all_answers(db: Session = Depends(database.get_db)):
    """
    Retrieve all answers from the database.
    """
    answers = db.query(models.Answer).all()
    if not answers:
        raise HTTPException(status_code=404, detail="No answers found")
    return answers

@router.post("/", response_model=schemas.Answer)
async def save_audio_answer(
    elder_id: int = Form(...),
    question_id: int = Form(...),
    audio: UploadFile = Form(...),
    db: Session = Depends(database.get_db),
):
    """
    Save an audio answer to the database.
    """
    # Validate elder
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Validate question
    question = crud.get_question_by_id(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Generate a unique file name to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{audio.filename}"
    audio_file_path = os.path.join("/tmp", unique_filename)
    print(f"Saving audio file to {audio_file_path}")

    # Save the uploaded audio temporarily
    with open(audio_file_path, "wb") as f:
        content = await audio.read()
        f.write(content)

    # Transcribe audio using OpenAI Whisper
    try:
        transcription = transcribe_audio(audio_file_path)
    except Exception as e:
        os.remove(audio_file_path)  # Clean up the temp file
        raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(e)}")

    # Clean up the audio file after transcription
    os.remove(audio_file_path)

    # Save the transcription as an answer in the database
    answer_data = schemas.AnswerCreate(
        elder_id=elder_id,
        question_id=question_id,
        response=transcription,
        response_date=schemas.date.today(),
    )
    new_answer = crud.create_answer(db, answer=answer_data)

    return new_answer


@router.get("/question/{question_id}", response_model=List[schemas.Answer])
def get_answers_for_question(question_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all answers for a specific question.
    """
    question = crud.get_question_by_id(db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    answers = db.query(models.Answer).filter(models.Answer.question_id == question_id).all()
    if not answers:
        raise HTTPException(status_code=404, detail="No answers found for this question")

    return answers
