import re
import regex
from typing import Dict, List, Tuple, Optional

class DimensionParser:
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for dimension detection"""
        # Pattern for simple inches: 25", 34.5"
        self.simple_inches = re.compile(r'(\d+(?:\.\d+)?)\s*["″]')
        
        # Pattern for feet and inches: 2' 6", 3' 4.5"
        self.feet_inches = re.compile(r'(\d+)\s*[\'′]\s*(\d+(?:\.\d+)?)\s*["″]')
        
        # Pattern for fractions: 34 (1/2)", 25 3/4"
        self.fraction_pattern = re.compile(r'(\d+)\s*[\(]?\s*(\d+)\s*/\s*(\d+)\s*[\)]?\s*["″]')
        
        # Combined pattern for all types
        self.combined_pattern = regex.compile(r'''
            (?:
                # Feet and inches: 2' 6"
                (\d+)\s*[\'′]\s*(\d+(?:\.\d+)?)\s*["″]|
                
                # Fractions: 34 (1/2)"
                (\d+)\s*[\(]?\s*(\d+)\s*/\s*(\d+)\s*[\)]?\s*["″]|
                
                # Simple inches: 25"
                (\d+(?:\.\d+)?)\s*["″]
            )
        ''', regex.VERBOSE)
    
    def parse_fraction(self, whole: str, numerator: str, denominator: str) -> float:
        """Convert fraction to decimal"""
        try:
            whole_num = float(whole) if whole else 0
            fraction = float(numerator) / float(denominator)
            return whole_num + fraction
        except (ValueError, ZeroDivisionError):
            return 0.0
    
    def parse_dimension(self, text: str) -> Optional[float]:
        """Parse dimension text and return inches as float"""
        text = text.strip()
        
        # Try feet and inches pattern
        feet_match = self.feet_inches.search(text)
        if feet_match:
            feet = float(feet_match.group(1))
            inches = float(feet_match.group(2))
            return feet * 12 + inches
        
        # Try fraction pattern
        frac_match = self.fraction_pattern.search(text)
        if frac_match:
            return self.parse_fraction(frac_match.group(1), frac_match.group(2), frac_match.group(3))
        
        # Try simple inches
        inches_match = self.simple_inches.search(text)
        if inches_match:
            return float(inches_match.group(1))
        
        return None
    
    def extract_dimensions_from_text(self, text: str, bbox: List[float]) -> List[Dict]:
        """Extract dimensions from text with bounding boxes"""
        dimensions = []
        
        # Find all matches with their positions in text
        matches = list(self.combined_pattern.finditer(text))
        
        for match in matches:
            raw_text = match.group(0)
            inches_value = self.parse_dimension(raw_text)
            
            if inches_value is not None:
                dimensions.append({
                    "raw": raw_text,
                    "inches": round(inches_value, 2),
                    "bbox": bbox
                })
        
        return dimensions