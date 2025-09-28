# 🏠 Floorplan Dimension Extractor

A sophisticated Python pipeline for automatically extracting dimensions and cabinet codes from architectural floorplan PDFs. This tool converts various dimension formats into standardized measurements and provides structured output with visualization capabilities.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.23.7-green)

## 🚀 Features

- **PDF Text Extraction**: Support for both PyMuPDF and pdfplumber libraries
- **Smart Dimension Parsing**: Handles multiple formats (inches, feet-inches, fractions)
- **Cabinet Code Detection**: Identifies appliance and cabinet codes
- **Visualization**: Draws bounding boxes around detected elements
- **Web Interface**: User-friendly Streamlit dashboard
- **Structured Output**: JSON format with spatial coordinates
- **Batch Processing**: Command-line interface for automation

## 🛠 Tech Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **PyMuPDF/fitz** - High-performance PDF text extraction
- **pdfplumber** - Alternative PDF processing with detailed layout analysis
- **Streamlit** - Web application framework
- **OpenCV** - Image processing and visualization
- **Regex** - Advanced pattern matching

### Supporting Libraries
- **Pillow** - Image manipulation
- **NumPy** - Numerical operations
- **Matplotlib** - Data visualization (for internal analysis)

## 📁 Project Structure
```
floorplan-dimractor/
├── data/
│ ├── input/ # Uploaded PDF files
│ └── output/ # JSON extraction results
├── src/
│ ├── init.py
│ ├── pdf_processor.py # PDF text extraction
│ ├── dimension_parser.py # Dimension parsing logic
│ ├── code_detector.py # Cabinet code detection
│ ├── visualizer.py # Bounding box visualization
│ └── utils.py # Utility functions
├── tests/
│ └── test_extractor.py # Unit tests
├── main.py # Command-line interface
├── streamlit_app.py # Web interface
├── requirements.txt # Python dependencies
└── README.md
```

Advanced Dimension Parsing
Regex Patterns: Comprehensive pattern matching for various formats

Fraction Handling: Converts mixed numbers and fractions to decimals

Unit Conversion: Automatic feet-to-inches conversion

Spatial Analysis: Bounding box coordinates for each detection

Modular Design
Separation of Concerns: Each component handles specific responsibilities

Extensible Architecture: Easy to add new parsers or detectors

Error Handling: Graceful degradation and informative error messages