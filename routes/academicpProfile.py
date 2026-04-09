from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, AcademicProfile

academic_bp = Blueprint("academic_profile", __name__)

@academic_bp.route("/add", methods=["POST"])
@jwt_required()
def create_or_update_profile():

    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:

        profile = AcademicProfile.query.filter_by(user_id=user_id).first()

        if not profile:
            profile = AcademicProfile(user_id=user_id)

        profile.highest_qualification = data.get("highest_qualification")
        profile.branch = data.get("branch")

        cgpa = data.get("cgpa")
        profile.cgpa = float(cgpa) if cgpa else None

        interests = data.get("interests", [])
        skills = data.get("skills_known", [])

        if not isinstance(interests, list):
            interests = [interests]

        if not isinstance(skills, list):
            skills = [skills]

        profile.interests = interests
        profile.skills_known = skills

        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "message": "Academic profile saved successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@academic_bp.route("/", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = int(get_jwt_identity())

    profile = AcademicProfile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Academic profile not found"}), 404

    skills = profile.skills_known
    interests = profile.interests

    if not isinstance(skills, list):
        skills = [skills] if skills else []

    if not isinstance(interests, list):
        interests = [interests] if interests else []

    return jsonify({
        "highest_qualification": profile.highest_qualification,
        "branch": profile.branch,
        "cgpa": float(profile.cgpa) if profile.cgpa else None,
        "interests": interests,
        "skills_known": skills
    })