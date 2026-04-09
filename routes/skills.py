from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models import Skill


skills_bp = Blueprint('skills', __name__)

from sqlalchemy.exc import IntegrityError

@skills_bp.route("/", methods=["POST"])
def add_skill():
    data = request.get_json()

    skill_name = data.get("skill_name")
    skill_type = data.get("skill_type")

    if not skill_name or not skill_type:
        return jsonify({"error": "All fields required"}), 400

    # Duplicate check
    existing = Skill.query.filter(
        db.func.lower(Skill.skill_name) == skill_name.lower()
    ).first()

    if existing:
        return jsonify({"error": "Skill already exists"}), 409

    new_skill = Skill(
        skill_name=skill_name,
        skill_type=skill_type
    )

    db.session.add(new_skill)
    db.session.commit()

    return jsonify({"message": "Skill added"}), 201

@skills_bp.route('/', methods=['GET'])
@jwt_required()
def get_skills():
    skills = Skill.query.all()
    return jsonify([
        {
            'id': s.id,
            'skill_name': s.skill_name,
            'skill_type': s.skill_type
        } for s in skills
    ])




@skills_bp.route('/<int:skill_id>', methods=['PUT'])
@jwt_required()
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    data = request.get_json()

    # ✅ SAFE extraction
    new_name = data.get('skill_name')
    new_type = data.get('skill_type')

    if not new_name or not new_name.strip():
        return jsonify({'error': 'Skill name is required'}), 400

    new_name = new_name.strip()

    # ✅ Check duplicate (ignore same record)
    existing_skill = Skill.query.filter_by(skill_name=new_name).first()

    if existing_skill and existing_skill.id != skill.id:
        return jsonify({'error': 'Skill name already exists'}), 400

    # ✅ Update safely
    skill.skill_name = new_name
    skill.skill_type = new_type

    try:
        db.session.commit()
        return jsonify({'message': 'Skill updated'})
    except Exception as e:
        db.session.rollback()
        print("🔥 ERROR:", str(e))  # VERY IMPORTANT
        return jsonify({'error': 'Update failed'}), 500

@skills_bp.route('/<int:skill_id>', methods=['DELETE'])
@jwt_required()
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return jsonify({'message': 'Skill deleted'})
