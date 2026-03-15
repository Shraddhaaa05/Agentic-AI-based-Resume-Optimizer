# 🎯 CareerCatalyst AI — Agentic Resume Optimizer

> An async multi-agent AI pipeline that rewrites resumes for ATS compatibility and scores them — the rewritten output scores 92 on ATS checks.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://agentic-ai-based-resume-optimizer.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## The problem

Most job seekers applying to many roles at once do not have time to rewrite their resume for every job description. But ATS filters scan resumes for specific keywords before a human ever reads them. A good candidate with a generic resume often gets filtered out before anyone sees their name.

---

## How it works

The system runs four agents in sequence. Within each stage, fifteen modules execute at the same time using `asyncio.gather()` to keep things fast.

```
Job Description Text Input
         │
         ▼
┌────────────────────────────────────────────────────────┐
│         asyncio.gather() — 15 concurrent modules        │
│                                                        │
│  Agent 1           Agent 2           Agent 3           │
│  JD Analysis       Resume Critique   Intelligent       │
│                                      Rewrite           │
│  Uses TF-IDF to    Runs cosine sim   Sends gap         │
│  extract key       to find where     analysis to       │
│  keywords from     the resume falls  Gemini API for    │
│  the JD            short             structured        │
│                                      rewriting         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
                    Agent 4
                    ATS Scoring
                    Benchmarks the
                    rewritten resume
                           │
                           ▼
          Rewritten Resume + ATS Score + Keyword Gap Report
```

> **Add your architecture diagram here**
> Export from draw.io as a PNG and embed it:
> `![Architecture Diagram](docs/architecture.png)`

---

## Results

| What was measured | Result |
|---|---|
| ATS compatibility score | 92 out of 100 |
| Async modules running at once | 15 |
| Pipeline stages | 4 |
| Keyword extraction method | TF-IDF |
| Skill gap scoring | Cosine similarity |
| Rewriting model | Gemini API |

---

## Why these technology choices

**Why Gemini API instead of a local model?**
The rewriting step needs a model that follows detailed instructions well. Running a local model large enough to do this well requires a GPU. Since this runs on Streamlit Cloud without GPU access, Gemini API was the right call.

**Why asyncio.gather() instead of running agents one at a time?**
All four agents plus their sub-modules can start with the same inputs. Running them concurrently cuts the wall-clock time compared to waiting for each one to finish before starting the next.

**Why TF-IDF for keyword extraction?**
TF-IDF finds terms that appear often in one specific job description but not across all job descriptions — which is exactly what makes a keyword meaningful for a particular role.

---

## Folder structure

```
Agentic-AI-based-Resume-Optimizer/
├── app.py                    # Streamlit entry point
├── agents/
│   ├── jd_analyzer.py        # Agent 1 — TF-IDF keyword extraction
│   ├── resume_critic.py      # Agent 2 — cosine similarity gap analysis
│   ├── rewriter.py           # Agent 3 — Gemini API rewriting
│   └── ats_scorer.py         # Agent 4 — ATS compatibility scoring
├── utils/
│   ├── preprocessing.py      # Text cleaning and tokenisation
│   └── async_runner.py       # asyncio.gather() orchestration
├── requirements.txt
├── .env.example              # API key template — never commit your .env file
└── README.md
```

---

## Screenshots

> **Add screenshots here** — this is one of the first things a recruiter will look for.
>
> Suggested shots:
> - The main interface where you paste the JD and resume
> - The output showing the ATS score
> - The keyword gap panel
> - The rewritten resume section
>
> ```markdown
> ![Main Interface](docs/screenshots/main.png)
> ![ATS Score Output](docs/screenshots/ats_score.png)
> ![Keyword Gap](docs/screenshots/keywords.png)
> ```

---

## How to run locally

```bash
# Clone the repo
git clone https://github.com/shraddha-gidde/Agentic-AI-based-Resume-Optimizer.git
cd Agentic-AI-based-Resume-Optimizer

# Set up a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Open .env and add: GEMINI_API_KEY=your_key_here
# Get a free key at: https://makersuite.google.com/app/apikey

# Run
streamlit run app.py
```

---

## Requirements

```
streamlit
google-generativeai
scikit-learn
pandas
python-dotenv
```

---

## What I would add next

- [ ] Architecture diagram in docs/
- [ ] PDF resume upload support via PyPDF2
- [ ] Side-by-side comparison of original and rewritten resume
- [ ] Batch mode for testing multiple job descriptions at once

---

## About me

**Shraddha Gidde** — Final-year B.Tech AI and Data Science, MIT WPU Pune

[![Portfolio](https://img.shields.io/badge/Portfolio-shraddha--gidde.netlify.app-blue)](https://shraddha-gidde.netlify.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://linkedin.com/in/shraddha-gidde-063506242)
[![GitHub](https://img.shields.io/badge/GitHub-shraddha--gidde-181717?logo=github)](https://github.com/shraddha-gidde)
