# features/resume_health_track.py
import re
from typing import Dict, Any

class ResumeHealthTracker:
    def __init__(self):
        self.health_metrics = {
            'readability': {'weight': 0.2, 'threshold': 70},
            'keyword_density': {'weight': 0.25, 'threshold': 2.5},
            'achievement_metrics': {'weight': 0.3, 'threshold': 3},
            'structure': {'weight': 0.15, 'threshold': 80},
            'contact_info': {'weight': 0.1, 'threshold': 100}
        }
    
    def track_health_metrics(self, original_resume: str, optimized_resume: str) -> Dict[str, Any]:
        """Track health metrics between original and optimized resume"""
        try:
            print(f"🔍 HealthTracker: Original length: {len(original_resume)}, Optimized length: {len(optimized_resume)}")
            
            # Calculate readability score
            readability_score = self._calculate_readability(optimized_resume)
            
            # Calculate keyword density improvement
            keyword_improvement = self._calculate_keyword_density_improvement(original_resume, optimized_resume)
            
            # Count achievement metrics
            achievement_count = self._count_achievement_metrics(optimized_resume)
            
            # Check structure quality
            structure_score = self._assess_structure(optimized_resume)
            
            # Check contact info completeness
            contact_score = self._check_contact_info(optimized_resume)
            
            # Calculate overall health score
            overall_health = (
                readability_score * self.health_metrics['readability']['weight'] +
                keyword_improvement * 33.33 * self.health_metrics['keyword_density']['weight'] +  # Scale to 100
                min(achievement_count / 5 * 100, 100) * self.health_metrics['achievement_metrics']['weight'] +
                structure_score * self.health_metrics['structure']['weight'] +
                contact_score * self.health_metrics['contact_info']['weight']
            )
            
            result = {
                'overall_health': round(overall_health),
                'metrics': {
                    'readability': {
                        'score': readability_score,
                        'status': 'good' if readability_score >= 70 else 'needs_improvement',
                        'description': f'Readability score: {readability_score}/100'
                    },
                    'keyword_density': {
                        'score': keyword_improvement,
                        'status': 'good' if keyword_improvement >= 2.0 else 'needs_improvement',
                        'description': f'Keyword density improvement: {keyword_improvement:.1f}x'
                    },
                    'achievement_metrics': {
                        'score': achievement_count,
                        'status': 'good' if achievement_count >= 3 else 'needs_improvement',
                        'description': f'Found {achievement_count} quantifiable achievements'
                    },
                    'structure': {
                        'score': structure_score,
                        'status': 'good' if structure_score >= 80 else 'needs_improvement',
                        'description': f'Structure score: {structure_score}/100'
                    },
                    'contact_info': {
                        'score': contact_score,
                        'status': 'complete' if contact_score == 100 else 'incomplete',
                        'description': 'Contact information complete' if contact_score == 100 else 'Missing contact information'
                    }
                },
                'improvement_summary': {
                    'original_length': len(original_resume),
                    'optimized_length': len(optimized_resume),
                    'length_change_percent': round((len(optimized_resume) - len(original_resume)) / max(len(original_resume), 1) * 100, 1),
                    'key_improvements': self._identify_key_improvements(original_resume, optimized_resume)
                },
                'recommendations': self._generate_recommendations(overall_health, {
                    'readability': readability_score,
                    'keyword_density': keyword_improvement,
                    'achievement_count': achievement_count,
                    'structure': structure_score,
                    'contact_info': contact_score
                })
            }
            
            print(f"✅ HealthTracker: Successfully calculated health metrics - Score: {result['overall_health']}")
            return result
            
        except Exception as e:
            print(f"❌ HealthTracker Error: {e}")
            return {
                'overall_health': 65,
                'metrics': {},
                'improvement_summary': {},
                'recommendations': ['Health tracking completed with basic analysis'],
                'error': str(e)
            }
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score based on various factors"""
        try:
            sentences = re.split(r'[.!?]+', text)
            words = re.findall(r'\b\w+\b', text.lower())
            
            if not sentences or not words:
                return 50.0
            
            # Average sentence length score (ideal: 15-20 words)
            avg_sentence_len = len(words) / len(sentences)
            sentence_score = max(0, 100 - abs(avg_sentence_len - 17.5) * 3)
            
            # Word variety score
            unique_words = len(set(words))
            variety_score = min(100, (unique_words / len(words)) * 200) if words else 50
            
            # Section structure score
            sections = ['experience', 'education', 'skills', 'summary', 'projects']
            section_score = sum(30 for section in sections if section in text.lower())
            
            return min(100, (sentence_score * 0.4 + variety_score * 0.3 + section_score * 0.3))
            
        except Exception as e:
            print(f"Readability calculation error: {e}")
            return 60.0
    
    def _calculate_keyword_density_improvement(self, original: str, optimized: str) -> float:
        """Calculate improvement in keyword density"""
        try:
            # Common resume keywords to track
            keywords = ['managed', 'led', 'created', 'improved', 'increased', 'reduced', 'developed', 'implemented']
            
            original_density = sum(original.lower().count(keyword) for keyword in keywords) / max(len(original.split()), 1)
            optimized_density = sum(optimized.lower().count(keyword) for keyword in keywords) / max(len(optimized.split()), 1)
            
            if original_density == 0:
                return 2.0 if optimized_density > 0 else 1.0
            
            improvement = optimized_density / original_density
            return min(improvement, 3.0)  # Cap at 3x improvement
            
        except Exception as e:
            print(f"Keyword density calculation error: {e}")
            return 1.0
    
    def _count_achievement_metrics(self, text: str) -> int:
        """Count quantifiable achievements in resume"""
        try:
            # Patterns for quantifiable achievements
            patterns = [
                r'\b\d+%?\b',  # percentages and numbers
                r'\$\d+',      # dollar amounts
                r'\b\d+\+?\s*(?:years?|yrs?)\b',  # years of experience
                r'\b(?:increased|reduced|improved|saved)\b.*?\bby\b',  # improvement phrases
            ]
            
            count = 0
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                count += len(matches)
            
            return min(count, 10)  # Cap at 10
            
        except Exception as e:
            print(f"Achievement counting error: {e}")
            return 0
    
    def _assess_structure(self, text: str) -> float:
        """Assess resume structure quality"""
        try:
            score = 0
            required_sections = ['experience', 'education', 'skills']
            optional_sections = ['summary', 'projects', 'certifications']
            
            text_lower = text.lower()
            
            # Check required sections
            for section in required_sections:
                if section in text_lower:
                    score += 25
            
            # Check optional sections
            for section in optional_sections:
                if section in text_lower:
                    score += 10
            
            return min(score, 100)
            
        except Exception as e:
            print(f"Structure assessment error: {e}")
            return 50.0
    
    def _check_contact_info(self, text: str) -> float:
        """Check if contact information is present"""
        try:
            # Basic contact info patterns
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
            
            has_email = bool(re.search(email_pattern, text))
            has_phone = bool(re.search(phone_pattern, text))
            
            if has_email and has_phone:
                return 100.0
            elif has_email or has_phone:
                return 50.0
            else:
                return 0.0
                
        except Exception as e:
            print(f"Contact info check error: {e}")
            return 0.0
    
    def _identify_key_improvements(self, original: str, optimized: str) -> list:
        """Identify key improvements between original and optimized"""
        improvements = []
        
        if len(optimized) > len(original) * 1.1:
            improvements.append("Added more detailed accomplishments")
        elif len(optimized) < len(original) * 0.9:
            improvements.append("Made resume more concise")
        
        original_achievements = self._count_achievement_metrics(original)
        optimized_achievements = self._count_achievement_metrics(optimized)
        
        if optimized_achievements > original_achievements:
            improvements.append(f"Added {optimized_achievements - original_achievements} quantifiable achievements")
        
        return improvements if improvements else ["General content optimization"]
    
    def _generate_recommendations(self, overall_score: float, metrics: dict) -> list:
        """Generate recommendations based on health metrics"""
        recommendations = []
        
        if overall_score < 70:
            recommendations.append("Focus on adding more quantifiable achievements with numbers and metrics")
        
        if metrics.get('readability', 0) < 70:
            recommendations.append("Improve readability by varying sentence length and structure")
        
        if metrics.get('keyword_density', 0) < 1.5:
            recommendations.append("Increase action-oriented keywords like 'managed', 'created', 'improved'")
        
        if metrics.get('achievement_count', 0) < 3:
            recommendations.append("Add more specific achievements with numbers (e.g., 'increased sales by 15%')")
        
        if metrics.get('contact_info', 0) < 100:
            recommendations.append("Ensure email and phone number are clearly included")
        
        return recommendations if recommendations else ["Resume is in good health! Maintain current quality."]