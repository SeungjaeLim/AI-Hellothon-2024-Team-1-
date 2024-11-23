from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database, models

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
    All parameters (elder_id, title, and question_ids) are provided in the request body.
    """
    # Validate elder
    elder = crud.get_elder_by_id(db, elder_id=guide_with_questions.elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Validate questions
    for question_id in guide_with_questions.question_ids:
        question = crud.get_question_by_id(db, question_id=question_id)
        if not question:
            raise HTTPException(
                status_code=404, detail=f"Question with ID {question_id} not found"
            )

    # Create the activity guide
    guide_data = models.ActivityGuide(
        elder_id=guide_with_questions.elder_id,
        title=guide_with_questions.title,
        have_studied=False
    )
    db.add(guide_data)
    db.commit()
    db.refresh(guide_data)

    # Link the guide to each question
    for question_id in guide_with_questions.question_ids:
        crud.link_guide_to_question(db, guide_id=guide_data.id, question_id=question_id)

    return guide_data


@router.patch("/finish/{guide_id}", response_model=schemas.ActivityGuide)
def finish_guide(
    guide_id: int,
    db: Session = Depends(database.get_db),
):
    """
    Mark an activity guide as finished by setting have_studied to True.
    """
    # Fetch the activity guide by ID
    guide = db.query(models.ActivityGuide).filter(models.ActivityGuide.id == guide_id).first()
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    # Update the have_studied column
    guide.have_studied = True
    db.commit()
    db.refresh(guide)

    return guide


@router.get("/{guide_id}/questions", response_model=List[schemas.QuestionWithAnswer])
def get_questions_for_guide(guide_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all questions linked to a specific activity guide, including the first answer for each question.
    """
    # Validate the guide
    guide = crud.get_activity_guide_by_id(db, guide_id=guide_id)
    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found")

    # Fetch questions linked to the guide
    questions = crud.get_questions_for_activity_guide(db, guide_id=guide_id)
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this guide")

    # Include the first answer for each question
    enriched_questions = []
    for question in questions:
        first_answer = (
            db.query(models.Answer)
            .filter(models.Answer.question_id == question.id)
            .order_by(models.Answer.response_date.asc())
            .first()
        )

        enriched_questions.append({
            "id": question.id,
            "text": question.text,
            "created_at": question.created_at,
            "first_answer": {
                "id": first_answer.id,
                "response": first_answer.response,
                "response_date": first_answer.response_date,
                "created_at": first_answer.created_at,
            } if first_answer else None,
        })

    return enriched_questions

