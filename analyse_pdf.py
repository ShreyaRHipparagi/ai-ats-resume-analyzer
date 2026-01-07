import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import typing_extensions as typing

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

# --- 1. DEFINE THE SCHEMA (The Structure) ---
# This forces the model to adhere to this exact structure.
# We use a dictionary definition for maximum compatibility.

resume_analysis_schema = {
    "type": "object",
    "properties": {
        "candidate_info": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "title": {"type": "string"},
                "career_persona": {"type": "string", "description": "Creative title like 'The Disruptive Innovator'"},
                "readiness_score": {"type": "integer"}
            },
            "required": ["name", "title", "career_persona", "readiness_score"]
        },
        "ats_analysis": {
            "type": "object",
            "properties": {
                "overall_score": {"type": "integer"},
                "section_scores": {
                    "type": "object",
                    "properties": {
                        "quantification": {"type": "integer"},
                        "experience": {"type": "integer"},
                        "tech_stack": {"type": "integer"},
                        "education": {"type": "integer"}
                    },
                    "required": ["quantification", "experience", "tech_stack", "education"]
                },
                "breakdown": {
                    "type": "object",
                    "properties": {
                        "skill_match": {"type": "integer"},
                        "keyword_match": {"type": "integer"},
                        "experience_relevance": {"type": "integer"},
                        "formatting_quality": {"type": "integer"}
                    },
                    "required": ["skill_match", "keyword_match", "experience_relevance", "formatting_quality"]
                },
                "explanation": {
                    "type": "object",
                    "properties": {
                        "executive_summary": {"type": "string", "description": "High-level fit summary (100+ words). NO bolding (**)."},
                        "keyword_parity": {"type": "string", "description": "Analysis of keyword alignment/gaps (75+ words). NO bolding (**)."},
                        "quantification_review": {"type": "string", "description": "Audit of metric usage and impact (75+ words). NO bolding (**)."},
                        "structural_feedback": {"type": "string", "description": "Formatting and layout critique (50+ words). NO bolding (**)."}
                    },
                    "required": ["executive_summary", "keyword_parity", "quantification_review", "structural_feedback"]
                }
            },
            "required": ["overall_score", "section_scores", "breakdown", "explanation"]
        },
        "market_intel": {
            "type": "object",
            "properties": {
                "salary_range_usd": {"type": "string"},
                "salary_range_inr": {"type": "string"},
                "market_demand": {"type": "string", "enum": ["High", "Medium", "Low"]},
                "top_competencies": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["salary_range_usd", "salary_range_inr", "market_demand", "top_competencies"]
        },
        "advanced_insights": {
            "type": "object",
            "properties": {
                "technical_depth_scouter": {"type": "string", "description": "Highly technical evaluation of candidate's stack maturity and architectural depth (150+ words)."},
                "culture_fit_predictor": {"type": "string", "description": "Detailed analysis of placement probability based on soft skills and company values (150+ words)."},
                "faang_matchmaker": {"type": "string", "description": "Specific Big Tech match evaluation with deep reasoning (150+ words)."},
                "skill_radar": {
                    "type": "object",
                    "properties": {
                        "Technical": {"type": "integer"},
                        "Leadership": {"type": "integer"},
                        "Communication": {"type": "integer"},
                        "Problem Solving": {"type": "integer"},
                        "Innovation": {"type": "integer"}
                    },
                    "required": ["Technical", "Leadership", "Communication", "Problem Solving", "Innovation"]
                },
                "skills_gap_chart": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "skill": {"type": "string"},
                            "required": {"type": "integer"},
                            "possessed": {"type": "integer"}
                        },
                        "required": ["skill", "required", "possessed"]
                    }
                }
            },
            "required": ["technical_depth_scouter", "culture_fit_predictor", "faang_matchmaker", "skill_radar", "skills_gap_chart"]
        },
        "recruiter_review": {
            "type": "object",
            "properties": {
                "decision": {"type": "string", "enum": ["Shortlisted", "Rejected", "Maybe"]},
                "honest_feedback": {"type": "string", "description": "Brutally honest feedback. Minimum 200 words. NO bolding (**)."},
                "critical_fail_points": {"type": "array", "items": {"type": "string"}},
                "key_strengths": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["decision", "honest_feedback", "critical_fail_points", "key_strengths"]
        },
        "resume_tailoring": {
            "type": "object",
            "properties": {
                "new_summary": {"type": "string"},
                "optimized_skills": {"type": "array", "items": {"type": "string"}},
                "enhanced_bullets": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "original": {"type": "string"},
                            "improved": {"type": "string", "description": "Using Google X-Y-Z formula. NO bolding (**)."},
                            "impact": {"type": "string", "description": "NO bolding (**)."}
                        },
                        "required": ["original", "improved", "impact"]
                    }
                },
                "linkedin_tips": {"type": "array", "items": {"type": "string", "description": "NO bolding (**)."}},
                "cover_letter": {"type": "string", "description": "Formal business letter (Date, Salutation, 3-Paragraph Body, Professional Sign-off). Use markdown for spacing. NO bolding (**)."}
            },
            "required": ["new_summary", "optimized_skills", "enhanced_bullets", "linkedin_tips", "cover_letter"]
        },
        "skill_gap_analysis": {
            "type": "object",
            "properties": {
                "missing_technical_skills": {"type": "array", "items": {"type": "string"}},
                "missing_soft_skills": {"type": "array", "items": {"type": "string"}},
                "recommended_projects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "description": {"type": "string", "description": "100+ words detailed description"},
                            "tech_stack": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["title", "description", "tech_stack"]
                    }
                },
                "certifications": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["missing_technical_skills", "missing_soft_skills", "recommended_projects", "certifications"]
        },
        "interview_prep": {
            "type": "object",
            "properties": {
                "technical_questions": {"type": "array", "items": {"type": "string"}},
                "behavioral_questions": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["technical_questions", "behavioral_questions"]
        },
        "career_roadmap": {
            "type": "object",
            "properties": {
                "learning_plan_6_months": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "month": {"type": "integer"},
                            "focus": {"type": "string"}
                        },
                        "required": ["month", "focus"]
                    }
                },
                "final_advice": {"type": "string", "description": "Minimum 150 words. NO bolding (**)."}
            },
            "required": ["learning_plan_6_months", "final_advice"]
        }
    },
    "required": [
        "candidate_info", "ats_analysis", "market_intel", "advanced_insights", 
        "recruiter_review", "resume_tailoring", "skill_gap_analysis", 
        "interview_prep", "career_roadmap"
    ]
}

# --- 2. CONFIGURE MODEL ---
MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": resume_analysis_schema,
        "temperature": 0.7,
    }
)

def analyse_resume_gemini(resume_content, job_description):
    # MISSION DESCRIPTION
    # The prompt focuses on reasoning quality while the schema handles structure.
    
    prompt = f"""
    You are the 'Supreme AI Career Architect' - an ensemble of elite personas acting as one mind:
    1. THE CYNICAL SCANNER (ATS): A cold algorithm that calculates keyword density and formatting parsing.
    2. THE GOOGLE BAR RAISER: A Principal Engineer who demands 'zero tolerance' for fluff and enforces the X-Y-Z bullet point formula.
    3. THE VISIONARY MENTOR: A Silicon Valley growth-hacker focused on 'Adjacent Mastery'.

    INPUT DATA:
    - Candidate Resume: {resume_content}
    - Target Job Description (JD): {job_description}

    MISSION:
    Perform a ruthlessly detailed analysis of the candidate's fit for the role. 
    
    CRITICAL THINKING RULES:
    1. CONTEXTUAL SOVEREIGNTY: Do NOT recommend skills irrelevant to the specific JD (e.g., don't suggest DevOps to a Frontend Dev unless required).
    2. QUANTIFICATION OBSESSION: If the resume lacks numbers, the score must drop significantly.
    3. INTERNAL DEBATE: Before generating the output, simulate a debate between the Cynic and the Mentor to find the realistic middle ground.
    4. CONTENT DEPTH: 
       - 'honest_feedback' must be a brutal reality check (200+ words).
       - 'explanation' fields must collectively provide a granular breakdown: executive_summary (100+), keyword_parity (75+), quantification_review (75+), and structural_feedback (50+).
       - 'technical_depth_scouter', 'culture_fit_predictor', and 'faang_matchmaker' must be comprehensive, multi-paragraph deep dives (MINIMUM 150 words each).
        - 'recommended_projects' must be complex, portfolio-grade system designs (100+ words each).
        - 'cover_letter' must follow a strict High-Fidelity Business Format: 
           1. [Candidate Name/Header]
           2. [Current Date]
           3. [Hiring Manager Salutation]
           4. [Intro: Specific Hook to JD]
           5. [Body: 2 Paragraphs connecting resume experience to JD pain points]
           6. [Call to Action & Sign-off].
    5. MARKET REALISM: Use Q1 2026 Salary benchmarks.
    6. NO BOLDING: Do NOT use bolding (**) in any part of the response text (explanation, feedback, bullets, etc.) as the UI handles its own styling.
    7. STRUCTURED FLOW: Use professional markdown structuring (bullet points, numbered lists, sub-headers) within long text fields to ensure maximum scannability and a "proper" professional feel. Avoid dense walls of text.
    
    Generate the response filling the provided JSON schema.
    """
    
    try:
        print(f"DEBUG: Invoking Gemini API with {MODEL_NAME}...")
        response = model.generate_content(prompt)
        
        # Check for blocked content
        if response.prompt_feedback and response.prompt_feedback.block_reason:
             return {"error": f"SYSTEM BREACH: Analysis Blocked: {response.prompt_feedback.block_reason}"}

        # The text is already valid JSON due to response_schema
        result = json.loads(response.text)
        print("DEBUG: Successfully parsed JSON response.")
        return result

    except Exception as e:
        print(f"ERROR: Gemini Processing Failed: {str(e)}")
        # Collect available models for diagnostics
        try:
            available_models = [m.name for m in genai.list_models()]
        except:
            available_models = ["Unknown (API Error)"]
            
        return {
            "error": f"SYSTEM BREACH: Failed to parse AI response: {str(e)}",
            "diagnostics": {
                "available_models": available_models,
                "current_model": MODEL_NAME
            },
            "raw": response.text if 'response' in locals() else "No response generated"
        }
