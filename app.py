
import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import base64

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API key
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    print("Error: GEMINI_API_KEY not found. Please set it in your .env file.")
    exit()

# This is the model you'll be using. See the hackathon docs for the correct model name.
# We'll use a placeholder for now.
MODEL_NAME = "gemini-2.5-flash-image-preview" # Replace with the actual model name from the hackathon docs

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/generate-comic', methods=['POST'])
def generate_comic():
    """
    Handles the POST request to generate comic panels.
    Expects a JSON payload with 'character', 'style', and 'panels'.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    character_desc = data.get('character')
    style_desc = data.get('style')
    panel_prompts = data.get('panels')

    if not all([character_desc, style_desc, panel_prompts]):
        return jsonify({"error": "Missing character, style, or panel descriptions"}), 400

    generated_images = []
    
    # Initialize the generative model
    # Note: You might need to adjust generation_config based on the API documentation
    # Initialize the generative model
    model = genai.GenerativeModel(model_name=MODEL_NAME)

    for panel_action in panel_prompts:
        if not panel_action:
            continue # Skip empty panel prompts

        # --- This is the core prompt engineering part ---
        # We combine the character, style, and panel-specific action
        # to maintain consistency across the generated images.
        full_prompt = f"""
        A comic book panel.
        **Style:** {style_desc}.
        **Character:** {character_desc}.
        **Action:** {panel_action}.
        """

        try:
            print("--- Generating image ---")
            response = model.generate_content(full_prompt)
            
            image_bytes = None
            # The response can have multiple parts, iterate through them to find the image.
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    image_bytes = part.inline_data.data
                    break # Stop after finding the first image

            if image_bytes:
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                data_url = f"data:image/png;base64,{image_base64}"
                generated_images.append(data_url)
                print("--- Successfully generated and processed image ---")
            else:
                # This happens if the API returns a response with no image part.
                print("!!! WARNING: API response did not contain an image. Using placeholder.")
                generated_images.append("https://dummyimage.com/256x256/ff9900/ffffff.png&text=API_No_Image")

        except Exception as e:
            print(f"!!! AN ERROR OCCURRED: {e}")
            # Return a placeholder or error image for other errors
            generated_images.append("https://dummyimage.com/256x256/ff0000/ffffff.png&text=Error")


    return jsonify({"images": generated_images})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
