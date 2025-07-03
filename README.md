# Employee Management System

A modular, extensible HR management system built with Python, Streamlit, PostgreSQL/SQLite, and SQLAlchemy. This project provides a comprehensive platform for managing employees, projects, timesheets, attendance, allocations, and more, with support for AI-powered summaries and custom queries.

## Features

- Employee master data management
- Project and allocation tracking
- Timesheet and attendance management
- AI-powered task summaries
- Custom SQL query assistant
- File upload and ETL pipeline
- Data validation and error logging
- Modular Streamlit UI
- PostgreSQL and SQLite support

## Folder Structure

```
employee_management/
│
├── core/           # Core backend logic (database, models, ETL, etc.)
├── pages/          # Streamlit UI pages and components
├── auth/           # Authentication logic
├── config/         # Configuration files
├── logs/           # Logging utilities and log files
├── csv_files/      # Sample and uploaded CSVs
├── data/           # Data files
├── uploads/        # User uploads
├── init_db/        # Database initialization scripts
├── main.py         # Main entry point
├── requirements.txt# Python dependencies
├── .env            # Environment variables
└── ...             # Other supporting files
```

## Getting Started

### Prerequisites
- Python 3.8+
- pip
- (Optional) Docker
- PostgreSQL (or use SQLite for local testing)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd employee_management
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and update values as needed (database credentials, API keys, etc.)

5. **Set up the database:**
   - Edit `config/config.py` for your database settings.
   - Run the table creation script:
     ```bash
     python core/tables.py
     ```

6. **(Optional) Seed initial data:**
   ```bash
   python core/data_seeder.py
   ```

### Running the Application

- **Streamlit UI:**
  ```bash
  streamlit run pages/app.py
  ```
- **Main entry (if using FastAPI or other backend):**
  ```bash
  python main.py
  ```

### Using Docker

1. Build and run the container:
   ```bash
   docker-compose up --build
   ```

## Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements
- Streamlit
- SQLAlchemy
- PostgreSQL
- OpenAI/Google Gemini (for AI features)

---
For questions or support, open an issue or contact the maintainer.
