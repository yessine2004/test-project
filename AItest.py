import google.generativeai as genai
from config import API_KEY

# configure AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_test_case(feature):
    prompt = f"""
    Create a complete manual test case for this feature: {feature}.
    Include:
    - Test Case ID
    - Title
    - Preconditions
    - Test Steps
    - Expected Result
    """
    response = model.generate_content(prompt)
    return response.text

def generate_test_ideas(feature):
    prompt = f"""
    Generate 10 structured test ideas for this feature: {feature}.
    Format: ID | Title | Short Description
    """
    response = model.generate_content(prompt)
    return response.text


# TEST
print(generate_test_case("Checkout - invalid promo code"))
print(generate_test_ideas("Login page"))
