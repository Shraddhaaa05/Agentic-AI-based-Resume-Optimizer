# agents/resume_rewriter_agent.py
from typing import Optional


class ResumeRewriterAgent:
    WEAK_OPENERS = {
        'worked on':       'Contributed to',
        'helped with':     'Collaborated on',
        'responsible for': 'Managed',
        'did':             'Executed',
        'made':            'Developed',
    }
    KNOWN_SKILLS = [
        'Python', 'SQL', 'Excel', 'Tableau', 'Power BI', 'R', 'AWS', 'Azure',
        'Machine Learning', 'Statistics', 'ETL', 'Spark', 'Docker', 'JavaScript', 'Java',
    ]
    METRICS_TIP = (
        '\n[Tip: Add metrics to your bullets — '
        'e.g. "Reduced report generation time by 30%" '
        'or "Managed a dataset of 1M+ rows"]'
    )

    async def rewrite_resume(
        self,
        resume_text: str,
        job_description: str = None,
        target_role: str = "",
        location: str = "",
    ) -> str:
        """Rewrite and enhance resume. Falls back to the original on any error."""
        try:
            if not resume_text or len(resume_text.strip()) < 10:
                return "Please provide a resume to optimize."
            optimized = self._enhance_resume(resume_text, job_description, target_role, location)
            return optimized if optimized and len(optimized.strip()) > 10 else resume_text
        except Exception as e:
            print(f"Resume rewrite failed: {e}")
            return resume_text

    # ------------------------------------------------------------------ #

    def _enhance_resume(
        self,
        resume: str,
        jd: Optional[str],
        target_role: str,
        location: str,
    ) -> str:
        parts = []

        # --- Professional Summary (inject if missing) ---
        if 'summary' not in resume.lower() and 'objective' not in resume.lower():
            role_label = target_role or "professional"
            depth = "extensive" if len(resume.split()) > 300 else "solid"
            summary_text = (
                "PROFESSIONAL SUMMARY\n"
                "Results-driven " + role_label + " with a " + depth + " background "
                "in data analysis, process improvement, and cross-functional collaboration. "
                "Proven ability to transform complex data into actionable business insights."
            )
            parts.append(summary_text)

        # --- Enhance bullet points ---
        has_metrics = any(c.isdigit() for c in resume)
        enhanced_lines = []
        for line in resume.strip().splitlines():
            stripped = line.strip()
            for weak, strong in self.WEAK_OPENERS.items():
                if stripped.lower().startswith(weak):
                    line = line.replace(stripped[:len(weak)], strong, 1)
                    break
            enhanced_lines.append(line)

        if not has_metrics:
            enhanced_lines.append(self.METRICS_TIP)

        parts.append("\n".join(enhanced_lines))

        # --- JD-aligned skills block ---
        if jd:
            jd_lower = jd.lower()
            found = [s for s in self.KNOWN_SKILLS if s.lower() in jd_lower]
            if found:
                parts.append("KEY SKILLS (JD-Aligned)\n" + ", ".join(found[:8]))

        # --- Location tag ---
        if location and location.lower() not in resume.lower():
            parts.append("Location Preference: " + location)

        return "\n\n".join(parts)