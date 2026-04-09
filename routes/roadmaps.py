from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Roadmap, Career, Resource

roadmaps_bp = Blueprint("roadmaps", __name__)
@roadmaps_bp.route("/", methods=["GET"])

def get_all_roadmaps():
    roadmaps = Roadmap.query.all()
    data = []
    for r in roadmaps:
        career = Career.query.get(r.career_id)
        data.append({
            "roadmap_id": r.id,
            "career_name": career.career_name if career else None,
            "step_number": r.stage_number,
            "step_title": r.stage_title,
            "description": r.description
        })
    return jsonify(data), 200

# GET roadmap for a career
@roadmaps_bp.route("/<int:career_id>", methods=["GET"])

def get_career_roadmap(career_id):
    career = Career.query.get_or_404(career_id)

    stages = (
        Roadmap.query
        .filter_by(career_id=career_id)
        .order_by(Roadmap.stage_number)
        .all()
    )

    roadmap_data = []
    for stage in stages:
        resources = Resource.query.filter_by(roadmap_id=stage.id).all()
        roadmap_data.append({
            "roadmap_id": stage.id,
            "stage_number": stage.stage_number,
            "stage_title": stage.stage_title,
            "description": stage.description,
            "resources": [
                {
                    "resource_title": r.resource_title,
                    "resource_type": r.resource_type,
                    "resource_link": r.resource_link
                }
                for r in resources
            ]
        })

    return jsonify({
        "career": {
            "career_id": career.id,
            "career_name": career.career_name
        },
        "total_stages": len(roadmap_data),
        "roadmap": roadmap_data
    }), 200

# POST create a roadmap stage
@roadmaps_bp.route("/", methods=["POST"])
def create_roadmap():
    data = request.get_json()
    career = Career.query.filter_by(career_name=data.get("career_name")).first_or_404()
    roadmap = Roadmap(
        stage_number=data.get("stage_number"),
        career_id=career.id,
        stage_title=data.get("stage_title"),
        description=data.get("description")
    )
    db.session.add(roadmap)
    db.session.commit()
    return jsonify({"message": "Roadmap stage created", "roadmap_id": roadmap.id}), 201

# PUT update a roadmap stage
@roadmaps_bp.route("/<int:roadmap_id>", methods=["PUT"])
def update_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    data = request.get_json()
    roadmap.stage_number = data.get("stage_number", roadmap.stage_number)
    roadmap.stage_title = data.get("stage_title", roadmap.stage_title)
    roadmap.description = data.get("description", roadmap.description)
    db.session.commit()
    return jsonify({"message": "Roadmap stage updated"})

# DELETE a roadmap stage
@roadmaps_bp.route("/<int:roadmap_id>", methods=["DELETE"])
def delete_roadmap(roadmap_id):
    roadmap = Roadmap.query.get_or_404(roadmap_id)
    db.session.delete(roadmap)
    db.session.commit()
    return jsonify({"message": "Roadmap stage deleted"})
