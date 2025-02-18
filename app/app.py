from flask import Flask
from api.routes import uvsim_api

app = Flask(__name__)

# Register API blueprint
app.register_blueprint(uvsim_api, url_prefix='/api')

if __name__ == "__main__":
    app.run(debug=True)
