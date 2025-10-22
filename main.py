from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PyPDF2 import PdfReader, PdfWriter
import io
import base64

app = FastAPI()

class PDFInput(BaseModel):
    base64_pdf: str

@app.post("/split-base64")
async def split_pdf_base64(input_data: PDFInput):
    try:
        # Decode incoming base64 PDF
        pdf_bytes = base64.b64decode(input_data.base64_pdf)
        reader = PdfReader(io.BytesIO(pdf_bytes))

        pages_base64 = []

        # Split each page and convert back to base64
        for i in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            output_buffer = io.BytesIO()
            writer.write(output_buffer)
            output_buffer.seek(0)

            # Convert to base64
            page_base64 = base64.b64encode(output_buffer.read()).decode('utf-8')
            pages_base64.append(page_base64)

        return {
            "status": "success",
            "total_pages": len(pages_base64),
            "pages_base64": pages_base64
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
