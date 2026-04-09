from flask import Flask, request
from flask_cors import CORS
from config import Config
from extensions import db,jwt,mail
from routes import register_routes
from models import* # IMPORTANT: loads all models
from flask_jwt_extended import JWTManager,get_jwt,get_jwt_identity
from datetime import timedelta
import os
from routes.blocklist import jwt_blocklist



app = Flask(__name__)



# CORS(app, supports_credentials=True)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config.from_object(Config)


db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blocklist


register_routes(app)






# Token expiry settings
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)



@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    user_id = jwt_data["sub"]
    token_version = jwt_data.get("token_version")

    user = db.session.get(User, user_id)

    if not user or user.token_version != token_version:
        return None

    return user

# print(app.url_map)

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        return '', 200

@app.route("/")
def home():
    return {"status": "Flask + PostgreSQL connected successfully"}



if __name__ == "__main__":
     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


