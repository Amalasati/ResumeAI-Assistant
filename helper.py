import google.generativeai as genai
import PyPDF2 as pdf
import json

def configure_genai(api_key):
    """Configure the Generative AI API with error handling."""
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        raise Exception(f"Failed to configure Generative AI: {str(e)}")
    

def get_gemini_response(prompt):
    """Generate a response using Gemini with enhanced error handling and response validation."""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt)
        
        # Ensure response is not empty
        if not response or not response.text:
            raise Exception("Empty response received from Gemini")
            
        # Try to parse the response as JSON
        try:
            response_json = json.loads(response.text)
            
            # Validate required fields
            required_fields = ["JD Match", "MissingKeywords", "Profile Summary"]
            for field in required_fields:
                if field not in response_json:
                    raise ValueError(f"Missing required field: {field}")
                    
            return response.text
            
        except json.JSONDecodeError:
            # If response is not valid JSON, try to extract JSON-like content
            import re
            json_pattern = r'\{.*\}'
            match = re.search(json_pattern, response.text, re.DOTALL)
            if match:
                return match.group()
            else:
                raise Exception("Could not extract valid JSON response")
                
    except Exception as e:
        raise Exception(f"Error generating response: {str(e)}")

def extract_pdf_text(uploaded_file):
    """Extract text from PDF with enhanced error handling."""
    try:
        reader = pdf.PdfReader(uploaded_file)
        if len(reader.pages) == 0:
            raise Exception("PDF file is empty")
            
        text = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)
                
        if not text:
            raise Exception("No text could be extracted from the PDF")
            
        return " ".join(text)
        
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")
    


def prepare_prompt(resume_text, job_description):
    """Prepare the input prompt with improved structure and validation."""
    if not resume_text or not job_description:
        raise ValueError("Resume text and job description cannot be empty")
        
    prompt_template = """
    Act as an expert Applicant Tracking System (ATS) specialist with deep understanding in:
    - Technical fields
    - Software engineering
    - Data science
    - Data analysis
    - Big data engineering
    
    Evaluate the following resume against the job description. Consider that the job market is highly competitive. Provide detailed feedback for resume improvement.
    
    Resume:
    {resume_text}
    
    Job Description:
    {job_description}
    
    Based on the evaluation, generate a tailored cold message to send to a recruiter or hiring manager for the position, highlighting the key qualifications and why the candidate is a strong fit for the role. Limit the cold message to 150-200 words.
    
    Also, provide specific improvements that can be added to the resume to better match the job description. These improvements should be categorized into:
    1. Experience - bullet points that could be added to existing experience sections
    2. Skills - specific skills that should be added or highlighted
    
    Provide a response in the following JSON format ONLY:
    {{
        "JD Match": A percentage (0-100) indicating the overall alignment of the resume with the job description,
        "MissingKeywords": List of specific skills, tools, or phrases missing in the resume but present in the job description,
        "Profile Summary": Detailed analysis of the match and specific improvement suggestions,
        "Improvements": {{
            "Skills": [List of skills to add or highlight],
        }},
        "Cold Message": A persuasive, tailored message (50-100 words) highlighting key qualifications and enthusiasm for the role, designed to attract the recruiter or hiring manager
    }}
    """
    # "detailed analysis of the match and specific improvement suggestions"  "professionally crafted cold message, between 50-100 words"
    return prompt_template.format(
        resume_text=resume_text.strip(),
        job_description=job_description.strip()
    )