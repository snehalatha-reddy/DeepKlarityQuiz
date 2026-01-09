
from database import SessionLocal, engine
from models import Base, QuizRecord, Question
from sqlalchemy import text

def clear_cache():
    try:
        db = SessionLocal()
        # Delete all quizzes and questions
        db.query(Question).delete()
        db.query(QuizRecord).delete()
        db.commit()
        print("Database cache cleared successfully.")
    except Exception as e:
        print(f"Error clearing cache: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_cache()
