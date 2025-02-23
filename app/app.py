import os
from flask import Flask, render_template
from app.api.routes import uvsim_api, uvsim_model  # Import the UVSim model

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(uvsim_api, url_prefix='/api')

@app.route('/')
def home():
    # accumulator_value = uvsim_model.accumulator  # Get accumulator value
    api_base = os.environ.get("API_BASE", "http://127.0.0.1:5000/api")  # Use Render URL or default to local
    return render_template('index.html', API_BASE=api_base)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s provided PORT or default to 5000
    app.run(host="0.0.0.0", port=port, debug=False)
