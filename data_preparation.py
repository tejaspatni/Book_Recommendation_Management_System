import pandas as pd
from sqlalchemy import create_engine, MetaData, Table

# Load data from CSV
books_df = pd.read_csv('synthetic_books.csv')
reviews_df = pd.read_csv('synthetic_reviews.csv')

# Connect to PostgreSQL
engine = create_engine('postgresql+psycopg2://postgres:2108@localhost:5432/books_db')

# Define metadata
metadata = MetaData()

# Reflect the existing tables
metadata.reflect(bind=engine)

# Drop the reviews table if it exists
if 'reviews' in metadata.tables:
    reviews = Table('reviews', metadata, autoload_with=engine)
    reviews.drop(engine)

# Drop the books table if it exists
if 'books' in metadata.tables:
    books = Table('books', metadata, autoload_with=engine)
    books.drop(engine)

# Insert new data
books_df.to_sql('books', engine, if_exists='replace', index=False)
reviews_df.to_sql('reviews', engine, if_exists='replace', index=False)

print("Data has been loaded into the database.")
