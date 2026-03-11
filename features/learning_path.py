# features/learning_path.py
import asyncio
from typing import Dict, List, Any


class LearningPathAgent:
    ROLE_SKILLS = {
        'Data Analyst':     {'technical':['SQL','Python','Statistics'],'tools':['Excel','Tableau','Power BI'],'soft_skills':['Communication','Problem-solving']},
        'Data Scientist':   {'technical':['Python','Machine Learning','Statistics'],'tools':['Jupyter','Pandas','Scikit-learn'],'soft_skills':['Research','Analytical Thinking']},
        'Business Analyst': {'technical':['SQL','Data Analysis'],'tools':['Excel','PowerPoint','JIRA'],'soft_skills':['Stakeholder Management','Documentation']},
    }
    RESOURCES = {
        'SQL':              ['SQLZoo interactive tutorials','Mode Analytics SQL tutorial','LeetCode SQL practice'],
        'Python':           ['DataCamp Python courses','Real Python tutorials','Python for Everybody (Coursera)'],
        'Tableau':          ['Tableau Public gallery','Tableau official training videos'],
        'Power BI':         ['Microsoft Learn Power BI modules','YouTube tutorial series'],
        'Statistics':       ['Khan Academy statistics','StatQuest YouTube channel'],
        'Machine Learning': ['Coursera ML Specialisation','Fast.ai practical deep learning','Kaggle micro-courses'],
        'Communication':    ['Toastmasters','Writing practice','Presentation workshops'],
    }

    async def generate_learning_plan(self, resume_text: str, target_role: str = "",
                                     jd_analysis: Dict = None) -> Dict[str, Any]:
        try:
            print("📚 Generating learning plan...")
            current = self._current_skills(resume_text)
            gaps    = self._gaps(current, jd_analysis, target_role)
            return {
                'current_skills':       current,
                'skill_gaps':           gaps,
                'learning_path':        self._path(gaps),
                'recommended_resources':self._resources(gaps),
                'timeline':             self._timeline(gaps),
                'status': 'success',
            }
        except Exception as e:
            print(f"❌ Learning plan failed: {e}")
            return self._default_plan()

    def _current_skills(self, text: str) -> Dict[str, List[str]]:
        tl = text.lower()
        tech  = [s for s in ['Python','SQL','Statistics','Machine Learning'] if s.lower() in tl]
        tools = [s for s in ['Tableau','Power BI','Excel','AWS'] if s.lower() in tl]
        soft  = []
        if 'communication' in tl: soft.append('Communication')
        if 'lead' in tl or 'managed' in tl: soft.append('Leadership')
        if 'team' in tl: soft.append('Teamwork')
        return {'technical': tech or ['Basic Data Analysis'], 'tools': tools or ['Spreadsheet Software'], 'soft_skills': soft or ['Professional Communication']}

    def _gaps(self, current: Dict, jd_analysis: Dict, target_role: str) -> Dict[str, List[str]]:
        expected = self.ROLE_SKILLS.get(target_role, self.ROLE_SKILLS['Data Analyst'])
        gaps = {}
        for cat in ['technical', 'tools', 'soft_skills']:
            cur = set(current.get(cat, []))
            exp = set(expected.get(cat, []))
            g   = list(exp - cur)
            if jd_analysis and 'key_skills' in jd_analysis:
                cur_lower = {s.lower() for s in cur}
                g += [s for s in jd_analysis['key_skills'] if s.lower() not in cur_lower][:2]
            gaps[cat] = list(dict.fromkeys(g))[:3]
        return gaps

    def _path(self, gaps: Dict) -> List[Dict]:
        path = []
        for skill in gaps.get('technical', [])[:2]:
            path.append({'skill':skill,'category':'technical','resources':self.RESOURCES.get(skill,['Online courses']),'timeline':'4-6 weeks','priority':'High'})
        for skill in gaps.get('tools', [])[:2]:
            path.append({'skill':skill,'category':'tools','resources':self.RESOURCES.get(skill,['Official tutorials']),'timeline':'2-4 weeks','priority':'Medium'})
        for skill in gaps.get('soft_skills', [])[:1]:
            path.append({'skill':skill,'category':'soft_skills','resources':self.RESOURCES.get(skill,['Practice & workshops']),'timeline':'Ongoing','priority':'Medium'})
        return path or [{'skill':'Data Analysis Fundamentals','category':'technical','resources':['Online courses'],'timeline':'4 weeks','priority':'High'}]

    def _resources(self, gaps: Dict) -> Dict[str, List[str]]:
        r = {'courses':[],'books':[],'practice':[],'communities':[]}
        if 'Python' in gaps.get('technical',[]): r['courses'].append('Python for Data Science Bootcamp'); r['practice'].append('Build data analysis projects')
        if 'SQL'    in gaps.get('technical',[]): r['courses'].append('SQL for Data Analysis'); r['practice'].append('Practice SQL on real datasets')
        if not r['courses']:
            r['courses'].append('Data Analysis Specialisation on Coursera')
            r['books'].append('"Storytelling with Data" by Cole Nussbaumer Knaflic')
            r['practice'].append('Work on personal data projects')
            r['communities'].append('Join data science meetups or forums')
        return r

    def _timeline(self, gaps: Dict) -> Dict[str, str]:
        total = sum(len(v) for v in gaps.values())
        if total >= 5: return {'level':'Comprehensive','duration':'3-6 months','focus':'Build strong foundation'}
        if total >= 3: return {'level':'Focused','duration':'2-3 months','focus':'Develop key missing skills'}
        return {'level':'Refinement','duration':'1-2 months','focus':'Polish existing skills'}

    def _default_plan(self) -> Dict[str, Any]:
        return {
            'current_skills':{'technical':['Data Analysis'],'tools':['Spreadsheet Software'],'soft_skills':['Communication']},
            'skill_gaps':{'technical':['SQL','Python'],'tools':['Tableau/Power BI'],'soft_skills':['Data Storytelling']},
            'learning_path':[{'skill':'Data Analysis Fundamentals','category':'technical','resources':['Online courses'],'timeline':'4 weeks','priority':'High'}],
            'recommended_resources':{'courses':['Data Analysis Specialisation'],'books':['Industry books'],'practice':['Hands-on projects'],'communities':['Professional networks']},
            'timeline':{'level':'Foundation','duration':'2-3 months','focus':'Build core skills'},
            'status':'default_plan',
        }