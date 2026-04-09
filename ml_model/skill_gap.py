from models import UserSkill, Skill, CareerSkillMapping, Career

def calculate_skill_gap(user_id, career_id):

    career = Career.query.get(career_id)

    # Get required skills for the career
    career_skills = (
        CareerSkillMapping.query
        .join(Skill, Skill.id == CareerSkillMapping.skill_id)
        .filter(CareerSkillMapping.career_id == career_id)
        .all()
    )

    # Get user's skills
    user_skills = {
        us.skill_id: us.proficiency_level
        for us in UserSkill.query.filter_by(user_id=user_id).all()
    }

    gap_report = []
    improvement_needed = 0

    for cs in career_skills:

        skill = Skill.query.get(cs.skill_id)

        required = cs.importance_level
        user_level = user_skills.get(cs.skill_id, 0)

        gap = required - user_level

        status = "Good" if gap <= 0 else "Needs Improvement"

        if gap > 0:
            improvement_needed += 1

        gap_report.append({
            "name": skill.skill_name if skill else "Unknown",
            "required": required,
            "yours": user_level,
            "gap": max(gap, 0),
            "status": status
        })

    total_skills = len(career_skills)

    readiness = int(((total_skills - improvement_needed) / total_skills) * 100) if total_skills > 0 else 0

    return {
        "career": career.career_name if career else "Unknown Career",
        "readiness": readiness,
        "total_skills": total_skills,
        "improvement_needed": improvement_needed,
        "skills": gap_report
    }