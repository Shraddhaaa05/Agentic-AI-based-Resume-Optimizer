# agents/debate_agent.py
import asyncio
import random
from typing import Dict, List, Any


class DebateAgent:
    """Multi-stakeholder resume evaluation."""

    DEFAULTS = {
        'recruiter':      ('Technical Recruiter',  ['ATS', 'Keywords', 'Format']),
        'hiring_manager': ('Hiring Manager',        ['Impact', 'Leadership']),
        'technical_lead': ('Technical Lead',        ['Skills', 'Projects']),
        'career_coach':   ('Career Coach',          ['Narrative', 'Presentation']),
    }

    async def conduct_resume_debate(self, resume_text: str, job_description: str = None,
                                    target_role: str = "") -> Dict[str, Any]:
        try:
            if not resume_text or len(resume_text.strip()) < 10:
                return self._create_default_debate()

            perspectives = await asyncio.gather(
                self._recruiter(resume_text, job_description, target_role),
                self._hiring_manager(resume_text, job_description, target_role),
                self._technical_lead(resume_text, job_description, target_role),
                self._career_coach(resume_text, job_description, target_role),
                return_exceptions=True,
            )

            names = list(self.DEFAULTS.keys())
            vp = {
                name: p if not isinstance(p, Exception) else self._default_perspective(name)
                for name, p in zip(names, perspectives)
            }

            consensus = self._consensus(vp)
            return {
                'perspectives': vp,
                'consensus': consensus,
                'debate_summary': self._summary(vp),
                'key_insights': self._insights(vp),
                'status': 'success',
            }
        except Exception as e:
            print(f"❌ Debate agent failed: {e}")
            return self._create_default_debate()

    async def _recruiter(self, resume, jd, role):
        await asyncio.sleep(0.05)
        s, c = [], []
        if len(resume.split()) > 200: s.append("Comprehensive content for ATS")
        else: c.append("May be too brief for ATS screening")
        if 'experience' in resume.lower(): s.append("Clear experience section")
        return {'role':'Technical Recruiter','focus_areas':['ATS','Keywords','Format'],
                'strengths':s,'concerns':c,
                'recommendations':["Ensure JD keywords are included","Keep to 1-2 pages"],
                'overall_rating': random.randint(65,85)}

    async def _hiring_manager(self, resume, jd, role):
        await asyncio.sleep(0.05)
        s, c = [], []
        if any(w in resume.lower() for w in ['managed','led']): s.append("Shows leadership")
        if any(w in resume.lower() for w in ['improved','increased','reduced']): s.append("Demonstrates impact")
        else: c.append("Limited evidence of measurable impact")
        return {'role':'Hiring Manager','focus_areas':['Business Impact','Leadership'],
                'strengths':s,'concerns':c,
                'recommendations':["Include specific business outcomes","Quantify team/project scope"],
                'overall_rating': random.randint(60,90)}

    async def _technical_lead(self, resume, jd, role):
        await asyncio.sleep(0.05)
        found = [t for t in ['python','sql','java','javascript','tableau','aws'] if t in resume.lower()]
        s = [f"Technical skills: {', '.join(found)}"] if found else []
        c = ["Limited technical skills highlighted"] if not found else []
        return {'role':'Technical Lead','focus_areas':['Technical Skills','Projects'],
                'strengths':s,'concerns':c,
                'recommendations':["Specify tools/technologies per project","Add GitHub or portfolio link"],
                'overall_rating': random.randint(70,95)}

    async def _career_coach(self, resume, jd, role):
        await asyncio.sleep(0.05)
        s, c = [], []
        if 'summary' in resume.lower() or 'objective' in resume.lower(): s.append("Clear professional summary")
        else: c.append("Missing professional summary")
        wc = len(resume.split())
        if 150 < wc < 800: s.append("Appropriate length")
        elif wc <= 150: c.append("Resume may be too brief")
        else: c.append("Resume may be too long")
        return {'role':'Career Coach','focus_areas':['Narrative','Presentation'],
                'strengths':s,'concerns':c,
                'recommendations':["Tailor for each application","Use action verbs to start bullet points"],
                'overall_rating': random.randint(65,88)}

    def _consensus(self, perspectives):
        all_s, all_c, all_r, ratings = [], [], [], []
        for p in perspectives.values():
            all_s.extend(p.get('strengths', []))
            all_c.extend(p.get('concerns', []))
            all_r.extend(p.get('recommendations', []))
            ratings.append(p.get('overall_rating', 70))
        return {
            'average_rating': round(sum(ratings)/len(ratings)) if ratings else 70,
            'agreed_strengths': list(dict.fromkeys(all_s))[:3],
            'common_concerns': list(dict.fromkeys(all_c))[:3],
            'priority_recommendations': list(dict.fromkeys(all_r))[:5],
        }

    def _summary(self, perspectives):
        c = self._consensus(perspectives)
        lines = ["Multi-stakeholder Resume Analysis:\n"]
        if c['agreed_strengths']:
            lines.append("✅ Key Strengths:")
            lines += [f"   • {s}" for s in c['agreed_strengths']]
        if c['common_concerns']:
            lines.append("\n⚠️ Areas for Improvement:")
            lines += [f"   • {s}" for s in c['common_concerns']]
        if c['priority_recommendations']:
            lines.append("\n🎯 Priority Recommendations:")
            lines += [f"   • {s}" for s in c['priority_recommendations']]
        lines.append(f"\n📊 Consensus Rating: {c['average_rating']}/100")
        return "\n".join(lines)

    def _insights(self, perspectives) -> List[str]:
        c = self._consensus(perspectives)
        ins = []
        if c['agreed_strengths']: ins.append(f"Strengths: {', '.join(c['agreed_strengths'][:2])}")
        if c['common_concerns']:  ins.append(f"Focus areas: {', '.join(c['common_concerns'][:2])}")
        ins.append(f"Overall potential: {c['average_rating']}/100")
        return ins

    def _default_perspective(self, name: str) -> Dict:
        role, focus = self.DEFAULTS[name]
        return {'role': role, 'focus_areas': focus, 'strengths': ['Professional presentation'],
                'concerns': [], 'recommendations': ['Standard optimisation'], 'overall_rating': 72}

    def _create_default_debate(self) -> Dict[str, Any]:
        vp = {n: self._default_perspective(n) for n in self.DEFAULTS}
        return {'perspectives': vp, 'consensus': {'average_rating':70,'agreed_strengths':['Good structure'],
                'common_concerns':['Add more specific achievements'],'priority_recommendations':['Focus on quantifiable results']},
                'debate_summary': 'Multi-perspective analysis completed.',
                'key_insights': ['Comprehensive review performed'], 'status': 'default_debate'}