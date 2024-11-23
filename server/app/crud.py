from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from typing import List, Optional


# Elders
def get_elder_by_id(db: Session, elder_id: int):
    """
    Retrieve an elder by their ID.
    """
    return db.query(models.Elder).filter(models.Elder.id == elder_id).first()


def get_answers_by_question_id(db: Session, question_id: int):
    """
    Retrieve all answers for a specific question ID.
    """
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()


def get_all_elders(db: Session):
    """
    Retrieve all elders.
    """
    return db.query(models.Elder).all()


def create_elder(db: Session, elder: schemas.ElderCreate):
    """
    Create a new elder.
    """
    db_elder = models.Elder(**elder.dict())
    db.add(db_elder)
    db.commit()
    db.refresh(db_elder)
    return db_elder


# Records
def get_record_by_id(db: Session, record_id: int):
    """
    Retrieve a record by its ID.
    """
    return db.query(models.Record).filter(models.Record.id == record_id).first()


def get_records_by_elder_id(db: Session, elder_id: int):
    """
    Retrieve all records for a specific elder.
    """
    return db.query(models.Record).filter(models.Record.elder_id == elder_id).all()


def create_record(db: Session, record: schemas.RecordCreate) -> models.Record:
    """
    Create a new record in the database.
    """
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record



# Questions
def get_question_by_id(db: Session, question_id: int):
    """
    Retrieve a question by its ID.
    """
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_question_by_text(db: Session, text: str):
    """
    Retrieve a question by its text.
    """
    return db.query(models.Question).filter(models.Question.text == text).first()


def get_questions_by_record_id(db: Session, record_id: int):
    """
    Retrieve all questions linked to a specific record.
    """
    return (
        db.query(models.Question)
        .join(models.RecordQuestion, models.RecordQuestion.question_id == models.Question.id)
        .filter(models.RecordQuestion.record_id == record_id)
        .all()
    )


def create_question(db: Session, question: schemas.QuestionCreate):
    """
    Create a new question.
    """
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_answers_by_question_ids(db: Session, elder_id: int, question_ids: list):
    """
    Retrieve answers for a list of question IDs by a specific elder, including question text.
    """
    return (
        db.query(models.Answer, models.Question.text)
        .join(models.Question, models.Answer.question_id == models.Question.id)
        .filter(models.Answer.elder_id == elder_id, models.Answer.question_id.in_(question_ids))
        .all()
    )

def create_answer(db: Session, answer: schemas.AnswerCreate):
    """
    Create a new answer.
    """
    db_answer = models.Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


# Keywords
def get_keywords_by_elder_id(db: Session, elder_id: int):
    """
    Retrieve all keywords and preferences associated with an elder.
    """
    return (
        db.query(models.Keyword, models.KeywordPreference.is_preferred)
        .join(models.KeywordPreference, models.Keyword.id == models.KeywordPreference.keyword_id)
        .filter(models.KeywordPreference.elder_id == elder_id)
        .all()
    )


def toggle_keyword_preference(db: Session, elder_id: int, keyword_id: int):
    """
    Toggle the preference for a specific keyword for an elder.
    """
    preference = (
        db.query(models.KeywordPreference)
        .filter(models.KeywordPreference.elder_id == elder_id, models.KeywordPreference.keyword_id == keyword_id)
        .first()
    )
    if not preference:
        return None
    preference.is_preferred = not preference.is_preferred
    db.commit()
    db.refresh(preference)
    return preference


# Activity Guides
def create_activity_guide(db: Session, guide: schemas.ActivityGuideCreate):
    """
    Create a new activity guide (lesson plan).
    """
    db_guide = models.ActivityGuide(**guide.dict())
    db.add(db_guide)
    db.commit()
    db.refresh(db_guide)
    return db_guide


def get_all_activity_guides(db: Session):
    """
    Retrieve all activity guides.
    """
    return db.query(models.ActivityGuide).all()


def get_activity_guides_by_record_ids(db: Session, record_ids: list):
    """
    Retrieve activity guides linked to specific record IDs.
    """
    return (
        db.query(models.ActivityGuide)
        .join(models.GuideQuestion, models.ActivityGuide.id == models.GuideQuestion.guide_id)
        .filter(models.GuideQuestion.record_id.in_(record_ids))
        .all()
    )


# Guide-Question Relationships
def link_guide_to_question(db: Session, guide_id: int, question_id: int):
    """
    Link a guide to a specific question.
    """
    guide_question = models.GuideQuestion(guide_id=guide_id, question_id=question_id)
    db.add(guide_question)
    db.commit()


def get_questions_for_activity_guide(db: Session, guide_id: int):
    """
    Retrieve all questions linked to a specific activity guide.
    """
    return (
        db.query(models.Question)
        .join(models.GuideQuestion, models.GuideQuestion.question_id == models.Question.id)
        .filter(models.GuideQuestion.guide_id == guide_id)
        .all()
    )

def create_or_get_keyword(db: Session, keyword: str) -> models.Keyword:
    """
    Create a new keyword if it doesn't exist, or retrieve the existing one.
    Args:
        db (Session): SQLAlchemy session object.
        keyword (str): The keyword to create or retrieve.
    Returns:
        models.Keyword: The keyword instance.
    """
    db_keyword = db.query(models.Keyword).filter(models.Keyword.keyword == keyword).first()
    if db_keyword:
        return db_keyword

    new_keyword = models.Keyword(keyword=keyword)
    db.add(new_keyword)
    try:
        db.commit()
        db.refresh(new_keyword)
    except IntegrityError:
        db.rollback()
        db_keyword = db.query(models.Keyword).filter(models.Keyword.keyword == keyword).first()
        if db_keyword:
            return db_keyword
        raise
    return new_keyword

def add_keyword_to_record(db: Session, record_id: int, keyword_id: int):
    """
    Link a keyword to a specific record.
    Args:
        db (Session): SQLAlchemy session object.
        record_id (int): ID of the record.
        keyword_id (int): ID of the keyword.
    """
    record_keyword = models.RecordKeyword(record_id=record_id, keyword_id=keyword_id)
    db.add(record_keyword)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise Exception(f"Keyword {keyword_id} is already linked to Record {record_id}")

def add_image_to_record(db: Session, record_id: int, image_url: str):
    """
    Add an image to a specific record.
    """
    # Create an Image object
    image = models.Image(record_id=record_id, url=image_url)
    
    # Add it to the session and commit
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_image_by_record_id(db: Session, record_id: int) -> Optional[str]:
    """
    Fetch the single image URL for a record.
    """
    image = db.query(models.Image).filter(models.Image.record_id == record_id).first()
    return image.url if image else None

def get_keywords_by_record_id(db: Session, record_id: int) -> List[str]:
    """
    Fetch the list of keywords for a record.
    """
    keywords = (
        db.query(models.Keyword.keyword)
        .join(models.RecordKeyword, models.RecordKeyword.keyword_id == models.Keyword.id)
        .filter(models.RecordKeyword.record_id == record_id)
        .all()
    )
    return [keyword[0] for keyword in keywords]  # Extract the keyword strings

def add_record_question(db: Session, record_id: int, question_id: int):
    """
    Link a question to a record in the record_questions table.
    """
    record_question = models.RecordQuestion(record_id=record_id, question_id=question_id)
    db.add(record_question)
    db.commit()
    return record_question
