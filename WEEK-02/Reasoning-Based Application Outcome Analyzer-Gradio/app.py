import gradio as gr

# -------------------------------
# Reasoning Engine (Core Logic)
# -------------------------------

def analyze_application(
    application_type,
    role_type,
    cgpa,
    institution_tier,
    experience_years,
    experience_types,
    skill_confidence,
    resume_submitted,
    cover_letter,
    sop,
    references,
    referral,
    competitiveness,
    rejection_count,
    interviews
):
    beliefs = []
    inferences = []
    focus_actions = []
    reassurance = ""

    # ---- Academic Signal ----
    if application_type in ["Scholarship", "Program"] and cgpa < 3.0:
        beliefs.append("Your academic score is the main reason for rejection.")
        inferences.append(
            "For academic programs, CGPA does play a strong screening role. "
            "However, it is rarely the only deciding factor."
        )
    elif application_type in ["Internship", "Job"]:
        beliefs.append("Your CGPA caused the rejection.")
        inferences.append(
            "For internships and jobs, CGPA is usually a weak signal unless extremely low. "
            "Most rejections are not CGPA-driven."
        )

    # ---- Experience Signal ----
    if experience_years < 1:
        beliefs.append("You lack enough experience.")
        inferences.append(
            "Early-career roles often reject due to competition, not lack of experience alone."
        )

    # ---- Document Misattribution ----
    if application_type in ["Internship", "Job"] and not cover_letter:
        beliefs.append("Missing a cover letter caused rejection.")
        inferences.append(
            "Cover letters are often optional and rarely decisive unless explicitly required."
        )

    if application_type in ["Scholarship", "Program"] and not sop:
        beliefs.append("Missing SOP guaranteed rejection.")
        inferences.append(
            "Missing required documents can matter, but strong applicants are sometimes still reviewed."
        )

    # ---- Referral Myth ----
    if referral and not interviews:
        beliefs.append("Referral failed, so my profile is weak.")
        inferences.append(
            "Referrals increase visibility but do not override competition or role saturation."
        )

    # ---- Market Reality ----
    if competitiveness in ["High", "Unsure"] and interviews == "No":
        inferences.append(
            "High competition significantly reduces interview probability, even for strong profiles."
        )

    # ---- Counterfactual Reasoning ----
    focus_actions.append(
        "Improve differentiation signals (projects, specialization, visible impact) rather than completeness."
    )
    focus_actions.append(
        "Target narrower roles instead of increasing application volume."
    )

    # ---- Emotional Grounding ----
    if rejection_count > 5 and interviews == "No":
        reassurance = (
            "Repeated rejections in competitive markets do NOT strongly indicate personal inadequacy. "
            "They often reflect oversupply and signal similarity."
        )

    # ---- Output Formatting ----
    output = "🧠 **What you may be assuming:**\n"
    for b in beliefs:
        output += f"- {b}\n"

    output += "\n🔍 **What the system infers instead:**\n"
    for i in inferences:
        output += f"- {i}\n"

    output += "\n🎯 **What actually deserves your focus:**\n"
    for f in focus_actions:
        output += f"- {f}\n"

    if reassurance:
        output += f"\n🧘 **Contextual reassurance:**\n- {reassurance}\n"

    return output


# -------------------------------
# Gradio UI
# -------------------------------

with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # Reasoning-Based Application Outcome Analyzer  
        This tool helps you understand **why rejections may not mean what you think**.  
        It corrects common misattributions using reasoning, not judgment.
        """
    )

    with gr.Tab("Context"):
        application_type = gr.Dropdown(
            ["Internship", "Job", "Scholarship", "Program"],
            label="Application Type"
        )
        role_type = gr.Dropdown(
            ["Technical", "Research", "Corporate", "Academic"],
            label="Role Type"
        )

    with gr.Tab("Background"):
        cgpa = gr.Number(label="CGPA", value=3.0)
        institution_tier = gr.Dropdown(
            ["Top-tier", "Mid-tier", "Unknown", "Private"],
            label="Institution Tier"
        )
        experience_years = gr.Number(label="Years of Experience", value=0)
        experience_types = gr.CheckboxGroup(
            ["Internships", "Projects", "Freelance", "Research"],
            label="Experience Types"
        )

    with gr.Tab("Self-Perception"):
        skill_confidence = gr.Radio(
            ["Weak", "Average", "Strong"],
            label="Overall Skill Confidence"
        )

    with gr.Tab("Application Signals"):
        resume_submitted = gr.Radio(["Yes", "No"], label="Resume Submitted?")
        cover_letter = gr.Radio(["Yes", "No"], label="Cover Letter Submitted?")
        sop = gr.Radio(["Yes", "No"], label="Statement of Purpose Submitted?")
        references = gr.Radio(["Yes", "No"], label="References Submitted?")

    with gr.Tab("Market Context"):
        referral = gr.Radio(["Yes", "No"], label="Referral Present?")
        competitiveness = gr.Dropdown(
            ["Low", "Medium", "High", "Unsure"],
            label="Perceived Role Competitiveness"
        )
        rejection_count = gr.Slider(0, 20, step=1, label="Number of Rejections")
        interviews = gr.Radio(["Yes", "No"], label="Any Interviews?")

    analyze_btn = gr.Button("Analyze My Outcome")

    output = gr.Markdown()

    analyze_btn.click(
        analyze_application,
        inputs=[
            application_type,
            role_type,
            cgpa,
            institution_tier,
            experience_years,
            experience_types,
            skill_confidence,
            resume_submitted,
            cover_letter,
            sop,
            references,
            referral,
            competitiveness,
            rejection_count,
            interviews
        ],
        outputs=output
    )

demo.launch()
