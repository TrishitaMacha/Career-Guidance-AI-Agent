import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


# -------------------------------------------------------------
# ROADMAP GENERATOR
# -------------------------------------------------------------
def generate_roadmap(career):
    prompt = f"""
    You are a professional career planner.

    Create a complete 3-year structured roadmap to become: {career}

    Include:
    - Required technical skills
    - Courses to learn (prefer free platforms)
    - Important projects to build
    - Internship or work experience guidance
    - Certifications to complete
    - Expected salary range in India
    - Soft skills needed

    Format nicely with bullet points, headings, and year-wise sections.
    Add emojis for engagement but keep it professional.
    """
    response = model.generate_content(prompt)
    return response.text


# -------------------------------------------------------------
# CHAT AFTER ROADMAP (FOLLOW-UP QUESTIONS)
# -------------------------------------------------------------
def getting_reply(user_input: str, roadmap: str):
    """
    Handles follow-up questions after the roadmap is generated.
    """

    chat = model.start_chat(history=[])

    roadmap_prompt = f"""
    You are a professional and friendly Career Roadmap Assistant.

    Below is the roadmap you already generated:

    {roadmap}

    Now the user is asking a follow-up question.

    IMPORTANT INSTRUCTIONS:
    - Answer ONLY based on the roadmap above.
    - Give clear, detailed explanations if user asks "explain more".
    - Do NOT ask them which part — you must infer from their question.
    - Even if the user asks in 1–3 words, interpret correctly and answer.
    - Keep the response friendly, simple, and helpful.
    """

    full_prompt = roadmap_prompt + "\nUser: " + user_input

    response = chat.send_message(full_prompt)
    return response.text
