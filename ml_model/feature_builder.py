import numpy as np
from models import db, Skill, UserSkill
from ml_model.feature_config import SKILL_FEATURES


def build_skill_vector(user_id: int):
    """
    Builds ML-ready skill vector for a user.
    Missing skills are filled with 0.
    """

    # 1️⃣ Get all skills from DB
    skills = Skill.query.all()
    skill_name_to_id = {
        skill.skill_name: skill.id
        for skill in skills
    }

    # 2️⃣ Get user's skills
    user_skills = (
        db.session.query(UserSkill.skill_id, UserSkill.proficiency_level)
        .filter(UserSkill.user_id == user_id)
        .all()
    )

    # Convert to dict: {skill_id: level}
    user_skill_map = {
        skill_id: level
        for skill_id, level in user_skills
    }

    # 3️⃣ Build vector in correct order
    vector = []

    for skill_name in SKILL_FEATURES:
        skill_id = skill_name_to_id.get(skill_name)

        if skill_id and skill_id in user_skill_map:
            vector.append(user_skill_map[skill_id])
        else:
            vector.append(0)  # Missing skill → 0

    # 4️⃣ Return as numpy array (1 row)
    return np.array(vector).reshape(1, -1)