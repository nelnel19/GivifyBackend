from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_routes
from routes.campaign_routes import campaign_routes
from routes.donation_routes import donation_routes

app = Flask(__name__)

# ✅ Allow both local and deployed frontend URLs
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:3000",
    "https://givifyfrontend.onrender.com"
]}})

# JWT Secret Key
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Register routes
app.register_blueprint(auth_routes, url_prefix="/api/auth")
app.register_blueprint(campaign_routes)
app.register_blueprint(donation_routes)

@app.route("/")
def home():
    return {"message": "Givify API is running"}

if __name__ == "__main__":
    app.run(debug=True)
