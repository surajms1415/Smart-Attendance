Smart Attendance System

AI-Based Attendance using Face Recognition, Database and Reporting

Smart Attendance is a Python-based system that automates attendance marking using face recognition, along with user registration, database management, and reporting capabilities. It provides a complete solution for accurate and efficient attendance tracking.

Features
Face recognition-based attendance marking
Manual user registration with data capture
Structured database storage for users and attendance
Report generation for daily and individual records
Real-time processing using computer vision
System Workflow

User Registration → Database Storage → Face Encoding → Live Detection → Attendance Marking → Report Generation

Tech Stack
Python
OpenCV, face_recognition
NumPy, pandas
SQLite / CSV
Project Structure
Smart-Attendance/
│── attendance_system.py
│── manual_register.py
│── database_setup.py
│── reporting.py
│── dataset/
│── attendance.csv / database
Installation
git clone https://github.com/surajms1415/Smart-Attendance.git
cd Smart-Attendance
pip install opencv-python face-recognition numpy pandas
Usage
python database_setup.py
python manual_register.py
python attendance_system.py
python reporting.py
Output
Attendance stored with name, date, and time
Generated reports for analysis
Future Enhancements
Web dashboard integration
Cloud database support
Mobile application
Advanced analytics
Author

Suraj M S
https://github.com/surajms1415
