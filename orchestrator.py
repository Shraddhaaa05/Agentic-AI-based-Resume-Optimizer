import asyncio
import importlib
import os
from datetime import datetime

from utils.file_processor import FileProcessor
from agents.agent_manager import AgentManager
from agents.job_search_agent import JobSearchAgent

class DynamicFeatureStub:
    def __init__(self, feature_name, methods=None):
        self.feature_name = feature_name
        self.methods = methods or []

    def __getattr__(self, name):
        def stub(*args, **kwargs):
            return {'status': 'stub', 'feature': self.feature_name}
        return stub

class FastOrchestrator:
    def __init__(self):
        self.agent_manager = AgentManager()
        self.file_processor = FileProcessor()
        self.job_search_agent = JobSearchAgent()
        self.features = self._load_features()

    def _load_features(self):
        feature_config = {
            'ab_testing': ('ABTestingAgent', ['generate_variants']),
            'company_research': ('CompanyResearchAgent', ['analyze_company']),
            'culture_fit_analyzer': ('CultureFitAnalyzer', ['analyze_fit']),
            'global_optimizer': ('GlobalOptimizer', ['optimize_for_international']),
            'industry_specialist': ('IndustrySpecialist', ['analyze_industry_fit']),
            'interactive_builder': ('InteractiveBuilder', ['get_improvement_suggestions']),
            'interview_prep': ('InterviewPrepAgent', ['generate_questions']),
            'learning_path': ('LearningPathAgent', ['generate_learning_plan']),
            'market_intelligence': ('MarketIntelligenceAgent', ['get_market_insights']),
            'mobile_optimizer': ('MobileOptimizer', ['analyze_mobile_compatibility']),
            'networking_engine': ('NetworkingEngine', ['generate_networking_strategy']),
            'resume_health_track': ('ResumeHealthTracker', ['track_health_metrics']),
            'storytelling_agent': ('StorytellingAgent', ['craft_career_narrative']),
            'visual_analytics': ('VisualAnalytics', ['generate_analytics']),
            'resume_comparison': ('ResumeComparison', ['generate_comparison']),
        }

        feats = {}
        for name, (cls_name, methods) in feature_config.items():
            try:
                module = importlib.import_module(f'features.{name}')
                cls = getattr(module, cls_name)
                feats[name] = cls()
            except Exception as e:
                feats[name] = DynamicFeatureStub(name, methods)
        return feats

    async def process_resume(self, file_path, job_description, target_role, location):
        try:
            resume_text = self.file_processor.extract_text(file_path)

            core = await self.agent_manager.optimize_resume(
                resume_text, job_description, target_role, location
            )
            if isinstance(core, str):
                core = {
                    'optimized_resume': core,
                    'final_score': {'overall_score': 0, 'confidence_level': 'low'},
                    'improvement_percentage': 0,
                    'jd_analysis': {},
                    'critique': {},
                    'gap_analysis': {}
                }

            optimized_resume = core.get('optimized_resume', resume_text)
            feature_results = await self._run_features(resume_text, optimized_resume, job_description, target_role, location)
            jobs = await self._get_jobs(target_role, location)

            result = {
                **core,
                **feature_results,
                'job_listings': jobs,
                'processing_metadata': {
                    'timestamp': datetime.utcnow().isoformat(),
                    'features_count': len(feature_results),
                    'jobs_found': len(jobs),
                }
            }
            return result

        except Exception as e:
            return self._fallback(str(e))

    async def _run_features(self, orig, opt, jd, role, loc):
        tasks = []
        method_map = {
            'resume_comparison': (['generate_comparison'], [orig, opt, jd]),
            'learning_path': (['generate_learning_plan'], [opt, role]),
            # Add other feature mappings as needed
        }

        for fname, (methods, args) in method_map.items():
            feat = self.features.get(fname)
            if feat:
                for m in methods:
                    if hasattr(feat, m):
                        method = getattr(feat, m)
                        if asyncio.iscoroutinefunction(method):
                            tasks.append(method(*args))
                        else:
                            tasks.append(asyncio.to_thread(method, *args))
                        break

        results = await asyncio.gather(*tasks, return_exceptions=True)
        output = {}
        for fname, res in zip(method_map.keys(), results):
            if not isinstance(res, Exception):
                output[fname] = res
        return output

    async def _get_jobs(self, target_role, location):
        if not target_role:
            return []
        try:
            jobs = await self.job_search_agent.search_real_jobs(target_role, location)
            return jobs or []
        except Exception:
            return []

    def _fallback(self, error_msg):
        return {
            'error': error_msg,
            'optimized_resume': "",
            'final_score': {'overall_score': 0, 'confidence_level': 'low'},
            'improvement_percentage': 0,
            'jd_analysis': {},
            'critique': {},
            'gap_analysis': {},
            'job_listings': []
        }
