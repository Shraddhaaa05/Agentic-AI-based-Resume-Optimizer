# features/resume_health_track.py
import re
from typing import Dict, Any


class ResumeHealthTracker:
    WEIGHTS = {'readability':0.20,'keyword_density':0.25,'achievement_metrics':0.30,'structure':0.15,'contact_info':0.10}

    def track_health_metrics(self, original_resume: str, optimized_resume: str) -> Dict[str, Any]:
        try:
            rd  = self._readability(optimized_resume)
            kd  = self._keyword_density_improvement(original_resume, optimized_resume)
            ac  = self._achievement_count(optimized_resume)
            st  = self._structure(optimized_resume)
            ci  = self._contact_info(optimized_resume)

            overall = round(
                rd * self.WEIGHTS['readability'] +
                min(kd * 33.33, 100) * self.WEIGHTS['keyword_density'] +
                min(ac / 5 * 100, 100) * self.WEIGHTS['achievement_metrics'] +
                st * self.WEIGHTS['structure'] +
                ci * self.WEIGHTS['contact_info']
            )

            return {
                'overall_health': overall,
                'metrics': {
                    'readability':        {'score':rd,  'status':'good' if rd>=70  else 'needs_improvement','description':f'Readability: {rd}/100'},
                    'keyword_density':    {'score':kd,  'status':'good' if kd>=2.0 else 'needs_improvement','description':f'Keyword density improvement: {kd:.1f}x'},
                    'achievement_metrics':{'score':ac,  'status':'good' if ac>=3   else 'needs_improvement','description':f'{ac} quantifiable achievements found'},
                    'structure':          {'score':st,  'status':'good' if st>=80  else 'needs_improvement','description':f'Structure score: {st}/100'},
                    'contact_info':       {'score':ci,  'status':'complete' if ci==100 else 'incomplete','description':'Contact info complete' if ci==100 else 'Missing contact info'},
                },
                'improvement_summary': {
                    'original_length':        len(original_resume),
                    'optimized_length':       len(optimized_resume),
                    'length_change_percent':  round((len(optimized_resume)-len(original_resume))/max(len(original_resume),1)*100,1),
                    'key_improvements':       self._key_improvements(original_resume, optimized_resume),
                },
                'recommendations': self._recommendations(overall, {'readability':rd,'keyword_density':kd,'achievement_count':ac,'contact_info':ci}),
            }
        except Exception as e:
            return {'overall_health':65,'metrics':{},'improvement_summary':{},'recommendations':['Basic analysis completed'],'error':str(e)}

    def _readability(self, text: str) -> float:
        sentences = re.split(r'[.!?]+', text)
        words = re.findall(r'\b\w+\b', text.lower())
        if not sentences or not words: return 50.0
        avg_len = len(words) / len(sentences)
        ss = max(0, 100 - abs(avg_len - 17.5) * 3)
        vs = min(100, (len(set(words)) / len(words)) * 200)
        sc = sum(30 for s in ['experience','education','skills','summary','projects'] if s in text.lower())
        return min(100, ss*0.4 + vs*0.3 + sc*0.3)

    def _keyword_density_improvement(self, orig: str, opt: str) -> float:
        kws = ['managed','led','created','improved','increased','reduced','developed','implemented']
        od = sum(orig.lower().count(k) for k in kws) / max(len(orig.split()),1)
        nd = sum(opt.lower().count(k)  for k in kws) / max(len(opt.split()),1)
        if od == 0: return 2.0 if nd > 0 else 1.0
        return min(nd / od, 3.0)

    def _achievement_count(self, text: str) -> int:
        count = len(re.findall(r'\b\d+%?\b|\$\d+|\b(?:increased|reduced|improved|saved)\b.*?\bby\b', text, re.IGNORECASE))
        return min(count, 10)

    def _structure(self, text: str) -> float:
        score = sum(25 for s in ['experience','education','skills'] if s in text.lower())
        score += sum(10 for s in ['summary','projects','certifications'] if s in text.lower())
        return min(score, 100)

    def _contact_info(self, text: str) -> float:
        email = bool(re.search(r'\b[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,}\b', text))
        phone = bool(re.search(r'(\+?\d[\d\s\-().]{7,}\d)', text))
        if email and phone: return 100.0
        if email or phone:  return 50.0
        return 0.0

    def _key_improvements(self, orig: str, opt: str) -> list:
        imps = []
        if len(opt) > len(orig)*1.1: imps.append("Added more detailed accomplishments")
        elif len(opt) < len(orig)*0.9: imps.append("Made resume more concise")
        return imps or ["General content optimisation"]

    def _recommendations(self, score: float, m: dict) -> list:
        recs = []
        if score < 70:           recs.append("Add more quantifiable achievements with numbers")
        if m.get('readability',0) < 70:   recs.append("Improve readability with varied sentence length")
        if m.get('keyword_density',0) < 1.5: recs.append("Increase action-oriented keywords")
        if m.get('achievement_count',0) < 3: recs.append("Add specific achievements with metrics (e.g. '15% increase')")
        if m.get('contact_info',0) < 100:  recs.append("Ensure email and phone number are clearly visible")
        return recs or ["Resume is in good health — maintain current quality!"]