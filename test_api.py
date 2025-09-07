


import os
import google.generativeai as genai
from dotenv import load_dotenv

print("--- Starting API Test ---")

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# 1. Configure the API key
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("!!! ERROR: GEMINI_API_KEY not found or not set in .env file.")
        exit()
    genai.configure(api_key=api_key)
    print("1. API Key configured successfully.")
except Exception as e:
    print(f"!!! ERROR configuring API key: {e}")
    exit()

# 2. Initialize the model
try:
    model_name = "gemini-2.5-flash-image-preview" # Make sure this is correct from hackathon docs
    model = genai.GenerativeModel(model_name=model_name)
    print(f"2. Initialized model: {model_name}")
except Exception as e:
    print(f"!!! ERROR initializing model: {e}")
    exit()

# 3. Generate content
try:
    prompt = "a simple picture of a blue dog"
    print(f"3. Sending prompt: '{prompt}'")
    response = model.generate_content(prompt)
    print("4. Received response from API.")
except Exception as e:
    print(f"!!! ERROR during API call: {e}")
    exit()

# 5. Analyze the response
try:
    print("\n--- Analyzing Response ---")
    print(f"Full response representation:\n{repr(response)}")

    image_bytes = response.candidates[0].content.parts[0].inline_data.data
    print(f"\nSUCCESS: Extracted image_bytes. Length: {len(image_bytes)}")

    if len(image_bytes) == 0:
        print("\n!!! TEST FAILED: The API returned an empty image.")
        print("This confirms the issue is with the API key or service, not the Flask app.")
    else:
        print("\n*** TEST PASSED: The API returned a valid image! ***")
        print("This is unexpected. If this test passes, there might be a subtle issue in the Flask app.")

except Exception as e:
    print(f"\n!!! TEST FAILED during response analysis: {e}")
    print("The response object from the API did not have the expected structure.")

