from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import models
from database import SQLALCHEMY_DATABASE_URL
import json

print(f"Connecting to: {SQLALCHEMY_DATABASE_URL}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(bind=engine)
db = Session()

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

print("Attempting to insert test record...")
try:
    test_record = models.QuizRecord(
        url="http://test.com",
        title="Test Title",
        summary="Test Summary",
        key_entities={"people": ["Test Person"]},
        sections=["Section 1"],
        related_topics=["Topic 1"]
    )
    db.add(test_record)
    db.commit()
    print("✅ Successfully inserted test record!")
    
    # Clean up
    db.delete(test_record)
    db.commit()
    print("✅ Successfully cleaned up.")
except Exception as e:
    print(f"❌ Failed to insert record.\nError: {e}")
finally:
    db.close()
