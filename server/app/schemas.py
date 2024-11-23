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


# Generate Follow-Up Question schemas
class GenerateFollowUpInput(BaseModel):
    """
    Input schema for generating a follow-up question.
    """
    elder_id: int
    question_ids: List[int]


class GenerateFollowUpResponse(BaseModel):
    """
    Response schema for the generated follow-up question.
    """
    generated_question: str
    question_id: int


class Question(BaseModel):
    id: int
    text: str
    is_reported: bool = False  # Default value for API response
    created_at: datetime

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
    elder_id: int
    title: str
    have_studied: bool = False


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


class ActivityGuideWithQuestionsCreate(BaseModel):
    """
    Schema for creating an activity guide with linked questions.
    """
    elder_id: int
    title: str
    question_ids: List[int]


# Guide-Question relationship schema (optional, for debugging purposes)
class GuideQuestion(BaseModel):
    """
    Schema for linking an activity guide to a question.
    """
    guide_id: int
    question_id: int

    class Config:
        orm_mode = True

class Task(BaseModel):
    """
    Response schema for a task.
    """
    id: int
    elder_id: int
    year: int
    week_number: int
    status: int
    iteration: int  # Ensure iteration is defined here
    created_at: datetime

    class Config:
        orm_mode = True



class TaskBase(BaseModel):
    """
    Shared base schema for tasks.
    """
    elder_id: int
    year: int
    week_number: int
    status: int


class TaskCreate(TaskBase):
    """
    Schema for creating a task.
    """
    pass



class Analysis(BaseModel):
    id: int
    question_id: int
    first_answer_id: int
    last_answer_id: int
    similarity: float
    report_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


class Report(BaseModel):
    id: int
    elder_id: int
    year: int
    week_number: int  # 변경된 부분
    created_at: datetime
    analyses: List[Analysis]

    class Config:
        from_attributes = True
