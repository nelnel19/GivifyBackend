from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_routes
from routes.campaign_routes import campaign_routes
from routes.donation_routes import donation_routes
import os

app = Flask(__name__)

# ✅ Allow CORS from local and deployed frontend
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "https://givify-o8ls.onrender.com"
]}})

# ✅ JWT Secret Key (for token signing)
# Use environment variable if available (safer for production)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "supersecretkey")
jwt = JWTManager(app)

# ✅ Register Blueprints (with proper prefixes)
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(campaign_routes)
app.register_blueprint(donation_routes)

# ✅ Health check route
@app.route("/")
def home():
    return jsonify({"message": "Givify API is running"}), 200

# ✅ Handle 404 errors gracefully
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

# ✅ Handle internal server errors gracefully
@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Set host to 0.0.0.0 so Render can access it
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
