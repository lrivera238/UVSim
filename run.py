import os
from app.app import app  # Import the Flask application instance

# gunicorn will use this app instance
if __name__ == "__main__":
    # For local development, use Flask's development server
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
