def create_reservation(user1, user2, date, time, location, db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("""
            INSERT INTO reservations (user1, user2, date, time, location)
            VALUES (?, ?, ?, ?, ?)
        """, (user1, user2, date, time, location))
        db_connection.commit()
        return {"code": 1, "message": "Reservation created successfully"}
    except Exception as e:
        return {"code": f"0_con_{str(e)}", "message": "Error creating reservation"}

def cancel_reservation(reservation_id, reason, db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
        db_connection.commit()
        return {"code": 1, "message": f"Reservation canceled: {reason}"}
    except Exception as e:
        return {"code": f"0_con_{str(e)}", "message": "Error canceling reservation"}
def notify_user(user, message):
    print(f"Notification sent to {user}: {message}")
