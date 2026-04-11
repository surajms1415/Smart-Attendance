# attendance_system.py
import cv2
import face_recognition
import numpy as np
import sqlite3
import json
from datetime import date
import os

# --- Database and Face Loading ---

DB_NAME = "attendance.db"
IMAGE_DIR = "registered_faces"

def load_known_faces_from_db():
    """Loads all known face encodings and corresponding IDs/names from the database."""
    known_face_encodings = []
    known_face_ids = []
    known_face_names = []

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, face_encoding FROM employees")
        rows = cursor.fetchall()

        for row in rows:
            employee_id, name, encoding_json = row
            # Convert the JSON string back to a numpy array
            encoding = np.array(json.loads(encoding_json))
            
            known_face_encodings.append(encoding)
            known_face_ids.append(employee_id)
            known_face_names.append(name)
            
    except sqlite3.Error as e:
        print(f"Database error while loading faces: {e}")
    finally:
        if conn:
            conn.close()
            
    print(f"Loaded {len(known_face_ids)} known faces from the database.")
    return known_face_encodings, known_face_ids, known_face_names

def register_new_face(frame, face_encoding):
    """Saves a new user's details and face encoding to the database."""
    print("Unknown face detected. Starting registration process...")
    
    # Get user details from console input
    employee_id = input("Enter new Employee ID: ").strip()
    if not employee_id:
        print("Registration cancelled: ID is required.")
        return None, None, None

    name = input("Enter new Employee Name: ").strip()
    if not name:
        print("Registration cancelled: Name is required.")
        return None, None, None
        
    email = input("Enter new Employee Email (optional): ").strip()

    # Save the image
    image_filename = f"{employee_id}_{name}.jpg"
    image_path = os.path.join(IMAGE_DIR, image_filename)
    
    # We use the original frame for saving to get better quality
    cv2.imwrite(image_path, frame)
    print(f"Saved new face image to: {image_path}")

    # Convert numpy array to a list for JSON serialization
    encoding_list = face_encoding.tolist()
    encoding_json = json.dumps(encoding_list)

    # Save to database
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (id, name, email, face_encoding, image_path) VALUES (?, ?, ?, ?, ?)",
            (employee_id, name, email, encoding_json, image_path)
        )
        conn.commit()
        print(f"Successfully registered new employee: {name} (ID: {employee_id})")
        return face_encoding, employee_id, name
        
    except sqlite3.IntegrityError:
        print(f"Error: Employee ID '{employee_id}' already exists.")
        return None, None, None
    except sqlite3.Error as e:
        print(f"Database error during registration: {e}")
        return None, None, None
    finally:
        if conn:
            conn.close()

def mark_attendance(employee_id, name):
    """Marks attendance for the given employee for the current day."""
    today = date.today().isoformat()
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Try to insert a new attendance record
        cursor.execute(
            "INSERT INTO attendance (employee_id, date, status) VALUES (?, ?, ?)",
            (employee_id, today, 'present')
        )
        conn.commit()
        print(f"Attendance MARKED for {name} (ID: {employee_id}) on {today}")
        
    except sqlite3.IntegrityError:
        # This error occurs if the (employee_id, date) pair already exists
        print(f"Attendance ALREADY marked for {name} (ID: {employee_id}) today.")
    except sqlite3.Error as e:
        print(f"Database error while marking attendance: {e}")
    finally:
        if conn:
            conn.close()

# --- Main Application Loop ---

def main():
    # Load known faces from the database
    known_face_encodings, known_face_ids, known_face_names = load_known_faces_from_db()

    # Initialize webcam
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    # Variables for registration logic
    unknown_face_encoding = None
    last_frame_with_unknown = None
    
    print("\nStarting video stream...")
    print("Press 'n' to register a new unknown face when one is detected.")
    print("Press 'q' to quit.")

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Resize frame for faster processing (optional)
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        current_face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Reset unknown face buffer if no faces are detected
        if not face_locations:
            unknown_face_encoding = None
            last_frame_with_unknown = None

        for face_encoding, face_location in zip(current_face_encodings, face_locations):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            employee_id = None

            # Use the first match
            if True in matches:
                first_match_index = matches.index(True)
                employee_id = known_face_ids[first_match_index]
                name = known_face_names[first_match_index]
                
                # If a known face is detected, mark attendance
                mark_attendance(employee_id, name)
                
                # Clear any pending unknown face
                unknown_face_encoding = None
                last_frame_with_unknown = None
            else:
                # If unknown, store the encoding and frame for possible registration
                unknown_face_encoding = face_encoding
                last_frame_with_unknown = frame # Store the full-res frame

            # --- Draw the box and name on the frame ---
            # Scale back up face locations
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Smart Attendance System', frame)

        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF

        # Quit on 'q'
        if key == ord('q'):
            break
        
        # Register on 'n'
        if key == ord('n'):
            if unknown_face_encoding is not None and last_frame_with_unknown is not None:
                # Call the registration function
                new_encoding, new_id, new_name = register_new_face(last_frame_with_unknown, unknown_face_encoding)
                
                # If registration was successful, add to known lists
                if new_id:
                    known_face_encodings.append(new_encoding)
                    known_face_ids.append(new_id)
                    known_face_names.append(new_name)
                
                # Clear the buffer regardless of success
                unknown_face_encoding = None
                last_frame_with_unknown = None
            else:
                print("No new unknown face detected to register. Please look at the camera.")

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    print("Video stream stopped.")

if __name__ == "__main__":
    main()