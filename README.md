# Workflow Status

[![Workflow Status](https://github.com/lussvontrier/kittygram_final/actions/workflows/main.yml/badge.svg)](https://github.com/lussvontrier/kittygram_final/actions)

# About

A website for food lovers to register, view, add recipes, favorite other users' recipes, add to shopping cart, download the ingredient list from shopping cart and follow each other.

# Techstack

- Python (backend language)
- Django (backend framework)
- Postgres (db)
- Gunicorn (intermediate HTTP server)
- Nginx (web server for reverse proxy)
- Docker (containerization)
- GitHub Actions (CI/CD)

# Installation

To run this project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/lussvontrier/kittygram_final.git
    ```
2. Navigate to the project directory:

    ```bash
    cd kittygram_final/backend
    ```
3. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    On macOS and Linux:
    ```bash
    source venv/bin/activate
    ```

    On Windows (PowerShell):
    ```bash
    .\venv\Scripts\Activate
    ```

5. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

6. Create an .env file in the project root directory and fill it according to .env.example

7. Apply database migrations:

    ```bash
    python manage.py migrate
    ```

8. Create a superuser for administrative access:

    ```bash
    python manage.py createsuperuser
    ```

9. Start the development server & access the application in your web browser at http://localhost:8000:

    ```bash
    python manage.py runserver
    ```
# API Request/Response Examples

1. Create a New Recipe:
## Request:
```http
POST /api/recipes/
Content-Type: application/json

{
    "ingredients": [
        {
            "id": 1123,
            "amount": 10
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
## Response:
```json
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 0,
    "tags": [
        {
            "id": 0,
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
        }
    ],
    "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
    },
    "ingredients": [
        {
            "id": 0,
            "name": "Картофель отварной",
            "measurement_unit": "г",
            "amount": 1
        }
    ],
    "is_favorited": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1
}
```

# Author 
@lussvontrier




