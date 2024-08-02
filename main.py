from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.sql import func
from pydantic import BaseModel
from models import Base, Book, Review  # Ensure this import is correct
from api import generate_summary
import uvicorn
import pickle
import os
import logging
from model_training import unique_genre

DATABASE_URL = "postgresql+asyncpg://postgres:2108@localhost:5432/books_db"
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

app = FastAPI()

# Load the trained model
model_path = os.path.join('models', 'book_recommendation_model.pkl')
with open(model_path, 'rb') as f:
    recommendation_model = pickle.load(f)

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: str

class ReviewCreate(BaseModel):
    user_id: int
    review_text: str
    rating: float

async def get_db():
    async with SessionLocal() as session:
        yield session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/books")
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Attempting to create book: {book}")
    new_book = Book(**book.dict())
    logger.info(f"Created book object: {new_book}")
    db.add(new_book)
    logger.info("Added book to session")
    try:
        await db.commit()
        logger.info("Committed session")
    except Exception as e:
        logger.error(f"Error committing session: {e}")
        await db.rollback()
        raise
    await db.refresh(new_book)
    logger.info(f"Refreshed book object: {new_book}")
    return new_book

@app.get("/books")
async def read_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).offset(skip).limit(limit))
    books = result.scalars().all()
    return books

@app.get("/books/{id}")
async def read_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{id}")
async def update_book(id: int, book: BookCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == id))
    existing_book = result.scalar_one_or_none()
    if existing_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(existing_book, key, value)
    await db.commit()
    await db.refresh(existing_book)
    return existing_book

@app.delete("/books/{id}")
async def delete_book(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(book)
    await db.commit()
    return {"message": "Book deleted"}

@app.post("/books/{id}/reviews")
async def create_review(id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    # Create the new review, ensure no duplication of book_id
    review_data = review.dict()
    new_review = Review(**review_data, book_id=id)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@app.get("/books/{id}/reviews")
async def read_reviews(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).where(Review.book_id == id))
    reviews = result.scalars().all()
    return reviews

@app.post("/generate-summary")
async def generate_book_summary(content: str):
    summary = generate_summary(content)
    return {"summary": summary}

@app.get("/books/{id}/summary")
async def get_book_summary(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    summary = generate_summary(book.summary)
    return {"summary": summary}

@app.get("/recommendations")
async def get_recommendations(genre: str, db: AsyncSession = Depends(get_db)):
    # Convert genre to the encoded value
    if genre not in unique_genre:
        raise HTTPException(status_code=400, detail="Genre not found in training data")

    genre_code = list(unique_genre).index(genre)

    # Fetch books with the given genre
    result = await db.execute(
        select(Book, func.avg(Review.rating).label('avg_rating'))
        .join(Review, Book.id == Review.book_id)
        .where(Book.genre == genre)
        .group_by(Book.id)
    )
    books = result.all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found for the given genre")

    # Prepare data for the recommendation model
    X = [[genre_code, book.Book.year_published] for book in books]  # Use the encoded genre code
    
    # Get predictions
    predictions = recommendation_model.predict(X)

    # Sort books by predicted ratings
    recommended_books = sorted(zip(books, predictions), key=lambda x: x[1], reverse=True)

    return [
        {
            "id": book.Book.id,
            "title": book.Book.title,
            "author": book.Book.author,
            "predicted_rating": float(pred)
        }
        for book, pred in recommended_books[:5]  # Return top 5 recommendations
    ]

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
    uvicorn.run(app, host="0.0.0.0", port=8000)
