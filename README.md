# 🏠 Floorplan Dimension Extractor

A sophisticated Python pipeline for automatically extracting dimensions and cabinet codes from architectural floorplan PDFs. This tool converts various dimension formats into standardized measurements and provides structured output with visualization capabilities.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.23.7-green)

---

## 🚀 Features

- **PDF Text Extraction**: Support for both PyMuPDF and pdfplumber libraries
- **Smart Dimension Parsing**: Handles multiple formats (inches, feet-inches, fractions)
- **Cabinet Code Detection**: Identifies appliance and cabinet codes
- **Visualization**: Draws bounding boxes around detected elements
- **Web Interface**: User-friendly Streamlit dashboard
- **Structured Output**: JSON format with spatial coordinates
- **Batch Processing**: Command-line interface for automation

---


## 🛠 Tech Stack

### Core Technologies
- **Python 3.8+** - Primary programming language
- **PyMuPDF/fitz** - High-performance PDF text extraction
- **pdfplumber** - Alternative PDF processing with detailed layout analysis
- **Streamlit** - Web application framework
- **OpenCV** - Image processing and visualization
- **Regex** - Advanced pattern matching

---


### Supporting Libraries
- **Pillow** - Image manipulation
- **NumPy** - Numerical operations
- **Matplotlib** - Data visualization (for internal analysis)

---

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
├── app.py # Web interface
├── requirements.txt # Python dependencies
└── README.md
```
---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jasoncobra3/Floorplan-Dimractor.git
   cd Floorplan-Dimractor


2. **Create Virtual Environment**
   ```bash
    python -m venv venv
   
3. **Activate the Virtual Environment**
   ```bash
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    venv/bin/activate

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt


---


##  🚀Run the App
   **Run the Script in Terminal**
   ```bash
     streamlit run app.py
   ```


---


## Advanced Dimension Parsing
- Regex Patterns: Comprehensive pattern matching for various formats
- Fraction Handling: Converts mixed numbers and fractions to decimals
- Unit Conversion: Automatic feet-to-inches conversion
- Spatial Analysis: Bounding box coordinates for each detection

## Modular Design
- Separation of Concerns: Each component handles specific responsibilities
- Extensible Architecture: Easy to add new parsers or detectors
- Error Handling: Graceful degradation and informative error messages

  
---

## 📸 Screenshots

| Scrape Chapter | AI Rewrite | Review & Edit |
|----------------|------------|---------------|
| ![](project_screenshots/scraper_ui.png) | ![](project_screenshots/spin_ai.png) | ![](project_screenshots/review_ui.png) |

| View Versions | Semantic Search |
|---------------|------------------|
| ![](project_screenshots/version_table.png) | ![](project_screenshots/semantic_search.png) |



---


## 🎯 Challenges & Solutions

1. **Challenge 1: PDF Text Extraction Variability**<br>
   **Problem: Different PDF generators create varying text layouts and encoding.**

    **Solution:**
   -  Implemented dual-library approach (PyMuPDF + pdfplumber)
   -  Combined text extraction with spatial analysis
   -  Added fallback mechanisms for different PDF types


2. **Challenge 2: Dimension Format Diversity**<br>
   **Problem: Architectural drawings use multiple dimension formats:**
   - 25" (Simple inches)
   - 2' 6" (Feet and inches)
   - 34 (1/2)" (Fractions)
   - 25 3/4" (Mixed numbers)

   **Solution:**
   - Created comprehensive regex patterns
   - Implemented format-specific parsers
   - Added validation and error recovery

3.  **Challenge 3: Bounding Box Accuracy**<br>
   **Problem: Text bounding boxes don't always match visual elements.**

    **Solution:**
    - Combined multiple text extraction methods
    - Implemented coordinate normalization
    - Added visualization for manual verification

4.  **Challenge 4: Performance Optimization**<br>
   **Problem: Large PDF files with complex layouts can be slow to process.**

    **Solution:**
    - Implemented efficient text filtering
    - Added progress tracking
    - Provided multiple processing options
  
  ---

## 📊 Approach Comparison: PyMuPDF vs pdfplumber

| Feature | PyMuPDF | pdfplumber |
|---------|---------|------------|
| Speed | Very Fast | Moderate |
| Text Accuracy | Good | Excellent |
| Layout Analysis | Basic | Excellent |
| Bounding Box Precision | Good | Excellent |
| Ease of Use | Very Easy | Easy |
| Memory Usage | Very Efficient | Moderate |
| Installation | Very Easy | Easy |
| Documentation | Good | Excellent |
| Complex Layout Handling | Limited | Excellent |
| Text Extraction Quality | Good | Excellent |
| Table Extraction | Basic | Excellent |
| Image Extraction | Excellent | Good |
| Performance with Large Files | Excellent | Good |
| Coordinate Accuracy | Good | Excellent |
| Font Information | Basic | Detailed |
| Active Maintenance | Yes | Yes |

**Summary**
- PyMuPDF (fitz) excels in speed and memory efficiency, making it ideal for processing large numbers of PDFs quickly. It's straightforward to use and handles basic text extraction well.
- pdfplumber provides superior layout analysis and text extraction accuracy, especially for complex documents. It offers more detailed information about text positioning and structure but at the cost of performance.

**Recommendation**
- Choose PyMuPDF for: High-volume processing, simple documents, when speed is critical
- Choose pdfplumber for: Complex layouts, accurate spatial data, detailed text analysis

---

<div align="center">
If you find this project useful, please give it a ⭐!
</div> 
