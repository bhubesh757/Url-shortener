# Implementation Notes

## 🔧 Design Decisions
- **In-memory storage** (`url_mapping` dictionary) was used to store the original URL, short code, timestamp, and click count. This keeps the app lightweight and simple for testing purposes.
- Short codes are generated using a **6-character alphanumeric string** to ensure uniqueness and readability.
- The project is modular:
  - `main.py`: API logic and route definitions.
  - `models.py`: In-memory storage structure and logic.
  - `utils.py`: Helper functions like short code generation and validation.

## 🛡️ Error Handling
- Returns `400 Bad Request` if the `url` is missing or malformed in the shorten endpoint.
- Returns `404 Not Found` if the short code doesn't exist for redirection or analytics.
- Handles edge cases like reusing short codes by ensuring randomness and retry.

## 📊 Analytics Endpoint
- `/api/stats/<short_code>` returns:
  - Original URL
  - Click count
  - Creation timestamp
- Clicks are incremented each time the short URL is accessed via redirection.

## 🔍 Testing
- Full test coverage is provided using `pytest`.
- Tests cover:
  - URL shortening
  - Redirection
  - Analytics tracking
- The Flask test client is used to simulate HTTP requests.

## 🔄 Extensibility
- Easy to switch from in-memory to a persistent store (e.g., SQLite, Redis, or MongoDB).
- Short code generation logic can be swapped for a hash-based method (e.g., base62).

## 💡 Future Improvements
- Add expiration support for URLs.
- Add user authentication to track personalized links.
- Rate limiting and spam filtering.

