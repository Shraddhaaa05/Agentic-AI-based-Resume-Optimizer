import streamlit as st
from typing import List, Dict, Any

class JobDisplay:
    @staticmethod
    def display_jobs(jobs: List[Dict[str, Any]]):
        """Display job listings using Streamlit with clickable apply links."""
        if not jobs:
            st.info("No job listings found for your search criteria.")
            return

        st.subheader("🎯 Real-Time Job Matches")

        for job in jobs:
            with st.container():
                st.markdown(f"**{job.get('title', 'Unknown Role')}**")
                st.markdown(f"🏢 {job.get('company', 'Unknown')} • 📍 {job.get('location', 'Remote')}")
                st.markdown(f"*{job.get('description', '')}*")
                # Use link_button for apply now
                apply_url = job.get('apply_url', None)
                if apply_url:
                    st.link_button(
                        "🚀 Apply Now",
                        apply_url,
                        type="primary",
                        use_container_width=True
                    )
                # Optionally show source, salary, etc.
                st.markdown(f"💰 **{job.get('salary', 'Competitive')}** — Source: {job.get('source', '')}")
                st.divider()
