import os
import webbrowser
from django.core.management import execute_from_command_line

def run_server():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IFPSystem.settings')

    print("Loading signals.py")
    print("Signals loaded")

    # Optional: Open browser
    webbrowser.open("http://127.0.0.1:8000")

    # 🛑 Run without the autoreloader
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000', '--noreload'])

if __name__ == "__main__":
    run_server()
