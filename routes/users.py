from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from routes.auth import role_required

users_bp = Blueprint('users', __name__)

@users_bp.route("/", methods=["POST"])
@jwt_required()
@role_required("admin")  # Only admins can add users
def add_user():
    data = request.get_json()

    # Basic validation
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    # Create new user
    new_user = User(
        name=data["name"],
        email=data["email"],
        role=data.get("role", "user")  # default role is 'user'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User added successfully",
        "user": {
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "role": new_user.role
        }
    }), 201


# # ---------------- GET USER (SELF or ADMIN) ----------------
# @users_bp.route('/<int:user_id>', methods=['GET'])
# @jwt_required()
# def get_user(user_id):
#     current_user_id = int(get_jwt_identity())
#     current_user = User.query.get(current_user_id)

#     if current_user.role != "admin" and current_user_id != user_id:
#         return jsonify({"error": "Access denied"}), 403

#     user = User.query.get_or_404(user_id)

#     return jsonify({
#         'user_id': user.user_id,
#         'name': user.name,
#         'email': user.email,
#         'role': user.role
#     })


# ---------------- UPDATE USER ----------------
@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)

    # Allow self-update OR admin role
    if current_user.role != "admin" and current_user_id != user_id:
        return jsonify({"error": "Access denied"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    # Optional: allow role change if admin
    if current_user.role == "admin":
        user.role = data.get('role', user.role)

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})

# ---------------- DELETE USER (ADMIN only) ----------------
@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required("admin")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})


# ---------------- GET ALL USERS (ADMIN only) ----------------
@users_bp.route("/", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_users():
    users = User.query.all()

    return jsonify([
        {
            "user_id": u.user_id,
            "name": u.name,
            "email": u.email,
            "role": u.role
        }
        for u in users
    ])