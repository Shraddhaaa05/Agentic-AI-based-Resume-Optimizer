# features/mobile_optimizer.py
class MobileOptimizer:
    def analyze_mobile_compatibility(self, resume_text: str) -> dict:
        return {
            'mobile_score': 85,
            'issues_found': ['Long paragraphs may be hard to read','Complex tables may not render'],
            'suggestions':  ['Use shorter paragraphs','Use bullet points','Increase font size'],
        }