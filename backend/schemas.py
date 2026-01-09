from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

class QuizRequest(BaseModel):
    url: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    key_entities: Dict[str, List[str]]
    sections: List[str]
    quiz: List[QuestionBase]
    related_topics: List[str]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HistoryItem(BaseModel):
    id: int
    url: str
    title: str
    created_at: datetime
    
    class Config:
        from_attributes = True
