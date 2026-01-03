from flask import Flask, request, render_template
import fitz  # PyMuPDF
from analyse_pdf import analyse_resume_gemini
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def extract_text_from_resume(pdf_path):
    print(f"DEBUG: Extracting text from PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    print(f"DEBUG: Successfully extracted {len(text)} characters.")
    return text


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        if resume_file.filename.endswith(".pdf"):
            print(f"DEBUG: Received file {resume_file.filename} and JD (length: {len(job_description)})")
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(pdf_path)

            resume_content = extract_text_from_resume(pdf_path)
            print("DEBUG: Sending content to Gemini for analysis...")
            result = analyse_resume_gemini(resume_content, job_description)
            print("DEBUG: Analysis complete.")

            return render_template("index.html", result=result, job_description=job_description)

    return render_template("index.html", result=None, job_description="")


if __name__ == "__main__":
    # use_reloader=False is necessary in some environments to avoid signal.signal errors
    app.run(debug=True, port=5000, use_reloader=False)
