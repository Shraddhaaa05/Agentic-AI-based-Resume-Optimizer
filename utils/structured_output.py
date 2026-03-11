# utils/structured_output.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class JobRequirements(BaseModel):
    required_skills: List[str] = Field(description="Must-have technical and soft skills")
    preferred_skills: List[str] = Field(description="Nice-to-have skills")
    qualifications: List[str] = Field(description="Educational and certification requirements")
    experience_level: str = Field(description="Entry, Mid, Senior, Executive")
    responsibilities: List[str] = Field(description="Key tasks and responsibilities")
    keywords: List[str] = Field(description="Important ATS keywords")

class ResumeGapAnalysis(BaseModel):
    missing_skills: List[str] = Field(description="Skills from JD missing in resume")
    weak_areas: List[str] = Field(description="Areas that need improvement")
    keyword_gaps: List[str] = Field(description="Missing important keywords")
    experience_gaps: List[str] = Field(description="Gaps in experience or qualifications")
    recommendations: List[str] = Field(description="Actionable improvement recommendations")

class ATSScore(BaseModel):
    overall_score: int = Field(description="ATS compatibility score 0-100")
    keyword_match: int = Field(description="Keyword match percentage")
    skills_match: int = Field(description="Skills alignment percentage")
    experience_match: int = Field(description="Experience level match")
    rationale: str = Field(description="Explanation of the score")

class JobListing(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    location: str = Field(description="Job location")
    url: str = Field(description="Job application URL")
    match_score: int = Field(description="Match score with resume 0-100")