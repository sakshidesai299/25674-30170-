# 25674-30170-
# U.S. Non-Performance Payrolls Dashboard

## 📊 Project Overview

This project is a business intelligence dashboard designed for a U.S. labor market think tank. It provides managers and employees with a simple, interactive tool to manage goals, track progress, and view performance insights. The application is built using **Python**, with **Streamlit** for the frontend and a **PostgreSQL** database for the backend.

### Key Features:

- **Goal & Task Setting:** Managers can set goals with descriptions, due dates, and statuses for their employees.
- **Progress Tracking:** Employees and managers can view the status of goals and track progress.
- **Feedback:** The system provides a mechanism for managers to give feedback on specific goals.
- **Reporting & Insights:** The dashboard offers a clear view of employee performance history and key business insights using data analytics.

## 🚀 Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

You will need the following software installed:

- **Python 3.8+**
- **PostgreSQL**
- **pip** (Python package installer)

### 1. Database Setup

First, you need to set up the PostgreSQL database and create the necessary tables.

1.  **Start your PostgreSQL server.**
2.  **Create a new database.** You can use the `psql` command-line tool or a GUI client like pgAdmin.
    ```bash
    CREATE DATABASE your_database_name;
    ```
3.  **Run the SQL script** to create the tables. You can copy the code below and execute it in your PostgreSQL client.

    ```sql
    -- SQL Data Definition Language (DDL) for the U.S. Non-Performance Payrolls Dashboard database schema.

    -- Drop tables in the correct order to avoid foreign key constraint errors
    DROP TABLE IF EXISTS feedback;
    DROP TABLE IF EXISTS tasks;
    DROP TABLE IF EXISTS goals;
    DROP TABLE IF EXISTS employees;

    -- Create the 'employees' table to store user information.
    CREATE TABLE employees (
        employee_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        is_manager BOOLEAN NOT NULL
    );

    -- Create the 'goals' table to store performance goals.
    -- It links to employees and their managers.
    CREATE TABLE goals (
        goal_id SERIAL PRIMARY KEY,
        employee_id INTEGER NOT NULL REFERENCES employees(employee_id),
        manager_id INTEGER NOT NULL REFERENCES employees(employee_id),
        description TEXT NOT NULL,
        due_date DATE NOT NULL,
        status VARCHAR(20) NOT NULL CHECK (status IN ('Draft', 'In Progress', 'Completed', 'Cancelled'))
    );

    -- Create the 'tasks' table to track specific actions for achieving a goal.
    -- Each task is associated with a single goal.
    CREATE TABLE tasks (
        task_id SERIAL PRIMARY KEY,
        goal_id INTEGER NOT NULL REFERENCES goals(goal_id),
        description TEXT NOT NULL,
        is_approved BOOLEAN DEFAULT FALSE
    );

    -- Create the 'feedback' table to store performance feedback from managers.
    -- Each feedback entry is tied to a specific goal and manager.
    CREATE TABLE feedback (
        feedback_id SERIAL PRIMARY KEY,
        goal_id INTEGER NOT NULL REFERENCES goals(goal_id),
        manager_id INTEGER NOT NULL REFERENCES employees(employee_id),
        text TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Optional: Insert some sample data to test the dashboard
    INSERT INTO employees (first_name, last_name, is_manager) VALUES
    ('John', 'Doe', TRUE),
    ('Jane', 'Smith', FALSE),
    ('Peter', 'Jones', TRUE),
    ('Mary', 'Williams', FALSE),
    ('Michael', 'Brown', FALSE);

    INSERT INTO goals (employee_id, manager_id, description, due_date, status) VALUES
    (2, 1, 'Complete project proposal by month-end.', '2025-10-31', 'In Progress'),
    (4, 1, 'Attend required training sessions.', '2025-09-30', 'Completed'),
    (5, 3, 'Draft new marketing strategy.', '2025-11-15', 'Draft'),
    (2, 1, 'Prepare quarterly performance report.', '2025-12-31', 'In Progress');

    INSERT INTO tasks (goal_id, description, is_approved) VALUES
    (1, 'Research market trends.', TRUE),
    (1, 'Write section on competitive analysis.', FALSE),
    (2, 'Register for "Data Science Fundamentals" course.', TRUE),
    (2, 'Complete course modules 1-3.', TRUE),
    (3, 'Gather team feedback on current strategy.', FALSE);

    INSERT INTO feedback (goal_id, manager_id, text) VALUES
    (1, 1, 'Good start, but needs more detail in the analysis section.'),
    (2, 1, 'Excellent work on completing the training on time.');
    ```
4.  **Update the connection string.** Open the `backend.py` file and update the `get_db_connection` function with your PostgreSQL credentials.

    ```python
    # backend.py (snippet)
    def get_db_connection():
        conn = psycopg2.connect(
            host="localhost",
            database="your_database_name",  # <-- Update this
            user="your_username",           # <-- Update this
            password="your_password"        # <-- Update this
        )
        return conn
    ```

### 2. Python Environment Setup

1.  **Install the required libraries** using pip:
    ```bash
    pip install streamlit psycopg2-binary pandas
    ```

### 3. Running the Application

1.  **Save the provided `backend.py` and `frontend.py` files** in the same directory.
2.  **Run the Streamlit application** from your terminal:
    ```bash
    streamlit run frontend.py
    ```
3.  Your default web browser should open automatically with the dashboard. If not, open your browser and navigate to `http://localhost:8501`.

## 🔒 Login Details

For this sample application, the password for each user is their **first name in lowercase**.

- **Example Manager Login:**
  - **Employee ID:** 1
  - **Password:** john
- **Example Employee Login:**
  - **Employee ID:** 2
  - **Password:** jane

## 🤝 How to Contribute

We welcome contributions! Please feel free to submit issues or pull requests to improve the application.

### File Descriptions

- `frontend.py`: The Streamlit application interface.
- `backend.py`: All database connection and CRUD logic.
- `README.md`: This file.
