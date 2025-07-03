# Employee Management System

A comprehensive, AI-powered HR management platform built with Python, Streamlit, PostgreSQL/SQLite, and SQLAlchemy. Streamline your workforce management with intelligent automation and intuitive interfaces.

## 🚀 Quick Start


```bash
# Clone and navigate
git clone https://github.com/yourusername/employee-management-system.git
cd employee-management-system

# Option 1: Docker (Recommended)
docker-compose up --build

# Option 2: Local Setup
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run pages/app.py
```

**Access the application:** http://localhost:8501

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [AI Features Setup](#-ai-features-setup)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)


## ✨ Features

### Core HR Management
- **Employee Master Data** - Complete employee profiles with personal and professional details
- **Project Management** - Track projects, assignments, and deliverables
- **Time Tracking** - Comprehensive timesheet and attendance management
- **Resource Allocation** - Optimize employee-project assignments

### Advanced Capabilities
- **AI-Powered Analytics** - Intelligent task summaries and insights
- **Custom Query Assistant** - Natural language to SQL conversion
- **File Upload & ETL** - Bulk data import with validation
- **Real-time Reporting** - Dynamic dashboards and analytics
- **Audit Trail** - Complete change logging and error tracking

### Technical Features
- **Modular Architecture** - Clean, extensible codebase
- **Multi-Database Support** - PostgreSQL for production, SQLite for development
- **Responsive UI** - Modern Streamlit interface
- **Docker Ready** - Containerized deployment

## 🛠 Prerequisites

- **Python 3.8+** (for local setup)
- **Docker & Docker Compose** (for containerized setup)
- **PostgreSQL** (optional - SQLite included for testing)
- **Internet Connection** (for AI features)

## 📦 Installation

### Option 1: Docker Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/employee-management-system.git
   cd employee-management-system
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - **Web Interface:** http://localhost:8501
   - **Database:** PostgreSQL on port 5432 (if using PostgreSQL)

### Option 2: Local Development Setup

1. **Clone and setup environment:**
   ```bash
   git clone https://github.com/yourusername/employee-management-system.git
   cd employee-management-system
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and API keys
   ```

4. **Initialize database:**
   ```bash
   python core/tables.py
   python core/data_seeder.py  # Optional: Add sample data
   ```

5. **Run the application:**
   ```bash
   streamlit run pages/app.py
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=sqlite:///employee_management.db
# For PostgreSQL: postgresql://username:password@localhost:5432/employee_db

# AI Features (Optional)
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### Database Setup

**SQLite (Default):**
- No additional setup required
- Database file created automatically

**PostgreSQL:**
```bash
# Create database
createdb employee_management

# Update DATABASE_URL in .env
DATABASE_URL=postgresql://username:password@localhost:5432/employee_management
```

## 🤖 AI Features Setup

### Gemini API Configuration

1. **Get API Key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with Google account
   - Click "Create API key"
   - Copy the generated key

2. **Configure the application:**
   ```bash
   # Add to .env file
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Enable Generative Language API:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable "Generative Language API"

4. **Test AI features:**
   - Navigate to "🤖 AI Query Assistant"
   - Try: "Show me all employees hired this year"
   - The AI will generate and execute SQL queries

### AI Features Available

- **Smart Query Assistant** - Natural language to SQL
- **Task Summaries** - AI-generated project insights


## 📁 Project Structure

```
employee_management/
├── __init__.py
├── .env
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose
├── docker-compose.yml
├── main.py
├── requirements.txt
├── sample_queries.md
├── README.md
│
├── auth/
│   └── auth.py
│
├── config/
│   └── config.py
│
├── core/
│   ├── data_seeder.py
│   ├── database.py
│   ├── etl.py
│   ├── models.py
│   └── tables.py
│
├── pages/
│   ├── allocations.py
│   ├── app.py
│   ├── custom_queries.py
│   ├── employee_master.py
│   ├── file_upload.py
│   ├── query_assistant.py
│   ├── report.py
│   ├── summary_reports.py
│   └── tasks_summariser.py
│
├── logs/
│   ├── activity_log_view.py
│   ├── activity_logger.py
│   ├── app.log
│   └── (many db_creation_*.log files)
│
├── csv_files/
│   ├── attendance_report_daily.csv
│   ├── employee_exit_report.csv
│   ├── employee_master.csv
│   ├── employee_work_profile.csv
│   ├── experience_report.csv
│   ├── project_allocations.csv
│   ├── resource_utilization.csv
│   └── timesheet_report_clean.csv
│
├── data/
│   └── (data files, if any)
│
├── uploads/
│   └── (uploaded files, if any)
│
├── init_db/
│   └── (database initialization scripts)
│
└── __pycache__/
    └── (Python cache files)
```

## 🔧 Troubleshooting

### Common Issues

**Application won't start:**
```bash
# Check if port 8501 is available
netstat -an | grep 8501

# Kill existing Streamlit processes
pkill -f streamlit

# Restart with different port
streamlit run pages/app.py --server.port 8502
```

**Database connection errors:**
```bash
# For SQLite - check file permissions
ls -la *.db

# For PostgreSQL - test connection
psql -h localhost -U username -d employee_management
```

**AI features not working:**
- Verify GEMINI_API_KEY is set correctly
- Check internet connection
- Ensure Generative Language API is enabled
- Try regenerating API key

**Docker issues:**
```bash
# Clean rebuild
docker-compose down
docker system prune -f
docker-compose up --build
```




## Acknowledgements

- **[Streamlit](https://streamlit.io/)** - Web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Database ORM
- **[PostgreSQL](https://www.postgresql.org/)** - Database engine
- **[Google Gemini](https://ai.google.dev/)** - AI capabilities
- **[Docker](https://www.docker.com/)** - Containerization



