from flask import Blueprint, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, UserSkill

user_skills_bp = Blueprint('user_skills', __name__)
CORS(user_skills_bp)

# ================= ADD / UPDATE USER SKILLS =================
@user_skills_bp.route('/add', methods=['POST'])
@jwt_required()
def add_user_skill():

    user_id = int(get_jwt_identity())
    data = request.get_json()
    print("Received data:", data)
    print("User ID:", user_id)

    if not data or "skills" not in data:
        return jsonify({"error": "Skills list required"}), 400

    skills = data["skills"]

    seen = set()

    try:

        # Remove previous skills
        UserSkill.query.filter_by(user_id=user_id).delete()

        for skill in skills:

            skill_id = skill.get("skill_id")
            proficiency = skill.get("proficiency_level", 1)

            if not skill_id:
                return jsonify({"error": "skill_id required"}), 400

            if skill_id in seen:
                return jsonify({"error": "Duplicate skill_id"}), 400

            seen.add(skill_id)

            if not (1 <= proficiency <= 5):
                return jsonify({"error": "proficiency_level must be 1–5"}), 400

            user_skill = UserSkill(
                user_id=user_id,
                skill_id=skill_id,
                proficiency_level=proficiency
            )

            db.session.add(user_skill)

        db.session.commit()

        return jsonify({
            "message": "User skills saved successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        return jsonify({
        "error": str(e)
    }), 500

       


# ================= GET USER SKILLS =================
@user_skills_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_skills():

    user_id = int(get_jwt_identity())

    skills = UserSkill.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "skill_id": s.skill_id,
            "proficiency_level": s.proficiency_level
        }
        for s in skills
    ])


# ================= RESET USER SKILLS =================
@user_skills_bp.route('/reset', methods=['DELETE'])
@jwt_required()
def reset_user_skills():

    user_id = int(get_jwt_identity())

    deleted = UserSkill.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    return jsonify({
        "message": "All skills reset successfully",
        "deleted_count": deleted
    }), 200