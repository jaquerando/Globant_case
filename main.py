from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
import sqlite3

app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# API Status
@app.get("/status", tags=["API Status"])
def get_status():
    return {"status": "API is running successfully!"}

# Departments Endpoints
@app.get("/departments/json", tags=["Departments"])
def get_departments_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments")
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"departments": data})

@app.get("/departments/html", tags=["Departments"])
def get_departments_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments")
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Departments Table</h2><table border='1'><tr><th>ID</th><th>Department Name</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Jobs Endpoints
@app.get("/jobs/json", tags=["Jobs"])
def get_jobs_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"jobs": data})

@app.get("/jobs/html", tags=["Jobs"])
def get_jobs_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Jobs Table</h2><table border='1'><tr><th>ID</th><th>Job Name</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Hired Employees Endpoints
@app.get("/hired_employees/json", tags=["Hired Employees"])
def get_hired_employees_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hired_employees")
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"hired_employees": data})

@app.get("/hired_employees/html", tags=["Hired Employees"])
def get_hired_employees_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hired_employees")
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Hired Employees Table</h2><table border='1'><tr><th>ID</th><th>Name</th><th>Datetime</th><th>Department ID</th><th>Job ID</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Query 1 Endpoints
@app.get("/query1/json", tags=["Queries"], description="Number of employees hired for each job and department in 2021 divided by quarter, ordered alphabetically by department and job")
def execute_query1_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        SELECT j.job AS job_name, d.department AS department_name,
               strftime('%Y', h.datetime) AS year,
               CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
                    WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
                    WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
                    ELSE 'Q4' END AS quarter,
               COUNT(*) AS total_hired
        FROM hired_employees h
        JOIN jobs j ON h.job_id = j.id
        JOIN departments d ON h.department_id = d.id
        WHERE strftime('%Y', h.datetime) = '2021'
        GROUP BY j.job, d.department, year, quarter
        ORDER BY d.department, j.job
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"query1_results": data})

@app.get("/query1/html", tags=["Queries"], description="Number of employees hired for each job and department in 2021 divided by quarter, ordered alphabetically by department and job")
def execute_query1_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        SELECT j.job AS job_name, d.department AS department_name,
               strftime('%Y', h.datetime) AS year,
               CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
                    WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
                    WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
                    ELSE 'Q4' END AS quarter,
               COUNT(*) AS total_hired
        FROM hired_employees h
        JOIN jobs j ON h.job_id = j.id
        JOIN departments d ON h.department_id = d.id
        WHERE strftime('%Y', h.datetime) = '2021'
        GROUP BY j.job, d.department, year, quarter
        ORDER BY d.department, j.job
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Query 1 Results</h2><table border='1'><tr><th>Job</th><th>Department</th><th>Year</th><th>Quarter</th><th>Total Hired</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Query 2 Endpoints
@app.get("/query2/json", tags=["Queries"], description="List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending)")
def execute_query2_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        WITH dept_hires AS (
            SELECT d.id, d.department, COUNT(*) AS total_hired
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE strftime('%Y', h.datetime) = '2021'
            GROUP BY d.id, d.department
        ),
        dept_avg AS (
            SELECT AVG(total_hired) AS avg_hired FROM dept_hires
        )
        SELECT id, department, total_hired
        FROM dept_hires, dept_avg
        WHERE total_hired > avg_hired
        ORDER BY total_hired DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"query2_results": data})

@app.get("/query2/html", tags=["Queries"], description="List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending)")
def execute_query2_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        WITH dept_hires AS (
            SELECT d.id, d.department, COUNT(*) AS total_hired
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE strftime('%Y', h.datetime) = '2021'
            GROUP BY d.id, d.department
        ),
        dept_avg AS (
            SELECT AVG(total_hired) AS avg_hired FROM dept_hires
        )
        SELECT id, department, total_hired
        FROM dept_hires, dept_avg
        WHERE total_hired > avg_hired
        ORDER BY total_hired DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Query 2 Results</h2><table border='1'><tr><th>ID</th><th>Department</th><th>Total Hired</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)
