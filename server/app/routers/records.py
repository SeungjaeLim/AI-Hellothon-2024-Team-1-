from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database, models
from app.utils.openai_client import summarize_text, generate_title, extract_keywords, generate_image

router = APIRouter()


@router.get("/", response_model=List[schemas.Record])
def get_all_records(db: Session = Depends(database.get_db)):
    """
    Retrieve all records, including an image and keywords.
    """
    records = db.query(models.Record).all()
    if not records:
        raise HTTPException(status_code=404, detail="No records found")

    response = []
    for record in records:
        image = crud.get_image_by_record_id(db, record_id=record.id)
        keywords = crud.get_keywords_by_record_id(db, record_id=record.id)
        response.append({
            "id": record.id,
            "title": record.title,
            "content": record.content,
            "elder_id": record.elder_id,
            "created_at": record.created_at,
            "image": image,
            "keywords": keywords,
        })

    return response



@router.get("/user/{elder_id}", response_model=List[schemas.Record])
def get_records_for_elder(elder_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all records for a specific elder by elder_id, including images and keywords.
    """
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    records = crud.get_records_by_elder_id(db, elder_id=elder_id)
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this elder")

    # Enrich each record with image and keywords
    enriched_records = []
    for record in records:
        image = crud.get_image_by_record_id(db, record_id=record.id)
        keywords = crud.get_keywords_by_record_id(db, record_id=record.id)
        enriched_records.append({
            "id": record.id,
            "title": record.title,
            "content": record.content,
            "elder_id": record.elder_id,
            "created_at": record.created_at,
            "image": image,
            "keywords": keywords
        })

    return enriched_records



@router.get("/{record_id}", response_model=schemas.Record)
def get_record_by_id(record_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a single record by its ID, including an image and keywords.
    """
    record = crud.get_record_by_id(db, record_id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    # Fetch the single image and keywords
    image = crud.get_image_by_record_id(db, record_id=record.id)
    keywords = crud.get_keywords_by_record_id(db, record_id=record.id)

    # Include image and keywords in the response
    return {
        "id": record.id,
        "title": record.title,
        "content": record.content,
        "elder_id": record.elder_id,
        "created_at": record.created_at,
        "image": image,
        "keywords": keywords,
    }

@router.post("/", response_model=dict)
def create_todays_record(
    record_create: schemas.RecordCreateInput,
    db: Session = Depends(database.get_db)
):
    """
    Create today's record for an elder using a list of question IDs, including keywords and images.
    """
    # Validate elder existence
    elder = crud.get_elder_by_id(db, elder_id=record_create.elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Validate questions and retrieve answers
    answers_with_questions = crud.get_answers_by_question_ids(
        db, elder_id=record_create.elder_id, question_ids=record_create.question_ids
    )
    if not answers_with_questions:
        raise HTTPException(status_code=404, detail="No answers found for the provided questions")

    # Combine answers into a single text
    combined_text = "\n".join([
        f"Q: {question_text}\nA: {answer.response}"
        for answer, question_text in answers_with_questions
    ])

    # Generate content using OpenAI
    summary = summarize_text(combined_text)
    title = generate_title(summary)
    keywords = extract_keywords(summary)
    image_path = generate_image(", ".join(keywords))  # Save the image locally

    # Create the record
    record_data = schemas.RecordCreate(
        title=title,
        content=summary,
        elder_id=record_create.elder_id,
    )
    new_record = crud.create_record(db, record=record_data)

    # Add keywords to the record
    for keyword in keywords:
        keyword_instance = crud.create_or_get_keyword(db, keyword=keyword)
        crud.add_keyword_to_record(db, record_id=new_record.id, keyword_id=keyword_instance.id)

    # Add image to the record in the database
    crud.add_image_to_record(db, record_id=new_record.id, image_url=image_path)

    # Add record questions for the used questions
    for answer, question_text in answers_with_questions:
        crud.add_record_question(db, record_id=new_record.id, question_id=answer.question_id)

    # Return the response including the image and keywords
    return {
        "id": new_record.id,
        "elder_id": new_record.elder_id,
        "title": new_record.title,
        "content": new_record.content,
        "created_at": new_record.created_at,
        "image": image_path,  # Return the local image path
        "keywords": keywords  # Return the list of keywords
    }
