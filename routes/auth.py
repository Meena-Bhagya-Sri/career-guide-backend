from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db,jwt
import re
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from datetime import timedelta
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from routes.blocklist import jwt_blocklist

auth_bp = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # ---------------- EMAIL VALIDATION ----------------
    email_pattern = r'^[a-zA-Z0-9._%+-]+@(gmail\.com|yahoo\.com|outlook\.com|hotmail\.com)$'
    if not re.match(email_pattern, email):
        return jsonify({
            "error": "Only Gmail, Yahoo, or Microsoft email addresses are allowed"
        }), 400

    # ---------------- PASSWORD VALIDATION ----------------
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    # Must NOT start with special character
    if not password[0].isalnum():
        return jsonify({
            "error": "Password must not start with a special character"
        }), 400

    # At least one uppercase, lowercase, digit
    if not re.search(r"[A-Z]", password):
        return jsonify({"error": "Password must contain at least one uppercase letter"}), 400

    if not re.search(r"[a-z]", password):
        return jsonify({"error": "Password must contain at least one lowercase letter"}), 400

    if not re.search(r"[0-9]", password):
        return jsonify({"error": "Password must contain at least one number"}), 400

    # ---------------- PASSWORD STRENGTH SCORING ----------------
    score = 0

    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    if len(password) >= 12:
        score += 1

    if score < 4:
        return jsonify({
            "error": "Password is too weak. Use a stronger password"
        }), 400

    # ---------------- USER EXISTS CHECK ----------------
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists please login"}), 409

    # ---------------- CREATE USER ----------------
    hashed_password = generate_password_hash(password)

    user = User(
    name=name,
    email=email,
    password_hash=hashed_password,
    role="student"
)

    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(
    identity=str(user.user_id),
    additional_claims={
        "role": user.role,
        "token_version": user.token_version
    }
)

    refresh_token = create_refresh_token(
    identity=str(user.user_id),
    additional_claims={
        "role": user.role,
        "token_version": user.token_version
    }
)
    return jsonify({
    "message": "User registered successfully",
    "user_id": user.user_id,
    "password_strength_score": score,
    "access_token": access_token,
    "refresh_token": refresh_token
}), 201
# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if role and user.role != role:
        return jsonify({"error": "Incorrect role selected"}), 403

    access_token = create_access_token(
    identity=str(user.user_id),
    additional_claims={
        "role": user.role,
        "token_version": user.token_version
    }
)

    refresh_token = create_refresh_token(
    identity=str(user.user_id),
    additional_claims={
        "role": user.role,
        "token_version": user.token_version
    }
)


    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.user_id,
            "name": user.name,
            "email": user.email
        }
    }), 200
# -------- REFRESH ACCESS TOKEN --------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())

    claims = get_jwt()

    new_access_token = create_access_token(
    identity=str(user_id),
    additional_claims={
        "role": claims["role"],
        "token_version": claims["token_version"]
    }
)

    return jsonify({
        "access_token": new_access_token
    }), 200

#-------LOGOOUT--------------

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blocklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200




 
# ------------RESET PASSWORD----------
import hashlib
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({"error": "Token and password are required"}), 400

    # Hash incoming token (must match stored hashed token)
    hashed_token = hashlib.sha256(token.encode()).hexdigest()

    user = User.query.filter_by(reset_token=hashed_token).first()

    # Validate token and expiry
    if (
        not user or
        not user.reset_token_expiry or
        user.reset_token_expiry < datetime.now(timezone.utc)
    ):
        return jsonify({"error": "Invalid or expired token"}), 400

    # ---------------- PASSWORD VALIDATION (REUSE RULES) ----------------
    if len(new_password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    if not new_password[0].isalnum():
        return jsonify({"error": "Password must not start with a special character"}), 400

    import re
    if not re.search(r"[A-Z]", new_password):
        return jsonify({"error": "Password must contain at least one uppercase letter"}), 400

    if not re.search(r"[a-z]", new_password):
        return jsonify({"error": "Password must contain at least one lowercase letter"}), 400

    if not re.search(r"[0-9]", new_password):
        return jsonify({"error": "Password must contain at least one number"}), 400

    # ---------------- UPDATE PASSWORD ----------------
    user.password_hash = generate_password_hash(new_password)

    # Invalidate reset token after use
    user.reset_token = None
    user.reset_token_expiry = None

    db.session.commit()

    return jsonify({"message": "Password reset successful"}), 200


# ---------------FORGOT PASSWORD---------------

from flask_mail import Message
from extensions import mail

import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from flask import request, jsonify
from models import db, User

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json(silent=True)

    if not data or not data.get("email"):
        return jsonify({"error": "Email is required"}), 400

    email = data["email"]

    user = User.query.filter_by(email=email).first()

    # IMPORTANT: Do NOT reveal if user exists
    if not user:
        return jsonify({
            "message": "If the email exists, a reset link was sent"
        }), 200

    # Generate secure token
    raw_token = secrets.token_urlsafe(32)

    # Hash token before storing (security best practice)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    user.reset_token = hashed_token
    user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(minutes=15)

    db.session.commit()

    reset_link = f"http://localhost:5173/reset-password?token={raw_token}"

    msg = Message(
    subject="Password Reset - Career Guidance System",
    recipients=[email],
    body=f"""
Hello,

You requested a password reset.

Click the link below to reset your password:
{reset_link}

This link expires in 15 minutes.

If you did not request this, please ignore this email.

Regards,
Career Guidance System Team
"""
)

    mail.send(msg)

    return jsonify({
        "message": "If the email exists, a reset link was sent"
    }), 200
# ----------ROLES--------
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt

# ---------------- ROLE-BASED ACCESS DECORATOR ----------------
def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role != required_role:
                return jsonify({
                    "error": "Access forbidden: insufficient permissions"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

