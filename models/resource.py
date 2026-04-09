from extensions import db

class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmaps.id", ondelete="CASCADE"))
    # name = db.Column(db.String(100))
    resource_title = db.Column(db.String(200))
    resource_link = db.Column(db.Text)
    resource_type = db.Column(db.String(50))
