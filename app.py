import streamlit as st
from dotenv import load_dotenv
import os
from io import BytesIO
from fpdf import FPDF
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import unicodedata
import pdfplumber

# Load .env
load_dotenv()

# Initialize LLM from Groq
llm = ChatGroq(model_name="llama3-8b-8192")

st.set_page_config(page_title="AI Resume & Feedback Generator", page_icon="📝", layout="wide")
st.title("📝 Advanced AI Resume & Cover Letter Generator with Professional Recruiter Feedback")

st.markdown("---")

# --- Candidate Information Section ---
st.header("👤 Candidate Information")

name = st.text_input("Full Name", key="name_input")

education_level = st.selectbox(
    "Highest Education",
    [
        "High School",
        "Diploma",
        "Bachelor's",
        "Master's",
        "PhD",
        "Other"
    ],
    index=2,
    key="education_select"
)

field_of_study = st.text_input(
    "Field of Study / Major",
    placeholder="E.g., Computer Science, Mechanical Engineering...",
    key="field_input"
)

university_name = st.text_input(
    "University/College Name",
    placeholder="E.g., IIT Bombay, Stanford University...",
    key="university_input"
)

cgpa = st.text_input(
    "CGPA / Percentage",
    placeholder="E.g., 8.6 CGPA or 78%",
    key="cgpa_input"
)

current_location = st.text_input(
    "Current Location (City, State/Country)",
    placeholder="E.g., Bangalore, India",
    key="location_input"
)

contact_email = st.text_input(
    "Contact Email",
    placeholder="E.g., name@example.com",
    key="email_input"
)

phone_number = st.text_input(
    "Phone Number",
    placeholder="E.g., +91-XXXXXXXXXX",
    key="phone_input"
)

linkedin_url = st.text_input(
    "LinkedIn/GitHub Profile URL (Optional)",
    placeholder="E.g., https://linkedin.com/in/username",
    key="linkedin_input"
)

achievements = st.text_area(
    "Key Achievements (Optional, leave blank if none):",
    placeholder="E.g., Improved system performance by 30%, led a team of 5 developers...",
    key="achievements_input"
)

st.markdown("---")

# --- Experience Section ---
st.header("💼 Professional Experience (Optional)")

experience_entries = []
num_experiences = st.number_input(
    "Number of previous companies you worked at (set 0 if fresher):",
    min_value=0, max_value=10, value=0, step=1, key="num_exp"
)

for i in range(int(num_experiences)):
    st.markdown(f"**Experience #{i+1}**")
    company = st.text_input(f"Company Name #{i+1}", key=f"company_{i}")
    role = st.text_input(f"Role/Position #{i+1}", key=f"role_{i}")
    duration = st.text_input(f"Duration (e.g., 1 year 6 months) #{i+1}", key=f"duration_{i}")
    experience_entries.append({"company": company, "role": role, "duration": duration})

# --- Projects Section ---
st.header("🚀 Projects (Optional)")

project_entries = []
num_projects = st.number_input(
    "Number of projects you want to showcase:",
    min_value=0, max_value=10, value=0, step=1, key="num_proj"
)

for i in range(int(num_projects)):
    project_name = st.text_input(f"Project Name #{i+1}", key=f"proj_{i}")
    project_entries.append(project_name)

st.markdown("---")

st.header("🏢 Company Details for Cover Letter")

hiring_manager = st.text_input(
    "Hiring Manager's Name",
    placeholder="E.g., Ms. Priya Sharma",
    key="hiring_manager_input"
)

company_name = st.text_input(
    "Company Name",
    placeholder="E.g., DataCorp",
    key="company_name_input"
)

company_address = st.text_area(
    "Company Address",
    placeholder="E.g., 123 Analytics Avenue, Data City, Country",
    key="company_address_input"
)
cover_letter_date = st.date_input(
    "Date for Cover Letter",
    key="cover_letter_date_input"
)


# --- Job Description Section ---
st.header("📄 Job Description")

job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="Copy-paste the job description of the role you’re applying for...",
    key="job_desc_input"
)

st.markdown("---")

# --- Optional Resume Upload ---
uploaded_resume_text = ""

st.header("📎 Upload Existing Resume (Optional)")

uploaded_resume = st.file_uploader(
    "Upload your existing resume PDF to provide additional context (optional):",
    type=["pdf"]
)

if uploaded_resume is not None:
    st.info("✅ Uploaded resume detected — parsing content...")
    try:
        with pdfplumber.open(uploaded_resume) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            uploaded_resume_text = "\n".join(pages).strip()
        if uploaded_resume_text:
            st.success("Resume parsed successfully and included in your profile!")
        else:
            st.warning("Uploaded resume has no readable text. Make sure it's not scanned as an image-only PDF.")
    except Exception as e:
        st.error(f"Error parsing uploaded resume: {e}")

st.markdown("---")

if not name or not job_description:
    st.warning("Please fill in your name and paste a job description to continue.")
else:
    # Assemble candidate data text
    experience_summary = ""
    if experience_entries:
        for idx, exp in enumerate(experience_entries, 1):
            if exp["company"].strip() or exp["role"].strip() or exp["duration"].strip():
                experience_summary += f"\n- Experience {idx}: {exp['role']} at {exp['company']} for {exp['duration']}."
    else:
        experience_summary = "\nNo professional experience provided."

    project_summary = ""
    if project_entries:
        for idx, proj in enumerate(project_entries, 1):
            if proj.strip():
                project_summary += f"\n- Project {idx}: {proj}"
    else:
        project_summary = "\nNo projects provided."

    candidate_info = f"""
    Name: {name}
    Education: {education_level} in {field_of_study if field_of_study.strip() else '[Not provided]'}
    University/College: {university_name if university_name.strip() else '[Not provided]'}
    CGPA/Percentage: {cgpa if cgpa.strip() else '[Not provided]'}
    Location: {current_location if current_location.strip() else '[Not provided]'}
    Contact Email: {contact_email if contact_email.strip() else '[Not provided]'}
    Phone: {phone_number if phone_number.strip() else '[Not provided]'}
    LinkedIn/GitHub: {linkedin_url if linkedin_url.strip() else '[Not provided]'}
    Professional Experiences:{experience_summary}
    Projects:{project_summary}
    Achievements: {achievements if achievements.strip() else 'None provided.'}
    Hiring Manager: {hiring_manager if hiring_manager.strip() else '[Not provided]'}
    Company Name: {company_name if company_name.strip() else '[Not provided]'}
    Company Address: {company_address if company_address.strip() else '[Not provided]'}
    Cover Letter Date: {cover_letter_date.strftime('%B %d, %Y')}
    """
    if uploaded_resume_text:
        candidate_info += f"\n\nUploaded Resume Note: {uploaded_resume_text}"

    col1, col2 = st.columns(2)

    # --- Resume & Cover Letter Generation ---
    with col1:
        if st.button("🚀 Generate High-Level Resume & Cover Letter", key="generate_resume_btn"):
            with st.spinner("Generating polished resume and exceptional cover letter..."):
                resume_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are an executive-level resume writer creating ATS-optimized documents."),
                    ("human", 
                     """Candidate Information:
                     {resume_info}

                     Job Description:
                     {job_description}

                     Task:
                    - Create a polished, high-level resume integrating the candidate’s experiences, projects, achievements, and education with keywords from the job description.
                    - For each project name, generate a professional one-line description relevant to the job description and candidate background.
                    - Organize resume into: Professional Summary, Key Skills, Experience Highlights, Projects, and Education.
                    - Then generate a separate, formal cover letter addressed to the hiring manager.
                    - The cover letter **must include at the top**: the selected date, the hiring manager’s name, the company name, and the company address exactly as provided by the candidate.
                    - Mark sections clearly with "=== Resume ===" and "=== Cover Letter ===".
                    """)
                ])
                resume_chain = LLMChain(llm=llm, prompt=resume_prompt)
                resume_result = resume_chain.invoke({
                    "resume_info": candidate_info,
                    "job_description": job_description
                })

                generated_text = resume_result["text"]

                # Split resume and cover letter
                resume_text, cover_letter_text = "", ""
                if "=== Cover Letter ===" in generated_text:
                    parts = generated_text.split("=== Cover Letter ===")
                    resume_text = parts[0].replace("=== Resume ===", "").strip()
                    cover_letter_text = parts[1].strip()
                else:
                    resume_text = generated_text.strip()
                 # Remove boilerplate first line if present
                if resume_text.lower().startswith("here is the polished"):
                    resume_text = "\n".join(resume_text.split("\n")[1:]).strip()
                st.subheader("📄 Generated Resume:")
                st.markdown(f"""
                <div style="
                    border:2px solid #4CAF50;
                    padding:20px;
                    border-radius:10px;
                    background-color:#ffffff !important;
                ">
                <pre style="
                    white-space:pre-wrap;
                    color:#000000 !important;
                ">{resume_text}</pre>
                </div>
                """, unsafe_allow_html=True)



                def safe_text(text):
                    return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")    

                def generate_pdf(text, filename="document.pdf"):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    safe_txt = safe_text(text)
                    for line in text.split("\n"):
                        pdf.multi_cell(0, 10, line)
                    pdf_bytes = pdf.output(dest="S").encode("latin1")  # get PDF as bytes
                    pdf_output = BytesIO(pdf_bytes)
                    pdf_output.seek(0)
                    return pdf_output

                resume_pdf = generate_pdf(resume_text, "generated_resume.pdf")
                st.download_button(
                    label="⬇️ Download Resume as PDF",
                    data=resume_pdf,
                    file_name="generated_resume.pdf",
                    mime="application/pdf",
                    key="download_resume_btn"
                )

                if cover_letter_text:
                    st.subheader("✉️ Generated Cover Letter:")
                    st.markdown(f"""
                    <div style="
                        border:2px solid #2196F3;
                        padding:20px;
                        border-radius:10px;
                        background-color:#ffffff !important;
                    ">
                    <pre style="
                        white-space:pre-wrap;
                        color:#000000 !important;
                    ">{cover_letter_text}</pre>
                    </div>
                    """, unsafe_allow_html=True)



                    cover_pdf = generate_pdf(cover_letter_text, "generated_cover_letter.pdf")
                    st.download_button(
                        label="⬇️ Download Cover Letter as PDF",
                        data=cover_pdf,
                        file_name="generated_cover_letter.pdf",
                        mime="application/pdf",
                        key="download_cover_btn"
                    )

    # --- Professional Recruiter Feedback ---
    with col2:
        if st.button("🔎 Get Professional Recruiter Feedback", key="feedback_btn"):
            with st.spinner("Generating detailed recruiter feedback..."):
                feedback_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a senior recruiter and ATS optimization specialist."),
                    ("human",
                     """Here is the candidate's resume:

                     {generated_resume}

                     And here is the job description:

                     {job_description}

                     Task: Provide a professional recruiter-style report with:
                     1) Detailed analysis of missing or weak keywords compared to the job description.
                     2) Evaluation of clarity, relevance, and impact of resume sections.
                     3) Overall ATS-friendliness score out of 100 with explanation.
                     4) Specific, actionable recommendations to optimize the resume for recruiters and ATS systems.
                     Use a confident, formal, professional tone.
                     """)
                ])
                feedback_chain = LLMChain(llm=llm, prompt=feedback_prompt)
                feedback_result = feedback_chain.invoke({
                    "generated_resume": candidate_info,
                    "job_description": job_description
                })
                st.subheader("🧐 Professional Recruiter Feedback:")
                st.markdown(f"""
                <div style="
                    border:2px solid #FF9800;
                    padding:20px;
                    border-radius:10px;
                    background-color:#ffffff !important;
                ">
                <pre style="
                    white-space:pre-wrap;
                    color:#000000 !important;
                ">{feedback_result["text"]}</pre>
                </div>
                """, unsafe_allow_html=True)
