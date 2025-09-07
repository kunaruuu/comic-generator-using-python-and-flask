# Consistent Character Comic Generator

This is a simple web application that uses Google's Gemini API to generate short comic strips with a consistent character and art style.

## Features

- Define a character and an art style.
- Generate a comic strip with multiple panels.
- Dynamically add or remove panels to create comics of different lengths.
- Built with a Python Flask backend and a simple HTML/JS frontend.

## Local Setup Instructions

To run this project on your local machine, please follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd comic-generator
    ```

2.  **Create and activate a Python virtual environment:**

    *On Windows:*
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

    *On macOS/Linux:*
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create your environment file:**
    - Create a new file in the project directory named `.env`.
    - Add your Gemini API key to this file, like so:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

5.  **Run the application:**
    ```bash
    flask run --port 5001
    ```

6.  Open your web browser and navigate to `http://127.0.0.1:5001`.

## Deployment

This application is configured for deployment on cloud services that support Python/WSGI, such as Render or Heroku. It uses Gunicorn as the production web server.
