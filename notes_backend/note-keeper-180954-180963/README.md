# note-keeper-180954-180963

Backend: Flask Notes API (notes_backend)

- Runs on port 3001
- OpenAPI docs available at /docs
- CORS enabled for future frontend integration

How to run locally
1. Change directory to the backend:
   cd notes_backend
2. Install dependencies (Python 3.10+ recommended):
   pip install -r requirements.txt
3. Start the server:
   python run.py
   The API will be available at http://localhost:3001 and docs at http://localhost:3001/docs

Health endpoint
- GET /health -> {"status":"ok"}

Notes endpoints
- POST /notes
  Request:
  {
    "title": "Shopping list",
    "content": "Eggs, Milk, Bread"
  }
  Responses:
  - 201 Created: note object
  - 400 Bad Request: validation error

- GET /notes
  Responses:
  - 200 OK: [note, ...]

- GET /notes/<id>
  Responses:
  - 200 OK: note object
  - 404 Not Found

- PUT /notes/<id>
  Request (any of):
  {
    "title": "Updated title"
  }
  or
  {
    "content": "Updated content"
  }
  Responses:
  - 200 OK: updated note object
  - 400 Bad Request: if no fields provided
  - 404 Not Found

- DELETE /notes/<id>
  Responses:
  - 204 No Content
  - 404 Not Found

Example curl requests
Create:
curl -s -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First","content":"Hello"}'

List:
curl -s http://localhost:3001/notes

Get one:
curl -s http://localhost:3001/notes/<id>

Update:
curl -s -X PUT http://localhost:3001/notes/<id> \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated"}'

Delete:
curl -i -X DELETE http://localhost:3001/notes/<id>

OpenAPI docs
When running, navigate to:
http://localhost:3001/docs

Environment variables
See notes_backend/.env.example for configuration placeholders to support future database integration.
