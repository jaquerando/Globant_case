import sqlite3
from fastapi.responses import JSONResponse, HTMLResponse

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

    html_content = "<h2>Query 1 Results</h2><table border='1'><tr><th>Department</th><th>Job</th><th>Q1</th><th>Q2</th><th>Q3</th><th>Q4</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)
