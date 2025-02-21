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
    app.run(debug=True)
