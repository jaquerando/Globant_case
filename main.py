from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import init_db, load_csv_to_db
from query1 import execute_query1
from query2 import execute_query2
import sqlite3

# Create FastAPI instance
app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Health Check
@app.get("/healthcheck", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Initialize Database
@app.get("/init-db", tags=["Database"])
def initialize_database():
    try:
        init_db()
        return {"message": "Database initialized successfully!"}
    except Exception as e:
        return {"error": str(e)}

# Load CSV Data into Database
@app.get("/load-data", tags=["Database"])
def load_data():
    try:
        load_csv_to_db()
        return {"message": "Data loaded successfully into the database!"}
    except Exception as e:
        return {"error": str(e)}

# View All Departments (HTML Table)
@app.get("/departments", tags=["Tables"], response_class=HTMLResponse)
def get_departments():
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments")
        rows = cursor.fetchall()
        conn.close()

        # Generate HTML Table
        html_content = "<h2>Departments Table</h2><table border='1'><tr><th>ID</th><th>Department Name</th></tr>"
        for row in rows:
            html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
        html_content += "</table>"
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")

# View All Jobs (HTML Table)
@app.get("/jobs", tags=["Tables"], response_class=HTMLResponse)
def get_jobs():
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs")
        rows = cursor.fetchall()
        conn.close()

        html_content = "<h2>Jobs Table</h2><table border='1'><tr><th>ID</th><th>Job Title</th></tr>"
        for row in rows:
            html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
        html_content += "</table>"
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")

# View All Hired Employees (HTML Table)
@app.get("/hired-employees", tags=["Tables"], response_class=HTMLResponse)
def get_hired_employees():
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hired_employees")
        rows = cursor.fetchall()
        conn.close()

        html_content = "<h2>Hired Employees Table</h2><table border='1'><tr><th>ID</th><th>Name</th><th>DateTime</th><th>Department ID</th><th>Job ID</th></tr>"
        for row in rows:
            html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
        html_content += "</table>"
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")


#  Filter Departments by ID
@app.get("/departments/{department_id}", tags=["Filters"], response_class=HTMLResponse)
def get_department_by_id(department_id: int):
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM departments WHERE id = ?", (department_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            html_content = f"<h2>Department ID: {row[0]}</h2><p>Name: {row[1]}</p>"
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(content="<h3>No department found with that ID.</h3>")
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")

# Filter Hired Employees by Year
@app.get("/hired-employees/year/{year}", tags=["Filters"], response_class=HTMLResponse)
def get_employees_by_year(year: str):
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hired_employees WHERE strftime('%Y', datetime) = ?", (year,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            html_content = f"<h2>Hired Employees in {year}</h2><table border='1'><tr><th>ID</th><th>Name</th><th>DateTime</th><th>Department ID</th><th>Job ID</th></tr>"
            for row in rows:
                html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
            html_content += "</table>"
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(content=f"<h3>No employees hired in {year}.</h3>")
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")

# Filter Hired Employees by Department
@app.get("/hired-employees/department/{department_id}", tags=["Filters"], response_class=HTMLResponse)
def get_employees_by_department(department_id: int):
    try:
        conn = sqlite3.connect("data_challenge.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hired_employees WHERE department_id = ?", (department_id,))
        rows = cursor.fetchall()
        conn.close()

        if rows:
            html_content = f"<h2>Employees in Department {department_id}</h2><table border='1'><tr><th>ID</th><th>Name</th><th>DateTime</th><th>Department ID</th><th>Job ID</th></tr>"
            for row in rows:
                html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
            html_content += "</table>"
            return HTMLResponse(content=html_content)
        else:
            return HTMLResponse(content=f"<h3>No employees found in department {department_id}.</h3>")
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error: {str(e)}</h3>")



# Run Query 1
@app.get("/query1", tags=["Queries"])
def run_query1():
    try:
        result = execute_query1()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

# Run Query 2
@app.get("/query2", tags=["Queries"])
def run_query2():
    try:
        result = execute_query2()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
