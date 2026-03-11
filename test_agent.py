# test_agent.py
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.jd_analysis_agent import JDAnalysisAgent
from agents.resume_critique_agent import ResumeCritiqueAgent
from agents.resume_rewriter_agent import ResumeRewriterAgent
from agents.final_scorer_agent import FinalScorerAgent
from agents.job_search_agent import JobSearchAgent
from agents.agent_manager import AgentManager

SAMPLE_RESUME = """
John Doe | john.doe@email.com | (123) 456-7890
Data Analyst

SUMMARY
Experienced Data Analyst with 4 years delivering insights that drive business decisions.

EXPERIENCE
Senior Data Analyst — ABC Corp (2021–Present)
- Analysed datasets of 10M+ rows using SQL and Python, reducing reporting time by 30%
- Built Tableau dashboards adopted by 5 business units
- Led data quality initiative improving accuracy by 25%

SKILLS
Python, SQL, Tableau, Power BI, Excel, Statistics, Machine Learning basics

EDUCATION
BSc Computer Science — State University, 2020
"""
SAMPLE_JD = "Data Analyst with SQL, Python, and Tableau. 3+ years required. Strong communication skills."

async def run_tests():
    tests = [
        ("JD Analysis",    _test_jd),
        ("Resume Critique", _test_critique),
        ("Resume Rewriter", _test_rewriter),
        ("Final Scorer",    _test_scorer),
        ("Job Search",      _test_jobs),
        ("Agent Manager",   _test_manager),
    ]
    print("🧪 Running CareerCatalyst AI test suite\n" + "="*50)
    results = []
    for name, fn in tests:
        try:
            ok = await fn()
            results.append((name, ok))
        except Exception as e:
            print(f"  ❌ Uncaught error in {name}: {e}")
            results.append((name, False))

    print("\n" + "="*50 + "\n📊 RESULTS")
    for name, ok in results:
        print(f"  {'✅' if ok else '❌'} {name}")
    passed = sum(1 for _, ok in results if ok)
    print(f"\n🎯 {passed}/{len(results)} passed")
    return passed == len(results)

async def _test_jd():
    r = await JDAnalysisAgent().analyze_job_description(SAMPLE_JD)
    ok = bool(r.get('key_skills'))
    print(f"  JD skills found: {r.get('key_skills',[])[:3]}")
    return ok

async def _test_critique():
    r = await ResumeCritiqueAgent().critique_resume(SAMPLE_RESUME, SAMPLE_JD)
    ok = bool(r.get('strengths'))
    print(f"  Strengths: {r.get('strengths',[])[:2]}")
    return ok

async def _test_rewriter():
    r = await ResumeRewriterAgent().rewrite_resume(SAMPLE_RESUME, SAMPLE_JD, "Data Analyst", "Remote")
    ok = len(r) > 50
    print(f"  Rewritten length: {len(r)} chars")
    return ok

async def _test_scorer():
    r = await FinalScorerAgent().calculate_final_score(SAMPLE_RESUME, SAMPLE_RESUME + " optimised", SAMPLE_JD, "Data Analyst")
    ok = 'overall_score' in r
    print(f"  Score: {r.get('overall_score')}% | Confidence: {r.get('confidence_level')}")
    return ok

async def _test_jobs():
    r = await JobSearchAgent().search_real_jobs("Data Analyst", "Remote")
    ok = isinstance(r, list) and len(r) > 0
    print(f"  Jobs found: {len(r)}")
    return ok

async def _test_manager():
    r = await AgentManager().optimize_resume(SAMPLE_RESUME, SAMPLE_JD, "Data Analyst", "Remote")
    ok = 'optimized_resume' in r and len(r.get('optimized_resume','')) > 10
    print(f"  Optimised length: {len(r.get('optimized_resume',''))} chars | Score: {r.get('final_score',{}).get('overall_score')}%")
    return ok

if __name__ == "__main__":
    asyncio.run(run_tests())