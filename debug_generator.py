
import sys
import os

# Ensure backend directory is in path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.quiz_generator import generate_quiz_from_text

text = """
Elon Reeve Musk (born June 28, 1971) is a businessman and investor known for his key roles in the space company SpaceX and the automotive company Tesla, Inc. Other major enterprises include X Corp., which owns the social media platform X (formerly Twitter); the tunnelling venture The Boring Company; xAI; and Neuralink. He is one of the wealthiest people in the world; as of January 2026, Forbes estimates his net worth to be US$427 billion.[4]

Musk was born in Pretoria to Maye and Errol Musk. He attended the University of Pretoria before immigrating to Canada at age 18, acquiring citizenship through his Canadian-born mother. Two years later, he matriculated at Queen's University at Kingston in Canada. Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University, but dropped out after two days and, with his brother Kimbal, co-founded online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999. That same year, Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In 2002, eBay acquired PayPal for $1.5 billion.
"""

print("Attempting to generate quiz...")
try:
    result = generate_quiz_from_text(text)
    print("Result Keys:", result.keys())
    if "quiz" in result:
        print("First Question:", result["quiz"][0])
    
    # Check if we got mock data
    if result.get("summary", "").startswith("This is a mock summary"):
        print("FAILED: Got mock data.")
    else:
        print("SUCCESS: Got real data.")
except Exception as e:
    print(f"CRASHED: {e}")
