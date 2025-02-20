from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import sqlite3

# Initialize the router
router = APIRouter()

# Mapping CSV filenames to database tables and expected columns
table_mappings = {
    "departments.csv": {
        "table_name": "departments",
        "columns": ["id", "department_name"]
    },
    "jobs.csv": {
        "table_name": "jobs",
        "columns": ["id", "job_name"]
    },
    "hired_employees.csv": {
        "table_name": "hired_employees",
        "columns": ["id", "name", "datetime", "department_id", "job_id"]
    }
}

@router.post("/upload", tags=["Data Upload"], description="Upload and load a CSV into the database.")
async def upload_and_load_csv(file: UploadFile = File(...)):
    try:
        if file.filename not in table_mappings:
            raise HTTPException(status_code=400, detail="Invalid file name. Expected one of: departments.csv, jobs.csv, hired_employees.csv")

        # Get table info
        table_info = table_mappings[file.filename]
        table_name = table_info["table_name"]
        expected_columns = table_info["columns"]

        # Read CSV directly from uploaded file
        # Read CSV directly from uploaded file
        df = pd.read_csv(file.file, names=expected_columns, header=0)
        
        # Drop rows where 'name' is missing or empty (for hired_employees)
        if file.filename == "hired_employees.csv":
            df["name"] = df["name"].astype(str).str.strip()  # Convert to string & strip spaces
            df = df[df["name"] != ""]  # Remove empty strings
            df = df.dropna(subset=["name"])  # Drop NaN in 'name'
        
            # Handle datetime format
            df["datetime"] = pd.to_datetime(df["datetime"], errors='coerce')
            df = df.dropna(subset=["datetime"])  # Drop invalid dates
            df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")  # Format for SQLite

        # Handle datetime format validation (especially for hired_employees)
        # Handle datetime format validation (especially for hired_employees)
        if file.filename == "hired_employees.csv":
            try:
                df["datetime"] = pd.to_datetime(df["datetime"], errors='coerce')
                df = df.dropna(subset=["datetime"])  # Drop rows with invalid datetime
        
                # Convert Timestamp to string (SQLite doesn't support Timestamp)
                df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid datetime format in 'datetime' column: {str(e)}")

        # Connect to the database
        conn = sqlite3.connect("data_challenge.db", timeout=10)  # Added timeout to avoid locks
        cursor = conn.cursor()

        # Check for duplicates and insert only new records
        inserted_rows = 0
        duplicates = 0

        for _, row in df.iterrows():
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE id = ?", (row["id"],))
            exists = cursor.fetchone()[0]

            if exists == 0:
                placeholders = ", ".join(["?"] * len(row))
                col_names = ", ".join(row.index)
                try:
                    cursor.execute(f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})", tuple(row))
                    inserted_rows += 1
                except sqlite3.IntegrityError as e:
                    raise HTTPException(status_code=400, detail=f"Integrity Error: {str(e)}")
            else:
                duplicates += 1

        conn.commit()

        return {
            "status": "success",
            "file": file.filename,
            "records_inserted": inserted_rows,
            "duplicates_skipped": duplicates
        }

    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database operational error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Ensure connection is always closed
        if 'conn' in locals():
            conn.close()
