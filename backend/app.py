from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mongo, jwt

app = Flask(__name__)
app.config.from_object(Config)

mongo.init_app(app)
jwt.init_app(app)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"])

# Register route blueprints
from routes.auth import auth_bp
from routes.upload import upload_bp
from routes.insights import insights_bp
from routes.export import export_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(upload_bp, url_prefix="/api/upload")
app.register_blueprint(insights_bp, url_prefix="/api/insights")
app.register_blueprint(export_bp, url_prefix="/api/export")

if __name__ == "__main__":
    app.run(debug=True, port=5000)