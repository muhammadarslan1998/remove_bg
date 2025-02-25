from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import shutil
import uvicorn
from rembg import remove
from PIL import Image
from io import BytesIO

app = FastAPI()

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)


@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Open and process image
        with open(input_path, "rb") as inp:
            img = remove(inp.read())

        # Save output image
        output_path = os.path.join(PROCESSED_FOLDER, f"no-bg-{file.filename}")
        with open(output_path, "wb") as out:
            out.write(img)

        # Delete uploaded file after processing
        os.remove(input_path)

        # Return processed image as a file response
        return FileResponse(output_path, media_type="image/png", filename=f"no-bg-{file.filename}")

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Running on port {port}")  
    uvicorn.run("remove_bg:app", host="0.0.0.0", port=port)
