class VisualAnalytics:
    def generate_analytics(self, resume_text):
        return {
            "word_count": len(resume_text.split()),
            "section_distribution": {
                "Experience": 40,
                "Skills": 25,
                "Education": 15,
                "Projects": 20
            },
            "keyword_frequency": {
                "Data": 12,
                "Analysis": 8,
                "SQL": 6,
                "Python": 5
            }
        }