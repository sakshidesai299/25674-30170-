import streamlit as st
import pandas as pd
from backend import *

# Initialize database
create_tables()

# Session state for authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'is_manager' not in st.session_state:
    st.session_state.is_manager = False

def login_form():
    """Renders the login form."""
    st.title("Login to the Dashboard")
    with st.form("login_form"):
        st.subheader("Please enter your Employee ID and password.")
        employee_id = st.text_input("Employee ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            try:
                # In a real application, you would check the password against a hashed value
                # and verify credentials. For this example, we'll assume the password is the
                # employee's first name in lowercase.
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("SELECT employee_id, is_manager, first_name FROM employees WHERE employee_id = %s", (int(employee_id),))
                user = cur.fetchone()
                cur.close()
                conn.close()

                if user and user[2].lower() == password.lower():
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.is_manager = user[1]
                    st.success("Login successful! Redirecting...")
                    st.experimental_rerun()
                else:
                    st.error("Invalid Employee ID or password.")
            except (ValueError, psycopg2.Error) as e:
                st.error(f"Error during login: {e}")

def dashboard_app():
    """Renders the main dashboard application."""
    st.title("U.S. Non-Performance Payrolls Dashboard")
    
    # Navigation
    st.sidebar.title("Dashboard Navigation")
    page = st.sidebar.radio("Go to", ["Manage Goals", "Business Insights"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.is_manager = False
        st.experimental_rerun()

    # ---
    # Page: Manage Goals (CRUD for Goals)
    # ---
    if page == "Manage Goals":
        st.header("Goal Management")

        all_employees = get_all_employees()
        employee_names = {e[0]: f"{e[1]} {e[2]}" for e in all_employees}
        
        # Only managers can set and update goals
        if st.session_state.is_manager:
            with st.form("goal_form"):
                st.subheader("Set a New Goal")
                employee_id = st.selectbox("Select Employee", list(employee_names.keys()), format_func=lambda x: employee_names[x])
                manager_id = st.session_state.user_id
                description = st.text_area("Goal Description")
                due_date = st.date_input("Due Date")
                status = st.selectbox("Status", ['Draft', 'In Progress', 'Completed', 'Cancelled'])
                submitted = st.form_submit_button("Create Goal")

                if submitted:
                    add_goal(employee_id, manager_id, description, due_date, status)
                    st.success("Goal created successfully!")

            st.subheader("View & Update Goals")
            employee_to_view = st.selectbox(
                "Select an employee to view their goals:",
                list(employee_names.keys()),
                format_func=lambda x: employee_names[x]
            )
            goals = get_goals_for_employee(employee_to_view)
            if goals:
                goals_df = pd.DataFrame(
                    goals,
                    columns=["ID", "Description", "Due Date", "Status", "Manager's First Name", "Manager's Last Name"]
                )
                st.table(goals_df)
                
                # Update goal status is a manager-only function
                st.subheader("Update Goal Status")
                goal_to_update = st.selectbox("Select Goal to Update", goals_df['ID'])
                if goal_to_update:
                    new_status = st.selectbox("New Status", ['In Progress', 'Completed', 'Cancelled'])
                    if st.button("Update Status"):
                        update_goal_status(goal_to_update, new_status)
                        st.success(f"Goal {goal_to_update} status updated to {new_status}!")
                        st.experimental_rerun()
            else:
                st.info("This employee has no goals.")
        else:
            st.warning("You must be a manager to set and update goals.")
            
            st.subheader(f"My Goals")
            my_goals = get_goals_for_employee(st.session_state.user_id)
            if my_goals:
                my_goals_df = pd.DataFrame(
                    my_goals,
                    columns=["ID", "Description", "Due Date", "Status", "Manager's First Name", "Manager's Last Name"]
                )
                st.table(my_goals_df)
            else:
                st.info("You have no goals assigned.")

    # ---
    # Page: Business Insights
    # ---
    elif page == "Business Insights":
        st.header("Business Intelligence Insights")
        insights = get_insights()

        st.subheader("Overall Employee Statistics")
        st.write(f"Total Number of Employees: **{insights['total_employees']}**")
        st.write(f"Average Number of Goals per Employee: **{insights['avg_goals_per_employee']:.2f}**")
        
        st.subheader("Task Approval Rates")
        st.write(f"MIN Task Approval Rate: **{insights['min_task_approval_rate']:.2f}**")
        st.write(f"MAX Task Approval Rate: **{insights['max_task_approval_rate']:.2f}**")
        st.write(f"AVG Task Approval Rate: **{insights['avg_task_approval_rate']:.2f}**")
        
        st.subheader("Goals by Status")
        goals_status_df = pd.DataFrame(insights['goals_by_status'], columns=["Status", "Count"])
        st.table(goals_status_df)
        st.bar_chart(goals_status_df.set_index("Status"))


if st.session_state.logged_in:
    dashboard_app()
else:
    login_form()