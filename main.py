from database import init_db, load_csv_to_db
from query1 import execute_query1
from query2 import execute_query2

from fastapi import FastAPI

app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    return {"message": "API is running successfully!"}

@app.get("/init-db")
def initialize_database():
    try:
        init_db()
        return {"message": "Database initialized successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/load-data")
def load_data():
    try:
        load_csv_to_db()
        return {"message": "Data loaded successfully into the database!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/query1")
def run_query1():
    try:
        result = execute_query1()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/query2")
def run_query2():
    try:
        result = execute_query2()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
