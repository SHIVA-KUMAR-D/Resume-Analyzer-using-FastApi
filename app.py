# from fastapi import FastAPI, Form
# from fastapi.responses import HTMLResponse
# import requests

# app = FastAPI()

# # 🔑 PUT YOUR GEMINI API KEY HERE
# API_KEY = "AIzaSyB2R33PqHBjv8plRrxZXNeNvQBs8jpQZpQ"

# def analyze_resume(resume, role):

#     prompt = f"""
# You are an expert technical recruiter.

# Analyze the following resume for the target role: {role}

# Provide structured output:

# 1. Resume Score (0-100)
# 2. Key Strengths
# 3. Missing Skills / Gaps
# 4. Improvement Suggestions
# 5. ATS Optimization Tips
# 6. Final Hiring Verdict (Short)

# Resume:
# {resume}
# """

#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"

#     payload = {
#         "contents": [
#             {"parts": [{"text": prompt}]}
#         ]
#     }

#     response = requests.post(url, json=payload)
#     data = response.json()

#     return data["candidates"][0]["content"]["parts"][0]["text"]


# @app.get("/", response_class=HTMLResponse)
# def home():
#     return """
# <!DOCTYPE html>
# <html>
# <head>
# <title>AI Resume Analyzer</title>
# <style>
# body {font-family: Arial; background:#0f172a; color:white; text-align:center; padding:20px;}
# .container {max-width:800px; margin:auto;}
# textarea, input {width:100%; padding:10px; margin:10px 0; border-radius:8px; border:none;}
# button {background:#22c55e; color:white; padding:12px 20px; border:none; border-radius:8px; font-size:16px; cursor:pointer;}
# button:hover {background:#16a34a;}
# .result {background:#1e293b; padding:20px; border-radius:12px; margin-top:20px; text-align:left;}
# </style>
# </head>

# <body>
# <div class="container">
# <h1>🚀 AI Resume Skill Gap Analyzer</h1>
# <p>Analyze your resume for a specific job role</p>

# <form action="/analyze" method="post">

# <input name="role" placeholder="Target Job Role (e.g., Software Engineer)" required>

# <textarea name="resume" rows="12" placeholder="Paste your resume here..." required></textarea>

# <button type="submit">Analyze Resume</button>

# </form>
# </div>
# </body>
# </html>
# """


# @app.post("/analyze", response_class=HTMLResponse)
# def analyze(role: str = Form(...), resume: str = Form(...)):

#     result = analyze_resume(resume, role)

#     return f"""
# <!DOCTYPE html>
# <html>
# <head>
# <title>Analysis Result</title>
# <style>
# body {{font-family: Arial; background:#0f172a; color:white; padding:20px;}}
# .container {{max-width:800px; margin:auto;}}
# .result {{background:#1e293b; padding:20px; border-radius:12px; white-space:pre-wrap;}}
# a {{color:#22c55e;}}
# </style>
# </head>

# <body>
# <div class="container">

# <h1>📊 Analysis Result</h1>

# <div class="result">
# {result}
# </div>

# <br>
# <a href="/">⬅ Analyze Another Resume</a>

# </div>
# </body>
# </html>
# """
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# 🔑 PUT YOUR GEMINI API KEY HERE
API_KEY = "YOUR_GEMINI_API_KEY"


def analyze_resume(resume, role):

    prompt = f"""
You are an expert technical recruiter.

Analyze the following resume for the target role: {role}

Provide:
1. Resume Score (0-100)
2. Key Strengths
3. Missing Skills
4. Improvement Suggestions
5. ATS Optimization Tips
6. Final Verdict

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


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<title>AI Resume Analyzer</title>
<style>
body {font-family: Arial; background:#0f172a; color:white; text-align:center; padding:20px;}
.container {max-width:800px; margin:auto;}
textarea, input {width:100%; padding:10px; margin:10px 0; border-radius:8px; border:none;}
button {background:#22c55e; color:white; padding:12px 20px; border:none; border-radius:8px; font-size:16px; cursor:pointer;}
button:hover {background:#16a34a;}
</style>
</head>

<body>
<div class="container">
<h1>🚀 AI Resume Skill Gap Analyzer</h1>
<p>Upload your resume file (.txt) and enter target role</p>

<form action="/analyze" method="post" enctype="multipart/form-data">

<input name="role" placeholder="Target Job Role (e.g., Software Engineer)" required>

<input type="file" name="file" accept=".txt" required>

<button type="submit">Analyze Resume</button>

</form>
</div>
</body>
</html>
"""


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(role: str = Form(...), file: UploadFile = File(...)):

    contents = await file.read()
    resume_text = contents.decode("utf-8")

    result = analyze_resume(resume_text, role)

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Analysis Result</title>
<style>
body {{font-family: Arial; background:#0f172a; color:white; padding:20px;}}
.container {{max-width:800px; margin:auto;}}
.result {{background:#1e293b; padding:20px; border-radius:12px; white-space:pre-wrap;}}
a {{color:#22c55e;}}
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