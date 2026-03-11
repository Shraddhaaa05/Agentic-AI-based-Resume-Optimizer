import asyncio
from typing import List, Dict, Any

class InterviewPrepAgent:
    QUESTIONS = {
        "data analyst":["Describe your SQL and data querying experience","How do you ensure data quality in your analyses?","Tell me about insights you found that impacted business decisions","What data visualization tools do you prefer and why?","How do you handle missing or inconsistent data?"],
        "software engineer":["Explain your programming language and framework experience","Describe a challenging technical problem you solved","How do you approach testing and quality assurance?","Tell me about a team project you contributed to","What's your experience with version control and CI/CD?"],
        "product manager":["How do you prioritize features in a roadmap?","Describe a difficult product decision you made","How do you gather and incorporate user feedback?","Tell me about a product launch you led","How do you measure product success?"],
        "default":["Tell me about yourself and your background","Why are you interested in this role?","Describe a challenging project and your approach","Where do you see yourself in 5 years?","What are your greatest strengths and areas for growth?"],
    }

    async def generate_questions(self, resume: str, target_role: str = "") -> Dict[str, Any]:
        await asyncio.sleep(0.05)
        cat = self._category(target_role)
        return {"role_specific_questions":self.QUESTIONS.get(cat,self.QUESTIONS["default"])[:5],"behavioral_questions":self._behavioral(resume),"technical_questions":self._technical(resume),"preparation_tips":["Research the company's recent news and products","Prepare 2–3 questions to ask the interviewer","Practice explaining your projects using the STAR method","Review the job description and align your experience","Prepare specific metrics and outcomes for each achievement"]}

    def _category(self, role):
        rl = role.lower()
        if any(k in rl for k in ['data','analyst','analytics']): return "data analyst"
        if any(k in rl for k in ['software','developer','engineer']): return "software engineer"
        if any(k in rl for k in ['product','manager','pm']): return "product manager"
        return "default"

    def _behavioral(self, resume):
        base = ["Describe a time when you worked under pressure to meet a deadline","Tell me about a conflict you resolved within your team","Give an example of how you handled a difficult stakeholder","Describe a project where you took initiative without supervision","Tell me about a mistake and how you handled it"]
        rl = resume.lower()
        if any(w in rl for w in ['team','collaborat']): base.append("Describe your experience working in a team environment")
        if any(w in rl for w in ['lead','manage','supervis']): base.append("Tell me about your leadership experience")
        return base[:5]

    def _technical(self, resume):
        rl, qs = resume.lower(), []
        if any(l in rl for l in ['python','java','javascript']): qs.append("Explain your proficiency with the programming languages on your resume")
        if any(t in rl for t in ['sql','tableau','power bi','excel']): qs.append("Describe your experience with data analysis and visualization tools")
        if 'machine learning' in rl: qs.append("Explain a machine learning project you have worked on")
        if any(c in rl for c in ['cloud','aws','azure']): qs.append("Describe your experience with cloud platforms")
        if any(a in rl for a in ['agile','scrum']): qs.append("What is your experience with Agile methodologies?")
        return qs[:3] or ["What technical skills are you most confident in?","Describe a technical challenge you recently faced","How do you stay current with industry trends?"]