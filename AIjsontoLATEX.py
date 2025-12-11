import json
import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def json_to_latex(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    prompt = f"""
    Convert the following JIRA JSON bug report into a professional LaTeX table.
    Columns:
    - Bug ID
    - Summary
    - Severity
    - Status
    - Steps to Reproduce

    Only output LaTeX: 
    \\begin{{tabular}} ...
    \\end{{tabular}}

    JSON:
    {json.dumps(data)}
    """

    response = model.generate_content(prompt)
    return response.text

# TEST
print(json_to_latex("bugreport.json"))
