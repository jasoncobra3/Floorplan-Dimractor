import re
from typing import List

class CodeDetector:
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup patterns for cabinet/appliance codes"""
        # Pattern for codes like DB24, SB42FH, MW30, etc.
        # 2-4 letters followed by 2-4 digits, optionally followed by 1-3 letters
        self.code_pattern = re.compile(r'\b[A-Z]{2,4}\d{2,4}[A-Z]{0,3}\b')
    
    def detect_codes(self, text: str) -> List[str]:
        """Detect cabinet and appliance codes in text"""
        codes = self.code_pattern.findall(text.upper())
        return list(set(codes))  # Remove duplicates