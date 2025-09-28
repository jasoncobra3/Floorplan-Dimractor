import unittest
from src.dimension_parser import DimensionParser
from src.code_detector import CodeDetector

class TestDimensionExtractor(unittest.TestCase):
    def setUp(self):
        self.parser = DimensionParser()
        self.detector = CodeDetector()
    
    def test_dimension_parsing(self):
        test_cases = [
            ('25"', 25.0),
            ('34 (1/2)"', 34.5),
            ('2\' 6"', 30.0),
            ('3\' 4.5"', 40.5),
            ('25 3/4"', 25.75)
        ]
        
        for text, expected in test_cases:
            with self.subTest(text=text):
                result = self.parser.parse_dimension(text)
                self.assertAlmostEqual(result, expected, places=2)
    
    def test_code_detection(self):
        text = "The kitchen has DB24, SB42FH, and MW30 cabinets"
        codes = self.detector.detect_codes(text)
        expected = ['DB24', 'SB42FH', 'MW30']
        self.assertEqual(set(codes), set(expected))

if __name__ == '__main__':
    unittest.main()