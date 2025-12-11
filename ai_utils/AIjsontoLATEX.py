import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

def json_to_latex(json_path, output_path="report.tex"):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return f"Error: File {json_path} not found."

    # Extract relevant info to save tokens and improve focus
    summary = data.get("summary", {})
    duration = data.get("duration", 0)
    
    # Process tests
    tests = data.get("tests", [])
    failed_tests = []
    passed_tests = []
    
    for test in tests:
        nodeid = test.get("nodeid", "Unknown")
        outcome = test.get("outcome", "Unknown")
        
        if outcome == "failed":
            # Extract error message
            longrepr = test.get("longrepr", "")
            crash = test.get("crash", {})
            message = crash.get("message", "No error message")
            if not message and isinstance(longrepr, str):
                 message = longrepr.split('\n')[-1] # Fallback to last line of repr
            
            failed_tests.append({
                "test": nodeid,
                "error": message
            })
        elif outcome == "passed":
            passed_tests.append(nodeid)

    # Construct the prompt with filtered data
    prompt = f"""
    You are a QA automation expert. Convert the following Test Execution Report Summary into a professional LaTeX document for the 'DemoWebShop' Migration Project.
    
    **Report Data:**
    - Total Duration: {duration:.2f} seconds
    - Summary: {json.dumps(summary)}
    - Failed Tests ({len(failed_tests)}):
      {json.dumps(failed_tests, indent=2)}
    - Passed Tests Count: {len(passed_tests)}
    
    **Requirements:**
    1. Create a "Test Execution Summary" section with a table showing Total, Passed, Failed, and Duration.
    2. Create a "Detailed Failures" section (if there are failures) listing each failed test and its error message in a table or list.
    3. Use standard LaTeX packages.
    4. ONLY output the raw LaTeX code (no markdown backticks).
    """

    print("Sending data to Gemini...")
    response = model.generate_content(prompt)
    latex_content = response.text
    
    # Strip markdown code blocks if present
    if latex_content.startswith("```latex"):
        latex_content = latex_content[8:]
    if latex_content.startswith("```"):
         latex_content = latex_content[3:]
    if latex_content.endswith("```"):
        latex_content = latex_content[:-3]

    with open(output_path, "w") as f:
        f.write(latex_content.strip())
    
    return f"LaTeX report generated at {output_path}"

# TEST
print(json_to_latex("report.json"))
