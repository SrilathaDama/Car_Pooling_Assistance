from settings import SECURITY_KEY

def validate_security_key(sk):
    if sk != SECURITY_KEY:
        return {"code": "0_sec_9999", "message": "Invalid security key"}
    return {"code": 1}
