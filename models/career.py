from extensions import db

class Career(db.Model):
    __tablename__ = "careers"

    id = db.Column(db.Integer, primary_key=True)
    career_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    avg_salary = db.Column(db.String(50))
    difficulty_level = db.Column(db.String(20))