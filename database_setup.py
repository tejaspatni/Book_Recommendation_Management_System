# database_setup.py
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Float

# Connect to PostgreSQL
engine = create_engine('postgresql://postgres:2108@localhost/books_db')
metadata = MetaData()

# Define books table
books = Table('books', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String),
              Column('author', String),
              Column('genre', String),
              Column('year_published', Integer),
              Column('summary', String))

# Define reviews table
reviews = Table('reviews', metadata,
                Column('id', Integer, primary_key=True),
                Column('book_id', Integer, ForeignKey('books.id')),
                Column('user_id', Integer),
                Column('review_text', String),
                Column('rating', Float))

# Create tables
metadata.create_all(engine)
print("Database setup complete.")
