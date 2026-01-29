# AutoRia Scraper & Automation Tool

## Technology Stack
* **Python 3**: Using `asyncio` and `aiohttp` for high-performance scraping.
* **Playwright**: Emulating user interactions (Stealth mode) to bypass protection and retrieve phone numbers.
* **Selectolax**: High-speed HTML data extraction using CSS selectors.
* **Postgres 16**: Reliable data persistence using the `asyncpg` driver and SQLAlchemy 2.0.
* **Alembic**: Database migration system for schema version control.
* **APScheduler**: Task scheduling for automating periodic scraping and backup jobs.
* **Docker & Docker Compose**: Full containerization for seamless deployment.

## Project Structure
```text
autoria-scraper-task/
├── dumps/                  # SQL backup files (.sql)
├── migrations/             # Alembic migration versions
├── src/
│   ├── database/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py     # Base declarative class
│   │   │   └── car.py      # SQLAlchemy car model
│   │   ├── repositories/
│   │   │   └── car_repository.py
│   │   ├── __init__.py
│   │   └── engine.py       # Async engine & session helper
│   ├── scraper/
│   │   ├── client.py       # Async HTTP client
│   │   ├── crawler.py      # Pagination & orchestration
│   │   ├── parser.py       # HTML extraction logic
│   │   └── phone.py        # Playwright service for numbers
│   ├── services/
│   │   ├── backup_manager.py
│   │   └── scheduler.py    # APScheduler configuration
│   ├── utils/
│   │   └── parsing.py      # Data cleaning utilities
│   ├── config.py           # Env variables & settings
│   └── main.py             # App entry point
├── .env                    # Environment variables
├── .env.example            # Template for environment variables
├── .gitignore
├── alembic.ini             # Alembic configuration
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── start.sh                # Startup & migration script
```

## 📦 Getting Started

### 1. Environment Configuration
To run the project, you simply need to define the variables listed in the **`.env.example`** file. Create a new **`.env`** file in the root directory and fill in your values

### 2. Run with Docker Compose
```
docker-compose up --build
```
