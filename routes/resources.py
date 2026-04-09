from flask import Blueprint, request, jsonify
from models import db, Resource

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/', methods=['POST'])
def create_resource():
    data = request.get_json()
    resource = Resource(
        roadmap_id=data['roadmap_id'],
        resource_title=data['resource_title'],
        resource_link=data['resource_link'],
        resource_type=data['resource_type']
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({'message': 'Resource created', 'id': resource.id})

@resources_bp.route('/', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([
        {
            'id': r.id,
            'roadmap_id': r.roadmap_id,
            'resource_title': r.resource_title,
            'resource_link': r.resource_link,
            'resource_type': r.resource_type
        } for r in resources
    ])

@resources_bp.route('/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    data = request.get_json()
    resource.resource_title = data.get('resource_title', resource.resource_title)
    resource.resource_link = data.get('resource_link', resource.resource_link)
    resource.resource_type = data.get('resource_type', resource.resource_type)
    db.session.commit()
    return jsonify({'message': 'Resource updated'})

@resources_bp.route('/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({'message': 'Resource deleted'})
