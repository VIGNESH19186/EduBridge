# API Reference

Base URL (local): `http://localhost:8000`

All authenticated endpoints require an `Authorization: Bearer <token>` header,
obtained from `/api/auth/login` or `/api/auth/register`.

## Auth

### POST /api/auth/register
Register a new user (student, teacher, or admin).

```json
{
  "name": "Aditi Sharma",
  "email": "aditi@example.com",
  "password": "password123",
  "role": "student",
  "preferred_language": "English"
}
```

Returns `{ access_token, token_type, user_id, name, role }`.

### POST /api/auth/login
```json
{ "email": "student@example.com", "password": "password123" }
```

### GET /api/auth/me
Returns the current authenticated user's profile.

---

## Students *(role: student)*

### GET /api/students/me
Returns mastery, accuracy, streak, questions solved, and weak topics.

### GET /api/students/progress
Returns per-topic progress records.

---

## Doubts *(role: student)*

### POST /api/doubts
```json
{
  "question_text": "Why does differentiation of x squared become 2x?",
  "language": "English",
  "explanation_level": "intermediate"
}
```
Runs the full doubt-solving pipeline (classification → RAG retrieval →
grounded generation → citations → translation). Returns the AI explanation,
citations, and a quick-check question. If no relevant source is found,
`grounded: false` and the explanation states this honestly.

### GET /api/doubts/history
Returns the student's past doubts, most recent first.

---

## Practice *(role: student)*

### POST /api/practice/generate
```json
{ "subject": "Mathematics", "topic": "Quadratic Equations", "count": 5 }
```
Selects questions at a difficulty level chosen adaptively from the student's
recent accuracy (see `backend/services/practice_generator.py`).

### POST /api/practice/submit
```json
{ "answers": [{ "question_id": 1, "given_answer": "2, 3" }] }
```
Scores answers, updates `student_progress`, and returns a recommended next
difficulty level.

---

## Recommendations *(role: student)*

### GET /api/recommendations
Returns a personalized learning path (topic, reason, difficulty, estimated
time) built from the student's lowest-mastery progress records.

---

## Analytics *(role: student)*

### GET /api/analytics/student
Returns subject mastery, topic performance, last-7-days activity, and overall
quiz accuracy — all backed by real `attempts`/`student_progress` rows.

---

## Teachers *(role: teacher, admin)*

### GET /api/teachers/dashboard
Total students, class average, count needing attention, topics needing review.

### GET /api/teachers/students
Class roster.

### GET /api/teachers/insights
Students needing attention, each with a risk level (HIGH/MEDIUM/LOW), the
specific measurable evidence behind it, the weakest topic, and a recommended
intervention. Never includes psychological or unsupported personal claims.

---

## Knowledge Base *(role varies)*

### POST /api/knowledge/upload *(teacher, admin)*
Multipart form: `file`, `subject`, `topic`, `title`, `author`, `url`, `license`.
Validates file type (`.pdf`, `.txt`, `.md`) and size (≤10MB).

### POST /api/knowledge/ingest?document_id=... *(teacher, admin)*
Extracts text, chunks it, stores `document_chunks`, and rebuilds the
retrieval index.

### GET /api/knowledge/search?query=... *(any authenticated role)*
Returns top-matching source chunks for a query, with citation metadata.

### GET /api/knowledge/resources *(any authenticated role)*
Returns a count of resources grouped by subject.

---

## Health

### GET /api/health
Returns `{ status, demo_mode, ai_provider }` — useful for confirming whether
the deployment is running with a live AI key or in DEMO MODE.
