from extensions import db

class AcademicProfile(db.Model):
    __tablename__ = "academic_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    highest_qualification = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    cgpa = db.Column(db.Numeric(3, 2))
    interests = db.Column(db.Text)
    skills_known = db.Column(db.Text)
    

