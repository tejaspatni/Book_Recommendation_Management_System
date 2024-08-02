# model_training.py
import pandas as pd
import os
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle

# Database connection
DATABASE_URL = "postgresql+psycopg2://postgres:2108@localhost:5432/books_db"
engine = create_engine(DATABASE_URL)

# Load data from PostgreSQL
books_df = pd.read_sql_table('books', engine)
reviews_df = pd.read_sql_table('reviews', engine)

# Debug: Print shapes of the DataFrames
print(f"Books DataFrame shape: {books_df.shape}")
print(f"Reviews DataFrame shape: {reviews_df.shape}")

# Prepare data for training
data = pd.merge(reviews_df, books_df, left_on='book_id', right_on='id')
data = data[['genre', 'rating', 'year_published']]  # Add other relevant features if needed
data = data.dropna()
unique_genre = data['genre'].unique()
# Debug: Print shape after merge and dropna
print(f"Merged DataFrame shape: {data.shape}")

# Encode categorical variables
data['genre'] = data['genre'].astype('category').cat.codes

# Split data into features and target
X = data[['genre', 'year_published']]  # Include other features if necessary
y = data['rating']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Create 'models' directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save the trained model
with open('models/book_recommendation_model.pkl', 'wb') as f:
    pickle.dump(model, f)
