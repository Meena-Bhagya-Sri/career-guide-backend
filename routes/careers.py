from flask import Blueprint, request, jsonify
from models import db, Career

careers_bp = Blueprint('careers', __name__)

# GET all careers
@careers_bp.route('/', methods=['GET'])
def get_careers():
    careers = Career.query.all()
    return jsonify([
        {
            'career_id': c.id,
            'career_name': c.career_name,
            'avg_salary': c.avg_salary,
            'difficulty_level': c.difficulty_level,
            'description': c.description
        } for c in careers
    ])

# POST create a new career
@careers_bp.route('/', methods=['POST'])
def create_career():
    data = request.get_json()
    career = Career(
        career_name=data.get('career_name'),
        avg_salary=data.get('avg_salary'),
        difficulty_level=data.get('difficulty_level'),
        description=data.get('description')
    )
    db.session.add(career)
    db.session.commit()
    return jsonify({'message': 'Career created', 'career_id': career.id}), 201

# PUT update an existing career
@careers_bp.route('/<int:career_id>', methods=['PUT'])
def update_career(career_id):
    career = Career.query.get_or_404(career_id)
    data = request.get_json()
    career.career_name = data.get('career_name', career.career_name)
    career.avg_salary = data.get('avg_salary', career.avg_salary)
    career.difficulty_level = data.get('difficulty_level', career.difficulty_level)
    career.description = data.get('description', career.description)
    db.session.commit()
    return jsonify({'message': 'Career updated'})

# DELETE a career
@careers_bp.route('/<int:career_id>', methods=['DELETE'])
def delete_career(career_id):
    career = Career.query.get_or_404(career_id)
    db.session.delete(career)
    db.session.commit()
    return jsonify({'message': 'Career deleted'})
