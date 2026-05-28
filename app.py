# app.py
# This is the main FastAPI application file.
# FastAPI is a modern Python web framework for building APIs quickly.

import os
from fastapi import FastAPI

# python-dotenv loads variables from a .env file into the environment.
# This lets us keep secrets out of our code and use them safely.
from dotenv import load_dotenv

# Load the .env file. In production (e.g. Render), environment variables
# are set directly in the dashboard — load_dotenv() simply has no effect there.
load_dotenv()

# Read the API_KEY from the environment.
# Never hardcode secrets like this: API_KEY = "abc123"
# Instead, store them in .env locally and in the hosting platform's settings.
API_KEY = os.getenv("API_KEY", "not-set")

# Create the FastAPI application instance.
app = FastAPI(
    title="CI/CD Demo",
    description="A beginner-friendly demo showing environment variables, CI, and CD.",
    version="1.0.0",
)


@app.get("/")
def root():
    """Home endpoint — confirms the app is running."""
    return {
        "message": "Welcome to the CI/CD demo!",
        "api_key_loaded": API_KEY != "not-set",  # True if .env was found
    }


@app.get("/health")
def health():
    """Health-check endpoint — used by Render and monitoring tools to verify the app is alive."""
    return {"status": "ok"}
