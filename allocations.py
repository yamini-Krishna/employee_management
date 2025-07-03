import streamlit as st
import pandas as pd
from datetime import datetime
from logs.activity_logger import get_logger
from sqlalchemy import text


def render_allocations(engine):
    """Render the allocations management page"""
    st.subheader("Project Allocations Management")

    # Get the global activity logger instance
    logger = get_logger()

    # Employee selection dropdown
    employees = get_employees_list(engine)
    if not employees:
        st.error("No employees found")
        return

    employee_options = {f"{emp[1]} ({emp[0]})": emp[0] for emp in employees}
    selected_employee_display = st.selectbox(
        "Select Employee",
        options=list(employee_options.keys()),
        key="allocations_employee_selector"
    )

    if selected_employee_display:
        selected_employee_code = employee_options[selected_employee_display]

        # Get employee details and allocations
        employee_details = get_employee_details(engine, selected_employee_code)
        allocations = get_employee_allocations(engine, selected_employee_code)

        if employee_details:
            display_employee_details(employee_details, allocations)

            if allocations:
                display_allocations_table(engine, allocations, selected_employee_code, logger)

                # Add save changes section below all details
                display_save_changes_section(engine, selected_employee_code, logger)
            else:
                st.info("No active project allocations found for this employee")


def get_employees_list(engine):
    """Get list of all active employees"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT employee_code, employee_name, department_name
                FROM employee
                WHERE status = 'Active'
                ORDER BY employee_name
            """))
            return result.fetchall()
    except Exception as e:
        st.error(f"Error fetching employees: {e}")
        return []


def get_employee_details(engine, employee_code):
    """Get employee basic details"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT employee_code, employee_name, department_name, email, mobile_number
                FROM employee
                WHERE employee_code = :employee_code AND status = 'Active'
            """), {"employee_code": employee_code})
            return result.fetchone()
    except Exception as e:
        st.error(f"Error fetching employee details: {e}")
        return None


def get_employee_allocations(engine, employee_code):
    """Get current active allocations for an employee"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    pa.allocation_id,
                    pa.project_id,
                    p.project_name,
                    pa.allocation_percentage,
                    p.start_date,
                    p.end_date,
                    pa.effective_from,
                    pa.effective_to,
                    COALESCE(
                        (SELECT SUM(t.hours_worked) 
                         FROM timesheet t 
                         WHERE t.employee_code = pa.employee_code 
                         AND t.project_id = pa.project_id), 0
                    ) as total_hours,
                    COALESCE(
                        (SELECT COUNT(DISTINCT t.work_date) 
                         FROM timesheet t 
                         WHERE t.employee_code = pa.employee_code 
                         AND t.project_id = pa.project_id), 0
                    ) as days_worked,
                    COALESCE(
                        (SELECT MIN(t.work_date) 
                         FROM timesheet t 
                         WHERE t.employee_code = pa.employee_code 
                         AND t.project_id = pa.project_id), p.start_date
                    ) as first_day,
                    COALESCE(
                        (SELECT MAX(t.work_date) 
                         FROM timesheet t 
                         WHERE t.employee_code = pa.employee_code 
                         AND t.project_id = pa.project_id), p.end_date
                    ) as last_day
                FROM project_allocation pa
                JOIN project p ON pa.project_id = p.project_id
                WHERE pa.employee_code = :employee_code AND pa.status = 'Active'
                ORDER BY pa.project_id
            """), {"employee_code": employee_code})
            return result.fetchall()
    except Exception as e:
        st.error(f"Error fetching allocations: {e}")
        return []


def get_valid_created_by(engine):
    """Get a valid employee code to use as created_by"""
    try:
        with engine.connect() as conn:
            # Try to get the current user from session state
            current_user = st.session_state.get('user')
            if current_user:
                result = conn.execute(text("""
                    SELECT employee_code FROM employee 
                    WHERE employee_code = :employee_code AND status = 'Active'
                """), {"employee_code": current_user})
                if result.fetchone():
                    return current_user

            # If no valid current user, get the first active employee
            result = conn.execute(text("""
                SELECT employee_code FROM employee 
                WHERE status = 'Active' 
                ORDER BY employee_code 
                LIMIT 1
            """))
            row = result.fetchone()
            return row[0] if row else None
    except Exception as e:
        st.error(f"Error getting valid created_by: {e}")
        return None


def display_employee_details(employee_details, allocations):
    """Display employee details card"""
    emp_code, emp_name, dept_name, email, mobile = employee_details

    # Calculate total allocation
    total_allocation = sum(allocation[3] for allocation in allocations) if allocations else 0

    st.markdown(f"""
    **{emp_name} ({emp_code}) - {dept_name}**

    **Email:** {email or 'N/A'}  
    **Mobile Number:** {mobile or 'N/A'}  
    **Total Allocation:** {total_allocation:.1f}%
    """)

    #if total_allocation > 100:
    #    st.error(f"Warning: Total allocation ({total_allocation:.1f}%) exceeds 100%")
    #elif total_allocation == 0:
    #    st.info("No active allocations")


def display_allocations_table(engine, allocations, employee_code, logger):
    """Display allocations table with clickable allocation percentages for editing"""
    st.markdown("**Project Assignments with Allocation:**")

    # Create columns for the table header (removed Edit column)
    col_headers = st.columns([1, 2.5, 1, 1, 1.2, 1.2, 1])
    headers = ["Project", "Project Name", "Hours", "Days", "First Day", "Last Day", "Allocation (%)"]

    for i, header in enumerate(headers):
        col_headers[i].markdown(f"**{header}**")

    st.markdown("---")

    # Display each allocation row
    for allocation in allocations:
        allocation_id, project_id, project_name, allocation_percentage, start_date, end_date, effective_from, effective_to, total_hours, days_worked, first_day, last_day = allocation

        cols = st.columns([1, 2.5, 1, 1, 1.2, 1.2, 1])

        with cols[0]:
            st.write(project_id)
        with cols[1]:
            st.write(project_name)
        with cols[2]:
            st.write(f"{total_hours:.1f}")
        with cols[3]:
            st.write(str(days_worked))
        with cols[4]:
            st.write(str(first_day) if first_day else "N/A")
        with cols[5]:
            st.write(str(last_day) if last_day else "N/A")
        with cols[6]:
            # Check if this allocation is being edited
            edit_key = f"edit_{allocation_id}"
            if st.session_state.get(edit_key, False):
                # Show edit form as number input
                new_percentage = st.number_input(
                    "",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(allocation_percentage),
                    step=0.1,
                    key=f"new_percentage_{allocation_id}"
                )
                # Auto-store the change when value changes
                if new_percentage != float(allocation_percentage):
                    st.session_state[f"pending_change_{allocation_id}"] = {
                        'new_percentage': new_percentage,
                        'allocation_id': allocation_id,
                        'employee_code': employee_code,
                        'old_percentage': float(allocation_percentage)
                    }
            else:
                # Show clickable allocation percentage
                if st.button(f"{allocation_percentage:.1f}%", key=f"allocation_btn_{allocation_id}",
                             help="Click to edit this allocation"):
                    st.session_state[edit_key] = True
                    st.rerun()


def display_save_changes_section(engine, employee_code, logger):
    """Display save changes section below all allocation details"""
    st.markdown("---")
    st.markdown("### Save Changes")

    # Check if there are any pending changes
    pending_changes = {}
    for key in st.session_state.keys():
        if key.startswith("pending_change_"):
            allocation_id = key.replace("pending_change_", "")
            pending_changes[allocation_id] = st.session_state[key]

    if pending_changes:
        st.markdown("**Pending Changes:**")
        for allocation_id, change_data in pending_changes.items():
            old_pct = change_data.get('old_percentage', 0)
            new_pct = change_data['new_percentage']
            st.write(f"- Allocation ID {allocation_id}: {old_pct:.1f}% → {new_pct:.1f}%")

        # Reason input for all changes
        change_reason = st.text_area(
            "Change Reason (Required for all changes):",
            key="bulk_change_reason",
            placeholder="Enter reason for allocation changes...",
            height=100
        )

        col_confirm, col_cancel_all = st.columns(2)

        with col_confirm:
            if st.button("Confirm All Changes", key="confirm_all_changes"):
                if change_reason.strip():
                    all_success = True
                    for allocation_id, change_data in pending_changes.items():
                        success = update_allocation(
                            engine,
                            change_data['allocation_id'],
                            change_data['employee_code'],
                            change_data['new_percentage'],
                            change_reason.strip(),
                            logger
                        )
                        if not success:
                            all_success = False

                    if all_success:
                        st.success("All allocations updated successfully!")
                        # Clear all pending changes and edit states
                        for allocation_id in pending_changes.keys():
                            st.session_state.pop(f"edit_{allocation_id}", None)
                            st.session_state.pop(f"pending_change_{allocation_id}", None)
                        st.session_state.pop("bulk_change_reason", None)
                        st.rerun()
                    else:
                        st.error("Some allocations failed to update. Please check the logs.")
                else:
                    st.error("Change reason is required for all changes")

        with col_cancel_all:
            if st.button("Cancel All Changes", key="cancel_all_changes"):
                # Clear all pending changes and edit states
                for allocation_id in pending_changes.keys():
                    st.session_state.pop(f"edit_{allocation_id}", None)
                    st.session_state.pop(f"pending_change_{allocation_id}", None)
                st.session_state.pop("bulk_change_reason", None)
                st.rerun()
    else:
        st.info("No pending changes to save")


def update_allocation(engine, old_allocation_id, employee_code, new_percentage, change_reason, logger):
    """Update allocation by creating new record and deactivating old one"""
    try:
        with engine.connect() as conn:
            # Start transaction
            trans = conn.begin()

            try:
                # Get current allocation details
                result = conn.execute(text("""
                    SELECT project_id, effective_from, effective_to, allocation_percentage
                    FROM project_allocation
                    WHERE allocation_id = :allocation_id
                """), {"allocation_id": old_allocation_id})

                allocation_data = result.fetchone()
                if not allocation_data:
                    st.error("Allocation not found")
                    return False

                project_id, effective_from, effective_to, old_percentage = allocation_data

                # Get a valid created_by employee code
                created_by = get_valid_created_by(engine)
                if not created_by:
                    st.error("No valid employee found for created_by field")
                    return False

                # Deactivate old allocation
                conn.execute(text("""
                    UPDATE project_allocation
                    SET status = 'Inactive'
                    WHERE allocation_id = :allocation_id
                """), {"allocation_id": old_allocation_id})

                # Insert new allocation record
                conn.execute(text("""
                    INSERT INTO project_allocation 
                    (employee_code, project_id, allocation_percentage, effective_from, 
                     effective_to, status, created_by, change_reason, created_at)
                    VALUES (:employee_code, :project_id, :allocation_percentage, :effective_from, 
                            :effective_to, :status, :created_by, :change_reason, :created_at)
                """), {
                    "employee_code": employee_code,
                    "project_id": project_id,
                    "allocation_percentage": new_percentage,
                    "effective_from": effective_from,
                    "effective_to": effective_to,
                    "status": "Active",
                    "created_by": created_by,
                    "change_reason": change_reason,
                    "created_at": datetime.now()
                })

                # Commit transaction
                trans.commit()

                # Log the allocation update
                logger.log_event(
                    event_type="ALLOCATION_UPDATE",
                    description=f"Updated allocation for {employee_code} on project {project_id}",
                    user=st.session_state.get('user', created_by),
                    details={
                        "employee_code": employee_code,
                        "project_id": project_id,
                        "old_percentage": float(old_percentage),
                        "new_percentage": new_percentage,
                        "change_reason": change_reason
                    }
                )

                return True

            except Exception as e:
                trans.rollback()
                raise e

    except Exception as e:
        st.error(f"Error updating allocation: {e}")

        # Log the error
        logger.log_event(
            event_type="ALLOCATION_UPDATE_ERROR",
            description=f"Failed to update allocation: {str(e)}",
            user=st.session_state.get('user', 'system'),
            details={"error": str(e), "allocation_id": old_allocation_id}
        )

        return False


def validate_total_allocation(engine, employee_code, exclude_allocation_id=None):
    """Validate that total allocation doesn't exceed 100%"""
    try:
        with engine.connect() as conn:
            if exclude_allocation_id:
                result = conn.execute(text("""
                    SELECT SUM(allocation_percentage)
                    FROM project_allocation
                    WHERE employee_code = :employee_code AND status = 'Active'
                    AND allocation_id != :exclude_allocation_id
                """), {
                    "employee_code": employee_code,
                    "exclude_allocation_id": exclude_allocation_id
                })
            else:
                result = conn.execute(text("""
                    SELECT SUM(allocation_percentage)
                    FROM project_allocation
                    WHERE employee_code = :employee_code AND status = 'Active'
                """), {"employee_code": employee_code})

            row = result.fetchone()
            return float(row[0]) if row[0] else 0.0

    except Exception as e:
        st.error(f"Error validating allocation: {e}")
        return 0.0