import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('data_challenge.db')
cursor = conn.cursor()

# Second SQL query: Departments with hires above average in 2021
query = """
    SELECT d.id AS department_id,
           d.department AS department_name,
           COUNT(h.id) AS hired_employees_count
    FROM hired_employees h
    JOIN departments d ON h.department_id = d.id
    WHERE strftime('%Y', h.datetime) = '2021'
    GROUP BY d.id, d.department
    HAVING hired_employees_count > (
        SELECT AVG(dept_count)
        FROM (
            SELECT COUNT(h2.id) AS dept_count
            FROM hired_employees h2
            WHERE strftime('%Y', h2.datetime) = '2021'
            GROUP BY h2.department_id
        )
    )
    ORDER BY hired_employees_count DESC;
"""

# Execute query
cursor.execute(query)
results = cursor.fetchall()

# Print results
for row in results:
    print(row)

# Close connection
conn.close()
