from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app import models, schemas


# Elders
def get_elder_by_id(db: Session, elder_id: int):
    """
    Retrieve an elder by their ID.
    """
    return db.query(models.Elder).filter(models.Elder.id == elder_id).first()


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


def create_record(db: Session, record: schemas.RecordCreate):
    """
    Create a new record.
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


# Answers
def get_answers_by_question_ids(db: Session, elder_id: int, question_ids: list):
    """
    Retrieve answers for a list of question IDs by a specific elder.
    """
    return (
        db.query(models.Answer)
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
