# features/interactive_builder.py
class InteractiveBuilder:
    def get_improvement_suggestions(self, resume_text: str) -> dict:
        return {
            'suggestions': ['Add quantifiable achievements','Include project metrics','Highlight leadership'],
            'quick_wins':  ['Optimise keywords','Add action verbs','Improve section ordering'],
        }