import os
from flask import Flask, render_template
from app.api.routes import uvsim_api, uvsim_model  # Import the UVSim model

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(uvsim_api, url_prefix='/api')

@app.route('/')
def home():
    # Get the API base URL from environment or construct it dynamically
    api_base = os.environ.get("API_BASE", "/api")
    return render_template('index.html', API_BASE=api_base)

if __name__ == "__main__":
    # Let gunicorn handle the port binding
    app.run(host="0.0.0.0", debug=False)
