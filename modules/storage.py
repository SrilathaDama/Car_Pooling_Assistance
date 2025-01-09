# import os
# from PIL import Image

# def upload_profile_picture(file_path, user_id):
#     try:
#         # Validate file size (<2MB)
#         file_size = os.path.getsize(file_path)
#         if file_size > 2 * 1024 * 1024:  # 2 MB
#             return {"code": "0_con_0001", "message": "File size exceeds 2MB"}

#         # Convert to JPG if not already JPG
#         with Image.open(file_path) as img:
#             output_path = f"storage_pfp/{user_id}.jpg"
#             img.convert("RGB").save(output_path, "JPEG", quality=85)

#         return {"code": 1, "message": f"Profile picture uploaded to {output_path}"}
#     except Exception as e:
#         return {"code": f"0_con_{str(e)}", "message": "Error uploading profile picture"}
import os
from PIL import Image
import traceback

# Ensure the storage directory exists
STORAGE_DIR = "storage_pfp"
os.makedirs(STORAGE_DIR, exist_ok=True)

def upload_profile_picture(file_path):
    print(f"File saved to: {file_path}")

    try:
        # Validate file size (limit: 2MB)
        if os.path.getsize(file_path) > 2 * 1024 * 1024:
            return {"code": "0_val_0005", "message": "File size exceeds 2MB"}

        # Log file path
        print("File path received:", file_path)

        # Convert the file to JPEG
        img = Image.open(file_path)
        img = img.convert("RGB")
        output_path = os.path.join(STORAGE_DIR, os.path.basename(file_path))

        # Log output path
        print("Output path will be:", output_path)

        img.save(output_path, "JPEG", quality=85)

        return {"code": 1, "message": "File uploaded successfully", "path": output_path}
    except Exception as e:
        # Log detailed error
        print("Error details:", traceback.format_exc())
        return {"code": "0_con_0006", "message": "An unexpected error occurred"}
