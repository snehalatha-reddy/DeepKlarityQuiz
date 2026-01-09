from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
try:
    from .database import Base
except ImportError:
    from database import Base

class QuizRecord(Base):
    __tablename__ = "quiz_records"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    title = Column(String)
    summary = Column(Text)
    key_entities = Column(JSON)  # Stores {people: [], organizations: [], ...}
    sections = Column(JSON)      # List of section headers
    related_topics = Column(JSON) # List of related topics
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to questions
    questions = relationship("Question", back_populates="quiz_record", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quiz_records.id"))
    question_text = Column(Text)
    options = Column(JSON)    # List of 4 options
    answer = Column(String)
    difficulty = Column(String)
    explanation = Column(Text)

    quiz_record = relationship("QuizRecord", back_populates="questions")
