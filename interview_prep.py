# features/interview_prep.py
import asyncio
from typing import List, Dict, Any

class InterviewPrepAgent:
    """Generates likely interview questions and STAR stories"""

    def __init__(self):
        self.role_specific_questions = {
            "data analyst": [
                "Describe your experience with SQL and data querying",
                "How do you ensure data quality in your analyses?",
                "Tell me about a time you found insights that impacted business decisions",
                "What data visualization tools are you most comfortable with and why?",
                "How do you handle missing or inconsistent data in your datasets?"
            ],
            "software engineer": [
                "Explain your experience with different programming languages and frameworks",
                "Describe a challenging technical problem you solved",
                "How do you approach code testing and quality assurance?",
                "Tell me about a project where you had to collaborate with a team",
                "What's your experience with version control systems like Git?"
            ],
            "product manager": [
                "How do you prioritize features in a product roadmap?",
                "Describe a time you had to make a difficult product decision",
                "How do you gather and incorporate user feedback?",
                "Tell me about a product you launched from concept to completion",
                "How do you measure product success?"
            ],
            "default": [
                "Tell me about yourself and your background",
                "Why are you interested in this role and our company?",
                "Describe a challenging project and how you approached it",
                "Where do you see yourself in 5 years?",
                "What are your greatest strengths and weaknesses?"
            ]
        }

    async def generate_questions(self, resume: str, target_role: str = "") -> Dict[str, Any]:
        """Generate interview questions based on resume and target role"""
        await asyncio.sleep(0.1)
        
        # Determine role category
        role_category = "default"
        if target_role:
            target_role_lower = target_role.lower()
            if any(keyword in target_role_lower for keyword in ['data', 'analyst', 'analytics']):
                role_category = "data analyst"
            elif any(keyword in target_role_lower for keyword in ['software', 'developer', 'engineer', 'programmer']):
                role_category = "software engineer"
            elif any(keyword in target_role_lower for keyword in ['product', 'manager', 'pm']):
                role_category = "product manager"

        # Get role-specific questions
        role_questions = self.role_specific_questions.get(role_category, self.role_specific_questions["default"])
        
        # Generate behavioral questions based on resume content
        behavioral_questions = self._generate_behavioral_questions(resume)
        
        # Generate technical questions based on skills mentioned
        technical_questions = self._generate_technical_questions(resume)
        
        return {
            "role_specific_questions": role_questions[:5],
            "behavioral_questions": behavioral_questions,
            "technical_questions": technical_questions,
            "preparation_tips": [
                "Research the company's recent news and products",
                "Prepare 2-3 questions to ask the interviewer",
                "Practice explaining your projects and achievements",
                "Review the job description and align your experience",
                "Prepare specific examples using the STAR method"
            ]
        }

    def _generate_behavioral_questions(self, resume: str) -> List[str]:
        """Generate behavioral questions based on resume content"""
        behavioral_questions = [
            "Describe a time when you had to work under pressure to meet a deadline",
            "Tell me about a situation where you had to resolve a conflict within your team",
            "Give an example of how you handled a difficult stakeholder or client",
            "Describe a project where you had to take initiative without direct supervision",
            "Tell me about a time you made a mistake and how you handled it"
        ]
        
        # Add context-specific questions based on resume content
        resume_lower = resume.lower()
        if any(word in resume_lower for word in ['team', 'collaborat', 'work with']):
            behavioral_questions.append("Describe your experience working in a team environment")
        
        if any(word in resume_lower for word in ['lead', 'manage', 'supervis']):
            behavioral_questions.append("Tell me about your leadership experience")
        
        if any(word in resume_lower for word in ['problem', 'challenge', 'difficult']):
            behavioral_questions.append("Describe a complex problem you solved and your approach")
        
        return behavioral_questions[:5]

    def _generate_technical_questions(self, resume: str) -> List[str]:
        """Generate technical questions based on skills mentioned in resume"""
        technical_questions = []
        resume_lower = resume.lower()
        
        # Programming languages
        if any(lang in resume_lower for lang in ['python', 'java', 'c++', 'javascript']):
            technical_questions.append("Explain your proficiency with programming languages mentioned in your resume")
        
        # Data analysis tools
        if any(tool in resume_lower for tool in ['sql', 'tableau', 'power bi', 'excel']):
            technical_questions.append("Describe your experience with data analysis and visualization tools")
        
        # Specific technical skills
        if 'machine learning' in resume_lower:
            technical_questions.append("Explain a machine learning project you've worked on")
        
        if 'cloud' in resume_lower or 'aws' in resume_lower or 'azure' in resume_lower:
            technical_questions.append("Describe your experience with cloud platforms")
        
        if 'agile' in resume_lower or 'scrum' in resume_lower:
            technical_questions.append("What's your experience with Agile methodologies?")
        
        # Add general technical questions if none specific found
        if not technical_questions:
            technical_questions = [
                "What technical skills are you most confident in?",
                "Describe a technical challenge you recently faced",
                "How do you stay updated with industry trends and technologies?"
            ]
        
        return technical_questions[:3]

    async def create_star_stories(self, achievements: List[str]) -> Dict[str, str]:
        """Create STAR method stories for achievements"""
        await asyncio.sleep(0.1)
        
        star_stories = {}
        for achievement in achievements[:5]:  # Limit to top 5 achievements
            # Extract key elements from achievement for context
            achievement_lower = achievement.lower()
            
            if any(word in achievement_lower for word in ['increase', 'growth', 'improve', 'boost']):
                context = "focused on driving measurable results and business impact"
            elif any(word in achievement_lower for word in ['lead', 'manage', 'coordinate']):
                context = "demonstrating leadership and project management skills"
            elif any(word in achievement_lower for word in ['develop', 'create', 'build', 'design']):
                context = "involving technical development and implementation"
            elif any(word in achievement_lower for word in ['analyze', 'research', 'evaluate']):
                context = "requiring analytical thinking and data-driven decision making"
            else:
                context = "showcasing professional skills and accomplishments"
            
            star_stories[achievement] = {
                "Situation": f"Working on a project where {achievement}",
                "Task": f"My responsibility was to achieve the objectives outlined in the achievement",
                "Action": f"I implemented strategic approaches including [specific actions based on your experience]",
                "Result": f"This led to {achievement} and provided valuable learning experience",
                "preparation_tip": f"Practice elaborating on the specific actions you took to achieve this result"
            }
        
        return star_stories

    async def get_role_specific_prep(self, target_role: str) -> Dict[str, Any]:
        """Get role-specific interview preparation guidance"""
        await asyncio.sleep(0.1)
        
        prep_guides = {
            "data analyst": {
                "technical_topics": ["SQL queries", "Data visualization", "Statistical analysis", "Data cleaning"],
                "case_studies": ["Analyzing sales data", "Customer segmentation", "A/B test results"],
                "tools_to_review": ["Excel", "SQL", "Tableau/Power BI", "Python/R"]
            },
            "software engineer": {
                "technical_topics": ["Algorithms", "System design", "Code review", "Testing strategies"],
                "coding_challenges": ["Data structures", "Problem solving", "System architecture"],
                "tools_to_review": ["Git", "Your main programming language", "Framework specifics"]
            },
            "product manager": {
                "technical_topics": ["Product strategy", "User research", "Metrics and KPIs", "Roadmap planning"],
                "case_studies": ["Product launch", "Feature prioritization", "User problem solving"],
                "tools_to_review": ["Analytics tools", "Prototyping tools", "Project management software"]
            },
            "default": {
                "technical_topics": ["Industry knowledge", "Company research", "Role-specific skills"],
                "case_studies": ["Past project experiences", "Problem-solving examples"],
                "tools_to_review": ["Relevant software", "Industry tools", "Technical skills"]
            }
        }
        
        role_category = "default"
        if target_role:
            target_role_lower = target_role.lower()
            if any(keyword in target_role_lower for keyword in ['data', 'analyst', 'analytics']):
                role_category = "data analyst"
            elif any(keyword in target_role_lower for keyword in ['software', 'developer', 'engineer']):
                role_category = "software engineer"
            elif any(keyword in target_role_lower for keyword in ['product', 'manager']):
                role_category = "product manager"
        
        return prep_guides[role_category]