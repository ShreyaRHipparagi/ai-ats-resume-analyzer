import google.generativeai as genai 
from dotenv import load_dotenv
import os 
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Using gemini-1.5-flash for reliability and broad availability.
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config={"response_mime_type": "application/json"}
)

def analyse_resume_gemini(resume_content, job_description):
    prompt = f"""
    You are the 'Supreme AI Career Architect' - an ensemble of elite personas:
    1. THE CYNICAL SCANNER (ATS): A cold, metric-driven algorithm that kills 99% of resumes.
    2. THE GOOGLE BAR RAISER: A senior engineer who has conducted 500+ interviews and has 'zero tolerance' for filler.
    3. THE VISIONARY MENTOR: A growth-hacker who knows the exact delta between 'Average' and 'FAANG-level'.

    INPUTS:
    - Resume: {resume_content}
    - Job Description: {job_description}

    TASK:
    Analyze the resume against the JD and provide a hyper-advanced, hackathon-winning evaluation. 
    You MUST return the response in strict JSON format.

    JSON STRUCTURE:
    {{
        "candidate_info": {{
            "name": "Full Name",
            "title": "Professional Title (e.g. Senior Software Engineer)",
            "career_persona": "A creative title (e.g., 'The Disruptive Innovator')",
            "readiness_score": 0-100
        }},
        "ats_analysis": {{
            "overall_score": 0-100,
            "section_scores": {{
                "quantification": 0-100,
                "experience": 0-100,
                "tech_stack": 0-100,
                "education": 0-100
            }},
            "breakdown": {{
                "skill_match": 0-100,
                "keyword_match": 0-100,
                "experience_relevance": 0-100,
                "formatting_quality": 0-100
            }},
            "explanation": "Markdown formatted deep dive into metrics. Use bolding and professional highlights."
        }},
        "market_intel": {{
            "salary_range_usd": "$120k - $150k",
            "salary_range_inr": "₹25L - ₹40L",
            "market_demand": "High/Medium/Low",
            "top_competencies": ["Competency 1", "Competency 2"]
        }},
        "advanced_insights": {{
            "technical_depth_scouter": "Score and analysis on the 'complexity' of work mentioned",
            "culture_fit_predictor": "Estimated placement probability based on soft skills and company values",
            "faang_matchmaker": "Which specific Big Tech company this resume is closest to",
            "skill_radar": {{
                "Technical": 0-100,
                "Leadership": 0-100,
                "Communication": 0-100,
                "Problem Solving": 0-100,
                "Innovation": 0-100
            }},
            "skills_gap_chart": [
                {{ "skill": "Skill Name", "required": 0-100, "possessed": 0-100 }}
            ]
        }},
        "recruiter_review": {{
            "decision": "Shortlisted" | "Rejected" | "Maybe",
            "honest_feedback": "Brutally honest recruiter perspective, focused on career trajectory.",
            "critical_fail_points": ["Point 1", "Point 2"],
            "key_strengths": ["Strength 1", "Strength 2"]
        }},
        "resume_tailoring": {{
            "new_summary": "Tailored high-impact professional summary",
            "optimized_skills": ["Skill 1", "Skill 2"],
            "enhanced_bullets": [
                {{
                    "original": "Old bullet point",
                    "improved": "FAANG-level bullet point using Google's X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z].",
                    "impact": "Explanation of why this bullet wins"
                }}
            ],
            "linkedin_tips": ["Tip 1", "Tip 2"],
            "cover_letter": "A high-impact, professional cover letter (approx 300 words) tailored to the job description."
        }},
        "skill_gap_analysis": {{
            "missing_technical_skills": ["Skill A"],
            "missing_soft_skills": ["Skill C"],
            "recommended_projects": [
                {{
                    "title": "Project Name",
                    "description": "Comprehensive project description addressing the skill gap",
                    "tech_stack": ["Tech X"]
                }}
            ],
            "certifications": ["Recommended Certification"]
        }},
        "interview_prep": {{
            "technical_questions": ["Technical Question 1"],
            "behavioral_questions": ["Behavioral Question 1"]
        }},
        "career_roadmap": {{
            "learning_plan_6_months": [
                {{ "month": 1, "focus": "Month 1 detailed focus area" }},
                {{ "month": 2, "focus": "Month 2 detailed focus area" }},
                {{ "month": 3, "focus": "Month 3 detailed focus area" }},
                {{ "month": 4, "focus": "Month 4 detailed focus area" }},
                {{ "month": 5, "focus": "Month 5 detailed focus area" }},
                {{ "month": 6, "focus": "Month 6 detailed focus area" }}
            ],
            "final_advice": "Elite winning strategy for long-term career growth."
        }}
    }}

    CRITICAL RULES:
    1. EXCLUSIVITY: The 'learning_plan_6_months' array MUST contain exactly 6 entries (one for each month).
    2. DEPTH: Do not provide one-word answers. Each 'focus' and 'explanation' must be content-rich.
    3. FORMATTING: Use Markdown for formatting inside strings (bolding, italics, etc.).
    4. X-Y-Z FORMULA: Bullet points MUST follow: Accomplished [X] as measured by [Y], by doing [Z].
    5. REALISM: Salary ranges must be realistic benchmarks for the role and location.
    """
    
    try:
        print(f"DEBUG: Invoking Gemini API with prompt (truncated): {prompt[:200]}...")
        response = model.generate_content(prompt)
        print("DEBUG: Gemini API response received.")
        
        # Parse the JSON to ensure it's valid before returning
        result = json.loads(response.text)
        print("DEBUG: Successfully parsed JSON response.")
        return result
    except Exception as e:
        print(f"ERROR: Gemini Processing Failed: {str(e)}")
        # Collect available models for diagnostics
        try:
            available_models = [m.name for m in genai.list_models()]
            print(f"INFO: Available models: {available_models}")
        except:
            available_models = ["Unknown (API Error)"]
            
        return {
            "error": f"SYSTEM BREACH: Failed to parse AI response: {str(e)}",
            "diagnostics": {
                "available_models": available_models,
                "current_model": "gemini-2.5-flash-lite"
            },
            "raw": response.text if 'response' in locals() else "No response generated"
        }
