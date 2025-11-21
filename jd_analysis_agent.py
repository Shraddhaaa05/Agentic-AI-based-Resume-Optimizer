# agents/jd_analysis_agent.py
import asyncio
import re
from typing import Dict, List, Any

class JDAnalysisAgent:
    def __init__(self):
        self.required_keys = ['key_skills', 'experience_level', 'missing_skills', 'company_culture', 'requirements_analysis']
    
    async def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """Comprehensive job description analysis"""
        try:
            if not job_description or len(job_description.strip()) < 10:
                return self._create_default_analysis()
            
            print("🔍 Analyzing job description...")
            
            analysis = {
                'key_skills': self._extract_skills(job_description),
                'experience_level': self._determine_experience_level(job_description),
                'missing_skills': [],
                'company_culture': self._analyze_culture(job_description),
                'requirements_analysis': self._analyze_requirements(job_description),
                'salary_indicators': self._extract_salary_indicators(job_description),
                'education_requirements': self._extract_education(job_description),
                'certification_requirements': self._extract_certifications(job_description),
                'status': 'success'
            }
            
            # Ensure all required keys are present
            for key in self.required_keys:
                if key not in analysis:
                    analysis[key] = self._get_default_value(key)
            
            return analysis
            
        except Exception as e:
            print(f"❌ JD Analysis failed: {e}")
            return self._create_default_analysis()
    
    def _extract_skills(self, jd: str) -> List[str]:
        """Extract technical and soft skills from JD"""
        try:
            technical_skills = [
                'python', 'sql', 'excel', 'tableau', 'power bi', 'r programming', 'java', 
                'javascript', 'aws', 'azure', 'google cloud', 'docker', 'kubernetes',
                'machine learning', 'data visualization', 'statistics', 'etl', 'api',
                'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'spark'
            ]
            
            soft_skills = [
                'communication', 'problem-solving', 'teamwork', 'leadership', 'analytical',
                'critical thinking', 'time management', 'adaptability', 'creativity',
                'collaboration', 'presentation', 'storytelling', 'strategic thinking'
            ]
            
            jd_lower = jd.lower()
            found_skills = []
            
            # Technical skills
            for skill in technical_skills:
                if skill in jd_lower:
                    found_skills.append(skill.title())
            
            # Soft skills
            for skill in soft_skills:
                if skill in jd_lower:
                    found_skills.append(skill.title().replace('-', ' '))
            
            return found_skills if found_skills else ['Analytical Skills', 'Communication']
            
        except Exception as e:
            print(f"Skill extraction error: {e}")
            return ['General Skills']
    
    def _analyze_requirements(self, jd: str) -> Dict[str, Any]:
        """Comprehensive requirements analysis"""
        try:
            jd_lower = jd.lower()
            
            # Experience requirements
            experience_years = self._extract_experience_years(jd_lower)
            
            # Education requirements
            education_level = self._extract_education_level(jd_lower)
            
            # Technical requirements
            technical_requirements = self._extract_technical_requirements(jd_lower)
            
            # Soft skills requirements
            soft_skills_required = self._extract_soft_skills(jd_lower)
            
            return {
                'experience_years': experience_years,
                'education_level': education_level,
                'technical_requirements': technical_requirements,
                'soft_skills_required': soft_skills_required,
                'key_responsibilities': self._extract_responsibilities(jd),
                'preferred_qualifications': self._extract_preferred_qualifications(jd)
            }
            
        except Exception as e:
            print(f"Requirements analysis error: {e}")
            return self._get_default_requirements()
    
    def _extract_experience_years(self, jd_lower: str) -> str:
        """Extract experience requirements"""
        patterns = [
            r'(\d+)\+?\s*years?',
            r'(\d+)\s*-\s*(\d+)\s*years?',
            r'minimum\s+of\s+(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, jd_lower)
            if matches:
                if isinstance(matches[0], tuple):  # Range like "3-5 years"
                    return f"{matches[0][0]}-{matches[0][1]} years"
                else:  # Single number like "5 years"
                    return f"{matches[0]}+ years"
        
        return "Not specified"
    
    def _extract_education_level(self, jd_lower: str) -> str:
        """Extract education requirements"""
        education_keywords = {
            'bachelor': "Bachelor's Degree",
            'bs': "Bachelor's Degree", 
            'ba': "Bachelor's Degree",
            'master': "Master's Degree",
            'ms': "Master's Degree",
            'phd': "PhD",
            'doctorate': "PhD"
        }
        
        for keyword, level in education_keywords.items():
            if keyword in jd_lower:
                return level
        
        return "Bachelor's Degree (assumed)"
    
    def _extract_technical_requirements(self, jd_lower: str) -> List[str]:
        """Extract specific technical requirements"""
        requirements = []
        
        if 'sql' in jd_lower:
            requirements.append("SQL proficiency")
        if 'python' in jd_lower:
            requirements.append("Python programming")
        if 'tableau' in jd_lower or 'power bi' in jd_lower:
            requirements.append("Data visualization tools")
        if 'excel' in jd_lower:
            requirements.append("Advanced Excel skills")
        if 'statistic' in jd_lower:
            requirements.append("Statistical analysis")
        
        return requirements if requirements else ["Data analysis tools"]
    
    def _extract_soft_skills(self, jd_lower: str) -> List[str]:
        """Extract soft skills requirements"""
        skills = []
        
        if 'communication' in jd_lower:
            skills.append("Strong communication skills")
        if 'team' in jd_lower:
            skills.append("Team collaboration")
        if 'problem' in jd_lower:
            skills.append("Problem-solving ability")
        if 'analytic' in jd_lower:
            skills.append("Analytical thinking")
        
        return skills if skills else ["Professional communication"]
    
    def _extract_responsibilities(self, jd: str) -> List[str]:
        """Extract key responsibilities"""
        responsibilities = []
        jd_lower = jd.lower()
        
        if 'analy' in jd_lower:
            responsibilities.append("Data analysis and interpretation")
        if 'report' in jd_lower:
            responsibilities.append("Report generation and presentation")
        if 'dashboard' in jd_lower:
            responsibilities.append("Dashboard creation and maintenance")
        if 'clean' in jd_lower or 'process' in jd_lower:
            responsibilities.append("Data cleaning and processing")
        
        return responsibilities if responsibilities else ["Data-related tasks and projects"]
    
    def _extract_preferred_qualifications(self, jd: str) -> List[str]:
        """Extract preferred qualifications"""
        jd_lower = jd.lower()
        preferred = []
        
        if 'preferred' in jd_lower or 'plus' in jd_lower:
            # Extract context around "preferred" or "plus"
            lines = jd.split('\n')
            for line in lines:
                line_lower = line.lower()
                if 'preferred' in line_lower or 'plus' in line_lower:
                    preferred.append(line.strip())
        
        return preferred if preferred else ["Additional relevant experience or certifications"]
    
    def _extract_salary_indicators(self, jd: str) -> Dict[str, str]:
        """Extract salary range indicators"""
        jd_lower = jd.lower()
        salary_info = {}
        
        if 'competitive' in jd_lower:
            salary_info['indicator'] = "Competitive salary"
        if 'benefits' in jd_lower:
            salary_info['benefits'] = "Comprehensive benefits package"
        if 'equity' in jd_lower or 'stock' in jd_lower:
            salary_info['equity'] = "Equity/stock options available"
        
        return salary_info if salary_info else {"indicator": "Market rate compensation"}
    
    def _extract_education(self, jd: str) -> List[str]:
        """Extract education requirements"""
        jd_lower = jd.lower()
        education = []
        
        if 'degree' in jd_lower:
            education.append("Relevant degree required")
        if 'computer science' in jd_lower or 'statistics' in jd_lower:
            education.append("Technical field degree preferred")
        if 'mathematics' in jd_lower or 'economics' in jd_lower:
            education.append("Quantitative background valued")
        
        return education if education else ["Relevant educational background"]
    
    def _extract_certifications(self, jd: str) -> List[str]:
        """Extract certification requirements"""
        jd_lower = jd.lower()
        certifications = []
        
        if 'certification' in jd_lower:
            certifications.append("Relevant certifications preferred")
        if 'google' in jd_lower and 'analytics' in jd_lower:
            certifications.append("Google Analytics certification")
        if 'aws' in jd_lower and 'certified' in jd_lower:
            certifications.append("AWS certification")
        
        return certifications
    
    def _determine_experience_level(self, jd: str) -> str:
        """Determine experience level"""
        try:
            jd_lower = jd.lower()
            if any(word in jd_lower for word in ['senior', 'lead', 'principal', '5+', '8+']):
                return 'Senior'
            elif any(word in jd_lower for word in ['junior', 'entry', '0-2', '1-3']):
                return 'Junior'
            elif any(word in jd_lower for word in ['mid', '3-5', '2-4']):
                return 'Mid-level'
            else:
                return 'Mid-level'
        except:
            return 'Mid-level'
    
    def _analyze_culture(self, jd: str) -> str:
        """Analyze company culture"""
        try:
            jd_lower = jd.lower()
            if any(word in jd_lower for word in ['startup', 'fast-paced', 'innovative']):
                return 'Innovative/Startup'
            elif any(word in jd_lower for word in ['enterprise', 'corporate', 'fortune']):
                return 'Corporate/Structured'
            elif any(word in jd_lower for word in ['remote', 'flexible', 'work from home']):
                return 'Remote/Flexible'
            else:
                return 'Professional/Traditional'
        except:
            return 'Professional'
    
    def _get_default_value(self, key: str):
        """Get default value for missing keys"""
        defaults = {
            'key_skills': ['Analytical Skills', 'Communication'],
            'experience_level': 'Mid-level',
            'missing_skills': [],
            'company_culture': 'Professional',
            'requirements_analysis': self._get_default_requirements()
        }
        return defaults.get(key, [])
    
    def _get_default_requirements(self) -> Dict[str, Any]:
        """Get default requirements"""
        return {
            'experience_years': '3-5 years',
            'education_level': "Bachelor's Degree",
            'technical_requirements': ['Data analysis tools'],
            'soft_skills_required': ['Professional communication'],
            'key_responsibilities': ['Data analysis and reporting'],
            'preferred_qualifications': ['Additional relevant experience']
        }
    
    def _create_default_analysis(self) -> Dict[str, Any]:
        """Create default analysis"""
        return {
            'key_skills': ['Analytical Skills', 'Communication', 'Problem-solving'],
            'experience_level': 'Mid-level',
            'missing_skills': [],
            'company_culture': 'Professional',
            'requirements_analysis': self._get_default_requirements(),
            'salary_indicators': {'indicator': 'Competitive compensation'},
            'education_requirements': ['Relevant degree preferred'],
            'certification_requirements': [],
            'status': 'default_analysis'
        }