# test_system.py — end-to-end orchestrator test
import asyncio, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orchestrator import FastOrchestrator

SAMPLE = """
Jane Smith | jane@email.com | +1-555-0100
Software Developer

SUMMARY
Full-stack developer with 3 years building scalable web applications.

EXPERIENCE
Software Developer — XYZ Startup (2021–Present)
- Developed REST APIs in Python (FastAPI), serving 50k+ daily requests
- Built React dashboards reducing customer support tickets by 40%
- Migrated legacy monolith to microservices on AWS

SKILLS
Python, JavaScript, React, Node.js, AWS, Docker, PostgreSQL, Git

EDUCATION
BS Computer Science — Tech University, 2021
"""

async def main():
    print("🧪 End-to-end orchestrator test")
    with open("_test_resume.txt", "w") as f: f.write(SAMPLE)
    try:
        result = await FastOrchestrator().process_resume(
            "_test_resume.txt",
            "Python developer with React experience. AWS knowledge a plus. 2+ years required.",
            "Software Developer",
            "Remote",
        )
        print(f"✅ Score:       {result['final_score']['overall_score']}/100")
        print(f"✅ Improvement: +{result.get('improvement_percentage',0):.1f}%")
        print(f"✅ Features:    {result.get('processing_metadata',{}).get('features_count',0)} processed")
        print(f"✅ Jobs:        {result.get('processing_metadata',{}).get('jobs_found',0)} found")
    finally:
        if os.path.exists("_test_resume.txt"): os.remove("_test_resume.txt")

if __name__ == "__main__":
    asyncio.run(main())