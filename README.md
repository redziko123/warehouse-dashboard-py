# Warehouse Dashboard

Internal web dashboard for warehouse staff. Runs on Flask + PostgreSQL.

Built for daily use at the warehouse shows truck loading stats, news, safety warnings, training materials and upcoming birthdays. Admins manage all content through a built-in panel.

---

## Stack

- Python 3.11 / Flask 3.0
- PostgreSQL 14+
- SQLAlchemy (ORM) + Flask-Migrate
- Gunicorn (production server)
- Bootstrap 5 (frontend)

---

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <repo-url>
cd "whs dashboard python/warehouse_python"
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac
pip install -r requirements.txt
```

**2. Configure environment variables**

Copy `.env.example` to `.env` and fill in the values:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=warehouse_db
DB_USER=postgres
DB_PASSWORD=your_password
SECRET_KEY=   # generate: python -c "import secrets; print(secrets.token_hex(32))"
HTTPS=false   # set to true behind SSL proxy
TRUCK_API_URL=  # optional, leave empty if not available yet
```

**3. Create the database**

```bash
psql -U postgres -c "CREATE DATABASE warehouse_db;"
python app.py   # creates all tables on first run and exits
```

**4. Create the first admin account**

On first run, go to `http://localhost:5000/register` - this page is only available when no users exist yet and automatically creates an admin account.

---

## Running

**Development**

```bash
python app.py
```

App starts on `http://0.0.0.0:5000`.

**Production (Gunicorn)**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Should be placed behind Nginx or another reverse proxy that handles SSL. When running with HTTPS, set `HTTPS=true` in `.env` to enable the Secure cookie flag.

---

## Project structure

```
warehouse_python/
├── app.py              # app factory + entry point
├── config.py           # all config, reads from .env
├── models/             # SQLAlchemy models
├── routes/             # blueprints: auth, main, admin, api
├── utils/helpers.py    # shared decorators and file upload helpers
├── templates/          # Jinja2 HTML templates
└── static/             # CSS, JS, uploaded images
```

---

## Notes

- Uploaded images go to `static/uploads/` - this folder is not in the repo, make sure it exists on the server and is backed up separately.
- The `TRUCK_API_URL` variable is optional. If not set, the navbar shows `--` instead of live truck counts. The endpoint at `/api/truck-stats` acts as a proxy so the browser never calls the source API directly.
- Weekly stats can be entered manually via the admin panel or synced from an API when one is available. (to do)


