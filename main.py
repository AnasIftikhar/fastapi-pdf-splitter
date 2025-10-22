from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader, PdfWriter
import io
import base64

app = FastAPI(title="PDF Splitter API", version="1.1")

# Input model for PDF in base64
class PDFInput(BaseModel):
    base64_pdf: str

# Existing endpoint: split PDF into pages and return base64
@app.post("/split-base64")
async def split_pdf_base64(input_data: PDFInput):
    try:
        # Decode incoming base64 PDF
        pdf_bytes = base64.b64decode(input_data.base64_pdf)
        reader = PdfReader(io.BytesIO(pdf_bytes))

        pages_base64 = []

        # Split each page and convert back to base64
        for page in reader.pages:
            writer = PdfWriter()
            writer.add_page(page)

            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)

            # Convert to base64
            page_base64 = base64.b64encode(output_buffer.read()).decode("utf-8")
            pages_base64.append(page_base64)

        return {
            "status": "success",
            "total_pages": len(pages_base64),
            "pages_base64": pages_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New lightweight endpoint: health check for keep-alive
@app.get("/health")
async def health_check():
    """
    Simple endpoint to keep the app awake on hosting platforms like Render.
    """
    return {"status": "alive"}
