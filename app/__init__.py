import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('data_challenge.db')
cursor = conn.cursor()

# First SQL query
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

# Execute query
cursor.execute(query)
results = cursor.fetchall()

# Print results
for row in results:
    print(row)

# Close connection
conn.close()
