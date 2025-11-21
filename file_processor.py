# utils/file_processor.py
import pdfplumber
from docx import Document
import pypdf

class FileProcessor:
    @staticmethod
    def extract_text(file_path: str) -> str:
        """Fast text extraction from PDF/DOCX/TXT"""
        try:
            if file_path.endswith('.pdf'):
                return FileProcessor._extract_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return FileProcessor._extract_from_docx(file_path)
            else:
                # Assume text file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            print(f"File processing error: {e}")
            return ""
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF using pdfplumber (primary) and pypdf (fallback)"""
        text = ""
        
        # Try pdfplumber first (better for most PDFs)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages[:4]:  # Only first 4 pages for speed
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Fallback to pypdf
        try:
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages[:4]:  # Only first 4 pages
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pypdf also failed: {e}")
        
        return text
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX files"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return ""