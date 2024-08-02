# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_book():
    response = client.post("/books", json={"title": "Sample Book", "author": "John Doe", "genre": "Fiction", "year_published": 2023, "summary": "This is a sample book summary."})
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Book"

def test_read_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Sample Book"

def test_update_book():
    response = client.put("/books/1", json={"title": "Updated Title", "author": "John Doe", "genre": "Non-Fiction", "year_published": 2024, "summary": "Updated summary."})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted"

def test_create_review():
    response = client.post("/books/1/reviews", json={"book_id": 1, "user_id": 1, "review_text": "Great book!", "rating": 4.5})
    assert response.status_code == 200
    assert response.json()["review_text"] == "Great book!"

def test_get_recommendations():
    response = client.get("/recommendations?genre=Fiction")
    assert response.status_code == 200
    assert len(response.json()) > 0
