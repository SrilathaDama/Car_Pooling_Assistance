def match_users(user1, user2, time, location):

    if time and location:
        return {"match": True, "message": f"Users {user1} and {user2} matched at {location} on {time}"}
    return {"match": False, "message": "No match found"}

def remove_match(match_id, database_connection):
    try:
        cursor = database_connection.cursor()
        cursor.execute("DELETE FROM matches WHERE id = ?", (match_id,))
        database_connection.commit()
        return {"code": 1, "message": "Match removed successfully"}
    except Exception as e:
        return {"code": f"0_con_{str(e)}", "message": "Error removing match"}
