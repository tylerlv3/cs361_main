import sys
import os

# Add the parent directory to the path if needed
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5002)
