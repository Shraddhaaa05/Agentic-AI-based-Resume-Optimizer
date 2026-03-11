# agents/jd_analysis_agent.py
import re
from typing import Dict, List, Any


class JDAnalysisAgent:
    def __init__(self):
        self.required_keys = [
            'key_skills', 'experience_level', 'missing_skills',
            'company_culture', 'requirements_analysis',
        ]

    async def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
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
                'status': 'success',
            }
            for key in self.required_keys:
                if key not in analysis:
                    analysis[key] = self._get_default_value(key)
            return analysis
        except Exception as e:
            print(f"❌ JD Analysis failed: {e}")
            return self._create_default_analysis()

    def _extract_skills(self, jd: str) -> List[str]:
        technical = ['python','sql','excel','tableau','power bi','r programming','java',
                     'javascript','aws','azure','google cloud','docker','kubernetes',
                     'machine learning','data visualization','statistics','etl','api',
                     'pandas','numpy','scikit-learn','tensorflow','pytorch','spark']
        soft = ['communication','problem-solving','teamwork','leadership','analytical',
                'critical thinking','time management','adaptability','creativity',
                'collaboration','presentation','storytelling','strategic thinking']
        jd_lower = jd.lower()
        found = [s.title() for s in technical if s in jd_lower]
        found += [s.title().replace('-', ' ') for s in soft if s in jd_lower]
        return found or ['Analytical Skills', 'Communication']

    def _analyze_requirements(self, jd: str) -> Dict[str, Any]:
        jd_lower = jd.lower()
        return {
            'experience_years': self._extract_experience_years(jd_lower),
            'education_level': self._extract_education_level(jd_lower),
            'technical_requirements': self._extract_technical_requirements(jd_lower),
            'soft_skills_required': self._extract_soft_skills(jd_lower),
            'key_responsibilities': self._extract_responsibilities(jd),
            'preferred_qualifications': self._extract_preferred_qualifications(jd),
        }

    def _extract_experience_years(self, jd_lower: str) -> str:
        for pattern in [r'(\d+)\+?\s*years?', r'(\d+)\s*-\s*(\d+)\s*years?']:
            m = re.findall(pattern, jd_lower)
            if m:
                return f"{m[0][0]}-{m[0][1]} years" if isinstance(m[0], tuple) else f"{m[0]}+ years"
        return "Not specified"

    def _extract_education_level(self, jd_lower: str) -> str:
        for kw, level in [('phd','PhD'),('master',"Master's Degree"),('bachelor',"Bachelor's Degree")]:
            if kw in jd_lower:
                return level
        return "Bachelor's Degree (assumed)"

    def _extract_technical_requirements(self, jd_lower: str) -> List[str]:
        reqs = []
        if 'sql' in jd_lower: reqs.append("SQL proficiency")
        if 'python' in jd_lower: reqs.append("Python programming")
        if 'tableau' in jd_lower or 'power bi' in jd_lower: reqs.append("Data visualisation tools")
        if 'excel' in jd_lower: reqs.append("Advanced Excel skills")
        if 'statistic' in jd_lower: reqs.append("Statistical analysis")
        return reqs or ["Data analysis tools"]

    def _extract_soft_skills(self, jd_lower: str) -> List[str]:
        skills = []
        if 'communication' in jd_lower: skills.append("Strong communication skills")
        if 'team' in jd_lower: skills.append("Team collaboration")
        if 'problem' in jd_lower: skills.append("Problem-solving ability")
        if 'analytic' in jd_lower: skills.append("Analytical thinking")
        return skills or ["Professional communication"]

    def _extract_responsibilities(self, jd: str) -> List[str]:
        jd_lower = jd.lower()
        resp = []
        if 'analy' in jd_lower: resp.append("Data analysis and interpretation")
        if 'report' in jd_lower: resp.append("Report generation and presentation")
        if 'dashboard' in jd_lower: resp.append("Dashboard creation and maintenance")
        if 'clean' in jd_lower or 'process' in jd_lower: resp.append("Data cleaning and processing")
        return resp or ["Data-related tasks and projects"]

    def _extract_preferred_qualifications(self, jd: str) -> List[str]:
        preferred = [l.strip() for l in jd.split('\n') if 'preferred' in l.lower() or 'plus' in l.lower()]
        return preferred or ["Additional relevant experience or certifications"]

    def _extract_salary_indicators(self, jd: str) -> Dict[str, str]:
        jd_lower = jd.lower()
        info = {}
        if 'competitive' in jd_lower: info['indicator'] = "Competitive salary"
        if 'benefits' in jd_lower: info['benefits'] = "Comprehensive benefits package"
        if 'equity' in jd_lower or 'stock' in jd_lower: info['equity'] = "Equity/stock options"
        return info or {"indicator": "Market rate compensation"}

    def _extract_education(self, jd: str) -> List[str]:
        jd_lower = jd.lower()
        edu = []
        if 'degree' in jd_lower: edu.append("Relevant degree required")
        if 'computer science' in jd_lower or 'statistics' in jd_lower: edu.append("Technical field degree preferred")
        if 'mathematics' in jd_lower or 'economics' in jd_lower: edu.append("Quantitative background valued")
        return edu or ["Relevant educational background"]

    def _extract_certifications(self, jd: str) -> List[str]:
        jd_lower = jd.lower()
        certs = []
        if 'certification' in jd_lower: certs.append("Relevant certifications preferred")
        if 'google' in jd_lower and 'analytics' in jd_lower: certs.append("Google Analytics certification")
        if 'aws' in jd_lower and 'certified' in jd_lower: certs.append("AWS certification")
        return certs

    def _determine_experience_level(self, jd: str) -> str:
        jd_lower = jd.lower()
        if any(w in jd_lower for w in ['senior','lead','principal','5+','8+']): return 'Senior'
        if any(w in jd_lower for w in ['junior','entry','0-2','1-3']): return 'Junior'
        return 'Mid-level'

    def _analyze_culture(self, jd: str) -> str:
        jd_lower = jd.lower()
        if any(w in jd_lower for w in ['startup','fast-paced','innovative']): return 'Innovative/Startup'
        if any(w in jd_lower for w in ['enterprise','corporate','fortune']): return 'Corporate/Structured'
        if any(w in jd_lower for w in ['remote','flexible','work from home']): return 'Remote/Flexible'
        return 'Professional/Traditional'

    def _get_default_value(self, key: str):
        defaults = {
            'key_skills': ['Analytical Skills', 'Communication'],
            'experience_level': 'Mid-level',
            'missing_skills': [],
            'company_culture': 'Professional',
            'requirements_analysis': self._get_default_requirements(),
        }
        return defaults.get(key, [])

    def _get_default_requirements(self) -> Dict[str, Any]:
        return {
            'experience_years': '3-5 years',
            'education_level': "Bachelor's Degree",
            'technical_requirements': ['Data analysis tools'],
            'soft_skills_required': ['Professional communication'],
            'key_responsibilities': ['Data analysis and reporting'],
            'preferred_qualifications': ['Additional relevant experience'],
        }

    def _create_default_analysis(self) -> Dict[str, Any]:
        return {
            'key_skills': ['Analytical Skills', 'Communication', 'Problem-solving'],
            'experience_level': 'Mid-level',
            'missing_skills': [],
            'company_culture': 'Professional',
            'requirements_analysis': self._get_default_requirements(),
            'salary_indicators': {'indicator': 'Competitive compensation'},
            'education_requirements': ['Relevant degree preferred'],
            'certification_requirements': [],
            'status': 'default_analysis',
        }