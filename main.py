from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64, os
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

app = FastAPI()

class PDFInput(BaseModel):
    file: str  # base64 PDF string

@app.post("/split-base64")
def split_pdf_base64(data: PDFInput):
    try:
        # Decode the base64 PDF
        pdf_bytes = base64.b64decode(data.file)
        pdf_reader = PdfReader(BytesIO(pdf_bytes))

        # Create output folder if not exists
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)

        total_pages = len(pdf_reader.pages)
        saved_files = []

        # Split and save each page as a PDF
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(pdf_reader.pages[i])

            file_path = os.path.join(output_folder, f"page_{i+1}.pdf")
            with open(file_path, "wb") as f:
                writer.write(f)

            saved_files.append(file_path)

        return {
            "status": "success",
            "total_pages": total_pages,
            "saved_files": saved_files
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
