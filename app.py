import streamlit as st
import fitz  # PyMuPDF
from analyse_pdf import analyse_resume_gemini
import os
import tempfile
from jinja2 import Environment, FileSystemLoader

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def extract_text_from_resume(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name
    
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    os.unlink(pdf_path)
    return text

def main():
    # Load Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('index.html')

    # Session State for results
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""

    # Streamlit Landing/Input
    if st.session_state.result is None:
        st.title("🚀 AI Resume Analyzer")
        st.markdown("### Powered by Google Gemini & Premium Insights")
        
        col1, col2 = st.columns(2)
        with col1:
            resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
        with col2:
            job_description = st.text_area("Paste Job Description", height=200, value=st.session_state.job_description)

        if st.button("🚀 ANALYZE RESUME"):
            if resume_file and job_description:
                with st.spinner("🧠 AI Architect is scanning your profile..."):
                    resume_text = extract_text_from_resume(resume_file)
                    result = analyse_resume_gemini(resume_text, job_description)
                    st.session_state.result = result
                    st.session_state.job_description = job_description
                    st.rerun()
            else:
                st.warning("Please upload a resume and paste the job description.")

    # Render results using the custom HTML
    if st.session_state.result:
        # Check if there's an error in the result
        if "error" in st.session_state.result:
            st.error(st.session_state.result["error"])
            if st.button("Try Again"):
                st.session_state.result = None
                st.rerun()
        else:
            # Render the Jinja2 template
            html_content = template.render(
                result=st.session_state.result,
                job_description=st.session_state.job_description
            )
            
            # Use st.components.v1.html to render the dashboard
            # We set a large height to ensure the dashboard is visible
            import streamlit.components.v1 as components
            components.html(html_content, height=2500, scrolling=True)
            
            if st.button("Analyze Another Resume"):
                st.session_state.result = None
                st.rerun()

if __name__ == "__main__":
    main()
