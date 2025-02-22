# Globant_case
# Data Engineering Challenge - FastAPI and SQLite

## Overview
This project is part of the **Globant Data Engineering Coding Challenge**. The goal is to:
1. **Create a REST API** to process and store employee data.
2. **Load CSV data** into an SQLite database.
3. **Provide API endpoints** to interact with the stored data.

## Requirements
- Python 3.11+
- FastAPI
- SQLite
- Docker (optional for containerization)

## Setup Instructions

### Install Dependencies

```
pip install -r requirements.txt
```

# SQL QUERIES

📊 **SQL Queries Explanation – Data Challenge API**

## **Query 1 – Employees Hired per Quarter in 2021**

📋 Question:
**"Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job."**

💡 ## **SQL Code:**

```sql
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

```
## 📊 Output:
![image](https://github.com/user-attachments/assets/89dd1707-395c-4b12-976f-4054a0ad12b6)

## ✅ Explanation:
Data Filtering (WHERE strftime('%Y', h.datetime) = '2021'):

This filters the data to only include employees hired in 2021.
strftime('%Y', h.datetime) extracts the year from the datetime field.
Joining Tables (JOIN statements):

The query joins the hired_employees table with:
departments to get the department name.
jobs to get the job title.
These joins allow us to display readable department and job names instead of IDs.
Quarterly Count (SUM(CASE WHEN ... THEN 1 ELSE 0 END)):

The query divides the year into four quarters:
Q1: January - March
Q2: April - June
Q3: July - September
Q4: October - December
It uses a CASE statement to count hires in each quarter by checking the month extracted from the datetime field.
Grouping & Ordering (GROUP BY and ORDER BY):

GROUP BY groups the results by department and job so that counts are calculated for each combination.
ORDER BY ensures the output is sorted alphabetically first by department and then by job.




## **Query 2 – Departments Hiring Above the Average**
📋 Question:
**"List of IDs, names, and the number of employees hired for each department that hired more employees than the average in 2021. The list should be ordered by the number of employees hired (descending)."**

## 💡 SQL Code:

```sql
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
```

##  📊 Output:
![image](https://github.com/user-attachments/assets/d56f72a4-dea6-4b6e-8a2b-f40eaf38f28f)


 ## ✅ **Explanation:**

Using CTEs (WITH clauses):

This query uses Common Table Expressions (CTEs) for clarity and to break down the logic into manageable parts.
CTE 1 – department_hires:

Calculates the total number of hires for each department in 2021.
Groups by department to count how many employees were hired per department.
CTE 2 – average_hires:

Computes the average number of hires across all departments by taking the average of the total hires from department_hires.
Main Query:

Selects departments from department_hires where the total number of hires is greater than the average calculated in average_hires.
Sorting (ORDER BY dh.total_hired DESC):

Orders the result in descending order so that the departments with the highest number of hires appear at the top.





🧠 **Why This Approach?**

Performance Optimization:

CTEs help in breaking down complex queries, making them more readable and easier to debug.
Calculating the average only once using average_hires instead of recalculating it in every row improves efficiency.
Data Integrity:

By using joins with the departments and jobs tables, the queries always display human-readable names instead of IDs.
Flexibility:

The use of dynamic filtering (like strftime('%Y', h.datetime) = '2021') allows easy adjustment for different years.

# ** Data Dictionary - Data Challenge API **

## ** Overview **

The Data Challenge API manages and analyzes employee hiring data. This document describes the database schema, including tables, columns, data types, and relationships.

Tables and Columns

## 1️⃣  **Table: departments**

Stores information about company departments.

![image](https://github.com/user-attachments/assets/c882f634-1196-408a-83be-0817af52e01e)


## 2️⃣ **Table: jobs**

Stores available job positions.

![image](https://github.com/user-attachments/assets/4479927d-fc8f-4ad3-bae2-b771ef91597c)


## 3️⃣ **Table: hired_employees**

Stores employee hiring records.

![image](https://github.com/user-attachments/assets/d4cec034-5066-4018-977a-eb363c796d33)

## **Relationships Between Tables**

hired_employees.department_id → 🔗 departments.id

hired_employees.job_id → 🔗 jobs.id

**Business Rules**

An employee must be assigned to both a department and a job position.

The datetime field only accepts valid dates in the format YYYY-MM-DD HH:MM:SS.

Duplicate records with the same id are not allowed in any table.

The system prevents the insertion of data with invalid foreign keys.



