from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import pytesseract
from PIL import Image
from io import BytesIO

app = FastAPI()

class PDFUpload(BaseModel):
    file: UploadFile

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        text = pytesseract.image_to_string(img)
        
        if text.strip():
            return {"message": "PDF uploaded successfully", "content": text}
        else:
            raise HTTPException(status_code=400, detail="No readable text detected in the PDF")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
