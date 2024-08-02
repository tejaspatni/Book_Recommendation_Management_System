# Book_Recommendation_Management_System

This project implements an intelligent book management system using Python, a locally running Llama3 generative AI model, and a PostgreSQL database. The system allows users to manage books, reviews, and provides book recommendations based on user preferences.

## Features

- Add, retrieve, update, and delete books from a PostgreSQL database
- Generate summaries for books using a locally running Llama3 model
- Manage user reviews for books
- Generate rating and review summaries for books
- Provide book recommendations based on user preferences
- RESTful API for accessing all functionalities

## Technologies Used

- Python
- PostgreSQL
- Llama3 generative AI model
- FastAPI/Flask (for RESTful API)
- SQLAlchemy (for database interactions)
- Scikit-learn (for recommendation model)

## Setup and Installation

1. Clone the repository
2. Set up a virtual environment
3. Install dependencies
4. Set up PostgreSQL database and update the connection string
5. Set up Llama3 model locally (follow Llama3 documentation for installation)
6. Run database migrations
7. Train the model
8. Start the application

## API Endpoints

- POST /books: Add a new book
- GET /books: Retrieve all books
- GET /books/<id>: Retrieve a specific book by its ID
- PUT /books/<id>: Update a book's information
- DELETE /books/<id>: Delete a book
- POST /books/<id>/reviews: Add a review for a book
- GET /books/<id>/reviews: Retrieve all reviews for a book
- GET /books/<id>/summary: Get a summary and aggregated rating for a book
- GET /recommendations: Get book recommendations
- POST /generate-summary: Generate a summary for given book content

## Future Improvements

- AWS deployment
- Implement caching for book recommendations
- Add authentication and security measures
- Set up CI/CD pipeline
