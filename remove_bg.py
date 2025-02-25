import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import io

# Create FastAPI instance
app = FastAPI()

# Ensure the uploads directory exists
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Background Remover API is running!"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Open image and remove background
        with Image.open(file_path) as input_image:
            output_image = remove(input_image)

            # Convert image to bytes
            img_byte_arr = io.BytesIO()
            output_image.save(img_byte_arr, format="PNG")
            img_byte_arr.seek(0)

        # Delete the original uploaded file after processing
        os.remove(file_path)

        # Return the processed image
        return FileResponse(img_byte_arr, media_type="image/png", filename="output.png")

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render assigns PORT dynamically
    print(f"🚀 Running on port {port}")  # Debugging log to check port
    uvicorn.run("remove_bg:app", host="0.0.0.0", port=port)
