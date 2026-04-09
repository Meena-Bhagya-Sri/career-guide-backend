from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import extract

from models import db, User, Skill, Career, Roadmap, Resource
from flask_jwt_extended import jwt_required
from routes.auth import role_required

admin_bp = Blueprint("admin", __name__)


# ================= DASHBOARD STATS =================
@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@role_required("admin")
def dashboard_stats():

    return jsonify({
        "total_users": User.query.count(),
        "total_skills": Skill.query.count(),
        "total_careers": Career.query.count(),
        "total_roadmaps": Roadmap.query.count(),
        "total_resources": Resource.query.count()
    })


# ================= ANALYTICS =================
@admin_bp.route("/analytics", methods=["GET"])
@jwt_required()
@role_required("admin")
def analytics():

    year = request.args.get("year", default=datetime.now().year, type=int)

    monthly_users = []

    for month in range(1, 13):

        count = User.query.filter(
            extract("year", User.created_at) == year,
            extract("month", User.created_at) == month
        ).count()

        monthly_users.append(count)

    return jsonify({
        "monthlyUsers": monthly_users
    })