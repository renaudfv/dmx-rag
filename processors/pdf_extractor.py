import os
import re
import fitz  # PyMuPDF

class PDFProcessor:
    @staticmethod
    def extract_text(pdf_path):
        """
        Extract text from PDF, handling multi-page documents
        """
        try:
            document = fitz.open(pdf_path)
            full_text = ""
            
            for page in document:
                text = page.get_text()
                # Basic text cleaning
                text = re.sub(r'\s+', ' ', text).strip()
                full_text += text + "\n"
            
            document.close()
            return full_text
        
        except Exception as e:
            print(f"Error processing {pdf_path}: {e}")
            return ""
    
    @staticmethod
    def clean_text(text):
        """
        Advanced text cleaning
        """
        # Remove page numbers, website references
        text = re.sub(r'(Page \d+|www\.[^\s]+)', '', text)
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @classmethod
    def process_pdf_directory(cls, directory):
        """
        Process all PDFs in a directory
        """
        processed_docs = []
        
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                filepath = os.path.join(directory, filename)
                raw_text = cls.extract_text(filepath)
                cleaned_text = cls.clean_text(raw_text)
                processed_docs.append({
                    'filename': filename,
                    'text': cleaned_text
                })
        
        return processed_docs