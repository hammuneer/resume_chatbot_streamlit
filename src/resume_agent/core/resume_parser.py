from pypdf import PdfReader
from io import BytesIO
from typing import Optional

def extract_text_from_pdf_bytes(pdf_bytes: Optional[bytes]) -> str:
    """
    Extract plain text from a PDF given bytes.
    Returns empty string if bytes are None or parsing fails.
    """
    if not pdf_bytes:
        return ""
    try:
        reader = PdfReader(BytesIO(pdf_bytes))
        chunks = []
        for page in reader.pages:
            txt = page.extract_text() or ""
            chunks.append(txt)
        return "\n".join(chunks).strip()
    except Exception:
        # If the PDF is encrypted or malformed, just return empty text.
        return ""
