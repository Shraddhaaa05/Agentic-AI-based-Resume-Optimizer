# utils/file_processor.py
import pdfplumber
from docx import Document

class FileProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extract text from PDF, DOCX, or TXT files."""
        try:
            if file_path.endswith('.pdf'):
                return FileProcessor._extract_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return FileProcessor._extract_from_docx(file_path)
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            print(f"File processing error: {e}")
            return ""

    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF using pdfplumber with pypdf fallback."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages[:4]:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}")

        try:
            import pypdf
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages[:4]:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pypdf also failed: {e}")

        return text

    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX files."""
        try:
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return ""