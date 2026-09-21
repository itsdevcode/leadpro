# Minimalist Lead Management & CRM Backend API

A minimalist, robust CRM and Lead Management REST API built with FastAPI. Features OTP authentication, complete lead lifecycle management, notes, reminders, follow-ups, and dashboard analytics.

## 🚀 Key Features

* **Authentication**: Passwordless login using Email OTP and JWT session tokens.
* **Dashboard**: Key metrics, statistics, and upcoming follow-ups breakdown.
* **Lead Management**: Complete CRUD operations, status transitions, and advanced filters.
* **Notes**: Chronological notes for leads (Add, Edit, Update, Delete).
* **Reminders**: Scheduled follow-up reminders with filter support.
* **User Profile**: User details view and profile update endpoints.
* **Support & Info**: Contact/feedback message submissions, privacy policy, and about metadata.

---

## 🛠 Tech Stack

* **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
* **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
* **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
* **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
* **Server**: [Uvicorn](https://www.uvicorn.org/)

---

## 📁 Project Structure

```text
lead-crm-api/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py          # OTP login & verification
│   │   │   ├── dashboard.py     # Stats & follow-ups
│   │   │   ├── leads.py         # Lead lifecycle & filters
│   │   │   ├── notes.py         # Note CRUD
│   │   │   ├── reminders.py     # Reminders & follow-ups
│   │   │   ├── users.py         # Profile management
│   │   │   └── support.py       # Support & static info
│   │   └── deps.py              # Auth & DB dependencies
│   ├── core/                    # Config, security & DB setup
│   ├── models/                  # SQLAlchemy ORM models
│   ├── schemas/                 # Pydantic schemas (Request/Response)
│   ├── services/                # Email (OTP) & business logic
│   └── main.py                  # App entrypoint
├── alembic/                     # Database migrations
├── .env.example
├── requirements.txt
└── README.md
