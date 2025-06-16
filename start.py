import os
import sys
import webbrowser
import time
from django.core.management import execute_from_command_line

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IFPSystem.settings")  # Replace 'yourproject' with your project name

def run_server():
    # Start the Django development server
    execute_from_command_line(["manage.py", "runserver", "8000"])  # Port 8000

if __name__ == "__main__":
    # Open the browser to localhost:8000
    webbrowser.open("http://127.0.0.1:8000")
    time.sleep(1)  # Wait briefly to ensure server starts
    run_server()