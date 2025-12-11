import sys
import os
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import google.generativeai as genai
from config import API_KEY

# configure AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")

def generate_test_case(feature):
    prompt = f"""
    You are a QA Lead. Create a comprehensive manual test case for the following feature: "{feature}".
    
    Output structured Markdown:
    # Test Case: [Feature Name]
    
    | Field | Details |
    |---|---|
    | **ID** | TC_GEN_001 |
    | **Title** | Verify {feature} functionality |
    | **Priority** | High |
    | **Preconditions** | List relevant preconditions here. |
    
    ## Test Steps
    1. [Step 1]
    2. [Step 2]
    ...
    
    ## Expected Result
    [Clear description of expected outcome]
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating test case: {str(e)}"

def generate_test_ideas(feature):
    prompt = f"""
    You are a QA Lead. Brainstorm 10 creative and rigorous test scenarios for: "{feature}".
    Include happy paths, edge cases, and negative testing.
    
    Output as a Markdown table:
    | ID | Title | Test Type (Positive/Negative) | Description |
    |---|---|---|---|
    | ... | ... | ... | ... |
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating test ideas: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Cases or Ideas using Gemini AI")
    parser.add_argument("--feature", type=str, required=True, help="The feature to test (e.g., 'Login Page')")
    parser.add_argument("--type", type=str, choices=["case", "ideas"], default="case", help="Generate a full test 'case' or a list of test 'ideas'")
    
    args = parser.parse_args()
    
    if args.type == "case":
        print(generate_test_case(args.feature))
    elif args.type == "ideas":
        print(generate_test_ideas(args.feature))
