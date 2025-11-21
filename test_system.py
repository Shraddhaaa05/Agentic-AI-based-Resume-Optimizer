# test_system.py
import asyncio
import os
from orchestrator import FastOrchestrator

async def test_system():
    """Test the system with a sample resume"""
    print("🧪 Testing the resume optimizer system...")
    
    # Create a sample resume text file for testing
    sample_resume = """
    JOHN DOE
    Software Developer
    john.doe@email.com | (123) 456-7890 | linkedin.com/in/johndoe
    
    SUMMARY
    Experienced software developer with 3 years in web development.
    
    EXPERIENCE
    Software Developer, ABC Tech (2021-Present)
    - Developed web applications using Python and JavaScript
    - Worked on frontend and backend features
    - Collaborated with team members
    
    SKILLS
    Python, JavaScript, HTML, CSS, React, Node.js
    """
    
    # Save sample resume
    with open("test_resume.txt", "w") as f:
        f.write(sample_resume)
    
    # Test the system
    orchestrator = FastOrchestrator()
    result = await orchestrator.process_resume(
        "test_resume.txt", 
        "Looking for a Python developer with React experience. Must have 2+ years in web development.",
        "Software Developer",
        "Remote"
    )
    
    print("✅ Test completed successfully!")
    print(f"📊 ATS Score: {result['final_score']['overall_score']}/100")
    print(f"📈 Improvement: +{result['improvement_percentage']}%")
    
    # Cleanup
    os.remove("test_resume.txt")

if __name__ == "__main__":
    asyncio.run(test_system())