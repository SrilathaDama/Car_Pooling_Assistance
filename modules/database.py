import mariadb
import os
import re
import bcrypt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to connect to the database
def connect():
    try:
        conn = mariadb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )
        return conn
    except mariadb.Error as e:
        return {"code": f"0_db_{str(e)}", "message": "Database error"}

# Helper function to validate username format
def validate_username(username):
    return re.match(r'^[A-Za-z0-9_-]+$', username) is not None

# Helper function to validate password format
def validate_password(password):
    return re.match(r'^[A-Za-z0-9!@#$%^&*]+$', password) is not None

# Main function to handle requests
def handle_request(request_type, params):
    conn = connect()
    if isinstance(conn, dict):  # Check for connection errors
        return conn
    cursor = conn.cursor()
    try:
        # Handle account registration
        if request_type == "database_acc_register":
            username = params.get("username")
            password = params.get("password")

            # Validate input
            if not validate_username(username):
                return {"code": "0_val_0001", "message": "Invalid username format"}
            if not validate_password(password):
                return {"code": "0_val_0002", "message": "Invalid password format"}

            # Check if the username already exists
            cursor.execute("SELECT id FROM accounts WHERE username = ?", (username,))
            if cursor.fetchone():
                return {"code": "0_db_0001", "message": "Username already exists"}

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Insert the new user into the database
            cursor.execute("""
                INSERT INTO accounts (username, password, date_created)
                VALUES (?, ?, NOW())
            """, (username, hashed_password))
            conn.commit()
            return {"code": 1, "message": "User registered successfully"}

        # Handle account login
        elif request_type == "database_acc_login":
            username = params.get("username")
            password = params.get("password")

            # Debugging: Print login attempt
            print(f"Login attempt for username: {username}")

            # Retrieve the hashed password from the database
            cursor.execute("SELECT id, password FROM accounts WHERE username = ?", (username,))
            result = cursor.fetchone()

            # Debugging: Print database result
            print(f"Database query result: {result}")

            if result:
                user_id, hashed_password = result

                # Check if the password is properly hashed
                if len(hashed_password) < 60:
                    return {"code": "0_db_0003", "message": "Invalid password format in database"}

                # Verify the password
                password_match = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

                # Debugging: Print password check result
                print(f"Password check result: {password_match}")

                if password_match:
                    return {"code": 1, "message": "Login successful", "user_id": user_id}
            return {"code": "0_db_0002", "message": "Invalid username or password"}

        # Handle match rejection
        elif request_type == "match_reject":
            match_id = params.get("match_id")
            if not match_id:
                return {"code": "0_val_0003", "message": "Missing match ID"}
            
            # Remove the match from the database
            cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
            conn.commit()
            return {"code": 1, "message": "Match rejected successfully"}

        # Handle reservation creation
        elif request_type == "reservation_create":
            match_id = params.get("match_id")
            if not match_id:
                return {"code": "0_val_0004", "message": "Missing match ID"}

            # Create a reservation from the match
            cursor.execute("""
                INSERT INTO reservations (match_id, created_at)
                SELECT id, NOW() FROM matches WHERE id = ?
            """, (match_id,))
            conn.commit()

            # Optionally remove the match from the matches table
            cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
            conn.commit()

            return {"code": 1, "message": "Reservation created successfully"}

        return {"code": "0_db_0003", "message": "Invalid request type"}

    except Exception as e:
        # Handle unexpected errors
        print(f"Internal error occurred: {e}")
        return {"code": "0_con_0001", "message": "An unexpected error occurred"}

    finally:
        cursor.close()
        conn.close()
def save_image_metadata(user_id, file_path):
    query = """
        INSERT INTO images (user_id, file_path, upload_date)
        VALUES (%s, %s, NOW())
    """
    execute_query(query, (user_id, file_path))
