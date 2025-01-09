import mariadb
import schedule
import time
from dotenv import load_dotenv
import os

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
        print(f"Database connection error: {e}")
        return None

# Notify users of upcoming reservations
def notify_upcoming_reservations():
    print("Checking for upcoming reservations...")
    conn = connect()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Fetch reservations happening within the next 24 hours
        cursor.execute("""
            SELECT r.id, m.account_id, m.matched_account_id
            FROM reservations r
            INNER JOIN matches m ON r.match_id = m.id
            WHERE r.created_at >= NOW() - INTERVAL 1 DAY
        """)
        reservations = cursor.fetchall()

        for reservation in reservations:
            reservation_id, account_id, matched_account_id = reservation

            # Placeholder notification logic (e.g., email or SMS)
            print(f"Notification: Reservation {reservation_id} is happening soon for accounts {account_id} and {matched_account_id}.")

    except mariadb.Error as e:
        print(f"Error fetching reservations: {e}")
    finally:
        conn.close()

# Notify users about pending matches
def notify_pending_matches():
    print("Checking for pending matches...")
    conn = connect()
    if not conn:
        return

    cursor = conn.cursor()
    try:
        # Fetch matches that are pending for more than 3 days
        cursor.execute("""
            SELECT id, account_id, matched_account_id
            FROM matches
            WHERE created_at <= NOW() - INTERVAL 3 DAY
        """)
        matches = cursor.fetchall()

        for match in matches:
            match_id, account_id, matched_account_id = match

            # Placeholder notification logic (e.g., email or SMS)
            print(f"Notification: Match {match_id} pending for action between accounts {account_id} and {matched_account_id}.")

    except mariadb.Error as e:
        print(f"Error fetching matches: {e}")
    finally:
        conn.close()

# Schedule periodic checks
schedule.every(1).minute.do(notify_upcoming_reservations)
schedule.every(1).minute.do(notify_pending_matches)

if __name__ == "__main__":
    print("Starting notification service...")
    while True:
        schedule.run_pending()
        time.sleep(1)
