# 🎯 CareerCatalyst AI — Agentic Resume Optimizer

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://agentic-ai-based-resume-optimizer.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-Google-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://makersuite.google.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

---

Most job seekers send the same resume to every application. ATS filters reject it before a recruiter ever reads it — not because the candidate is unqualified, but because the resume does not use the right keywords for that specific role.

**CareerCatalyst AI** is a full multi-agent career platform that goes far beyond simple resume tweaking. Paste a job description and your resume, and the system analyzes the gap, rewrites your resume, scores it for ATS compatibility, prepares you for interviews, researches the company, maps out your learning path, and gives you a networking strategy — all in one Streamlit app powered by the Gemini API and Python asyncio.


## 🔗 Live Demo

**Try it here → [agentic-ai-based-resume-optimizer.streamlit.app](https://agentic-ai-based-resume-optimizer.streamlit.app)**

Paste any job description and your current resume. The system handles the rest.

---

## ✨ Features

### Core Resume Pipeline
- **JD keyword extraction** — uses TF-IDF to identify the most important terms in any job description
- **Skill gap detection** — compares your resume to the JD using cosine similarity and highlights exactly what is missing
- **Resume rewriting** — Gemini API rewrites the weak sections to match the role naturally, not just stuffing in keywords
- **ATS compatibility scoring** — scores the rewritten resume so you can see the improvement
- **Resume critique** — detailed feedback on what your current resume is doing wrong before the rewrite

### Resume Testing and Analysis Tools
- **A/B resume testing** (`ab_testing.py`) — paste two versions of your resume and see which one scores better against the same job description
- **Resume comparison** (`resume_comparison.py`) — side by side view of your original resume vs the rewritten version
- **Resume health tracker** (`resume_health_track.py`) — an overall health score for your resume across multiple dimensions
- **Storytelling agent** (`storytelling_agent.py`) — rewrites your bullet points to follow a stronger narrative structure that reads better to humans
- **Interactive resume builder** (`interactive_builder.py`) — build or restructure your resume section by section with guided AI prompts
- **Mobile optimiser** (`mobile_optimizer.py`) — checks how your resume reads when viewed on a mobile device

### Career Intelligence
- **Interview preparation** (`interview_prep.py`) — generates likely interview questions for the specific role you applied to, with suggested talking points for each
- **Company research** (`company_research.py`) — surfaces relevant information about the company based on the job description and public signals
- **Culture fit analyser** (`culture_fit_analyzer.py`) — checks whether the tone and content of your resume match the company's stated values
- **Industry specialist** (`industry_specialist.py`) — gives tailored resume and application advice based on the specific industry the role is in
- **Market intelligence** (`market_intelligence.py`) — shows demand trends for the skills mentioned in the job description
- **Salary converter** (`salary_converter.py`) — estimates a realistic salary range for the role based on location and seniority signals
- **Learning path** (`learning_path.py`) — recommends specific skills or courses to close the gaps between your current profile and the role requirements
- **Networking engine** (`networking_engine.py`) — suggests who to connect with and gives you a message template to get referred into the company
- **Job search agent** (`job_search_agent.py`) — finds similar open roles to the one you pasted
- **Global optimiser** (`global_optimizer.py`) — adapts your resume format and language for different countries and hiring norms if the role is international

### Output and Visualisation
- **Visual analytics** (`visual_analytics.py`) — charts showing your keyword coverage, gap analysis, and score progression
- **Structured output** (`structured_output.py`) — exports all results in a clean structured format you can copy or save
- **Debate agent** (`debate_agent.py`) — two AI perspectives argue for and against your resume to surface blind spots a single reviewer would miss

### System Design
- **Async execution** — all agents run using Python `asyncio` with `asyncio.gather()` so multiple modules process concurrently
- **Multi-agent orchestration** (`orchestrator.py`, `agent_manager.py`) — coordinates which agents run, in what order, and how their outputs connect
- **File processing** (`file_processor.py`) — handles resume input whether pasted as text or uploaded as a file
- **Configurable** (`config.py`) — centralised configuration for model settings, thresholds, and feature flags

---

## ⚙️ How It Works

The system runs in two layers. The core pipeline handles your resume. The specialist agents add career intelligence on top.

**Stage 1 — JD Analysis** (`jd_analysis_agent.py`)
Runs TF-IDF on the job description. Filters out generic words and surfaces the role-specific terms that carry the most weight for this particular job. These become the benchmark your resume is measured against.

**Stage 2 — Resume Critique** (`resume_critique_agent.py`)
Converts both the JD and your resume into TF-IDF vectors. Computes cosine similarity to produce a gap score. Identifies which high-weight JD keywords are completely absent from your resume and which sections are weakest.

**Stage 3 — Resume Rewrite** (`resume_rewriter_agent.py`)
Sends the gap analysis plus your original resume to the Gemini API with a structured prompt. The model rewrites the underperforming sections — adding missing keywords in context, strengthening bullet points, and improving how your experience is framed for this specific role. The output is a real rewrite based on your content, not a template.

**Stage 4 — Final Scoring** (`final_scorer_agent.py`)
Runs the rewritten resume through the same TF-IDF and cosine similarity pipeline as Stage 2. The resulting score shows how much closer the new version is to the job description. This is your ATS compatibility score.

**Orchestration Layer** (`orchestrator.py`, `agent_manager.py`)
Once the core pipeline finishes, the orchestrator dispatches the specialist agents — interview prep, company research, learning path, market intelligence, salary estimation, culture fit, and others — concurrently using `asyncio.gather()`. Results are formatted by `structured_output.py` and visualised by `visual_analytics.py` before reaching the Streamlit UI.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Streamlit | Web interface and UI |
| scikit-learn | TF-IDF vectorisation and cosine similarity |
| pandas | Text preprocessing and data handling |
| Gemini API | All AI generation — rewriting, critique, interview prep, research |
| asyncio | Concurrent multi-agent execution |
| python-dotenv | Secure API key loading |

---

## 📊 Example Results

| Scenario | Original Score | After Rewrite |
|---|---|---|
| ML Engineer JD + generic resume | 38 / 100 | 92 / 100 |
| Data Analyst JD + project-focused resume | 51 / 100 | 88 / 100 |
| Backend Python JD + ML-heavy resume | 44 / 100 | 85 / 100 |

> Scores are computed using TF-IDF cosine similarity between the resume and the job description. Higher means stronger keyword alignment with the role.

---

## 📁 Project Structure

```
Agentic-AI-based-Resume-Optimizer/
│
├── app.py                       # Streamlit entry point — UI and tab routing
├── orchestrator.py              # Coordinates agent execution order
├── agent_manager.py             # Manages agent lifecycle and async dispatch
├── config.py                    # App-wide configuration and constants
│
├── jd_analysis_agent.py         # TF-IDF keyword extraction from job description
├── resume_critique_agent.py     # Cosine similarity gap analysis
├── resume_rewriter_agent.py     # Gemini API resume rewriting
├── final_scorer_agent.py        # ATS compatibility scoring
│
├── interview_prep.py            # Role-specific interview questions and answers
├── company_research.py          # Company background and culture signals
├── culture_fit_analyzer.py      # Culture fit check against company values
├── industry_specialist.py       # Industry-specific resume advice
├── market_intelligence.py       # Skill demand trends and market signals
├── salary_converter.py          # Salary range estimation
├── learning_path.py             # Skill gap to course recommendations
├── networking_engine.py         # Referral and networking strategy
├── job_search_agent.py          # Similar role discovery
├── global_optimizer.py          # International resume adaptation
├── debate_agent.py              # Two-perspective resume critique
│
├── resume_comparison.py         # Original vs rewritten side by side
├── resume_health_track.py       # Overall resume health score
├── ab_testing.py                # Compare two resume versions
├── storytelling_agent.py        # Narrative structure improvement
├── interactive_builder.py       # Section-by-section resume builder
├── mobile_optimizer.py          # Mobile view optimisation
│
├── visual_analytics.py          # Charts and keyword coverage visualisations
├── structured_output.py         # Structured results export
├── job_display.py               # Job result rendering
├── job_formatter.py             # Job data formatting
├── file_processor.py            # File upload parsing and cleaning
│
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Installation

**Clone the repository**

```bash
git clone https://github.com/shraddha-gidde/Agentic-AI-based-Resume-Optimizer.git
cd Agentic-AI-based-Resume-Optimizer
```

**Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

**Install all dependencies**

```bash
pip install -r requirements.txt
```

---

## 🔑 API Setup

This project uses the **Gemini API** for all AI generation. You need a free API key to run it locally.

**Step 1** — Get your free key from [Google AI Studio](https://makersuite.google.com/app/apikey)

**Step 2** — Create your `.env` file from the example template

```bash
cp .env.example .env
```

**Step 3** — Open `.env` and add your key

```
GEMINI_API_KEY=your_api_key_here
```

> Your `.env` file is already in `.gitignore`. Never commit it to GitHub.

---

## ▶️ How to Run

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

**How to use it:**
1. Paste the job description in the input panel
2. Paste your current resume or upload a file
3. Click **Analyze and Optimize**
4. Work through each tab — ATS score, keyword gap, rewritten resume, interview prep, company research, learning path, salary insights, and networking strategy

---

## 🔮 Future Improvements

- [ ] Side-by-side diff view showing exactly which sentences changed in the rewrite
- [ ] Batch mode — paste multiple job descriptions and get optimised resumes for all of them at once
- [ ] Section-level ATS score breakdown — separate scores for skills, experience, education, and summary
- [ ] Save and compare results across multiple sessions
- [ ] Option to run with a local open-source LLM as an alternative to the Gemini API

---

## 👩‍💻 Author

**Shraddha Gidde**
B.Tech — Artificial Intelligence and Data Science
MIT World Peace University, Pune

[![Portfolio](https://img.shields.io/badge/Portfolio-shraddha--gidde.netlify.app-2563EB?style=flat-square)](https://shraddha-gidde.netlify.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/shraddha-gidde-063506242)
[![GitHub](https://img.shields.io/badge/GitHub-shraddha--gidde-181717?style=flat-square&logo=github)](https://github.com/shraddha-gidde)

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
