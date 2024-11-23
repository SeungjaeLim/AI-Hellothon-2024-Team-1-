from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List
from app import schemas, crud, database, models
from app.utils.openai_client import get_text_embedding
from scipy.spatial.distance import cosine

router = APIRouter()

@router.get("/", response_model=dict)
def get_report(
    elder_id: int,
    year: int,
    week_number: int,
    db: Session = Depends(database.get_db),
):
    """
    Get a report and its associated analyses by elder_id, year, and week_number,
    including question content and answer details.
    """
    # Fetch the report
    report = (
        db.query(models.Report)
        .filter(
            models.Report.elder_id == elder_id,
            models.Report.year == year,
            models.Report.week_number == week_number,
        )
        .first()
    )
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    # Fetch associated analyses and join with question and answer data
    analyses = (
        db.query(
            models.Analysis.id,
            models.Analysis.question_id,
            models.Question.text.label("question"),
            models.Analysis.first_answer_id,
            func.coalesce(models.Answer.response, "").label("first_answer"),
            models.Analysis.last_answer_id,
            func.coalesce(models.Answer.response, "").label("last_answer"),
            models.Analysis.similarity,
            models.Analysis.report_id,
            models.Analysis.created_at,
        )
        .join(models.Question, models.Question.id == models.Analysis.question_id)
        .join(models.Answer, models.Answer.id == models.Analysis.first_answer_id)
        .join(models.Answer, models.Answer.id == models.Analysis.last_answer_id)
        .filter(models.Analysis.report_id == report.id)
        .all()
    )

    # Format the analyses response
    analyses_details = [
        {
            "id": analysis.id,
            "question_id": analysis.question_id,
            "question": analysis.question,
            "first_answer_id": analysis.first_answer_id,
            "first_answer": analysis.first_answer,
            "last_answer_id": analysis.last_answer_id,
            "last_answer": analysis.last_answer,
            "similarity": analysis.similarity,
            "report_id": analysis.report_id,
            "created_at": analysis.created_at,
        }
        for analysis in analyses
    ]

    return {
        "id": report.id,
        "elder_id": report.elder_id,
        "year": report.year,
        "week_number": report.week_number,
        "created_at": report.created_at,
        "analyses": analyses_details,
    }


@router.post("/", response_model=dict)
def create_or_update_report(
    elder_id: int,
    year: int,
    week_number: int,
    db: Session = Depends(database.get_db),
):
    """
    Create or update a report for a given elder, year, and week_number,
    including analyses of question answers with question and answer details.
    """
    from datetime import datetime, timedelta

    # Validate elder existence
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    # Calculate start and end dates for the week
    start_date = datetime.strptime(f"{year}-{week_number}-1", "%Y-%W-%w")
    end_date = start_date + timedelta(days=6)

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
        db.query(models.Analysis).filter(models.Analysis.report_id == report.id).delete()
        db.commit()
    else:
        report = models.Report(elder_id=elder_id, year=year, week_number=week_number)
        db.add(report)
        db.commit()
        db.refresh(report)

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

    question_ids = []
    for guide in studied_guides:
        questions = crud.get_questions_for_activity_guide(db, guide_id=guide.id)
        question_ids.extend([q.id for q in questions])

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
            continue

        first_answer, last_answer = answers[0], answers[-1]
        first_embedding = get_text_embedding(first_answer.response)
        last_embedding = get_text_embedding(last_answer.response)
        similarity = 1 - cosine(first_embedding, last_embedding)

        analysis = models.Analysis(
            elder_id=elder_id,
            question_id=question_id,
            first_answer_id=first_answer.id,
            last_answer_id=last_answer.id,
            similarity=round(similarity * 100, 2),
            report_id=report.id,
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        analyses.append({
            "id": analysis.id,
            "question_id": question_id,
            "question": db.query(models.Question).filter(models.Question.id == question_id).first().text,
            "first_answer_id": first_answer.id,
            "first_answer": first_answer.response,
            "last_answer_id": last_answer.id,
            "last_answer": last_answer.response,
            "similarity": analysis.similarity,
            "report_id": report.id,
            "created_at": analysis.created_at,
        })

    return {
        "id": report.id,
        "elder_id": report.elder_id,
        "year": report.year,
        "week_number": report.week_number,
        "created_at": report.created_at,
        "analyses": analyses,
    }
