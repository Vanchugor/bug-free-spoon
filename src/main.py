import sqlite3
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

DB_PATH = "reviews.db"


# schemas.py
class ReviewIn(BaseModel):
    text: str


class ReviewOut(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str


# utils.py, but actually could be part of a special ML service functionality
def analyze_sentiment(text: str) -> str:
    text = text.lower()
    if any(word in text for word in ["плохо", "ненавиж", "ужас", "отстой"]):
        return "negative"
    elif any(word in text for word in ["хорош", "люблю", "нравит", "класс"]):
        return "positive"
    else:
        return "neutral"


# Could be in lifespan
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        conn.commit()


init_db()


@app.post("/reviews", response_model=ReviewOut)
def create_review(review: ReviewIn):
    sentiment = analyze_sentiment(review.text)
    created_at = datetime.now().isoformat()

    # In real project must be moved to the repository class
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
            (review.text, sentiment, created_at),
        )
        conn.commit()
        review_id = cursor.lastrowid

    return ReviewOut(
        id=review_id, text=review.text, sentiment=sentiment, created_at=created_at
    )


@app.get("/reviews", response_model=List[ReviewOut])
def get_reviews(sentiment: Optional[str] = Query(None)):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if sentiment:
            cursor.execute("SELECT * FROM reviews WHERE sentiment = ?", (sentiment,))
        else:
            cursor.execute("SELECT * FROM reviews")

        rows = cursor.fetchall()

    return [
        ReviewOut(id=row[0], text=row[1], sentiment=row[2], created_at=row[3])
        for row in rows
    ]
