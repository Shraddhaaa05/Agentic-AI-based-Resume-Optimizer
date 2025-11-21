class JobFormatter:
    @staticmethod
    def format_job_listings(jobs):
        """
        jobs: list of dicts
        Returns jobs with clean keys and sanitized values for UI.
        """
        formatted = []
        for job in jobs:
            formatted.append({
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "salary": job.get("salary", ""),
                "apply_url": job.get("apply_url", ""),
                "description": job.get("description", ""),
                "source": job.get("source", "unknown"),
                "verified": job.get("verified", False),
            })
        return formatted
