from fastapi import FastAPI, Query, UploadFile, File, HTTPException, Body
from fastapi.responses import JSONResponse, HTMLResponse
from app import upload
from typing import List
import sqlite3
import shutil
import os
import pandas as pd
from query1 import execute_query1_json, execute_query1_html
from query2 import execute_query2_json, execute_query2_html
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Data Challenge API",
    description="An API to manage and analyze employee hiring data.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(upload.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
SELECT d.department_name AS department,
       j.job_name AS job,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
FROM hired_employees h
JOIN departments d ON h.department_id = d.id
JOIN jobs j ON h.job_id = j.id
WHERE strftime('%Y', h.datetime) = '2021'
GROUP BY d.department_name, j.job_name
ORDER BY d.department_name, j.job_name;
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
SELECT d.department_name AS department,
       j.job_name AS job,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 1 ELSE 0 END) AS Q1,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 1 ELSE 0 END) AS Q2,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 1 ELSE 0 END) AS Q3,
       SUM(CASE WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 10 AND 12 THEN 1 ELSE 0 END) AS Q4
FROM hired_employees h
JOIN departments d ON h.department_id = d.id
JOIN jobs j ON h.job_id = j.id
WHERE strftime('%Y', h.datetime) = '2021'
GROUP BY d.department_name, j.job_name
ORDER BY d.department_name, j.job_name;
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
WITH department_hires AS (
    SELECT d.id, d.department_name, COUNT(*) AS total_hired
    FROM hired_employees h
    JOIN departments d ON h.department_id = d.id
    WHERE strftime('%Y', h.datetime) = '2021'
    GROUP BY d.id, d.department_name
),
average_hires AS (
    SELECT AVG(total_hired) AS avg_hired FROM department_hires
)
SELECT dh.id, dh.department_name, dh.total_hired AS hired
FROM department_hires dh, average_hires ah
WHERE dh.total_hired > ah.avg_hired
ORDER BY dh.total_hired DESC;
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
WITH department_hires AS (
    SELECT d.id, d.department_name, COUNT(*) AS total_hired
    FROM hired_employees h
    JOIN departments d ON h.department_id = d.id
    WHERE strftime('%Y', h.datetime) = '2021'
    GROUP BY d.id, d.department_name
),
average_hires AS (
    SELECT AVG(total_hired) AS avg_hired FROM department_hires
)
SELECT dh.id, dh.department_name, dh.total_hired AS hired
FROM department_hires dh, average_hires ah
WHERE dh.total_hired > ah.avg_hired
ORDER BY dh.total_hired DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    html_content = "<h2>Query 2 Results</h2><table border='1'><tr><th>ID</th><th>Department</th><th>Total Hired</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)

# Batch Insert Endpoint
@app.post("/batch-insert", tags=["Data Upload"])
def batch_insert(file: UploadFile = File(...)):
    try:
        conn = sqlite3.connect("data_challenge.db")
        df = pd.read_csv(file.file)
        if len(df) > 1000:
            raise HTTPException(status_code=400, detail="Batch size exceeds 1000 rows.")
        df.to_sql("hired_employees", conn, if_exists='append', index=False)
        conn.close()
        return {"status": f"Batch of {len(df)} records inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@app.delete("/clear-data", tags=["Data Upload"], description="Delete all data from the database tables")
def clear_data():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM departments")
        cursor.execute("DELETE FROM jobs")
        cursor.execute("DELETE FROM hired_employees")
        conn.commit()
        conn.close()
        return JSONResponse(content={"message": "All tables have been cleared."})
    except Exception as e:
        conn.rollback()
        conn.close()
        return JSONResponse(content={"error": str(e)}, status_code=500)
        
