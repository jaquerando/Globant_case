from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Database configuration
DATABASE_URL = "sqlite:///data_challenge.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define tables
class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, nullable=True)  # Allow NULL

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, nullable=True)  # Allow NULL

class HiredEmployee(Base):
    __tablename__ = "hired_employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)  # Allow NULL
    datetime = Column(String, nullable=True)  # Kept as string for simplicity
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)  # Allow NULL
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True)  # Allow NULL

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)

# Load CSV data into the database
def load_csv_to_db():
    session = SessionLocal()

    try:
        # Load Departments
        print("Departments CSV:")
        departments_df = pd.read_csv("departments.csv", names=["id", "department"])
        print(departments_df.head())

        for _, row in departments_df.iterrows():
            if not session.query(Department).filter_by(id=int(row["id"])).first():
                session.add(Department(
                    id=int(row["id"]),
                    department=row["department"] if pd.notna(row["department"]) else None
                ))

        # Load Jobs
        print("Jobs CSV:")
        jobs_df = pd.read_csv("jobs.csv", names=["id", "job"])
        print(jobs_df.head())

        for _, row in jobs_df.iterrows():
            if not session.query(Job).filter_by(id=int(row["id"])).first():
                session.add(Job(
                    id=int(row["id"]),
                    job=row["job"] if pd.notna(row["job"]) else None
                ))

        # Load Hired Employees
        print("Hired Employees CSV:")
        hired_employees_df = pd.read_csv("hired_employees.csv", names=["id", "name", "datetime", "department_id", "job_id"])
        print(hired_employees_df.head())

        for _, row in hired_employees_df.iterrows():
            if not session.query(HiredEmployee).filter_by(id=int(row["id"])).first():
                session.add(HiredEmployee(
                    id=int(row["id"]),
                    name=row["name"] if pd.notna(row["name"]) else None,
                    datetime=row["datetime"] if pd.notna(row["datetime"]) else None,
                    department_id=int(row["department_id"]) if pd.notna(row["department_id"]) else None,
                    job_id=int(row["job_id"]) if pd.notna(row["job_id"]) else None
                ))

        session.commit()
        print("✅ Data successfully loaded into the database.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error loading data: {e}")

    finally:
        session.close()
