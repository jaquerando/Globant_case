import sqlite3

def execute_query2():
    conn = sqlite3.connect('data_challenge.db')
    cursor = conn.cursor()

    query = """
    SELECT d.department, COUNT(*) AS hired_count
    FROM hired_employees h
    JOIN departments d ON h.department_id = d.id
    WHERE strftime('%Y', h.datetime) = '2021'
    GROUP BY d.department
    HAVING hired_count > (
        SELECT AVG(dept_count) FROM (
            SELECT COUNT(*) AS dept_count
            FROM hired_employees
            WHERE strftime('%Y', datetime) = '2021'
            GROUP BY department_id
        )
    )
    ORDER BY hired_count DESC;
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results
