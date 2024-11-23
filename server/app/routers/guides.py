from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database

router = APIRouter()

@router.get("/", response_model=List[schemas.ActivityGuide])
def get_all_guides(db: Session = Depends(database.get_db)):
    """
    Retrieve all activity guides.
    """
    guides = crud.get_all_activity_guides(db)
    if not guides:
        raise HTTPException(status_code=404, detail="No activity guides found")
    return guides


@router.post("/create_with_questions", response_model=schemas.ActivityGuide)
def create_guide_with_questions(
    guide_with_questions: schemas.ActivityGuideWithQuestionsCreate,
    db: Session = Depends(database.get_db),
):
    """
    Create an activity guide and link it to specific questions.
    All parameters (record_id, question_ids, and guide_data) are provided in the request body.
    """
    # Validate record
    record = crud.get_record_by_id(db, record_id=guide_with_questions.record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Validate questions
    for question_id in guide_with_questions.question_ids:
        question = crud.get_question_by_id(db, question_id=question_id)
        if not question:
            raise HTTPException(
                status_code=404, detail=f"Question with ID {question_id} not found"
            )

    # Create the activity guide
    new_guide = crud.create_activity_guide(db, guide=guide_with_questions.guide_data)

    # Link the guide to each question
    for question_id in guide_with_questions.question_ids:
        crud.link_guide_to_question(db, guide_id=new_guide.id, question_id=question_id)

    return new_guide


@router.get("/{guide_id}/questions", response_model=List[schemas.Question])
def get_questions_for_guide(guide_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all questions linked to a specific activity guide.
    """
    guide = crud.get_activity_guide_by_id(db, guide_id=guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    questions = crud.get_questions_for_activity_guide(db, guide_id=guide_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this guide")

    return questions
