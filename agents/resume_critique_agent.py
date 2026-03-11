# agents/resume_critique_agent.py
from typing import Dict, Any, List


class ResumeCritiqueAgent:
    def __init__(self):
        self.required_keys = ['strengths', 'recommendations', 'overall_assessment']

    async def critique_resume(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        try:
            if not resume_text or len(resume_text.strip()) < 10:
                return self._create_default_critique()
            print("📝 Critiquing resume...")
            critique = {
                'strengths': self._identify_strengths(resume_text),
                'recommendations': self._generate_recommendations(resume_text, job_description),
                'overall_assessment': self._provide_assessment(resume_text),
                'status': 'success',
            }
            for key in self.required_keys:
                if key not in critique:
                    critique[key] = self._get_default_critique_value(key)
            return critique
        except Exception as e:
            print(f"❌ Resume critique failed: {e}")
            return self._create_default_critique()

    def _identify_strengths(self, resume: str) -> List[str]:
        strengths = []
        if len(resume) > 200:            strengths.append("Good content length")
        if 'experience' in resume.lower(): strengths.append("Clear experience section")
        if 'education'  in resume.lower(): strengths.append("Education background included")
        if 'skill'      in resume.lower(): strengths.append("Skills section present")
        return strengths or ['Well-structured resume']

    def _generate_recommendations(self, resume: str, jd: str = None) -> List[str]:
        recs = ['Add quantifiable achievements with specific numbers']
        if 'summary' not in resume.lower():
            recs.append("Add a professional summary at the top")
        if jd and len(resume.split()) < 300:
            recs.append("Expand on key experiences to better match JD")
        if not any(c.isdigit() for c in resume):
            recs.append("Include metrics (%, $, team sizes) to show impact")
        return recs

    def _provide_assessment(self, resume: str) -> str:
        wc = len(resume.split())
        if wc > 400: return 'Comprehensive resume with good detail'
        if wc > 200: return 'Well-balanced resume'
        return 'Good foundation — consider adding more detail'

    def _get_default_critique_value(self, key: str):
        return {
            'strengths':          ['Clear structure', 'Good formatting'],
            'recommendations':    ['Add more achievements', 'Include metrics'],
            'overall_assessment': 'Good resume foundation',
        }.get(key, [])

    def _create_default_critique(self) -> Dict[str, Any]:
        return {
            'strengths':          ['Professional presentation', 'Clear sections'],
            'recommendations':    ['Add quantifiable results', 'Highlight key skills'],
            'overall_assessment': 'Good resume with room for optimisation',
            'status': 'default_critique',
        }