# ResumeAI-Assistant

The **ResumeAI-Assistant** is a web application designed to help users analyze their resumes in relation to a job description (JD). It provides a matching score between the resume and JD, identifies missing keywords, generates a summary of the resume, and even creates a cold message for outreach.

## Features:
- **Resume & Job Description Matching**: Calculates a score to indicate how well the resume matches the job description.
- **Missing Keywords**: Identifies key skills or words that are present in the job description but missing from the resume.
- **Resume Summary**: Provides a brief summary of the resume based on its content.
- **Cold Message Generation**: Generates a professional cold message for outreach based on the resume and job description.

## Requirements:
- Python 3.x
- Streamlit

## Installation

### Step 1: Install Dependencies
Before running the application, ensure that all necessary dependencies are installed. You can do this by installing the packages listed in the `requirements.txt` file.

Run the following command in your terminal:

`pip install -r requirements.txt`

### Step 2: Run the Application
After the dependencies are installed, you can run the application using Streamlit. In your terminal, execute the following command:

`streamlit run app.py`

<img width="916" alt="image" src="https://github.com/user-attachments/assets/c9dfbb24-1822-409d-812c-6e2ef28ebf1c" />


## How to Use:

1. **Upload Resume**: Upload your resume (in PDF, DOCX, or TXT format).
2. **Upload Job Description**: Upload the job description file that you want to compare the resume against.
3. **Analyze**: The application will display:
   - A matching score showing how well your resume aligns with the job description.
   - A list of missing keywords that should be included in your resume.
   - A summary of your resume.
   - A cold message template for professional outreach.
4. **Review Output**: Review the matching score, missing keywords, resume summary, and cold message that the application generates to improve your resume and tailor it to the job description.

