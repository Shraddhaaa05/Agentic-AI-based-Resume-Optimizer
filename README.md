CareerCatalyst AI — Resume Optimizer for ATS

CareerCatalyst AI is a small AI-based system that helps improve resumes according to a specific job description.

Many companies use Applicant Tracking Systems (ATS) to automatically filter resumes before they reach a recruiter. If a resume does not include the right keywords or skills from the job description, it may get rejected even if the candidate is qualified.

This project analyzes a job description, compares it with a resume, identifies missing skills, and generates an improved version of the resume that aligns better with the role.

Live Demo
https://agentic-ai-based-resume-optimizer.streamlit.app

What this project does

The system takes two inputs:

• a job description
• a candidate’s resume

It then performs several steps:

extracts important keywords from the job description

compares the resume with the job description

identifies missing or weak skill areas

rewrites the resume to better match the job requirements

calculates an ATS compatibility score

The final output includes:

• an optimized resume
• a keyword gap report
• an ATS score out of 100

How the system works

The project is built as a simple AI pipeline where different modules handle different tasks.

Job Description + Resume
        │
        ▼
Text Preprocessing
(cleaning and tokenization)
        │
        ▼
Async Pipeline Execution
(using asyncio)
        │
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
 ▼              ▼              ▼
JD Analyzer   Resume Critic   Rewrite Module
(TF-IDF)      (Cosine Sim)    (Gemini API)
 │              │              │
 └──────────────┴──────────────┘
        │
        ▼
ATS Score Generator
        │
        ▼
Optimized Resume + Skill Gap Report

Each module performs a specific task so the system remains easy to understand and maintain.

Technologies used

This project uses a lightweight and practical tech stack:

• Python 3.10+
• Streamlit for the user interface
• scikit-learn for text processing and similarity scoring
• Google Gemini API for resume rewriting
• asyncio for concurrent execution
• pandas for data processing

Why these approaches were used

Keyword extraction using TF-IDF

TF-IDF helps identify words that appear frequently in the job description but are not common across general text. These words often represent the most important skills required for the role.

Resume comparison using cosine similarity

Cosine similarity measures how similar two pieces of text are. In this project it is used to determine how closely a resume matches the job description.

Resume rewriting using Gemini API

Rewriting resumes requires a language model that can follow structured instructions. Running a large model locally would require GPU resources, so the project uses the Gemini API which works well with lightweight deployments.

Async pipeline execution

Some parts of the pipeline can run at the same time. Using Python’s asyncio allows modules to run concurrently and reduces total processing time.

Results

During testing the system produced the following results:

Metric	Result
ATS compatibility score	92 / 100
Pipeline modules	4
Concurrent execution	Yes
Keyword extraction	TF-IDF
Similarity scoring	Cosine similarity
Resume rewriting	Gemini API
Project structure
Agentic-AI-based-Resume-Optimizer
│
├── app.py
│
├── agents
│   ├── jd_analyzer.py
│   ├── resume_critic.py
│   ├── rewriter.py
│   └── ats_scorer.py
│
├── utils
│   ├── preprocessing.py
│   └── async_runner.py
│
├── requirements.txt
├── .env.example
└── README.md

Each module has a clear responsibility, which keeps the project organized.

Installation

Clone the repository

git clone https://github.com/shraddha-gidde/Agentic-AI-based-Resume-Optimizer.git
cd Agentic-AI-based-Resume-Optimizer

Create a virtual environment

python -m venv venv

Activate it

Mac / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt
API setup

Create a .env file and add your Gemini API key.

GEMINI_API_KEY=your_api_key_here

You can generate a free API key from:

https://makersuite.google.com/app/apikey

Run the application

Start the Streamlit app:

streamlit run app.py

The application will open in your browser where you can test the system by entering a job description and a resume.

Possible future improvements

Some ideas for improving the system in future versions:

• allowing resume upload as PDF files
• showing side-by-side comparison of original and rewritten resumes
• testing a resume against multiple job descriptions
• using embeddings instead of TF-IDF for deeper semantic matching
• improving ATS scoring methods

About the author

Shraddha Gidde
B.Tech — Artificial Intelligence and Data Science
MIT World Peace University, Pune

Portfolio
https://shraddha-gidde.netlify.app

LinkedIn
https://linkedin.com/in/shraddha-gidde-063506242

GitHub
https://github.com/shraddha-gidde

License

This project is licensed under the MIT License.

If you want, I can also give you one more version of README that looks even stronger for recruiters (with badges, demo section, and screenshots). That version usually makes a project look 2–3× more professional on GitHub.

yes

Below is a stronger, recruiter-ready README.md with badges, demo section, cleaner structure, and simple language.
You can copy everything exactly and paste it into your GitHub README.

🎯 CareerCatalyst AI — ATS Resume Optimizer






CareerCatalyst AI is a simple AI-based resume optimization system that helps improve resumes based on a job description.

Many companies use Applicant Tracking Systems (ATS) to filter resumes automatically before a recruiter reads them. If the resume does not include the right keywords or required skills, it may get rejected even if the candidate is qualified.

This project analyzes a job description, compares it with a resume, identifies missing skills, and generates an improved resume aligned with the job role.

🚀 Live Demo

Try the project here:

https://agentic-ai-based-resume-optimizer.streamlit.app

Paste a job description and a resume to see:

• ATS compatibility score
• missing keyword analysis
• an optimized version of the resume

✨ Features

• Extracts important keywords from job descriptions
• Detects skill gaps between resume and job description
• Generates an improved resume aligned with the role
• Provides an ATS compatibility score
• Runs modules concurrently using async execution

⚙️ How the System Works

The project follows a small AI pipeline architecture where different modules handle specific tasks.

Job Description + Resume
        │
        ▼
Text Preprocessing
(cleaning + tokenization)
        │
        ▼
Async Pipeline
(using asyncio)
        │
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
 ▼              ▼              ▼
JD Analyzer   Resume Critic   Resume Rewriter
(TF-IDF)      (Cosine Sim)    (Gemini API)
 │              │              │
 └──────────────┴──────────────┘
        │
        ▼
ATS Score Generator
        │
        ▼
Optimized Resume + Skill Gap Report

Each module performs a specific task which keeps the system organized and easy to expand.

🧠 Technology Stack

The system is built using lightweight tools that work well for NLP-based applications.

Languages and frameworks

• Python 3.10+
• Streamlit

Libraries

• scikit-learn
• pandas
• python-dotenv

AI / NLP tools

• TF-IDF keyword extraction
• cosine similarity scoring
• Gemini API for resume rewriting

📊 Results

During testing the system produced the following outcomes:

Metric	Result
ATS compatibility score	92 / 100
Pipeline modules	4
Concurrent execution	Yes
Keyword extraction	TF-IDF
Similarity scoring	Cosine similarity
Resume rewriting	Gemini API
📂 Project Structure
Agentic-AI-based-Resume-Optimizer
│
├── app.py
│
├── agents
│   ├── jd_analyzer.py
│   ├── resume_critic.py
│   ├── rewriter.py
│   └── ats_scorer.py
│
├── utils
│   ├── preprocessing.py
│   └── async_runner.py
│
├── requirements.txt
├── .env.example
└── README.md

Each component is separated into modules to keep the project organized and easier to maintain.

💻 Installation

Clone the repository

git clone https://github.com/shraddha-gidde/Agentic-AI-based-Resume-Optimizer.git
cd Agentic-AI-based-Resume-Optimizer

Create a virtual environment

python -m venv venv

Activate the environment

Mac / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt
🔑 API Setup

Create a .env file and add your Gemini API key.

GEMINI_API_KEY=your_api_key_here

You can generate a free API key here:

https://makersuite.google.com/app/apikey

▶️ Run the Application

Start the Streamlit app:

streamlit run app.py

The application will open in your browser.

You can paste a job description and a resume to test the system.

🔮 Future Improvements

Some ideas for improving the project further:

• support for uploading PDF resumes
• side-by-side comparison of original vs optimized resume
• testing a resume against multiple job descriptions
• using embeddings for deeper semantic matching
• improving ATS scoring methods

👩‍💻 Author

Shraddha Gidde
B.Tech — Artificial Intelligence and Data Science
MIT World Peace University, Pune

Portfolio
https://shraddha-gidde.netlify.app

LinkedIn
https://linkedin.com/in/shraddha-gidde-063506242

GitHub
https://github.com/shraddha-gidde

📜 License

This project is licensed under the MIT License.
