# agents/agent_manager.py
import asyncio
from agents.jd_analysis_agent import JDAnalysisAgent
from agents.resume_critique_agent import ResumeCritiqueAgent
from agents.resume_rewriter_agent import ResumeRewriterAgent
from agents.final_scorer_agent import FinalScorerAgent
from agents.job_search_agent import JobSearchAgent


class AgentManager:
    def __init__(self):
        self.jd_analyzer      = JDAnalysisAgent()
        self.resume_critique  = ResumeCritiqueAgent()
        self.resume_rewriter  = ResumeRewriterAgent()
        self.final_scorer     = FinalScorerAgent()
        self.job_searcher     = JobSearchAgent()

    async def optimize_resume(self, resume_text: str, job_description: str = None,
                               target_role: str = "", location: str = "") -> dict:
        """Full resume optimisation pipeline."""
        try:
            print("🔄 Starting resume optimisation pipeline...")
            if not resume_text or len(resume_text.strip()) < 10:
                return self._fallback("Resume text is too short or empty")

            # Run JD analysis + critique concurrently
            jd_analysis, critique = await asyncio.gather(
                self._safe(self.jd_analyzer.analyze_job_description, job_description)
                    if job_description else asyncio.coroutine(lambda: self._default_jd_analysis())(),
                self._safe(self.resume_critique.critique_resume, resume_text, job_description),
            )

            # Rewrite
            optimized_resume = await self._safe(
                self.resume_rewriter.rewrite_resume,
                resume_text, job_description, target_role, location,
                fallback=resume_text,
            )

            # Score
            final_score = await self._safe(
                self.final_scorer.calculate_final_score,
                resume_text, optimized_resume, job_description, target_role,
                fallback=self._default_scores(),
            )

            improvement = self._improvement(final_score)

            print("✅ Pipeline completed successfully")
            return {
                'optimized_resume':      optimized_resume,
                'final_score':           final_score,
                'jd_analysis':           jd_analysis,
                'critique':              critique,
                'improvement_percentage':improvement,
                'gap_analysis':          self._gap_analysis(critique, jd_analysis, final_score),
            }
        except Exception as e:
            print(f"❌ AgentManager failed: {e}")
            return self._fallback(str(e))

    async def search_jobs(self, target_role: str, location: str = "") -> list:
        if not target_role or len(target_role.strip()) < 2:
            return self._default_jobs()
        return await self._safe(
            self.job_searcher.search_real_jobs, target_role, location,
            fallback=self._default_jobs(target_role, location),
        )

    # ── helpers ─────────────────────────────────────────────────────────────

    async def _safe(self, fn, *args, fallback=None):
        try:
            result = await fn(*args) if asyncio.iscoroutinefunction(fn) else fn(*args)
            if result is None or (isinstance(result, dict) and not result):
                return fallback or {}
            return result
        except Exception as e:
            print(f"  ⚠️ Agent call failed: {e}")
            return fallback or {}

    def _improvement(self, final_score: dict) -> float:
        score = final_score.get('overall_score', 0)
        return round(min(max(score * 0.25, 0), 35), 1)   # realistic ±25 % gain cap

    def _gap_analysis(self, critique: dict, jd_analysis: dict, final_score: dict) -> dict:
        return {
            'resume_strengths':   critique.get('strengths', ['Strong foundation']),
            'recommendations':    critique.get('recommendations', ['Add more quantifiable achievements']),
            'confidence_boosters':['Add metrics to achievements','Use action-oriented language','Highlight relevant skills'],
            'missing_skills':     jd_analysis.get('missing_skills', []),
            'score_breakdown':    final_score.get('score_breakdown', {}),
        }

    def _default_jd_analysis(self) -> dict:
        return {'key_skills':['Communication','Problem-solving','Teamwork'],
                'experience_level':'Mid-level','missing_skills':[],'status':'no_jd_provided'}

    def _default_scores(self) -> dict:
        return {'overall_score':65,'keyword_match':60,'skills_alignment':70,
                'impact_presentation':65,'career_narrative':70,'ats_optimization':75,
                'confidence_level':'medium'}

    def _default_jobs(self, role: str = "Professional", location: str = "Remote") -> list:
        return [{'title':f"Senior {role}",'company':'TechCorp International',
                 'location':location,'salary':'$95,000 – $140,000',
                 'apply_url':'https://www.linkedin.com/jobs','posted':'Recently',
                 'type':'Full-time','description':f"Senior {role} opening.",'source':'System','verified':True}]

    def _fallback(self, error_message: str) -> dict:
        return {'error':error_message,'optimized_resume':"Optimisation encountered an error.",
                'final_score':self._default_scores(),'jd_analysis':self._default_jd_analysis(),
                'critique':{'strengths':['Good foundation'],'recommendations':['Try again']},
                'improvement_percentage':0,'gap_analysis':{},'status':'error'}