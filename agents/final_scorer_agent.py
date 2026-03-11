# agents/final_scorer_agent.py
import re
from typing import Dict, Any


class FinalScorerAgent:
    def __init__(self):
        self.scoring_criteria = {
            'keyword_match':      {'weight': 0.25, 'description': 'JD keyword alignment'},
            'skills_alignment':   {'weight': 0.20, 'description': 'Skills match to target role'},
            'impact_presentation':{'weight': 0.15, 'description': 'Quality of achievement statements'},
            'career_narrative':   {'weight': 0.15, 'description': 'Clarity of career progression'},
            'ats_optimization':   {'weight': 0.25, 'description': 'ATS-friendly formatting'},
        }

    async def calculate_final_score(self, original_resume: str, optimized_resume: str,
                                    job_description: str = None, target_role: str = "") -> Dict[str, Any]:
        try:
            print("🎯 Calculating final score...")
            kw    = self._score_keyword_match(optimized_resume, job_description)
            sk    = self._score_skills_alignment(optimized_resume, target_role)
            imp   = self._score_impact_presentation(optimized_resume)
            narr  = self._score_career_narrative(optimized_resume)
            ats   = self._score_ats_optimization(optimized_resume)

            overall = round(
                kw  * self.scoring_criteria['keyword_match']['weight'] +
                sk  * self.scoring_criteria['skills_alignment']['weight'] +
                imp * self.scoring_criteria['impact_presentation']['weight'] +
                narr* self.scoring_criteria['career_narrative']['weight'] +
                ats * self.scoring_criteria['ats_optimization']['weight']
            )

            confidence = 'high' if overall >= 80 else ('medium' if overall >= 60 else 'low')
            scores = {
                'overall_score':       overall,
                'keyword_match':       kw,
                'skills_alignment':    sk,
                'impact_presentation': imp,
                'career_narrative':    narr,
                'ats_optimization':    ats,
                'confidence_level':    confidence,
                'score_breakdown': {
                    k: {'score': v, 'weight': self.scoring_criteria[k]['weight'],
                        'description': self.scoring_criteria[k]['description']}
                    for k, v in [('keyword_match', kw), ('skills_alignment', sk),
                                 ('impact_presentation', imp), ('career_narrative', narr),
                                 ('ats_optimization', ats)]
                }
            }
            print(f"✅ Final score: {overall}%")
            return scores
        except Exception as e:
            print(f"❌ Scoring failed: {e}")
            return self._default_scores()

    # ── scoring sub-methods ──────────────────────────────────────────────────

    def _score_keyword_match(self, resume: str, jd: str = None) -> int:
        if not jd:
            return 65
        jd_words = set(re.findall(r'\b\w{4,}\b', jd.lower()))
        res_words = set(re.findall(r'\b\w{4,}\b', resume.lower()))
        if not jd_words:
            return 65
        overlap = len(jd_words & res_words) / len(jd_words)
        return min(int(overlap * 200), 100)          # scale generously

    def _score_skills_alignment(self, resume: str, target_role: str) -> int:
        skills = ['python','sql','excel','tableau','power bi','machine learning',
                  'javascript','java','aws','azure','docker','statistics']
        found = sum(1 for s in skills if s in resume.lower())
        base = min(found * 12, 80)
        role_bonus = 10 if target_role and target_role.lower() in resume.lower() else 0
        return min(base + role_bonus + 20, 100)

    def _score_impact_presentation(self, resume: str) -> int:
        action_verbs = ['managed','led','created','developed','implemented','improved',
                        'increased','reduced','saved','optimized','delivered','achieved']
        has_metrics = bool(re.search(r'\d+%|\$\d+|\d+\s*(?:users|clients|projects)', resume, re.IGNORECASE))
        verb_count = sum(1 for v in action_verbs if v in resume.lower())
        base = min(verb_count * 8, 60)
        return min(base + (25 if has_metrics else 0) + 15, 100)

    def _score_career_narrative(self, resume: str) -> int:
        score = 50
        if 'summary' in resume.lower() or 'objective' in resume.lower(): score += 20
        if 'experience' in resume.lower():  score += 15
        if 'education'  in resume.lower():  score += 10
        if 'skill'      in resume.lower():  score += 5
        return min(score, 100)

    def _score_ats_optimization(self, resume: str) -> int:
        score = 60
        if '@' in resume:                   score += 10   # email present
        if re.search(r'\d{3}[-.\s]\d{4}', resume): score += 5  # phone
        if 'experience' in resume.lower():  score += 10
        if 'education'  in resume.lower():  score += 10
        if 'skill'      in resume.lower():  score += 5
        # Penalise likely table/column formatting
        if resume.count('|') > 5:           score -= 10
        return max(min(score, 100), 0)

    def _default_scores(self) -> Dict[str, Any]:
        return {
            'overall_score': 65, 'keyword_match': 60, 'skills_alignment': 70,
            'impact_presentation': 65, 'career_narrative': 70, 'ats_optimization': 75,
            'confidence_level': 'medium',
        }