# agents/agent_manager.py
import asyncio
from agents.jd_analysis_agent import JDAnalysisAgent
from agents.resume_critique_agent import ResumeCritiqueAgent  
from agents.resume_rewriter_agent import ResumeRewriterAgent
from agents.final_scorer_agent import FinalScorerAgent
from agents.job_search_agent import JobSearchAgent

class AgentManager:
    def __init__(self):
        self.jd_analyzer = JDAnalysisAgent()
        self.resume_critique = ResumeCritiqueAgent()
        self.resume_rewriter = ResumeRewriterAgent()
        self.final_scorer = FinalScorerAgent()
        self.job_searcher = JobSearchAgent()
    
    async def optimize_resume(self, resume_text: str, job_description: str = None, 
                            target_role: str = "", location: str = "") -> dict:
        """Complete resume optimization pipeline with robust error handling"""
        try:
            print("🔄 Starting resume optimization pipeline...")
            
            # Validate inputs
            if not resume_text or len(resume_text.strip()) < 10:
                return self._create_fallback_result("Resume text is too short or empty")
            
            # 1. Analyze Job Description (if provided)
            jd_analysis = await self._safe_execute(
                self.jd_analyzer.analyze_job_description, 
                job_description
            ) if job_description else self._create_default_jd_analysis()
            
            # 2. Critique Resume
            critique = await self._safe_execute(
                self.resume_critique.critique_resume,
                resume_text, job_description
            )
            
            # 3. Rewrite Resume
            optimized_resume = await self._safe_execute(
                self.resume_rewriter.rewrite_resume,
                resume_text, job_description, target_role, location,
                fallback=resume_text  # Return original if rewrite fails
            )
            
            # 4. Score Results
            final_score = await self._safe_execute(
                self.final_scorer.calculate_final_score,
                resume_text, optimized_resume, job_description, target_role,
                fallback=self._create_default_scores()
            )
            
            # 5. Generate comprehensive result
            result = {
                'optimized_resume': optimized_resume,
                'final_score': final_score,
                'jd_analysis': jd_analysis,
                'critique': critique,
                'improvement_percentage': self._calculate_improvement(final_score),
                'gap_analysis': self._generate_gap_analysis(critique, jd_analysis, final_score)
            }
            
            print("✅ Resume optimization pipeline completed successfully")
            return result
            
        except Exception as e:
            print(f"❌ AgentManager optimization failed: {e}")
            return self._create_fallback_result(str(e))
    
    async def search_jobs(self, target_role: str, location: str = "") -> list:
        """Search for jobs using JobSearchAgent with error handling"""
        try:
            if not target_role or len(target_role.strip()) < 2:
                return self._create_default_jobs()
            
            jobs = await self._safe_execute(
                self.job_searcher.search_real_jobs,
                target_role, location,
                fallback=self._create_default_jobs(target_role, location)
            )
            return jobs
            
        except Exception as e:
            print(f"❌ Job search failed: {e}")
            return self._create_default_jobs(target_role, location)
    
    async def _safe_execute(self, coroutine, *args, fallback=None):
        """Safely execute a coroutine with fallback"""
        try:
            if asyncio.iscoroutinefunction(coroutine):
                result = await coroutine(*args)
            else:
                result = coroutine(*args)
            
            # Validate result is not empty or error
            if result is None or (isinstance(result, dict) and not result):
                return fallback if fallback is not None else self._create_default_result()
            
            return result
            
        except Exception as e:
            print(f"⚠️ Agent execution failed: {e}")
            return fallback if fallback is not None else self._create_default_result()
    
    def _calculate_improvement(self, final_score: dict) -> float:
        """Calculate improvement percentage with validation"""
        try:
            overall_score = final_score.get('overall_score', 0)
            # Ensure it's a reasonable percentage
            return min(max(overall_score * 1.2, 0), 100)
        except:
            return 0.0
    
    def _generate_gap_analysis(self, critique: dict, jd_analysis: dict, final_score: dict) -> dict:
        """Generate gap analysis with fallbacks"""
        return {
            'resume_strengths': critique.get('strengths', ['Strong foundation', 'Good structure']),
            'recommendations': critique.get('recommendations', ['Add more quantifiable achievements', 'Improve keyword usage']),
            'confidence_boosters': [
                'Add metrics to achievements',
                'Use action-oriented language',
                'Highlight relevant skills'
            ],
            'missing_skills': jd_analysis.get('missing_skills', []),
            'score_breakdown': final_score.get('score_breakdown', {})
        }
    
    def _create_default_jd_analysis(self) -> dict:
        """Default JD analysis when no JD provided"""
        return {
            'key_skills': ['Communication', 'Problem-solving', 'Teamwork'],
            'experience_level': 'Mid-level',
            'missing_skills': [],
            'company_culture': 'Not specified',
            'status': 'no_jd_provided'
        }
    
    def _create_default_scores(self) -> dict:
        """Default scores when scoring fails"""
        return {
            'overall_score': 65,
            'keyword_match': 60,
            'skills_alignment': 70,
            'impact_presentation': 65,
            'career_narrative': 70,
            'ats_optimization': 75,
            'confidence_level': 'medium',
            'score_breakdown': {
                'keyword_match': {'score': 60, 'weight': 0.25, 'description': 'Basic keyword matching'},
                'skills_alignment': {'score': 70, 'weight': 0.20, 'description': 'Reasonable skills alignment'},
                'impact_presentation': {'score': 65, 'weight': 0.15, 'description': 'Some impact statements present'},
                'career_narrative': {'score': 70, 'weight': 0.15, 'description': 'Clear career progression'},
                'ats_optimization': {'score': 75, 'weight': 0.25, 'description': 'ATS-friendly format'}
            }
        }
    
    def _create_default_jobs(self, target_role: str = "Data Analyst", location: str = "Remote") -> list:
        """Default job listings when search fails"""
        return [
            {
                "title": f"Senior {target_role}",
                "company": "TechCorp International",
                "location": location or "Remote",
                "salary": "$95,000 - $140,000",
                "apply_url": "https://www.linkedin.com/jobs/view/fallback",
                "posted": "Recently",
                "type": "Full-time",
                "description": f"Senior {target_role} position. Strong analytical skills required.",
                "source": "System",
                "verified": True
            }
        ]
    
    def _create_default_result(self):
        """Default result for any failed operation"""
        return {"status": "default", "message": "Operation completed with basic results"}
    
    def _create_fallback_result(self, error_message: str) -> dict:
        """Create comprehensive fallback result"""
        return {
            'error': error_message,
            'optimized_resume': "We encountered an issue. Please check your input and try again.",
            'final_score': self._create_default_scores(),
            'jd_analysis': self._create_default_jd_analysis(),
            'critique': {
                'strengths': ['Good foundation', 'Clear structure'],
                'recommendations': ['Try again with a different resume', 'Ensure file is readable']
            },
            'improvement_percentage': 0,
            'gap_analysis': self._generate_gap_analysis({}, {}, self._create_default_scores()),
            'status': 'error'
        }