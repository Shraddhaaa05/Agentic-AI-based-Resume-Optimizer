# features/global_optimizer.py
class GlobalOptimizer:
    def optimize_for_international(self, resume_text: str, location: str = "") -> dict:
        return {
            'global_readiness': 'Medium',
            'suggested_changes': ['Add country code to phone','Include time zone','Remove local jargon'],
            'international_keywords': ['Global','Cross-cultural','Remote collaboration'],
        }