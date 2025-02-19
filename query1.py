import sqlite3

def execute_query1():
    conn = sqlite3.connect('data_challenge.db')
    cursor = conn.cursor()

    query = """
    SELECT j.job AS job_name, d.department AS department_name, 
           strftime('%Y', h.datetime) AS year, 
           CASE 
               WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 1 AND 3 THEN 'Q1'
               WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 4 AND 6 THEN 'Q2'
               WHEN CAST(strftime('%m', h.datetime) AS INTEGER) BETWEEN 7 AND 9 THEN 'Q3'
               ELSE 'Q4'
           END AS quarter, 
           COUNT(*) AS total_hired
    FROM hired_employees h
    JOIN jobs j ON h.job_id = j.id
    JOIN departments d ON h.department_id = d.id
    WHERE strftime('%Y', h.datetime) = '2021'
    GROUP BY job_name, department_name, year, quarter
    ORDER BY job_name, department_name, quarter;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results
