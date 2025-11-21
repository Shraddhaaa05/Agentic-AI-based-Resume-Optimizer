class ABTestingAgent:
    """Generates resume variants and predicts performance"""
    
    def generate_variants(self, base_resume: str, job_description: str):
        return {
            "skills_first": self._reorder_sections(base_resume, "skills_first"),
            "achievement_focused": self._emphasize_achievements(base_resume),
            "keyword_optimized": self._maximize_keyword_density(base_resume, job_description),
            "story_driven": self._enhance_narrative(base_resume)
        }

    def predict_performance(self, variants: dict, job_description: str):
        performance_scores = {}
        for name, resume in variants.items():
            performance_scores[name] = self._simulate_ats_parsing(resume, job_description)
        return performance_scores

    # --- Dummy helper methods ---
    def _reorder_sections(self, resume, style):
        return resume + f"\n[Reordered sections: {style}]"
    
    def _emphasize_achievements(self, resume):
        return resume + "\n[Achievements emphasized]"
    
    def _maximize_keyword_density(self, resume, jd):
        return resume + "\n[Keywords optimized]"
    
    def _enhance_narrative(self, resume):
        return resume + "\n[Narrative enhanced]"
    
    def _simulate_ats_parsing(self, resume, jd):
        # Returns dummy ATS score
        return len(resume.split()) % 100