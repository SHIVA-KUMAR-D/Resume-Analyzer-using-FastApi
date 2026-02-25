from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import requests
from PyPDF2 import PdfReader
from docx import Document
import io

app = FastAPI()

# 🔑 PUT YOUR GEMINI API KEY HERE
API_KEY = "YOUR_GEMINI_API_KEY"


# ================================
# FILE TEXT EXTRACTION
# ================================
def extract_text_from_file(file_bytes, filename):

    # TXT
    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    # PDF
    elif filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    # DOCX
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    else:
        return ""


# ================================
# AI ANALYSIS FUNCTION
# ================================
def analyze_resume(resume, role):

    prompt = f"""
You are an expert technical recruiter.

Analyze the following resume for the target role: {role}

Provide structured output:

1. Resume Score (0-100)
2. Key Strengths
3. Missing Skills / Gaps
4. Improvement Suggestions
5. ATS Optimization Tips
6. Final Hiring Verdict

Resume:
{resume}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if "candidates" not in data:
            return f"API Error: {data}"

        return data["candidates"][0]["content"]["parts"][0]["text"]

    except Exception as e:
        return f"Error occurred: {str(e)}"


# ================================
# HOME PAGE
# ================================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Resume Skill Gap Analyzer</title>

<style>
body {
    font-family: Arial;
    background:#0f172a;
    color:white;
    text-align:center;
    padding:20px;
}

.container {
    max-width:800px;
    margin:auto;
    background:#1e293b;
    padding:25px;
    border-radius:15px;
}

input, textarea {
    width:100%;
    padding:12px;
    margin:10px 0;
    border-radius:8px;
    border:none;
    font-size:16px;
}

button {
    background:#22c55e;
    color:white;
    padding:14px 25px;
    border:none;
    border-radius:10px;
    font-size:18px;
    cursor:pointer;
}

button:hover {
    background:#16a34a;
}
</style>
</head>

<body>

<div class="container">

<h1>🚀 AI Resume Skill Gap Analyzer</h1>
<p>Upload resume and analyze for your target job role</p>

<form action="/analyze" method="post" enctype="multipart/form-data">

<input name="role" placeholder="Target Job Role (e.g., Software Engineer)" required>

<input type="file" name="file" accept=".txt,.pdf,.docx" required>

<button type="submit">Analyze Resume</button>

</form>

</div>

</body>
</html>
"""


# ================================
# ANALYSIS ROUTE
# ================================
@app.post("/analyze", response_class=HTMLResponse)
async def analyze(role: str = Form(...), file: UploadFile = File(...)):

    file_bytes = await file.read()

    resume_text = extract_text_from_file(file_bytes, file.filename)

    if resume_text.strip() == "":
        return "<h2>No readable text found in file.</h2><a href='/'>Back</a>"

    result = analyze_resume(resume_text, role)

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Analysis Result</title>

<style>
body {{
    font-family: Arial;
    background:#0f172a;
    color:white;
    padding:20px;
}}

.container {{
    max-width:800px;
    margin:auto;
}}

.result {{
    background:#1e293b;
    padding:25px;
    border-radius:15px;
    white-space:pre-wrap;
    line-height:1.5;
}}

a {{
    color:#22c55e;
    font-size:18px;
}}
</style>
</head>

<body>

<div class="container">

<h1>📊 Analysis Result</h1>

<div class="result">
{result}
</div>

<br>
<a href="/">⬅ Analyze Another Resume</a>

</div>

</body>
</html>
"""