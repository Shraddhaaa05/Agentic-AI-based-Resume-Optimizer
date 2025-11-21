# test_agent.py
import asyncio
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.jd_analysis_agent import JDAnalysisAgent
from agents.resume_critique_agent import ResumeCritiqueAgent
from agents.resume_rewriter_agent import ResumeRewriterAgent
from agents.final_scorer_agent import FinalScorerAgent
from agents.job_search_agent import JobSearchAgent

async def test_jd_analysis_agent():
    """Test JD Analysis Agent"""
    print("1. Testing JD Analysis Agent...")
    try:
        agent = JDAnalysisAgent()
        jd_text = "We are looking for a Data Analyst with SQL, Python, and Tableau experience. 3+ years required."
        result = await agent.analyze_job_description(jd_text)
        print(f"✅ JD Analysis: {result}")
        return True
    except Exception as e:
        print(f"❌ JD Analysis Failed: {e}")
        return False

async def test_resume_critique_agent():
    """Test Resume Critique Agent"""
    print("2. Testing Resume Critique Agent...")
    try:
        agent = ResumeCritiqueAgent()
        resume_text = "Experienced Data Analyst with 5 years in SQL and Python. Managed data projects and created dashboards."
        jd_text = "Looking for Data Analyst with SQL and Python skills."
        result = await agent.critique_resume(resume_text, jd_text)
        print(f"✅ Resume Critique: {result}")
        return True
    except Exception as e:
        print(f"❌ Resume Critique Failed: {e}")
        return False

async def test_resume_rewriter_agent():
    """Test Resume Rewriter Agent"""
    print("3. Testing Resume Rewriter Agent...")
    try:
        agent = ResumeRewriterAgent()
        resume_text = "Data Analyst with SQL experience."
        jd_text = "Seeking Data Analyst with Python and SQL skills."
        result = await agent.rewrite_resume(resume_text, jd_text, "Data Analyst", "Remote")
        
        # Check if result is valid
        if result and len(result) > 10:
            print(f"✅ Resume Rewriter: Success! Output length: {len(result)} characters")
            return True
        else:
            print(f"❌ Resume Rewriter: Empty or invalid output")
            return False
    except Exception as e:
        print(f"❌ Resume Rewriter Failed: {e}")
        return False

async def test_final_scorer_agent():
    """Test Final Scorer Agent"""
    print("4. Testing Final Scorer Agent...")
    try:
        agent = FinalScorerAgent()
        original_resume = "Data Analyst with SQL skills."
        optimized_resume = "Experienced Data Analyst proficient in SQL, Python, and data visualization. Managed multiple data projects."
        jd_text = "Data Analyst with SQL and Python experience required."
        
        result = await agent.calculate_final_score(original_resume, optimized_resume, jd_text, "Data Analyst")
        print(f"✅ Final Scorer: Overall Score: {result.get('overall_score', 'N/A')}%")
        return True
    except Exception as e:
        print(f"❌ Final Scorer Failed: {e}")
        return False

async def test_job_search_agent():
    """Test Job Search Agent"""
    print("5. Testing Job Search Agent...")
    try:
        agent = JobSearchAgent()
        result = await agent.search_real_jobs("Data Analyst", "Remote")
        print(f"✅ Job Search: Found {len(result)} jobs")
        return True
    except Exception as e:
        print(f"❌ Job Search Failed: {e}")
        return False

async def test_agent_manager():
    """Test the complete Agent Manager"""
    print("6. Testing Agent Manager...")
    try:
        from agents.agent_manager import AgentManager
        manager = AgentManager()
        
        resume_text = """
        John Doe
        Data Analyst
        Experience:
        - Analyzed data using SQL and Python
        - Created reports and dashboards
        - Managed data quality projects
        """
        
        jd_text = "Data Analyst with SQL, Python, and Tableau experience. Strong analytical skills required."
        
        result = await manager.optimize_resume(resume_text, jd_text, "Data Analyst", "Remote")
        
        if result and 'optimized_resume' in result:
            print(f"✅ Agent Manager: Success! Optimized resume length: {len(result['optimized_resume'])} characters")
            print(f"✅ Overall Score: {result.get('final_score', {}).get('overall_score', 'N/A')}%")
            return True
        else:
            print("❌ Agent Manager: Invalid result")
            return False
            
    except Exception as e:
        print(f"❌ Agent Manager Failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Testing AI Agents...")
    print("=" * 50)
    
    results = []
    
    # Test individual agents
    results.append(await test_jd_analysis_agent())
    results.append(await test_resume_critique_agent())
    results.append(await test_resume_rewriter_agent())
    results.append(await test_final_scorer_agent())
    results.append(await test_job_search_agent())
    results.append(await test_agent_manager())
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(results)
    
    for i, passed in enumerate(results):
        status = "✅ PASS" if passed else "❌ FAIL"
        test_names = [
            "JD Analysis", "Resume Critique", "Resume Rewriter", 
            "Final Scorer", "Job Search", "Agent Manager"
        ]
        print(f"{i+1}. {test_names[i]}: {status}")
    
    print(f"\n🎯 Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! System is ready.")
    else:
        print("⚠️ Some tests failed. Check the implementations.")

if __name__ == "__main__":
    asyncio.run(main())
    