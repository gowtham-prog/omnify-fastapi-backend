# 🧪 Event Management System

A **Full Stack Event Management** application built with **FastAPI**, **PostgreSQL**, and **Next.js (Shadcn UI)**.
This system allows users to create events, register attendees, and view attendee lists while maintaining **data integrity**, **scalability**, and **clean architecture**.

---

## ⚙️ Tech Stack

**Backend:** FastAPI, SQLAlchemy (Async ORM), Alembic, PostgreSQL\
**Frontend:** Next.js (App Router) + Shadcn UI\
**Testing:** Pytest + HTTPX\
**Documentation:** Swagger / OpenAPI (auto-generated via FastAPI)

---


## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/event-management-system.git
cd event-management-system
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/events
```

> 💡 You can switch to SQLite for quick testing:
>
> ```
> DATABASE_URL=sqlite+aiosqlite:///./events.db
> ```

### 5️⃣ Run Database Migrations

```bash
alembic upgrade head
```

### 6️⃣ (Optional) Seed Sample Data

```bash
python -m app.seed
```

---

## 🧭 Running the Application

### FastAPI Backend

```bash
uvicorn app.main:app --reload
```

API available at:
👉 `http://127.0.0.1:8000`

Swagger docs:
👉 `http://127.0.0.1:8000/docs`
ReDoc docs:
👉 `http://127.0.0.1:8000/redoc`

---

## 🧩 API Endpoints

### 1️⃣ Create a New Event

**POST** `/events`

```bash
curl -X POST "http://127.0.0.1:8000/events" \
-H "Content-Type: application/json" \
-d '{
  "name": "AI Conference 2025",
  "location": "Bangalore",
  "start_time": "2025-11-10T09:00:00Z",
  "end_time": "2025-11-10T17:00:00Z",
  "max_capacity": 100
}'
```

### 2️⃣ List All Upcoming Events

**GET** `/events`

```bash
curl http://127.0.0.1:8000/events
```

### 3️⃣ Register an Attendee

**POST** `/events/{event_id}/register`

```bash
curl -X POST "http://127.0.0.1:8000/events/1/register" \
-H "Content-Type: application/json" \
-d '{
  "name": "Alice",
  "email": "alice@example.com"
}'
```

Prevents:

* Overbooking (max capacity limit)
* Duplicate email registration per event

### 4️⃣ List Attendees for an Event

**GET** `/events/{event_id}/attendees`

```bash
curl http://127.0.0.1:8000/events/1/attendees
```

### 5️⃣ (Bonus) Pagination Example

**GET** `/events/1/attendees?page=2&limit=10`

---

## 🧱 Database Schema

**Table: events**

| Column       | Type     | Description             |
| ------------ | -------- | ----------------------- |
| id           | Integer  | Primary key             |
| name         | String   | Event name              |
| location     | String   | Event location          |
| start_time   | DateTime | Start time (UTC)        |
| end_time     | DateTime | End time (UTC)          |
| max_capacity | Integer  | Max number of attendees |
| created_at   | DateTime | Record creation time    |

**Table: attendees**

| Column        | Type       | Description            |
| ------------- | ---------- | ---------------------- |
| id            | Integer    | Primary key            |
| name          | String     | Attendee name          |
| email         | String     | Unique per event       |
| event_id      | ForeignKey | Linked to events.id    |
| registered_at | DateTime   | Registration timestamp |

---

## 🧪 Running Tests

```bash
PYTHONPATH=$(pwd) pytest tests/ --disable-warnings -v
```

Example test file (`tests/test_events.py`):

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_events():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/events")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
```

---

## 📜 Assumptions

* Timezone stored in **UTC**; conversions handled client-side.
* No authentication layer (focus is on event management core).
* Async SQLAlchemy ORM used for optimal performance.
* PostgreSQL recommended; SQLite supported for testing.

---

## 🧰 Tools & Libraries Used

| Category      | Library                 |
| ------------- | ----------------------- |
| Web Framework | FastAPI                 |
| ORM           | SQLAlchemy (async)      |
| Migrations    | Alembic                 |
| Database      | PostgreSQL              |
| Testing       | Pytest, HTTPX           |
| Documentation | FastAPI Swagger / ReDoc |
| Frontend      | Next.js + Shadcn UI     |

---

## 📦 Migrations / Schema

To generate a new migration:

```bash
alembic revision --autogenerate -m "description"
```

To apply migrations:

```bash
alembic upgrade head
```

---

## 🎥 Loom Demo

A Loom walkthrough video should show:

* Server setup
* Event creation & listing
* Attendee registration
* Pagination + error handling
* Swagger docs demo

---

## 💬 Contact

**Author:** Your Name
**Email:** [yourname@example.com](mailto:yourname@example.com)
**GitHub:** [github.com/your-username](https://github.com/your-username)
