import os
from app.app import app  # Ensure this correctly imports your Flask instance

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s PORT or fallback to 5000
    app.run(host="0.0.0.0", port=port, debug=False)  # Ensure it binds to 0.0.0.0
