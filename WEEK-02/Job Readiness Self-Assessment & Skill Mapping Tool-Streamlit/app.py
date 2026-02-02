import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io

# -----------------------------
# Configuration
# -----------------------------
PROFICIENCY_LEVELS = {
    "Beginner": 1,
    "Intermediate": 2,
    "Advanced": 3
}

ROLES = {
    "Data Analyst": {
        "Excel": 3,
        "SQL": 2,
        "Python (Pandas & NumPy)": 2,
        "Data Visualization": 2,
        "Statistics": 2
    },
    "Data Scientist": {
        "Python (Pandas & NumPy)": 3,
        "Statistics": 3,
        "Machine Learning": 2,
        "SQL": 2,
        "Data Visualization": 2
    },
    "Machine Learning Engineer": {
        "Python": 3,
        "Machine Learning": 3,
        "Deep Learning": 2,
        "Statistics": 2,
        "Model Deployment": 2
    },
    "AI / GenAI Engineer": {
        "Python": 3,
        "Machine Learning": 3,
        "LLMs & Prompt Engineering": 2,
        "APIs & Integration": 2,
        "RAG & Vector Databases": 2
    }
}

LEARNING_RESOURCES = {
    "Excel": ["Microsoft Learn Excel", "Excel for Data Analysis – Coursera"],
    "SQL": ["Mode SQL Tutorial", "LeetCode SQL Problems"],
    "Python (Pandas & NumPy)": ["Pandas Documentation", "freeCodeCamp Data Analysis"],
    "Data Visualization": ["Power BI Docs", "Tableau Public Tutorials"],
    "Statistics": ["StatQuest YouTube", "Khan Academy Statistics"],
    "Machine Learning": ["Andrew Ng ML Course", "Hands-On ML Book"],
    "Deep Learning": ["DeepLearning.AI Specialization"],
    "Model Deployment": ["FastAPI Docs", "ML Deployment on Hugging Face"],
    "LLMs & Prompt Engineering": ["OpenAI Prompt Guide", "LangChain Docs"],
    "APIs & Integration": ["REST API Fundamentals"],
    "RAG & Vector Databases": ["Pinecone Docs", "LangChain RAG Guide"]
}

# -----------------------------
# Core Evaluation Logic
# -----------------------------
def evaluate_readiness(role, user_skills):
    required_skills = ROLES[role]
    total_weight = sum(required_skills.values()) * 3
    score = 0

    fully_met = []
    needs_improvement = []
    missing = []

    for skill, req_level in required_skills.items():
        if skill in user_skills:
            user_level = user_skills[skill]
            score += min(user_level, req_level) * 3

            if user_level >= req_level:
                fully_met.append(skill)
            else:
                needs_improvement.append({
                    "skill": skill,
                    "required": req_level,
                    "current": user_level
                })
        else:
            missing.append(skill)

    readiness = round((score / total_weight) * 100, 1)
    return readiness, fully_met, needs_improvement, missing

# -----------------------------
# Learning Roadmap
# -----------------------------
def build_roadmap(needs_improvement, missing):
    roadmap = []

    for item in needs_improvement:
        roadmap.append({
            "skill": item["skill"],
            "priority": "High",
            "resources": LEARNING_RESOURCES.get(item["skill"], [])
        })

    for skill in missing:
        roadmap.append({
            "skill": skill,
            "priority": "Critical",
            "resources": LEARNING_RESOURCES.get(skill, [])
        })

    return roadmap

# -----------------------------
# PDF Export
# -----------------------------
def generate_pdf(role, score, fully_met, needs_improvement, missing, roadmap):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 40
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, y, "Job Readiness Assessment Report")

    y -= 30
    pdf.setFont("Helvetica", 11)
    pdf.drawString(40, y, f"Target Role: {role}")
    y -= 20
    pdf.drawString(40, y, f"Overall Readiness Score: {score}%")

    y -= 30
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Skills Fully Met:")
    y -= 15
    pdf.setFont("Helvetica", 10)
    for s in fully_met:
        pdf.drawString(60, y, f"- {s}")
        y -= 12

    y -= 15
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Skills Needing Improvement:")
    y -= 15
    pdf.setFont("Helvetica", 10)
    for s in needs_improvement:
        pdf.drawString(60, y, f"- {s['skill']} (Current: {s['current']}, Required: {s['required']})")
        y -= 12

    y -= 15
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Missing Skills:")
    y -= 15
    pdf.setFont("Helvetica", 10)
    for s in missing:
        pdf.drawString(60, y, f"- {s}")
        y -= 12

    y -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(40, y, "Recommended Learning Roadmap:")
    y -= 15
    pdf.setFont("Helvetica", 10)
    for r in roadmap:
        pdf.drawString(60, y, f"- {r['skill']} ({r['priority']})")
        y -= 12

    pdf.save()
    buffer.seek(0)
    return buffer

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Job Readiness & Skill Mapping", layout="centered")

st.title("Job Readiness Self-Assessment & Skill Mapping Tool")
st.write("Understand where you stand and what to focus on next.")

role = st.selectbox("Select your target role", list(ROLES.keys()))

st.subheader("Select your current skills and proficiency")
user_skills = {}

for skill in ROLES[role]:
    level = st.selectbox(
        f"{skill} level",
        ["Not Learned", "Beginner", "Intermediate", "Advanced"]
    )
    if level != "Not Learned":
        user_skills[skill] = PROFICIENCY_LEVELS[level]

if st.button("Evaluate Readiness"):
    score, fully_met, needs_improvement, missing = evaluate_readiness(role, user_skills)
    roadmap = build_roadmap(needs_improvement, missing)

    st.subheader("Overall Readiness Score")
    st.metric("Readiness", f"{score}%")

    st.subheader("✅ Skills Fully Met")
    st.write(fully_met if fully_met else "None")

    st.subheader("⚠️ Skills Needing Improvement")
    st.write(needs_improvement if needs_improvement else "None")

    st.subheader("❌ Missing Skills")
    st.write(missing if missing else "None")

    st.subheader("📚 Suggested Learning Roadmap")
    for item in roadmap:
        st.write(f"**{item['skill']}** ({item['priority']})")
        for r in item["resources"]:
            st.write(f"- {r}")

    pdf_file = generate_pdf(role, score, fully_met, needs_improvement, missing, roadmap)
    st.download_button(
        "Download Assessment Report (PDF)",
        pdf_file,
        file_name="job_readiness_report.pdf"
    )

st.caption("More roles and AI-powered insights coming soon.")
