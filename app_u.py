# streamlit run app.py

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
import json
import io
from dotenv import load_dotenv
from helper_u import (
    configure_genai, 
    get_gemini_response, 
    extract_pdf_text, 
    extract_docx_text, 
    prepare_prompt,
    update_word_document,
    convert_docx_to_pdf
)

def init_session_state():
    """Initialize session state variables."""
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'docx_content' not in st.session_state:
        st.session_state.docx_content = None
    if 'updated_docx' not in st.session_state:
        st.session_state.updated_docx = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None


def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize session state
    init_session_state()
    
    # Configure Generative AI
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("Please set the GEMINI_API_KEY in your .env file")
        return
        
    try:
        configure_genai(api_key)
    except Exception as e:
        st.error(f"Failed to configure API: {str(e)}")
        return

    # Sidebar
    with st.sidebar:
        st.title("Smart Analyzer 🎯")
        st.subheader("About")
        st.write("""
        Smart Resume Analyzer:
        - Evaluate resume-job description match
        - Identify missing keywords
        - Get personalized improvement suggestions
        - Generate a cold message
        - Update your resume with suggested improvements
        - Download the updated resume as a PDF
        """)

    # Main content
    st.title("📄 Smart Resume Analyzer")
    st.subheader("Optimize Your Resume")
    
    # Input sections with validation
    jd = st.text_area(
        "Job Description",
        placeholder="Paste the job description here...",
        help="Enter the complete job description for accurate analysis"
    )
    
    file_type = st.radio(
        "Select Resume File Type",
        options=["Word Document (.docx)", "PDF Document (.pdf)"],
        horizontal=True
    )
    
    if file_type == "Word Document (.docx)":
        uploaded_file = st.file_uploader(
            "Resume (DOCX)",
            type="docx",
            help="Upload your resume in DOCX format"
        )
        if uploaded_file:
            st.success("Word document uploaded successfully!")
    else:
        uploaded_file = st.file_uploader(
            "Resume (PDF)",
            type="pdf",
            help="Upload your resume in PDF format"
        )
        if uploaded_file:
            st.success("PDF document uploaded successfully!")

    # Process button with loading state
    if st.button("Analyze Resume", disabled=st.session_state.processing):
        if not jd:
            st.warning("Please provide a job description.")
            return
            
        if not uploaded_file:
            st.warning("Please upload a resume.")
            return
            
        st.session_state.processing = True
        
        try:
            with st.spinner("📊 Analyzing your resume..."):
                # Extract text from file
                if file_type == "Word Document (.docx)":
                    docx_content = uploaded_file.read()
                    st.session_state.docx_content = docx_content
                    resume_text = extract_docx_text(io.BytesIO(docx_content))
                else:
                    resume_text = extract_pdf_text(uploaded_file)
                
                # Prepare prompt
                input_prompt = prepare_prompt(resume_text, jd)
                
                # Get and parse response
                response = get_gemini_response(input_prompt)
                
                # Remove control characters from the response
                response = response.replace("\n", " ").replace("\r", "").replace("\t", " ")
                response_json = json.loads(response)
                st.session_state.analysis_result = response_json
                
                # Display results
                st.success("✨ Analysis Complete!")
                
                # Match percentage
                match_percentage = response_json.get("JD Match", "N/A")
                st.metric("Match Score", match_percentage)
                
                # Missing keywords
                st.subheader("Missing Keywords")
                missing_keywords = response_json.get("MissingKeywords", [])
                if missing_keywords:
                    st.write(", ".join(missing_keywords))
                else:
                    st.write("No critical missing keywords found!")
                
                # Profile summary
                st.subheader("Profile Summary")
                st.write(response_json.get("Profile Summary", "No summary available"))
                
                # Suggested improvements
                st.subheader("Suggested Improvements")
                
                improvements = response_json.get("Improvements", {})
                
                if improvements:
                    experience_improvements = improvements.get("Experience", [])
                    if experience_improvements:
                        st.write("**Experience:**")
                        for item in experience_improvements:
                            st.write(f"- {item}")
                    
                    skills_improvements = improvements.get("Skills", [])
                    if skills_improvements:
                        st.write("**Skills:**")
                        for item in skills_improvements:
                            st.write(f"- {item}")
                    
                    projects_improvements = improvements.get("Projects", [])
                    if projects_improvements:
                        st.write("**Projects:**")
                        for item in projects_improvements:
                            st.write(f"- {item}")
                else:
                    st.write("No specific improvements suggested.")
                
                # Cold message
                st.subheader("Cold Message")
                st.write(response_json.get("Cold Message", "No message available"))
                
                # Update Word document (if applicable)
                if file_type == "Word Document (.docx)" and st.session_state.docx_content:
                    apply_changes = st.checkbox("Apply suggested improvements to my resume")
                    
                    if apply_changes:
                        with st.spinner("Updating your resume..."):
                            updated_docx_bytes = update_word_document(
                                io.BytesIO(st.session_state.docx_content),
                                response_json.get("Improvements", {})
                            )
                            st.session_state.updated_docx = updated_docx_bytes
                            
                            # Convert to PDF
                            pdf_bytes = convert_docx_to_pdf(io.BytesIO(updated_docx_bytes))
                            
                            # Provide download buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    "Download Updated Resume (DOCX)",
                                    data=updated_docx_bytes,
                                    file_name="updated_resume.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                )
                            with col2:
                                st.download_button(
                                    "Download Updated Resume (PDF)",
                                    data=pdf_bytes,
                                    file_name="updated_resume.pdf",
                                    mime="application/pdf"
                                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
        finally:
            st.session_state.processing = False

if __name__ == "__main__":
    main()