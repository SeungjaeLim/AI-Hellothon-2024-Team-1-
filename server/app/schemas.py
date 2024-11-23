from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# Elder schemas
class ElderBase(BaseModel):
    """
    Shared base schema for elders.
    """
    name: str
    birth_date: date
    gender: str
    care_level: str
    contact_info: Optional[str] = None


class ElderCreate(ElderBase):
    """
    Schema for creating a new elder.
    """
    pass


class Elder(ElderBase):
    """
    Response schema for an elder.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Record schemas
class RecordBase(BaseModel):
    """
    Shared base schema for records.
    """
    title: str
    content: Optional[str] = None


class RecordCreate(BaseModel):
    """
    Schema for creating a record in the database.
    """
    title: str
    content: Optional[str] = None
    elder_id: int


class RecordCreateInput(BaseModel):
    """
    Schema for API input, including question IDs.
    """
    elder_id: int
    question_ids: List[int]

class Record(RecordBase):
    """
    Response schema for a record.
    """
    id: int
    elder_id: int
    created_at: datetime
    image: Optional[str]  # Single image URL
    keywords: List[str]  # List of associated keywords

    class Config:
        orm_mode = True



# Question schemas
class QuestionBase(BaseModel):
    """
    Shared base schema for questions.
    """
    text: str


class QuestionCreate(QuestionBase):
    """
    Schema for creating a new question.
    """
    pass


class Question(QuestionBase):
    """
    Response schema for a question.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Answer schemas
class AnswerBase(BaseModel):
    """
    Shared base schema for answers.
    """
    response: str
    response_date: date


class AnswerCreate(AnswerBase):
    """
    Schema for creating a new answer.
    """
    elder_id: int
    question_id: int


class Answer(AnswerBase):
    """
    Response schema for an answer.
    """
    id: int
    elder_id: int
    question_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Keyword schemas
class Keyword(BaseModel):
    """
    Schema for a keyword.
    """
    id: int
    keyword: str

    class Config:
        orm_mode = True


class KeywordPreference(BaseModel):
    """
    Schema for keyword preferences.
    """
    elder_id: int
    keyword_id: int
    is_preferred: bool

    class Config:
        orm_mode = True


# Activity Guide schemas
class ActivityGuideBase(BaseModel):
    """
    Shared base schema for activity guides (lesson plans).
    """
    title: str


class ActivityGuideCreate(ActivityGuideBase):
    """
    Schema for creating a new activity guide.
    """
    pass


class ActivityGuide(ActivityGuideBase):
    """
    Response schema for an activity guide.
    """
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Guide-Question relationship schema (optional, for debugging purposes)
class GuideQuestion(BaseModel):
    """
    Schema for linking an activity guide to a question.
    """
    guide_id: int
    question_id: int

    class Config:
        orm_mode = True
