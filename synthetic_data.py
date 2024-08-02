# generate_synthetic_data.py
from faker import Faker
import pandas as pd
import random

# Initialize Faker
fake = Faker()

# Function to generate synthetic books data
def generate_books(num_books):
    books = []
    for _ in range(num_books):
        books.append({
            'id': _ + 1,
            'title': fake.catch_phrase(),
            'author': fake.name(),
            'genre': random.choice(['Fiction', 'Non-Fiction', 'Fantasy', 'Biography', 'Science']),
            'year_published': random.randint(1900, 2024),
            'summary': fake.text(max_nb_chars=200)
        })
    return pd.DataFrame(books)

# Function to generate synthetic reviews data
def generate_reviews(num_reviews, num_books):
    reviews = []
    for _ in range(num_reviews):
        reviews.append({
            'id': _ + 1,
            'book_id': random.randint(1, num_books),
            'user_id': random.randint(1, 100),  # Assume 100 users for example
            'review_text': fake.text(max_nb_chars=300),
            'rating': round(random.uniform(1, 5), 1)
        })
    return pd.DataFrame(reviews)

# Generate data
books_df = generate_books(10)
reviews_df = generate_reviews(50, 10)

# Save to CSV
books_df.to_csv('synthetic_books.csv', index=False)
reviews_df.to_csv('synthetic_reviews.csv', index=False)

print("Synthetic data has been generated and saved.")
