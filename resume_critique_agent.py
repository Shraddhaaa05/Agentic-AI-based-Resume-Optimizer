import asyncio
from typing import Dict, Any

class ResumeCritiqueAgent:
    def __init__(self):
        self.required_keys = ['strengths', 'recommendations', 'overall_assessment']
    
    async def critique_resume(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """Critique resume with error handling"""
        try:
            if not resume_text or len(resume_text.strip()) < 10:
                return self._create_default_critique()
            
            critique = {
                'strengths': self._identify_strengths(resume_text),
                'recommendations': self._generate_recommendations(resume_text, job_description),
                'overall_assessment': self._provide_assessment(resume_text),
                'status': 'success'
            }
            
            # Ensure all required keys
            for key in self.required_keys:
                if key not in critique:
                    critique[key] = self._get_default_critique_value(key)
            
            return critique
            
        except Exception as e:
            print(f"❌ Resume critique failed: {e}")
            return self._create_default_critique()
    
    def _identify_strengths(self, resume: str) -> list:
        """Identify resume strengths"""
        try:
            strengths = []
            if len(resume) > 200:
                strengths.append('Good content length')
            if 'experience' in resume.lower():
                strengths.append('Clear experience section')
            if 'education' in resume.lower():
                strengths.append('Education background included')
            
            return strengths if strengths else ['Well-structured resume']
        except:
            return ['Good foundation']
    
    def _generate_recommendations(self, resume: str, jd: str = None) -> list:
        """Generate recommendations"""
        try:
            recommendations = ['Add quantifiable achievements']
            if jd and len(resume.split()) < 300:
                recommendations.append('Expand on key experiences')
            if 'summary' not in resume.lower():
                recommendations.append('Add professional summary')
            
            return recommendations
        except:
            return ['Focus on adding metrics', 'Highlight key achievements']
    
    def _provide_assessment(self, resume: str) -> str:
        """Provide overall assessment"""
        try:
            word_count = len(resume.split())
            if word_count > 400:
                return 'Comprehensive resume with good detail'
            elif word_count > 200:
                return 'Well-balanced resume'
            else:
                return 'Good foundation, consider adding more detail'
        except:
            return 'Solid resume foundation'
    
    def _get_default_critique_value(self, key: str):
        """Get default critique values"""
        defaults = {
            'strengths': ['Clear structure', 'Good formatting'],
            'recommendations': ['Add more achievements', 'Include metrics'],
            'overall_assessment': 'Good resume foundation'
        }
        return defaults.get(key, [])
    
    def _create_default_critique(self) -> Dict[str, Any]:
        """Create default critique"""
        return {
            'strengths': ['Professional presentation', 'Clear sections'],
            'recommendations': ['Add quantifiable results', 'Highlight key skills'],
            'overall_assessment': 'Good resume with room for optimization',
            'status': 'default_critique'
        }