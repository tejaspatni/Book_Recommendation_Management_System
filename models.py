# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    year_published = Column(Integer)
    summary = Column(String)

    reviews = relationship('Review', back_populates='book')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer)
    review_text = Column(String)
    rating = Column(Float)

    book = relationship('Book', back_populates='reviews')
