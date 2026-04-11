# reporting.py
import sqlite3
from datetime import date, timedelta

DB_NAME = "attendance.db"

def list_all_employees():
    """Prints a list of all enrolled employees."""
    print("\n--- List of All Enrolled Employees ---")
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM employees ORDER BY name")
        rows = cursor.fetchall()
        
        if not rows:
            print("No employees are registered in the system.")
            return

        print(f"{'ID':<15} | {'Name':<25} | {'Email':<30}")
        print("-" * 73)
        for row in rows:
            print(f"{row[0]:<15} | {row[1]:<25} | {row[2]:<30}")
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def get_employee_report():
    """Searches for an employee and prints their 30-day attendance report."""
    search_term = input("\nEnter Employee ID or Name to search: ").strip()
    if not search_term:
        print("Search cancelled.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Find the employee
        cursor.execute(
            "SELECT id, name FROM employees WHERE id = ? OR name LIKE ?",
            (search_term, f"%{search_term}%")
        )
        employee = cursor.fetchone()

        if not employee:
            print(f"No employee found matching '{search_term}'.")
            return
            
        employee_id, name = employee
        print(f"\n--- Attendance Report for {name} (ID: {employee_id}) ---")
        print("--- (Based on the last 30 days) ---")

        # Define the 30-day period
        # We include today, so we go back 29 days
        end_date = date.today()
        start_date = end_date - timedelta(days=29)
        total_days_in_period = 30 
        
        # Query for attendance records within this period
        cursor.execute(
            "SELECT COUNT(date) FROM attendance WHERE employee_id = ? AND date BETWEEN ? AND ?",
            (employee_id, start_date.isoformat(), end_date.isoformat())
        )
        
        total_presents = cursor.fetchone()[0]
        total_absents = total_days_in_period - total_presents
        
        if total_days_in_period > 0:
            present_percentage = (total_presents / total_days_in_period) * 100
        else:
            present_percentage = 0.0

        # Print the report
        print(f"Reporting Period: {start_date.isoformat()} to {end_date.isoformat()}")
        print(f"Total Days in Period: {total_days_in_period}")
        print(f"Total Days Present:   {total_presents}")
        print(f"Total Days Absent:    {total_absents}")
        print(f"Present Percentage:   {present_percentage:.2f}%")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

def main_menu():
    """Displays the main reporting menu."""
    while True:
        print("\n--- Attendance Reporting System ---")
        print("1. List all enrolled employees")
        print("2. Get attendance report for an employee")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            list_all_employees()
        elif choice == '2':
            get_employee_report()
        elif choice == '3':
            print("Exiting reporting system.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()