from fastapi import FastAPI
from pydantic import BaseModel
import base64, io
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

class PDFInput(BaseModel):
    file: str

@app.get("/")
def home():
    return {"message": "FastAPI PDF Splitter is running successfully!"}

@app.post("/split-base64")
def split_pdf(input_data: PDFInput):
    pdf_bytes = base64.b64decode(input_data.file)
    pdf = PdfReader(io.BytesIO(pdf_bytes))

    pages_base64 = []

    for i, page in enumerate(pdf.pages, start=1):
        writer = PdfWriter()
        writer.add_page(page)
        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)
        b64_page = base64.b64encode(buffer.read()).decode('utf-8')
        pages_base64.append(b64_page)

    return {
        "status": "success",
        "total_pages": len(pages_base64),
        "pages_base64": pages_base64
    }
