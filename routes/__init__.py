from flask import Flask

from .users import users_bp
from .skills import skills_bp
from .careers import careers_bp
from .user_skills import user_skills_bp
from .roadmaps import roadmaps_bp
from .resources import resources_bp
from .auth import auth_bp 
# from .recommendations import recommend_career_ml
from .recommendations import recommendations_bp
from .academicpProfile import academic_bp
from .admin import admin_bp

def register_routes(app: Flask):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(skills_bp, url_prefix='/skills')
    app.register_blueprint(careers_bp, url_prefix='/careers')
    app.register_blueprint(user_skills_bp, url_prefix="/user_skills")
    app.register_blueprint(roadmaps_bp, url_prefix='/roadmaps')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    app.register_blueprint(recommendations_bp, url_prefix="/recommendations")
    app.register_blueprint(academic_bp,url_prefix="/academic-profile")
    app.register_blueprint(admin_bp, url_prefix="/admin")