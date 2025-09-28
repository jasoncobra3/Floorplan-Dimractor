import streamlit as st
import tempfile
import os
import json
from datetime import datetime
from src.pdf_processor import PDFProcessor
from src.visualizer import PDFVisualizer
from src.utils import (save_uploaded_file, generate_output_filename, 
                      save_json_output, get_recent_files, ensure_directories)

def main():
    st.set_page_config(
        page_title="Floorplan Dimension Extractor",
        page_icon="📐",
        layout="wide"
    )
    
    st.title("📐 Floorplan Dimension Extractor")
    st.markdown("Upload a floorplan PDF to extract dimensions and cabinet codes")
    
    # Ensure directories exist
    ensure_directories()
    
    # Sidebar for recent files
    st.sidebar.title("📁 Recent Files")
    
    # Show recent input files
    recent_inputs = get_recent_files('data/input', '.pdf')
    st.sidebar.subheader("Recent Uploads")
    if recent_inputs:
        for file_info in recent_inputs[:5]:  # Show last 5
            st.sidebar.write(f"📄 {file_info['name']}")
            st.sidebar.caption(f"Uploaded: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
    else:
        st.sidebar.info("No recent uploads")
    
    # Show recent output files
    recent_outputs = get_recent_files('data/output', '.json')
    st.sidebar.subheader("Recent Extractions")
    if recent_outputs:
        for file_info in recent_outputs[:5]:
            st.sidebar.write(f"📊 {file_info['name']}")
            st.sidebar.caption(f"Processed: {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
    else:
        st.sidebar.info("No recent extractions")
    
    # File upload section
    st.subheader("📤 Upload Floorplan PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="file_uploader")
    
    if uploaded_file is not None:
        # Display file info
        col1, col2, col3 = st.columns(3)
        col1.metric("File Name", uploaded_file.name)
        col2.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
        col3.metric("Upload Time", datetime.now().strftime("%H:%M:%S"))
        
        # Save uploaded file to data/input
        with st.spinner("Saving uploaded file..."):
            saved_path = save_uploaded_file(uploaded_file)
            st.success(f"File saved to: `{saved_path}`")
        
        # Processing options
        st.subheader("⚙️ Processing Options")
        col1, col2 = st.columns(2)
        
        with col1:
            processing_method = st.radio(
                "Processing Method",
                ["PyMuPDF", "pdfplumber"],
                help="PyMuPDF is generally faster, pdfplumber provides more detailed text extraction"
            )
            
            output_filename = st.text_input(
                "Output File Name",
                value=f"{os.path.splitext(uploaded_file.name)[0]}_extracted",
                help="Name for the output JSON file (without extension)"
            )
        
        with col2:
            generate_viz = st.checkbox("Generate Visualization", value=True)
            save_raw_data = st.checkbox("Save Raw Extraction Data", value=True)
        
        # Process PDF
        if st.button("🚀 Extract Dimensions", type="primary", use_container_width=True):
            with st.spinner("Processing PDF..."):
                try:
                    # Generate output path
                    output_path = generate_output_filename(saved_path, "extracted")
                    
                    # Process PDF
                    processor = PDFProcessor()
                    
                    if processing_method == "pdfplumber":
                        results = processor.extract_with_pdfplumber(saved_path)
                    else:
                        results = processor.extract_with_pymupdf(saved_path)
                    
                    # Add metadata
                    results["metadata"] = {
                        "processed_at": datetime.now().isoformat(),
                        "original_filename": uploaded_file.name,
                        "saved_path": saved_path,
                        "processing_method": processing_method,
                        "total_pages": len(results["pages"])
                    }
                    
                    # Save results
                    if save_json_output(results, output_path):
                        st.success(f"Results saved to: `{output_path}`")
                    else:
                        st.error("Failed to save results")
                    
                    # Display results
                    st.success("✅ PDF processed successfully!")
                    
                    # Summary statistics
                    total_pages = len(results["pages"])
                    total_dimensions = sum(len(page["dimensions"]) for page in results["pages"])
                    total_codes = sum(len(page["codes"]) for page in results["pages"])
                    
                    # Display summary
                    st.subheader("📊 Extraction Summary")
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Pages", total_pages)
                    col2.metric("Dimensions Found", total_dimensions)
                    col3.metric("Codes Found", total_codes)
                    col4.metric("Output File", os.path.basename(output_path))
                    
                    # Show visualization
                    if generate_viz and total_pages > 0 and total_dimensions > 0:
                        st.subheader("🎨 Visualization")
                        visualizer = PDFVisualizer()
                        viz_image = visualizer.create_visualization_report(saved_path, results)
                        st.image(viz_image, caption="Extracted Dimensions Visualization", width='stretch')
                        
                        # Save visualization
                        viz_output_path = output_path.replace('.json', '_visualization.pdf')
                        visualizer.draw_bounding_boxes(saved_path, results, viz_output_path)
                        st.info(f"Visualization saved to: `{viz_output_path}`")
                    
                    # Show extracted data in expandable sections
                    st.subheader("📋 Extracted Data")
                    
                    for page_data in results["pages"]:
                        with st.expander(f"Page {page_data['page']} - {len(page_data['dimensions'])} dimensions, {len(page_data['codes'])} codes"):
                            if page_data["dimensions"]:
                                st.write("**📏 Dimensions:**")
                                dim_col1, dim_col2 = st.columns(2)
                                
                                for i, dim in enumerate(page_data["dimensions"]):
                                    col = dim_col1 if i % 2 == 0 else dim_col2
                                    with col:
                                        st.code(f"{dim['raw']} → {dim['inches']} inches")
                            
                            if page_data["codes"]:
                                st.write("**🔤 Cabinet Codes:**")
                                code_cols = st.columns(4)
                                for i, code in enumerate(page_data["codes"]):
                                    col_index = i % 4
                                    with code_cols[col_index]:
                                        st.info(code)
                    
                    # Download results
                    st.subheader("💾 Download Results")
                    json_str = json.dumps(results, indent=2)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="📥 Download JSON Results",
                            data=json_str,
                            file_name=os.path.basename(output_path),
                            mime="application/json",
                            use_container_width=True
                        )
                    
                    with col2:
                        # Provide link to output directory
                        st.info(f"📁 Output directory: `data/output/`")
                        
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")
                    st.exception(e)
    
    else:
        # Show when no file is uploaded
        st.info("👆 Please upload a PDF file to get started")
        
        # Example output format
        with st.expander("📋 Expected Output Format"):
            st.json({
                "metadata": {
                    "processed_at": "2024-01-15T10:30:00",
                    "original_filename": "sample_floorplan.pdf",
                    "processing_method": "PyMuPDF",
                    "total_pages": 1
                },
                "pages": [
                    {
                        "page": 1,
                        "dimensions": [
                            {"raw": "34 (1/2)", "inches": 34.5, "bbox": [100, 200, 150, 220]}
                        ],
                        "codes": ["DB24", "SB42FH"]
                    }
                ]
            })
        
       

if __name__ == "__main__":
    main()