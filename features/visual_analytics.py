# features/visual_analytics.py
class VisualAnalytics:
    def generate_analytics(self, resume_text: str) -> dict:
        words = resume_text.split()
        return {
            'word_count': len(words),
            'section_distribution': {'Experience':40,'Skills':25,'Education':15,'Projects':20},
            'keyword_frequency': {'Data':resume_text.lower().count('data'),
                                  'Analysis':resume_text.lower().count('analys'),
                                  'SQL':resume_text.lower().count('sql'),
                                  'Python':resume_text.lower().count('python')},
        }