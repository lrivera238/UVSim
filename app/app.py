import os
from flask import Flask, render_template
from app.api.routes import uvsim_api, uvsim_model  # Import the UVSim model

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(uvsim_api, url_prefix='/api')

@app.route('/')
def home():
    accumulator_value = uvsim_model.accumulator  # Get accumulator value
    return render_template('index.html', accumulator=accumulator_value)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s provided PORT or default to 5000
    app.run(host="0.0.0.0", port=port, debug=False)
