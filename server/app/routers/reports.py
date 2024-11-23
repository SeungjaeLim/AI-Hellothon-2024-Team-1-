from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from app import schemas, crud, database, models
from app.utils.openai_client import get_text_embedding
from scipy.spatial.distance import cosine

router = APIRouter()


@router.get("/", response_model=schemas.Report)
def get_report(
    elder_id: int,
    year: int,
    week_number: int,  # Updated to week_number
    db: Session = Depends(database.get_db),
):
    """
    Get a report and its associated analyses by elder_id, year, and week_number.
    """
    report = (
        db.query(models.Report)
        .filter(
            models.Report.elder_id == elder_id,
            models.Report.year == year,
            models.Report.week_number == week_number,  # Use week_number
        )
        .first()
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Fetch associated analyses
    analyses = (
        db.query(models.Analysis)
        .filter(models.Analysis.report_id == report.id)
        .all()
    )

    return {
        "id": report.id,
        "elder_id": report.elder_id,
        "year": report.year,
        "week_number": report.week_number,
        "created_at": report.created_at,
        "analyses": analyses,
    }
@router.post("/", response_model=schemas.Report)
def create_or_update_report(
    elder_id: int,
    year: int,
    week_number: int,  # Updated to week_number
    db: Session = Depends(database.get_db),
):
    """
    Create or update a report for a given elder, year, and week_number,
    including analyses of question answers.
    """
    from datetime import datetime, timedelta

    # Validate elder existence
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Calculate start and end dates for the week
    start_date = datetime.strptime(f"{year}-{week_number}-1", "%Y-%W-%w")
    end_date = start_date + timedelta(days=6)
    print(f"Week range: {start_date} to {end_date}")

    # Check if the report already exists
    report = (
        db.query(models.Report)
        .filter(
            models.Report.elder_id == elder_id,
            models.Report.year == year,
            models.Report.week_number == week_number,
        )
        .first()
    )

    if report:
        print(f"Report already exists: {report}")
        # Delete existing analyses linked to the report
        db.query(models.Analysis).filter(models.Analysis.report_id == report.id).delete()
        db.commit()
        print(f"Deleted old analyses for report_id={report.id}")
    else:
        # Create a new report if it doesn't exist
        report = models.Report(
            elder_id=elder_id,
            year=year,
            week_number=week_number,
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        print(f"Created new report: {report}")

    # Fetch all studied guides for the given week range
    studied_guides = (
        db.query(models.ActivityGuide)
        .filter(
            models.ActivityGuide.elder_id == elder_id,
            models.ActivityGuide.have_studied == True,
            models.ActivityGuide.created_at >= start_date,
            models.ActivityGuide.created_at <= end_date,
        )
        .all()
    )

    if not studied_guides:
        raise HTTPException(status_code=404, detail="No studied guides found for this week")

    # Extract all questions from the studied guides
    question_ids = []
    for guide in studied_guides:
        questions = crud.get_questions_for_activity_guide(db, guide_id=guide.id)
        question_ids.extend([q.id for q in questions])
    print(f"All question IDs for studied guides: {question_ids}")

    # Analyze questions with at least two answers
    analyses = []
    for question_id in question_ids:
        answers = (
            db.query(models.Answer)
            .filter(
                models.Answer.question_id == question_id,
                models.Answer.elder_id == elder_id,
                models.Answer.response_date >= start_date,
                models.Answer.response_date <= end_date,
            )
            .order_by(models.Answer.response_date)
            .all()
        )
        if len(answers) < 2:
            print(f"Skipping question_id={question_id} as it has less than 2 answers.")
            continue  # Skip if there aren't at least two answers

        # Take the oldest and the most recent answers
        first_answer, last_answer = answers[0], answers[-1]

        # Generate embeddings for the responses
        first_embedding = get_text_embedding(first_answer.response)
        last_embedding = get_text_embedding(last_answer.response)

        # Calculate cosine similarity
        similarity = 1 - cosine(first_embedding, last_embedding)

        # Create an analysis entry
        analysis = models.Analysis(
            elder_id=elder_id,
            question_id=question_id,
            first_answer_id=first_answer.id,
            last_answer_id=last_answer.id,
            similarity=round(similarity * 100, 2),  # Convert to percentage
            report_id=report.id,  # Link to the created/updated report
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        analyses.append(analysis)

    return {
        "id": report.id,
        "elder_id": report.elder_id,
        "year": report.year,
        "week_number": report.week_number,
        "created_at": report.created_at,
        "analyses": analyses,
    }
