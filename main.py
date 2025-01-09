from flask import Flask, request, jsonify
import os
from modules.database import handle_request
from modules.security import validate_security_key
from modules.storage import upload_profile_picture
app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_post():
    print("POST request received")  # Debugging output
    data = request.json
    print("Request data:", data)  # Debugging output
    sk_validation = validate_security_key(data.get("sk"))
    if sk_validation["code"] != 1:
        return jsonify(sk_validation)

    request_type = data.get("type")
    params = data.get("params", {})
    print("Request type:", request_type, "Params:", params)  # Debugging output
    response = handle_request(request_type, params)
    return jsonify(response)


# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     response = upload_profile_picture(file.filename)
#     return jsonify(response)
STORAGE_DIR = "storage_pfp"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        file_path = os.path.join(STORAGE_DIR, file.filename)
        file.save(file_path)
        response = upload_profile_picture(file_path)
        return jsonify(response)
    except Exception as e:
        import traceback
        print("Error:", traceback.format_exc())
        return jsonify({"code": "0_con_0006", "message": "An unexpected error occurred"})
@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Test route is working"})
@app.route('/', methods=['GET'])
def home():
    return "<h1>Welcome to the Flask App</h1>", 200

if __name__ == "__main__":
    print("Listening on port 3672...")
    app.run(port=3672, threaded=True, debug=True)
    
