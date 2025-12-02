# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import pdfplumber

# # Load environment variables
# load_dotenv()

# # Configure Gemini API
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# model_name = "gemini-2.5-flash"
# model = genai.GenerativeModel(model_name)


# # -------------------------------------------------------------
# # PDF TEXT EXTRACTION
# # -------------------------------------------------------------
# def extract_text_from_pdf(uploaded_file):
#     """Extracts text from a PDF file"""
#     text = ""
#     with pdfplumber.open(uploaded_file) as pdf:
#         for page in pdf.pages:
#             text += page.extract_text() + "\n"
#     return text


# # -------------------------------------------------------------
# # RESUME ANALYSIS
# # -------------------------------------------------------------
# def analyze_resume(text):
#     """Uses AI to analyze a resume"""
#     prompt = f"""
#     You are a professional Resume Evaluator.

#     Analyze the resume content below and extract:

#     - Skills Summary
#     - Strengths
#     - Weaknesses
#     - Job Role Suitability
#     - Improvements Needed
#     - Hiring Likelihood (0-10 score)

#     Resume Content:
#     {text}

#     Return clean bullet points only.
#     """
#     response = model.generate_content(prompt)
#     return response.text


# # -------------------------------------------------------------
# # MARKSHEET ANALYSIS
# # -------------------------------------------------------------
# def analyze_marksheet(text):
#     """Uses AI to analyze academic marks and strengths"""
#     prompt = f"""
#     You are an Academic Performance Analyzer.

#     From the marksheet given below, extract:
#     - Subjects and Marks Table
#     - Highest scoring subjects
#     - Lowest scoring subjects
#     - Academic Strength Score (0-10)
#     - Suggested Career Fields

#     Marksheet Content:
#     {text}
#     extract every table form the marksheet and each subject from the tables given.

#     Return clean bullet points and a marks table.
#     """
#     response = model.generate_content(prompt)
#     return response.text

# def reply(user_in:str):
#     chat = model.start_chat(history=[])

#     evaluation_prompt = f""" 
#     You are a professional Evaluation master so , you have evaluated the marks.
#     Now you have some things form the given marksheet,
#     You have provided your evaluation, now you need to ask the user if they have any questions regarding your evaluation.
#     Start the conversation friendly as if they have any questions.
#     Give the answers based on their questions and the extracted marksheet.
#     """
#     ans = evaluation_prompt+'\nsuer'+user_in
#     response = model.generate_content(ans)
#     return response.text
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import pdfplumber

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model_name = "gemini-2.5-flash"
model = genai.GenerativeModel(model_name)


# -------------------------------------------------------------
# PDF TEXT EXTRACTION
# -------------------------------------------------------------
def extract_text_from_pdf(uploaded_file):
    """Extracts text from a PDF file"""
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


# -------------------------------------------------------------
# RESUME ANALYSIS
# -------------------------------------------------------------
def analyze_resume(text, target_role):
    """Uses AI to analyze resume for a specific job role with skill-gap analysis"""

    prompt = f"""
    You are an expert ATS Resume Evaluator and Career Mentor.

    The user is targeting the role: **{target_role}**

    Analyze the resume below and provide the following:

    1️⃣ **Skills Found in Resume**
    - Extract technical skills
    - Extract soft skills

    2️⃣ **Required Skills for {target_role}**
    - Give a list of 10–15 must-have skills for this role

    3️⃣ **Skill Gap Analysis**
    - Compare user's skills vs required skills
    - List missing skills clearly
    - Mark each missing skill as:
        • Beginner-friendly  
        • Moderate  
        • Hard-critical skill

    4️⃣ **Recommended Projects for the Target Role**
    - Give 3–5 project ideas based on missing skills

    5️⃣ **Strengths & Weaknesses**
    - Based on the resume content

    6️⃣ **ATS Score (0–100)**
    - Score the resume for the selected job role
    - Mention what lowered the score

    7️⃣ **Role Suitability (0–10)**

    8️⃣ **Rewrite The Resume for the Job Role**
    - Clean, structured, ATS-friendly
    - Should include: summary, skills, education, projects, experience (if any)
    - Rewrite using only the information found in the resume

    Resume Content:
    {text}

    Return the response in clean bullet points with proper sections.
    """
    response = model.generate_content(prompt)
    return response.text


# -------------------------------------------------------------
# MARKSHEET ANALYSIS
# -------------------------------------------------------------
def analyze_marksheet(text):
    """Uses AI to analyze academic marks and strengths"""
    prompt = f"""
    You are an Academic Performance Analyzer.

    From the marksheet given below, extract:
    - Subjects and Marks Table
    - Highest scoring subjects
    - Lowest scoring subjects
    - Academic Strength Score (0-10)
    - Suggested Career Fields

    Marksheet Content:
    {text}

    Extract every table and every subject clearly.

    Return clean bullet points and a marks table.
    """
    response = model.generate_content(prompt)
    return response.text


# -------------------------------------------------------------
# CHAT RESPONSE AFTER ANALYSIS
# -------------------------------------------------------------
def getting_reply(user_input: str, evaluation: str, target_role: str):
    """Handles follow-up questions after resume evaluation"""

    chat = model.start_chat(history=[])

    followup_prompt = f"""
    You are a friendly and professional Resume Evaluation Assistant.

    Below is the resume evaluation you already generated:

    {evaluation}

    The user is targeting the role: {target_role}

    Now the user is asking a follow-up question.
    
    Instructions:
    - Answer ONLY based on the above evaluation.
    - DO NOT create new evaluation points.
    - DO NOT ask which part. Infer from the question.
    - Give clear, short, practical answers.
    """

    full_prompt = followup_prompt + "\nUser: " + user_input

    response = chat.send_message(full_prompt)
    return response.text

from fpdf import FPDF

def generate_pdf_report(evaluation_text, target_role):
    """Creates a PDF file from the resume evaluation text"""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Resume Evaluation Report - {target_role}", ln=True)

    pdf.ln(5)

    # Body text
    pdf.set_font("Arial", size=12)

    # Split long text into lines
    for line in evaluation_text.split("\n"):
    # Remove emojis + unsupported unicode characters
        clean_line = re.sub(r'[^\x00-\x7F]+', ' ', line)
        pdf.multi_cell(0, 8, clean_line)

    # Save to a temporary file
    filename = "resume_evaluation_report.pdf"
    pdf.output(filename)

    return filename

import re

def extract_ats_score(evaluation_text):
    """Extracts ATS score from the evaluation text using regex."""
    match = re.search(r"ATS Score[:\- ]+(\d+)", evaluation_text)
    if match:
        return int(match.group(1))
    return None
