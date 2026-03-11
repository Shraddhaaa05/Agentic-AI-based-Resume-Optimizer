# features/ab_testing.py
class ABTestingAgent:
    def generate_variants(self, base_resume: str, job_description: str = "") -> dict:
        return {
            'skills_first':         self._reorder(base_resume, 'skills_first'),
            'achievement_focused':  self._emphasize(base_resume),
            'keyword_optimized':    self._keywords(base_resume, job_description),
            'story_driven':         self._narrative(base_resume),
        }
    def _reorder(self, r, s): return r + f"\n[Reordered: {s}]"
    def _emphasize(self, r):  return r + "\n[Achievements emphasised]"
    def _keywords(self, r, jd): return r + "\n[Keywords optimised]"
    def _narrative(self, r):  return r + "\n[Narrative enhanced]"