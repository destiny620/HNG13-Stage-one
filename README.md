# HNG13-Stage-one
String Analyzer

# String Analyzer API

A RESTful API service that analyzes strings and stores their computed properties. The service calculates various properties of input strings including length, palindrome status, unique character count, word count, SHA256 hash, and character frequency.

## Features

- Create and analyze strings
- Retrieve specific string analysis
- Filter strings using various parameters
- Natural language filtering support
- Delete string entries

## API Endpoints

### 1. Create/Analyze String
```http
POST /strings
Content-Type: application/json

{
    "string_value": "example"
}
```

**Success Response (201 Created)**
```json
{
    "string_value": "example",
    "length": 7,
    "is_palindrome": false,
    "unique_characters": 6,
    "word_count": 1,
    "sha256_hash": "2d9785c5...",
    "character_frequency_map": {"e": 2, "x": 1, "a": 1, "m": 1, "p": 1, "l": 1},
    "created_at": "2025-10-21T10:00:00Z"
}
```

**Error Responses:**
- 409 Conflict: String already exists
- 400 Bad Request: Invalid input
- 422 Unprocessable Entity: Validation error

### 2. Get Specific String
```http
GET /strings/{string_value}
```

### 3. Get All Strings with Filtering
```http
GET /strings?is_palindrome=true&min_length=5&max_length=20&word_count=2&contains_character=a
```

**Query Parameters:**
- is_palindrome (boolean)
- min_length (integer)
- max_length (integer)
- word_count (integer)
- contains_character (string)

### 4. Natural Language Filtering
```http
GET /strings/filter-by-natural-language?query=all single word palindromic strings
```

**Example Queries:**
- all single word palindromic strings
- strings longer than 10 characters
- palindromic strings that contain the first vowel
- strings containing the letter z

### 5. Delete String
```http
DELETE /strings/{string_value}
```

**Success Response:**
- 204 No Content

**Error Response:**
- 404 Not Found: String does not exist

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Technologies Used

- Django
- Django REST Framework
- Python 3.x
- SQLite (default database)

## License

MIT License

## Author

[Destiny Omorhienrhien]