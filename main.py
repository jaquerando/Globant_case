from fastapi import FastAPI
from app import query1, query2
from app.database import init_db, load_csv_to_db

# Create FastAPI instance with metadata
app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc UI
)

# Health Check Route
@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}

# Initial Route to check API status
@app.get("/")
def read_root():
    return {"message": "API is running successfully!"}

# Initialize database tables
@app.get("/init-db")
def initialize_database():
    try:
        init_db()
        return {"message": "Database initialized successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Load data from CSV into database
@app.get("/load-data")
def load_data():
    try:
        load_csv_to_db()
        return {"message": "Data loaded successfully into the database!"}
    except Exception as e:
        return {"error": str(e)}

# Query 1: Hired Employees by Quarter
@app.get("/hired-employees-by-quarter")
def hired_employees_by_quarter():
    try:
        result = query1.get_hired_employees_by_quarter()
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}

# Query 2: Departments Above Average Hires
@app.get("/departments-above-average")
def departments_above_average():
    try:
        result = query2.get_departments_above_average()
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
