# features/resume_comparison.py
import re
import difflib
from typing import Dict, List, Any


class ResumeComparison:
    def generate_comparison(self, original_resume: str, optimized_resume: str,
                            job_description: str = None) -> Dict[str, Any]:
        try:
            print("📊 Generating resume comparison...")
            return {
                'metrics':         self._metrics(original_resume, optimized_resume),
                'key_improvements':self._improvements(original_resume, optimized_resume),
                'visual_changes':  self._diff(original_resume, optimized_resume),
                'summary':         self._summary(original_resume, optimized_resume),
                'status': 'success',
            }
        except Exception as e:
            print(f"❌ Resume comparison failed: {e}")
            return self._default_comparison()

    def _metrics(self, orig: str, opt: str) -> Dict[str, Any]:
        ow, ow2 = len(orig.split()), len(opt.split())
        pct = round((ow2 - ow) / ow * 100, 1) if ow else 0
        return {
            'word_count':          {'original': ow,                       'optimized': ow2, 'change': ow2 - ow, 'change_percent': pct},
            'achievement_count':   {'original': self._achievements(orig),  'optimized': self._achievements(opt),  'change': self._achievements(opt) - self._achievements(orig)},
            'skill_mentions':      {'original': self._skills(orig),        'optimized': self._skills(opt),        'change': self._skills(opt) - self._skills(orig)},
            'action_verbs':        {'original': self._verbs(orig),         'optimized': self._verbs(opt),         'change': self._verbs(opt) - self._verbs(orig)},
            'quantifiable_results':{'original': self._quant(orig),         'optimized': self._quant(opt),         'change': self._quant(opt) - self._quant(orig)},
        }

    def _achievements(self, t): return sum(1 for w in ['achieved','accomplished','delivered','completed','won','awarded'] if w in t.lower())
    def _skills(self, t):       return sum(1 for s in ['python','sql','excel','tableau','power bi','java','javascript'] if s in t.lower())
    def _verbs(self, t):        return sum(1 for v in ['managed','led','created','developed','implemented','improved','increased','reduced','saved','optimized','analyzed','designed'] if v in t.lower())
    def _quant(self, t):        return len(re.findall(r'\d+%|\$\d+|\d+\s*(?:users|clients|projects)', t, re.IGNORECASE))

    def _improvements(self, orig: str, opt: str) -> List[str]:
        imps = []
        if len(opt.split()) > len(orig.split()) * 1.1: imps.append("Added more detailed content and context")
        elif len(opt.split()) < len(orig.split()) * 0.9: imps.append("Made resume more concise and focused")
        da = self._achievements(opt) - self._achievements(orig)
        if da > 0: imps.append(f"Added {da} achievement statement(s)")
        dq = self._quant(opt) - self._quant(orig)
        if dq > 0: imps.append(f"Added {dq} quantifiable metric(s)")
        dv = self._verbs(opt) - self._verbs(orig)
        if dv > 0: imps.append("Enhanced with more action-oriented language")
        return imps or ["General content optimisation applied"]

    def _diff(self, orig: str, opt: str) -> str:
        try:
            return '\n'.join(difflib.unified_diff(orig.splitlines(), opt.splitlines(),
                                                  fromfile='Original', tofile='Optimised', lineterm=''))
        except Exception:
            return "Comparison analysis available in detailed view"

    def _summary(self, orig: str, opt: str) -> str:
        m = self._metrics(orig, opt)
        parts = ["**Resume Optimisation Summary:**"]
        wc = m['word_count']['change']
        if wc > 0:  parts.append(f"• Added {wc} words for better detail")
        elif wc < 0: parts.append(f"• Reduced by {abs(wc)} words for conciseness")
        if m['achievement_count']['change'] > 0: parts.append(f"• Added {m['achievement_count']['change']} achievement statement(s)")
        if m['quantifiable_results']['change'] > 0: parts.append(f"• Added {m['quantifiable_results']['change']} quantifiable metric(s)")
        return '\n'.join(parts)

    def _default_comparison(self) -> Dict[str, Any]:
        z = {'original':0,'optimized':0,'change':0}
        return {'metrics':{'word_count':{**z,'change_percent':0},'achievement_count':z,'skill_mentions':z,'action_verbs':z,'quantifiable_results':z},
                'key_improvements':['Content optimisation applied'],'visual_changes':'Comparison completed',
                'summary':'Resume optimisation applied','status':'default_comparison'}