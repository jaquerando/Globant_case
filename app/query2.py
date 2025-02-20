import sqlite3
from fastapi.responses import JSONResponse, HTMLResponse

def execute_query2_json():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        WITH dept_hires AS (
            SELECT d.id, d.department_name, COUNT(*) AS total_hired
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE strftime('%Y', h.datetime) = '2021'
            GROUP BY d.id, d.department_name
        ),
        dept_avg AS (
            SELECT AVG(total_hired) AS avg_hired FROM dept_hires
        )
        SELECT id, department_name, total_hired
        FROM dept_hires, dept_avg
        WHERE total_hired > avg_hired
        ORDER BY total_hired DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"query2_results": data})

def execute_query2_html():
    conn = sqlite3.connect("data_challenge.db")
    cursor = conn.cursor()
    query = """
        WITH dept_hires AS (
            SELECT d.id, d.department_name, COUNT(*) AS total_hired
            FROM hired_employees h
            JOIN departments d ON h.department_id = d.id
            WHERE strftime('%Y', h.datetime) = '2021'
            GROUP BY d.id, d.department_name
        ),
        dept_avg AS (
            SELECT AVG(total_hired) AS avg_hired FROM dept_hires
        )
        SELECT id, department_name, total_hired
        FROM dept_hires, dept_avg
        WHERE total_hired > avg_hired
        ORDER BY total_hired DESC;
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    html_content = "<h2>Query 2 Results</h2><table border='1'><tr><th>ID</th><th>Department</th><th>Total Hired</th></tr>"
    for row in data:
        html_content += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html_content += "</table>"
    return HTMLResponse(content=html_content)
