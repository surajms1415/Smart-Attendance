# manual_register.py
import face_recognition
import sqlite3
import json
import os
import shutil  # Used for copying files

DB_NAME = "attendance.db"
IMAGE_DIR = "registered_faces"

def register_from_file():
    """
    Registers a new employee from an existing image file.
    """
    print("--- Manual Employee Registration Utility ---")
    
    # 1. Get the path to the image
    image_path = input("Enter the full path to the employee's image file: ").strip()
    
    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found at '{image_path}'")
        return

    # 2. Load and encode the face from the image
    try:
        # Load the image
        image = face_recognition.load_image_file(image_path)
        
        # Find all face encodings in the image
        # We assume one clear face per registration photo
        face_encodings = face_recognition.face_encodings(image)
        
        if not face_encodings:
            print("Error: No face could be detected in the provided image.")
            print("Please use a clear, forward-facing photo.")
            return
        elif len(face_encodings) > 1:
            print(f"Warning: {len(face_encodings)} faces found in the image. Registering the first one.")
            
        # Get the first (and hopefully only) face encoding
        face_encoding = face_encodings[0]

    except Exception as e:
        print(f"Error loading or processing the image: {e}")
        return
            
    # 3. Get the employee's details
    employee_id = input("Enter new Employee ID: ").strip()
    if not employee_id:
        print("Registration cancelled: ID is required.")
        return

    name = input("Enter new Employee Name: ").strip()
    if not name:
        print("Registration cancelled: Name is required.")
        return
        
    email = input("Enter new Employee Email (optional): ").strip()

    # 4. Copy the original image to the registered_faces directory
    # Get the original file extension (e.g., .jpg, .png)
    _, file_extension = os.path.splitext(image_path)
    new_image_filename = f"{employee_id}_{name}{file_extension}"
    new_image_path = os.path.join(IMAGE_DIR, new_image_filename)
    
    try:
        shutil.copyfile(image_path, new_image_path)
        print(f"Successfully copied image to '{new_image_path}'")
    except Exception as e:
        print(f"Warning: Could not copy image file. {e}")
        # We can still proceed to save the encoding
        new_image_path = None # Set path to None if copy failed

    # 5. Save all details to the database
    # Convert numpy array to a list for JSON serialization
    encoding_list = face_encoding.tolist()
    encoding_json = json.dumps(encoding_list)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (id, name, email, face_encoding, image_path) VALUES (?, ?, ?, ?, ?)",
            (employee_id, name, email, encoding_json, new_image_path)
        )
        conn.commit()
        print(f"\nSuccessfully registered new employee in database:")
        print(f"  ID:    {employee_id}")
        print(f"  Name:  {name}")
        
    except sqlite3.IntegrityError:
        print(f"\nError: An employee with ID '{employee_id}' already exists in the database.")
    except sqlite3.Error as e:
        print(f"\nDatabase error during registration: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Check if the database and folder exist before we start
    if not os.path.exists(DB_NAME) or not os.path.exists(IMAGE_DIR):
        print(f"Error: Cannot find '{DB_NAME}' or the '{IMAGE_DIR}' folder.")
        print("Please run 'database_setup.py' first to create them.")
    else:
        register_from_file()