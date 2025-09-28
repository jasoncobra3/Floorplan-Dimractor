import re
import json
import os
from typing import List, Dict, Tuple, Optional
from datetime import datetime

def setup_logging():
    """Setup basic logging configuration"""
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)

def ensure_directories():
    """Ensure data directories exist"""
    os.makedirs('data/input', exist_ok=True)
    os.makedirs('data/output', exist_ok=True)

def save_uploaded_file(uploaded_file, filename: str = None) -> str:
    """Save uploaded file to data/input directory"""
    ensure_directories()
    
    if filename is None:
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = uploaded_file.name
        name, ext = os.path.splitext(original_name)
        filename = f"{name}_{timestamp}{ext}"
    
    file_path = os.path.join('data/input', filename)
    
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def generate_output_filename(input_filename: str, suffix: str = "") -> str:
    """Generate output filename based on input filename"""
    ensure_directories()
    
    name, ext = os.path.splitext(os.path.basename(input_filename))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if suffix:
        output_filename = f"{name}_{suffix}_{timestamp}.json"
    else:
        output_filename = f"{name}_{timestamp}.json"
    
    return os.path.join('data/output', output_filename)

def save_json_output(data: Dict, output_path: str) -> bool:
    """Save extracted data to JSON file"""
    try:
        ensure_directories()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving JSON: {e}")
        return False

def get_recent_files(directory: str, extension: str = ".pdf") -> List[Dict]:
    """Get list of recent files in a directory"""
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            filepath = os.path.join(directory, filename)
            stat = os.stat(filepath)
            files.append({
                'name': filename,
                'path': filepath,
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime)
            })
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x['modified'], reverse=True)
    return files

def validate_pdf_path(pdf_path: str) -> bool:
    """Validate if PDF file exists and is accessible"""
    return os.path.exists(pdf_path) and pdf_path.lower().endswith('.pdf')