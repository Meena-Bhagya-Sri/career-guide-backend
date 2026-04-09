from extensions import db

class UserSkill(db.Model):
    __tablename__ = "user_skills"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id"), nullable=False)
    proficiency_level = db.Column(db.Integer, nullable=False)

    # 🔥 THIS LINE FIXES YOUR ERROR
    skill = db.relationship("Skill", backref="user_skills")
