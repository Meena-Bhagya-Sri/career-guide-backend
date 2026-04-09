from extensions import db

class CareerSkillMapping(db.Model):
    __tablename__ = "career_skill_mapping"

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.career_id", ondelete="CASCADE"))
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"))
    importance_level = db.Column(db.Integer, default=3)

    skill = db.relationship("Skill", backref="career_mappings")