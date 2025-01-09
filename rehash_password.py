import mariadb
import bcrypt

# Database credentials
db_config = {
    "user": "testuser",
    "password": "Test@1234",
    "host": "127.0.0.1",
    "database": "ding_db"
}

# Function to rehash the password for a specific user
def rehash_password(username, plaintext_password):
    try:
        # Connect to the database
        conn = mariadb.connect(**db_config)
        cursor = conn.cursor()

        # Hash the plaintext password
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Update the database with the hashed password
        cursor.execute("UPDATE accounts SET password = ? WHERE username = ?", (hashed_password, username))
        conn.commit()
        print(f"Password for {username} has been rehashed successfully!")

    except mariadb.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# Call the function for the user you need to fix
rehash_password("testuser", "Test@1234")
