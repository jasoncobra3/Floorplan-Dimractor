import pdfplumber
import fitz  # PyMuPDF
from typing import Dict, List, Tuple
from .dimension_parser import DimensionParser
from .code_detector import CodeDetector

class PDFProcessor:
    def __init__(self):
        self.dimension_parser = DimensionParser()
        self.code_detector = CodeDetector()
    
    def extract_with_pdfplumber(self, pdf_path: str) -> Dict:
        """Extract text and metadata using pdfplumber"""
        results = {"pages": []}
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_data = self.process_page_plumber(page, page_num)
                    results["pages"].append(page_data)
            
            return results
        except Exception as e:
            print(f"Error processing PDF with pdfplumber: {e}")
            return results
    
    def extract_with_pymupdf(self, pdf_path: str) -> Dict:
        """Extract text and metadata using PyMuPDF"""
        results = {"pages": []}
        
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_data = self.process_page_pymupdf(page, page_num + 1)
                results["pages"].append(page_data)
            
            doc.close()
            return results
        except Exception as e:
            print(f"Error processing PDF with PyMuPDF: {e}")
            return results
    
    def process_page_plumber(self, page, page_num: int) -> Dict:
        """Process a single page using pdfplumber"""
        dimensions = []
        all_codes = []
        
        # Extract text with bounding boxes
        words = page.extract_words()
        
        for word in words:
            text = word['text']
            bbox = [word['x0'], word['top'], word['x1'], word['bottom']]
            
            # Extract dimensions
            dims = self.dimension_parser.extract_dimensions_from_text(text, bbox)
            dimensions.extend(dims)
            
            # Extract codes
            codes = self.code_detector.detect_codes(text)
            all_codes.extend(codes)
        
        return {
            "page": page_num,
            "dimensions": dimensions,
            "codes": list(set(all_codes))  # Remove duplicates
        }
    
    def process_page_pymupdf(self, page, page_num: int) -> Dict:
        """Process a single page using PyMuPDF"""
        dimensions = []
        all_codes = []
        
        # Extract text blocks with bounding boxes
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        bbox = span["bbox"]  # [x0, y0, x1, y1]
                        
                        # Extract dimensions
                        dims = self.dimension_parser.extract_dimensions_from_text(text, bbox)
                        dimensions.extend(dims)
                        
                        # Extract codes
                        codes = self.code_detector.detect_codes(text)
                        all_codes.extend(codes)
        
        return {
            "page": page_num,
            "dimensions": dimensions,
            "codes": list(set(all_codes))
        }