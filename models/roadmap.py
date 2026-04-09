from extensions import db

class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True)
    stage_number = db.Column(db.Integer)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"))
    stage_title = db.Column(db.String(100))
    # steps = db.Column(db.ARRAY(db.String))
    description = db.Column(db.String(500))
