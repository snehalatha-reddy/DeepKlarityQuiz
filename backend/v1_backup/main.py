from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import json

try:
    from . import models, schemas
    from .database import engine, get_db
    from .scraper import scrape_wikipedia
    from .quiz_generator import generate_quiz_from_text
except ImportError:
    import models, schemas
    from database import engine, get_db
    from scraper import scrape_wikipedia
    from quiz_generator import generate_quiz_from_text

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WikiQuiz API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL (e.g., http://localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_quiz", response_model=schemas.QuizResponse)
def generate_quiz(request: schemas.QuizRequest, db: Session = Depends(get_db)):
    url = request.url
    
    # 1. Check Cache
    existing_quiz = db.query(models.QuizRecord).filter(models.QuizRecord.url == url).first()
    if existing_quiz:
        # Reconstruct response from DB
        questions = []
        for q in existing_quiz.questions:
            questions.append(schemas.QuestionBase(
                question=q.question_text,
                options=json.loads(q.options) if isinstance(q.options, str) else q.options,
                answer=q.answer,
                difficulty=q.difficulty,
                explanation=q.explanation
            ))
            
        return schemas.QuizResponse(
            id=existing_quiz.id,
            url=existing_quiz.url,
            title=existing_quiz.title,
            summary=existing_quiz.summary,
            key_entities=json.loads(existing_quiz.key_entities) if isinstance(existing_quiz.key_entities, str) else existing_quiz.key_entities,
            sections=json.loads(existing_quiz.sections) if isinstance(existing_quiz.sections, str) else existing_quiz.sections,
            quiz=questions,
            related_topics=json.loads(existing_quiz.related_topics) if isinstance(existing_quiz.related_topics, str) else existing_quiz.related_topics,
            created_at=existing_quiz.created_at
        )

    # 2. Scrape
    try:
        scraped_data = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping error: {str(e)}")

    # 3. Generate with LLM
    try:
        llm_data = generate_quiz_from_text(scraped_data["text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Generation error: {str(e)}")

    # 4. Save to DB
    # Convert lists/dicts to JSON strings if using SQLite/Text columns (SQLAlchemy JSON type handles this automatically on Postgres, but good to be safe if driver issues arise, though specific dialects handle it. Here we use JSON type which should work with SQLite as modern sqlalchemy supports it or falls back properly usually. Let's assume it works or we might need explicit serialization if using very old sqlite. Modern generic JSON type usually works.)
    # Actually, SQLAlchemy's JSON type on SQLite caches as generic JSON, but typically it expects the driver to handle it.
    # To be safe for a simple app: I'll trust SQLAlchemy JSON type or ensure input is python dicts.
    
    # Merge LLM summary with scraped summary (LLM summary is often better for a quick read, but Scraper got the first para). 
    # Let's use LLM summary as primary if available.
    final_summary = llm_data.get("summary", scraped_data["summary"])
    
    # CRITICAL FIX: Do NOT save mock data to the database!
    is_mock_data = "mock summary" in final_summary.lower() or "mock question" in str(llm_data).lower()
    
    if not is_mock_data:
        quiz_record = models.QuizRecord(
            url=url,
            title=scraped_data["title"],
            summary=final_summary,
            key_entities=llm_data.get("key_entities", {}),
            sections=scraped_data["sections"],
            related_topics=llm_data.get("related_topics", [])
        )
        db.add(quiz_record)
        db.commit()
        db.refresh(quiz_record)

        # Add questions
        generated_questions = llm_data.get("quiz", [])
        for q in generated_questions:
            question = models.Question(
                quiz_id=quiz_record.id,
                question_text=q["question"],
                options=q["options"],
                answer=q["answer"],
                difficulty=q["difficulty"],
                explanation=q["explanation"]
            )
            db.add(question)
        
        db.commit()
        
        # Return saved record structure
        return schemas.QuizResponse(
            id=quiz_record.id,
            url=url,
            title=quiz_record.title,
            summary=quiz_record.summary,
            key_entities=quiz_record.key_entities,
            sections=quiz_record.sections,
            quiz=[schemas.QuestionBase(**q) for q in generated_questions],
            related_topics=quiz_record.related_topics,
            created_at=quiz_record.created_at
        )

    else:
        # If it is mock data, return it directly without saving to DB
        # We need a dummy ID for the schema
        print("WARNING: Generated data appears to be mock/error data. Not saving to DB.")
        return schemas.QuizResponse(
            id=0, # Arbitrary ID for non-persisted data
            url=url,
            title=scraped_data["title"],
            summary=final_summary,
            key_entities=llm_data.get("key_entities", {}),
            sections=scraped_data["sections"],
            quiz=[schemas.QuestionBase(**q) for q in llm_data.get("quiz", [])],
            related_topics=llm_data.get("related_topics", []),
            created_at=None
        )

@app.get("/history", response_model=List[schemas.HistoryItem])
def get_history(db: Session = Depends(get_db)):
    quizzes = db.query(models.QuizRecord).order_by(models.QuizRecord.created_at.desc()).all()
    return quizzes

@app.get("/quiz/{quiz_id}", response_model=schemas.QuizResponse)
def get_quiz_details(quiz_id: int, db: Session = Depends(get_db)):
    quiz_record = db.query(models.QuizRecord).filter(models.QuizRecord.id == quiz_id).first()
    if not quiz_record:
        raise HTTPException(status_code=404, detail="Quiz not found")
        
    questions = []
    for q in quiz_record.questions:
        questions.append(schemas.QuestionBase(
            question=q.question_text,
            options=json.loads(q.options) if isinstance(q.options, str) else q.options,
            answer=q.answer,
            difficulty=q.difficulty,
            explanation=q.explanation
        ))

    return schemas.QuizResponse(
        id=quiz_record.id,
        url=quiz_record.url,
        title=quiz_record.title,
        summary=quiz_record.summary,
        key_entities=json.loads(quiz_record.key_entities) if isinstance(quiz_record.key_entities, str) else quiz_record.key_entities,
        sections=json.loads(quiz_record.sections) if isinstance(quiz_record.sections, str) else quiz_record.sections,
        quiz=questions,
        related_topics=json.loads(quiz_record.related_topics) if isinstance(quiz_record.related_topics, str) else quiz_record.related_topics,
        created_at=quiz_record.created_at
    )
