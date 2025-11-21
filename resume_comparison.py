# features/resume_comparison.py
import streamlit as st
from typing import Dict, List, Any
import difflib

class ResumeComparison:
    def __init__(self):
        self.comparison_metrics = [
            'word_count', 'achievement_count', 'skill_mentions', 
            'action_verbs', 'quantifiable_results'
        ]
    
    def generate_comparison(self, original_resume: str, optimized_resume: str, job_description: str = None) -> Dict[str, Any]:
        """Generate comprehensive before/after comparison"""
        try:
            print("📊 Generating resume comparison...")
            
            comparison = {
                'metrics': self._calculate_metrics(original_resume, optimized_resume),
                'key_improvements': self._identify_improvements(original_resume, optimized_resume),
                'visual_changes': self._generate_visual_diff(original_resume, optimized_resume),
                'summary': self._generate_summary(original_resume, optimized_resume),
                'status': 'success'
            }
            
            return comparison
            
        except Exception as e:
            print(f"❌ Resume comparison failed: {e}")
            return self._create_default_comparison()
    
    def _calculate_metrics(self, original: str, optimized: str) -> Dict[str, Any]:
        """Calculate comparison metrics"""
        original_words = len(original.split())
        optimized_words = len(optimized.split())
        
        return {
            'word_count': {
                'original': original_words,
                'optimized': optimized_words,
                'change': optimized_words - original_words,
                'change_percent': ((optimized_words - original_words) / original_words * 100) if original_words > 0 else 0
            },
            'achievement_count': {
                'original': self._count_achievements(original),
                'optimized': self._count_achievements(optimized),
                'change': self._count_achievements(optimized) - self._count_achievements(original)
            },
            'skill_mentions': {
                'original': self._count_skills(original),
                'optimized': self._count_skills(optimized),
                'change': self._count_skills(optimized) - self._count_skills(original)
            },
            'action_verbs': {
                'original': self._count_action_verbs(original),
                'optimized': self._count_action_verbs(optimized),
                'change': self._count_action_verbs(optimized) - self._count_action_verbs(original)
            },
            'quantifiable_results': {
                'original': self._count_quantifiable_results(original),
                'optimized': self._count_quantifiable_results(optimized),
                'change': self._count_quantifiable_results(optimized) - self._count_quantifiable_results(original)
            }
        }
    
    def _count_achievements(self, text: str) -> int:
        """Count achievement indicators"""
        achievement_words = ['achieved', 'accomplished', 'delivered', 'completed', 'won', 'awarded']
        return sum(1 for word in achievement_words if word in text.lower())
    
    def _count_skills(self, text: str) -> int:
        """Count technical skills mentioned"""
        skills = ['python', 'sql', 'excel', 'tableau', 'power bi', 'r programming', 'java', 'javascript']
        return sum(1 for skill in skills if skill in text.lower())
    
    def _count_action_verbs(self, text: str) -> int:
        """Count action verbs"""
        action_verbs = [
            'managed', 'led', 'created', 'developed', 'implemented', 'improved', 
            'increased', 'reduced', 'saved', 'optimized', 'analyzed', 'designed'
        ]
        return sum(1 for verb in action_verbs if verb in text.lower())
    
    def _count_quantifiable_results(self, text: str) -> int:
        """Count quantifiable results"""
        patterns = [r'\d+%', r'\$\d+', r'\d+\s*%', r'increased by', r'reduced by', r'saved \$']
        import re
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, text.lower()))
        return count
    
    def _identify_improvements(self, original: str, optimized: str) -> List[str]:
        """Identify key improvements"""
        improvements = []
        
        # Check word count improvement
        orig_words = len(original.split())
        opt_words = len(optimized.split())
        if opt_words > orig_words * 1.1:
            improvements.append("Added more detailed content and context")
        elif opt_words < orig_words * 0.9:
            improvements.append("Made resume more concise and focused")
        
        # Check achievement improvements
        orig_achievements = self._count_achievements(original)
        opt_achievements = self._count_achievements(optimized)
        if opt_achievements > orig_achievements:
            improvements.append(f"Added {opt_achievements - orig_achievements} achievement statements")
        
        # Check quantifiable results
        orig_quant = self._count_quantifiable_results(original)
        opt_quant = self._count_quantifiable_results(optimized)
        if opt_quant > orig_quant:
            improvements.append(f"Added {opt_quant - orig_quant} quantifiable metrics")
        
        # Check action verbs
        orig_verbs = self._count_action_verbs(original)
        opt_verbs = self._count_action_verbs(optimized)
        if opt_verbs > orig_verbs:
            improvements.append("Enhanced with more action-oriented language")
        
        return improvements if improvements else ["General content optimization and refinement"]
    
    def _generate_visual_diff(self, original: str, optimized: str) -> str:
        """Generate visual difference representation"""
        try:
            original_lines = original.split('\n')
            optimized_lines = optimized.split('\n')
            
            diff = difflib.unified_diff(
                original_lines, 
                optimized_lines,
                lineterm='',
                fromfile='Original',
                tofile='Optimized'
            )
            
            return '\n'.join(diff)
            
        except Exception as e:
            print(f"Visual diff error: {e}")
            return "Content comparison available in detailed view"
    
    def _generate_summary(self, original: str, optimized: str) -> str:
        """Generate comparison summary"""
        metrics = self._calculate_metrics(original, optimized)
        
        summary_parts = ["**Resume Optimization Summary:**"]
        
        # Word count analysis
        word_change = metrics['word_count']['change']
        if word_change > 0:
            summary_parts.append(f"• Added {word_change} words for better detail")
        elif word_change < 0:
            summary_parts.append(f"• Reduced by {abs(word_change)} words for conciseness")
        
        # Achievement analysis
        achievement_change = metrics['achievement_count']['change']
        if achievement_change > 0:
            summary_parts.append(f"• Added {achievement_change} achievement statements")
        
        # Quantifiable results
        quant_change = metrics['quantifiable_results']['change']
        if quant_change > 0:
            summary_parts.append(f"• Incorporated {quant_change} quantifiable metrics")
        
        return '\n'.join(summary_parts)
    
    def _create_default_comparison(self) -> Dict[str, Any]:
        """Create default comparison"""
        return {
            'metrics': {
                'word_count': {'original': 0, 'optimized': 0, 'change': 0, 'change_percent': 0},
                'achievement_count': {'original': 0, 'optimized': 0, 'change': 0},
                'skill_mentions': {'original': 0, 'optimized': 0, 'change': 0},
                'action_verbs': {'original': 0, 'optimized': 0, 'change': 0},
                'quantifiable_results': {'original': 0, 'optimized': 0, 'change': 0}
            },
            'key_improvements': ['Content optimization applied'],
            'visual_changes': 'Comparison analysis completed',
            'summary': 'Resume optimization improvements applied',
            'status': 'default_comparison'
        }