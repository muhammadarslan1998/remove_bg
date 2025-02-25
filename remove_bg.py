import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from rembg import remove
from PIL import Image
import uvicorn  # Import uvicorn explicitly

# Initialize FastAPI
app = FastAPI()

# Define directories
UPLOAD_DIR = "images"
OUTPUT_DIR = "output_images"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/remove-bg/")
async def remove_background(file: UploadFile = File(...)):
    input_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(OUTPUT_DIR, f"{os.path.splitext(file.filename)[0]}.png")

    # Save uploaded file
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Open image and remove background
        with Image.open(input_path) as img:
            output_image = remove(img)
            output_image.save(output_path)

        # Delete the uploaded image after processing
        os.remove(input_path)

        return FileResponse(output_path, media_type="image/png", filename=f"{os.path.splitext(file.filename)[0]}_no_bg.png")
    
    except Exception as e:
        # Delete the uploaded file if an error occurs
        if os.path.exists(input_path):
            os.remove(input_path)
        return {"error": str(e)}

# Ensure the app runs on the correct port
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render automatically assigns a port
    uvicorn.run(app, host="0.0.0.0", port=port,)