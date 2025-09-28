import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io
from typing import List, Dict

class PDFVisualizer:
    def __init__(self):
        self.colors = {
            'dimension': (1, 0, 0),  # Red for dimensions
            'code': (0, 0, 1),       # Blue for codes
            'text': (0, 1, 0)        # Green for labels
        }
    
    def draw_bounding_boxes(self, pdf_path: str, extraction_data: Dict, output_path: str):
        """Draw bounding boxes on PDF pages"""
        doc = fitz.open(pdf_path)
        
        for page_data in extraction_data["pages"]:
            page_num = page_data["page"] - 1
            page = doc[page_num]
            
            # Draw dimension bounding boxes
            for dim in page_data["dimensions"]:
                bbox = dim["bbox"]
                rect = fitz.Rect(bbox[0], bbox[1], bbox[2], bbox[3])
                
                # Draw rectangle
                page.draw_rect(rect, color=self.colors['dimension'], width=2)
                
                # Add label
                label = f"{dim['raw']} → {dim['inches']}in"
                page.insert_text(
                    (bbox[0], bbox[1] - 5),  # Position above bbox
                    label,
                    color=self.colors['text'],
                    fontsize=8
                )
        
        doc.save(output_path)
        doc.close()
    
    def create_visualization_report(self, pdf_path: str, extraction_data: Dict) -> Image.Image:
        """Create a visualization image for Streamlit"""
        doc = fitz.open(pdf_path)
        page = doc[0]  # First page for demo
        
        # Convert PDF page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution
        img_data = pix.tobytes("ppm")
        
        # Convert to OpenCV format
        img = cv2.imdecode(np.frombuffer(img_data, np.uint8), 1)
        
        # Draw bounding boxes on image
        page_data = next((p for p in extraction_data["pages"] if p["page"] == 1), None)
        if page_data:
            for dim in page_data["dimensions"]:
                bbox = [int(coord * 2) for coord in dim["bbox"]]  # Scale for higher res
                cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 0, 255), 2)
                
                # Add label
                label = f"{dim['raw']} → {dim['inches']}in"
                cv2.putText(img, label, (bbox[0], bbox[1] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # Convert back to PIL Image for Streamlit
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        
        doc.close()
        return pil_img