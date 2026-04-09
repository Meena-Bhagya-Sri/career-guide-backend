from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ml_model.skill_gap import calculate_skill_gap
from ml_model.feature_builder import build_skill_vector
from ml_model.ml_pipeline import predict_career
from models import db, Career
from flask_cors import CORS

recommendations_bp = Blueprint("recommendations", __name__)
CORS(recommendations_bp)


# @recommendations_bp.route("/ml-career", methods=["GET"])
@recommendations_bp.route("/ml-career", methods=["GET"])
@jwt_required()
def ml_career():

    user_id = int(get_jwt_identity())

    # Build skill vector
    X = build_skill_vector(user_id)

    # ML prediction
    career_name = predict_career(X)

    # Find career in database
    career = Career.query.filter_by(career_name=career_name).first()
    # print(career.avg_salary)
    # If career exists return full info
    if career:
        return jsonify({
            "career": career.career_name,
            "career_id": career.id,
            "description": career.description,
            "avg_salary": career.avg_salary,
            "difficulty_level": career.difficulty_level
        }), 200

    # If not found still return prediction
    return jsonify({
        "career": career_name,
        "career_id": None,
        "description": None,
        "avg_salary": None,
        "difficulty_level": None
    }), 200

# ---------SKILL GAP ANALYSIS---------
@recommendations_bp.route("/skill-gap/<int:career_id>", methods=["GET"])
@jwt_required()
def skill_gap_analysis(career_id):

    user_id = int(get_jwt_identity())

    gap = calculate_skill_gap(user_id, career_id)

    return jsonify({
        "career": gap["career"],
        "readiness": gap["readiness"],
        "totalSkills": gap["total_skills"],
        "improvementNeeded": gap["improvement_needed"],
        "skills": gap["skills"]
    }), 200