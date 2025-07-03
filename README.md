# 📝 AI Resume & Cover Letter Generator with Recruiter Feedback

Generate polished, ATS-optimized resumes and cover letters tailored to any job description, and receive professional recruiter-style feedback — all in one Streamlit app powered by Langchain + Groq.

---

## 🚀 Features

✅ Generate high-level resumes & cover letters  
✅ Add multiple experiences & projects  
✅ Upload your existing resume (PDF)  
✅ Get detailed recruiter feedback on keywords, clarity, and ATS score  
✅ Download your resume & cover letter as PDFs

---

## 🛠️ Tech Stack

- Python 3.8+
- Streamlit
- Langchain + Groq
- fpdf (PDF generation)
- pdfplumber (resume parsing)

---

## ⚙️ Setup

```bash
git clone https://github.com/Nilkamal21/Resume-Feedback-GenAI
cd Resume-Feedback-GenAI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run locally:
```bash
streamlit run app.py
```

---

## 🌐 Deployment

Host easily with [Streamlit Community Cloud](https://streamlit.io/cloud) — don’t forget to set environment variables.

---

## 📄 License

MIT License – free to use and adapt.
