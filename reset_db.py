import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('data_challenge.db')
cursor = conn.cursor()

# Step 1: Drop existing tables if they exist
cursor.execute("DROP TABLE IF EXISTS departments")
cursor.execute("DROP TABLE IF EXISTS jobs")
cursor.execute("DROP TABLE IF EXISTS hired_employees")
print("Existing tables dropped successfully.")

# Step 2: Create departments table
cursor.execute("""
    CREATE TABLE departments (
        id INTEGER PRIMARY KEY,
        department_name TEXT NOT NULL
    )
""")
print("Table 'departments' created.")

# Step 3: Create jobs table
cursor.execute("""
    CREATE TABLE jobs (
        id INTEGER PRIMARY KEY,
        job_name TEXT NOT NULL
    )
""")
print("Table 'jobs' created.")

# Step 4: Create hired_employees table
cursor.execute("""
    CREATE TABLE hired_employees (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        datetime TEXT NOT NULL,
        department_id INTEGER,
        job_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id),
        FOREIGN KEY (job_id) REFERENCES jobs(id)
    )
""")
print("Table 'hired_employees' created.")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database reset and tables created successfully.")
