Smart Attendance System

AI-Based Attendance using Face Recognition, Database and Reporting

Smart Attendance is a Python-based system that automates attendance marking using face recognition, along with user registration, database management, and reporting capabilities, providing a complete solution for accurate and efficient attendance tracking.

Features

Face recognition-based attendance marking, manual user registration with data capture, structured database storage for users and attendance, report generation for daily and individual records, real-time processing using computer vision.

System Workflow

User registration, database storage, face encoding, live detection, attendance marking, report generation.

Tech Stack

Python, OpenCV, face_recognition, NumPy, pandas, SQLite or CSV.

Project Structure
Smart-Attendance/  
attendance_system.py, manual_register.py, database_setup.py, reporting.py, dataset/, attendance.csv or database  
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

Attendance records with name, date and time, generated reports for analysis.

Future Enhancements

Web dashboard integration, cloud database support, mobile application, advanced analytics.

Author

Suraj M S, https://github.com/surajms1415
