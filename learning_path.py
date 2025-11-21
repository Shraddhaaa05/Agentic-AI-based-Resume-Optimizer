# features/learning_path.py
import asyncio
from typing import Dict, List, Any

class LearningPathAgent:
    def __init__(self):
        self.skill_categories = {
            'technical': ['SQL', 'Python', 'Data Visualization', 'Statistics', 'Machine Learning'],
            'tools': ['Tableau', 'Power BI', 'Excel', 'AWS', 'Git'],
            'soft_skills': ['Communication', 'Storytelling', 'Project Management', 'Leadership']
        }
    
    async def generate_learning_plan(self, resume_text: str, target_role: str = "", jd_analysis: Dict = None) -> Dict[str, Any]:
        """Generate personalized learning plan"""
        try:
            print("📚 Generating learning plan...")
            
            # Analyze current skills from resume
            current_skills = self._analyze_current_skills(resume_text)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(current_skills, jd_analysis, target_role)
            
            # Generate learning plan
            learning_plan = {
                'current_skills': current_skills,
                'skill_gaps': skill_gaps,
                'learning_path': self._create_learning_path(skill_gaps),
                'recommended_resources': self._recommend_resources(skill_gaps),
                'timeline': self._generate_timeline(skill_gaps),
                'status': 'success'
            }
            
            return learning_plan
            
        except Exception as e:
            print(f"❌ Learning plan generation failed: {e}")
            return self._create_default_learning_plan()
    
    def _analyze_current_skills(self, resume_text: str) -> Dict[str, List[str]]:
        """Analyze current skills from resume"""
        resume_lower = resume_text.lower()
        
        technical_skills = []
        tool_skills = []
        soft_skills = []
        
        # Technical skills detection
        if 'python' in resume_lower:
            technical_skills.append('Python')
        if 'sql' in resume_lower:
            technical_skills.append('SQL')
        if 'statistic' in resume_lower:
            technical_skills.append('Statistics')
        if 'machine learning' in resume_lower:
            technical_skills.append('Machine Learning')
        
        # Tool skills detection
        if 'tableau' in resume_lower:
            tool_skills.append('Tableau')
        if 'power bi' in resume_lower:
            tool_skills.append('Power BI')
        if 'excel' in resume_lower:
            tool_skills.append('Excel')
        if 'aws' in resume_lower or 'amazon web services' in resume_lower:
            tool_skills.append('AWS')
        
        # Soft skills detection
        if 'communication' in resume_lower:
            soft_skills.append('Communication')
        if 'lead' in resume_lower or 'managed' in resume_lower:
            soft_skills.append('Leadership')
        if 'team' in resume_lower:
            soft_skills.append('Teamwork')
        if 'problem' in resume_lower:
            soft_skills.append('Problem-solving')
        
        return {
            'technical': technical_skills if technical_skills else ['Basic Data Analysis'],
            'tools': tool_skills if tool_skills else ['Spreadsheet Software'],
            'soft_skills': soft_skills if soft_skills else ['Professional Communication']
        }
    
    def _identify_skill_gaps(self, current_skills: Dict, jd_analysis: Dict, target_role: str) -> Dict[str, List[str]]:
        """Identify skill gaps based on target role and JD analysis"""
        gaps = {
            'technical': [],
            'tools': [],
            'soft_skills': []
        }
        
        # Role-specific expected skills
        role_skills = self._get_role_skills(target_role)
        
        # Compare with current skills
        for category in ['technical', 'tools', 'soft_skills']:
            current = set(current_skills.get(category, []))
            expected = set(role_skills.get(category, []))
            
            # Add JD-specific skills if available
            if jd_analysis and 'key_skills' in jd_analysis:
                jd_skill_set = set(skill.lower() for skill in jd_analysis['key_skills'])
                current_lower = set(skill.lower() for skill in current)
                missing_jd_skills = [skill for skill in jd_analysis['key_skills'] 
                                   if skill.lower() not in current_lower]
                gaps[category].extend(missing_jd_skills[:3])  # Top 3 missing JD skills
            
            # Add role-specific gaps
            missing_skills = expected - current
            if missing_skills:
                gaps[category].extend(list(missing_skills)[:2])  # Top 2 role-specific gaps
        
        return gaps
    
    def _get_role_skills(self, target_role: str) -> Dict[str, List[str]]:
        """Get expected skills for target role"""
        role_skills = {
            'Data Analyst': {
                'technical': ['SQL', 'Python', 'Statistics', 'Data Analysis'],
                'tools': ['Excel', 'Tableau', 'Power BI', 'SQL Server'],
                'soft_skills': ['Communication', 'Problem-solving', 'Attention to Detail']
            },
            'Data Scientist': {
                'technical': ['Python', 'Machine Learning', 'Statistics', 'R Programming'],
                'tools': ['Jupyter', 'Pandas', 'Scikit-learn', 'TensorFlow'],
                'soft_skills': ['Research', 'Analytical Thinking', 'Storytelling']
            },
            'Business Analyst': {
                'technical': ['SQL', 'Data Analysis', 'Requirements Gathering'],
                'tools': ['Excel', 'PowerPoint', 'JIRA', 'Confluence'],
                'soft_skills': ['Stakeholder Management', 'Communication', 'Documentation']
            }
        }
        
        return role_skills.get(target_role, role_skills['Data Analyst'])
    
    def _create_learning_path(self, skill_gaps: Dict) -> List[Dict[str, Any]]:
        """Create structured learning path"""
        learning_path = []
        
        # Technical skills learning path
        for skill in skill_gaps['technical'][:3]:  # Top 3 technical gaps
            learning_path.append({
                'skill': skill,
                'category': 'technical',
                'resources': self._get_skill_resources(skill, 'technical'),
                'timeline': '4-6 weeks',
                'priority': 'High'
            })
        
        # Tool skills learning path
        for skill in skill_gaps['tools'][:2]:  # Top 2 tool gaps
            learning_path.append({
                'skill': skill,
                'category': 'tools',
                'resources': self._get_skill_resources(skill, 'tools'),
                'timeline': '2-4 weeks',
                'priority': 'Medium'
            })
        
        # Soft skills learning path
        for skill in skill_gaps['soft_skills'][:2]:  # Top 2 soft skill gaps
            learning_path.append({
                'skill': skill,
                'category': 'soft_skills',
                'resources': self._get_skill_resources(skill, 'soft_skills'),
                'timeline': 'Ongoing',
                'priority': 'Medium'
            })
        
        return learning_path if learning_path else [{
            'skill': 'Data Analysis Fundamentals',
            'category': 'technical',
            'resources': ['Online courses in data analysis', 'Practice with real datasets'],
            'timeline': '4 weeks',
            'priority': 'High'
        }]
    
    def _get_skill_resources(self, skill: str, category: str) -> List[str]:
        """Get learning resources for specific skill"""
        resource_map = {
            'SQL': ['SQLZoo interactive tutorials', 'Mode Analytics SQL tutorial', 'LeetCode SQL practice'],
            'Python': ['DataCamp Python courses', 'Real Python tutorials', 'Python for Everybody specialization'],
            'Tableau': ['Tableau Public gallery exploration', 'Tableau training videos', 'Build sample dashboards'],
            'Power BI': ['Microsoft Learn Power BI modules', 'YouTube tutorial series', 'Practice with business datasets'],
            'Statistics': ['Khan Academy statistics', 'StatQuest YouTube channel', 'Practical Statistics for Data Scientists'],
            'Communication': ['Toastmasters meetings', 'Writing practice', 'Presentation skills workshops'],
            'Machine Learning': ['Coursera Machine Learning course', 'Fast.ai practical deep learning', 'Kaggle micro-courses']
        }
        
        return resource_map.get(skill, [
            f"Online courses and tutorials for {skill}",
            f"Practical projects using {skill}",
            "Industry blogs and documentation"
        ])
    
    def _recommend_resources(self, skill_gaps: Dict) -> Dict[str, List[str]]:
        """Recommend learning resources"""
        resources = {
            'courses': [],
            'books': [],
            'practice': [],
            'communities': []
        }
        
        # Add recommendations based on skill gaps
        if any('Python' in skill for skill in skill_gaps['technical']):
            resources['courses'].append('Python for Data Science Bootcamp')
            resources['practice'].append('Build data analysis projects with Python')
        
        if any('SQL' in skill for skill in skill_gaps['technical']):
            resources['courses'].append('SQL for Data Analysis')
            resources['practice'].append('Practice SQL queries on real datasets')
        
        if any('Tableau' in skill or 'Power BI' in skill for skill in skill_gaps['tools']):
            resources['courses'].append('Data Visualization Fundamentals')
            resources['practice'].append('Create portfolio of data visualizations')
        
        # Default recommendations
        if not resources['courses']:
            resources['courses'].append('Data Analysis Specialization on Coursera')
            resources['books'].append('"Storytelling with Data" by Cole Nussbaumer Knaflic')
            resources['practice'].append('Work on personal data projects')
            resources['communities'].append('Join local data science meetups or online forums')
        
        return resources
    
    def _generate_timeline(self, skill_gaps: Dict) -> Dict[str, str]:
        """Generate learning timeline"""
        total_gaps = sum(len(gaps) for gaps in skill_gaps.values())
        
        if total_gaps >= 5:
            return {
                'level': 'Comprehensive',
                'duration': '3-6 months',
                'focus': 'Build strong foundation in multiple areas'
            }
        elif total_gaps >= 3:
            return {
                'level': 'Focused',
                'duration': '2-3 months', 
                'focus': 'Develop key missing skills'
            }
        else:
            return {
                'level': 'Refinement',
                'duration': '1-2 months',
                'focus': 'Polish existing skills and fill minor gaps'
            }
    
    def _create_default_learning_plan(self) -> Dict[str, Any]:
        """Create default learning plan"""
        return {
            'current_skills': {
                'technical': ['Data Analysis'],
                'tools': ['Basic Software'],
                'soft_skills': ['Communication']
            },
            'skill_gaps': {
                'technical': ['SQL', 'Python'],
                'tools': ['Tableau/Power BI'],
                'soft_skills': ['Data Storytelling']
            },
            'learning_path': [{
                'skill': 'Data Analysis Fundamentals',
                'category': 'technical',
                'resources': ['Online courses and practical projects'],
                'timeline': '4 weeks',
                'priority': 'High'
            }],
            'recommended_resources': {
                'courses': ['Data Analysis Specialization'],
                'books': ['Industry-relevant books'],
                'practice': ['Hands-on projects'],
                'communities': ['Professional networks']
            },
            'timeline': {
                'level': 'Foundation',
                'duration': '2-3 months',
                'focus': 'Build core data analysis skills'
            },
            'status': 'default_plan'
        }