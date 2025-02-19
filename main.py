from fastapi import FastAPI
from database import init_db, load_csv_to_db

# Create FastAPI instance
app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initial route to check API status
@app.get("/")
def read_root():
    return {"message": "API is running successfully!"}

# Healthcheck endpoint
@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

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
