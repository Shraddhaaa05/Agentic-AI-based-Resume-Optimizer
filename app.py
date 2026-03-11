# app.py
import streamlit as st
import asyncio
import os
import tempfile
from datetime import datetime
import plotly.graph_objects as go
import difflib

from orchestrator import FastOrchestrator

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CareerCatalyst AI | Resume Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  .main-header{font-size:3rem;font-weight:700;text-align:center;margin-bottom:1rem;
    background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
  .premium-card,.job-card,.metric-card{padding:1.5rem;border-radius:12px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);margin:1rem 0;}
  .premium-card{background:#fff;border:1px solid #e0e0e0;text-align:center;}
  .metric-card{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;text-align:center;}
  .job-card{background:#fff;border-left:4px solid #667eea;}
  .diff-added{background:#d4edda;padding:2px 4px;border-radius:3px;}
  .diff-removed{background:#f8d7da;padding:2px 4px;border-radius:3px;text-decoration:line-through;}
  .stButton>button{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;
    border-radius:8px;font-weight:600;}
</style>
""", unsafe_allow_html=True)


# ── Chart helpers ────────────────────────────────────────────────────────────

def radar_chart(score_data: dict) -> go.Figure:
    cats   = ['Technical Alignment','Strategic Impact','Career Narrative','Market Relevance','ATS Compliance']
    scores = [score_data.get('skills_alignment',0), score_data.get('impact_presentation',0),
              score_data.get('career_narrative',0),  score_data.get('keyword_match',0),
              score_data.get('ats_optimization',0)]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=scores+[scores[0]], theta=cats+[cats[0]],
        fill='toself', line=dict(color='#667eea',width=3), fillcolor='rgba(102,126,234,0.3)', name='Profile'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),
                      showlegend=False, height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def gauge_chart(current_score: float, improvement: float) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        delta={'reference': current_score - improvement, 'increasing': {'color': '#00d26a'}},
        title={'text': 'Competitive Score'},
        gauge={'axis': {'range': [None, 100]}, 'bar': {'color': '#667eea'},
               'steps': [{'range':[0,60],'color':'#ff6b6b'},{'range':[60,80],'color':'#ffd93d'},{'range':[80,100],'color':'#00d26a'}]},
    ))
    fig.update_layout(height=300)
    return fig

def improvement_chart(comparison_data: dict):
    if not comparison_data or 'metrics' not in comparison_data:
        return None
    m = comparison_data['metrics']
    cats = ['Content Volume', 'Achievements', 'Skills', 'Impact']
    orig = [m.get('word_count',{}).get('original',0), m.get('achievement_count',{}).get('original',0),
            m.get('skill_mentions',{}).get('original',0), m.get('action_verbs',{}).get('original',0)]
    opt  = [m.get('word_count',{}).get('optimized',0), m.get('achievement_count',{}).get('optimized',0),
            m.get('skill_mentions',{}).get('optimized',0), m.get('action_verbs',{}).get('optimized',0)]
    fig = go.Figure(data=[
        go.Bar(name='Before', x=cats, y=orig, marker_color='#95a5a6'),
        go.Bar(name='After',  x=cats, y=opt,  marker_color='#667eea'),
    ])
    fig.update_layout(barmode='group', title="Content Enhancement Analysis", height=400)
    return fig


# ── Display helpers ──────────────────────────────────────────────────────────

def display_jobs(jobs: list):
    if not jobs:
        st.info("🔍 No real-time jobs found. Check company career pages directly.")
        return
    st.markdown("### 🎯 Curated Career Opportunities")
    for job in jobs:
        with st.container():
            st.markdown("<div class='job-card'>", unsafe_allow_html=True)
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"#### {job.get('title','Professional Position')}")
                st.markdown(f"**🏛️ {job.get('company','Top Company')}** • 📍 {job.get('location','Remote')}")
                st.markdown(f"**💰** {job.get('salary','Competitive')}")
                st.markdown(f"*{job.get('description','')}*")
            with col2:
                url = job.get('apply_url') or '#'
                st.link_button("⚡ Apply Now", url, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

def show_diff(original: str, optimized: str):
    st.markdown("### 📝 Content Enhancements Preview")
    tab1, tab2 = st.tabs(["🔍 Side-by-Side", "🎯 Key Improvements"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Original Resume")
            diff_html = ""
            for line in difflib.ndiff(original.splitlines(), optimized.splitlines()):
                if line.startswith('-'):   diff_html += f"<div class='diff-removed'>{line[2:]}</div>"
                elif line.startswith('+'): diff_html += f"<div class='diff-added'>{line[2:]}</div>"
                else:                      diff_html += f"<div>{line[2:]}</div>"
            st.markdown(f"<div style='max-height:400px;overflow-y:auto;font-family:monospace;font-size:0.8rem'>{diff_html}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("#### Optimised Resume")
            st.text_area("", optimized, height=400, key="opt_resume_text")
    with tab2:
        st.markdown("#### Strategic Enhancements Applied")
        for imp in ["✅ ATS-optimised formatting","✅ Keyword integration for target role",
                    "✅ Action-oriented language","✅ Achievements emphasised",
                    "✅ Professional summary optimised","✅ Quantifiable results added"]:
            st.write(imp)

def display_features(result: dict, original_text: str = ""):
    """Render the full results dashboard."""
    st.markdown("## 📊 Executive Summary Dashboard")

    # ── Metric cards ──
    fs = result.get('final_score', {})
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{fs.get('overall_score',0)}%</div>Overall Score</div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>+{result.get('improvement_percentage',0):.1f}%</div>Performance Gain</div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{fs.get('ats_optimization',0)}%</div>ATS Ready</div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{fs.get('confidence_level','—').title()}</div>Confidence</div>", unsafe_allow_html=True)

    # ── Charts ──
    v1, v2 = st.columns(2)
    with v1: st.plotly_chart(radar_chart(fs), use_container_width=True)
    with v2: st.plotly_chart(gauge_chart(fs.get('overall_score',0), result.get('improvement_percentage',0)), use_container_width=True)

    if 'resume_comparison' in result:
        fig = improvement_chart(result['resume_comparison'])
        if fig: st.plotly_chart(fig, use_container_width=True)

    # ── Interview prep ──
    if 'interview_prep' in result:
        st.markdown("## 🎤 Interview Preparation")
        ip = result['interview_prep']
        with st.expander("View Interview Questions & Tips", expanded=False):
            st.markdown("**Role-Specific Questions:**")
            for q in ip.get('role_specific_questions', []):
                st.markdown(f"• {q}")
            st.markdown("**Behavioural Questions:**")
            for q in ip.get('behavioral_questions', []):
                st.markdown(f"• {q}")
            st.markdown("**Preparation Tips:**")
            for t in ip.get('preparation_tips', []):
                st.markdown(f"✅ {t}")

    # ── Learning path ──
    if 'learning_path' in result:
        st.markdown("## 📚 Personalised Learning Path")
        lp = result['learning_path']
        with st.expander("View Skill Development Plan", expanded=False):
            timeline = lp.get('timeline', {})
            st.info(f"**{timeline.get('level','')} Plan** | Duration: {timeline.get('duration','')} | Focus: {timeline.get('focus','')}")
            for item in lp.get('learning_path', [])[:5]:
                st.markdown(f"**{item['skill']}** ({item['priority']} priority, {item['timeline']})")
                for r in item.get('resources', [])[:2]:
                    st.markdown(f"  • {r}")

    # ── Market intelligence ──
    if 'market_intelligence' in result:
        st.markdown("## 📈 Market Intelligence")
        mi = result['market_intelligence']
        cols = st.columns(3)
        cols[0].metric("Salary Range",  mi.get('salary_range','—'))
        cols[1].metric("Demand Level",  mi.get('demand_level','—'))
        cols[2].metric("Growth Outlook", mi.get('growth_outlook','—'))

    # ── Jobs ──
    st.markdown("## 💼 Strategic Opportunity Pipeline")
    display_jobs(result.get('job_listings', []))

    # ── Resume diff & download ──
    if 'optimized_resume' in result and original_text:
        st.markdown("## 📄 Your Optimised Resume")
        dl_col, _ = st.columns([1, 3])
        with dl_col:
            st.download_button(
                "📥 Download Enhanced Resume",
                result['optimized_resume'],
                file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
            )
        show_diff(original_text, result['optimized_resume'])

    # ── Gap analysis ──
    if 'gap_analysis' in result and result['gap_analysis']:
        st.markdown("## 🔍 Gap Analysis & Recommendations")
        ga = result['gap_analysis']
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**✅ Strengths Identified:**")
            for s in ga.get('resume_strengths', []):
                st.markdown(f"• {s}")
        with col2:
            st.markdown("**🎯 Recommendations:**")
            for r in ga.get('recommendations', []):
                st.markdown(f"• {r}")


# ── Main ─────────────────────────────────────────────────────────────────────

def extract_text_from_upload(resume_file) -> str:
    """Extract text directly from the uploaded file object."""
    ext = os.path.splitext(resume_file.name)[1].lower()
    try:
        if ext == '.txt':
            return resume_file.getvalue().decode('utf-8')
        elif ext == '.pdf':
            import pdfplumber
            import io
            with pdfplumber.open(io.BytesIO(resume_file.getvalue())) as pdf:
                return "\n".join(p.extract_text() or "" for p in pdf.pages)
        elif ext == '.docx':
            from docx import Document
            import io
            doc = Document(io.BytesIO(resume_file.getvalue()))
            return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        st.warning(f"Text preview unavailable: {e}")
    return ""


def main():
    st.markdown("<h1 class='main-header'>CareerCatalyst AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888;margin-top:-1rem'>AI-Powered Resume Intelligence Suite</p>", unsafe_allow_html=True)

    original_text = ""

    # ── Sidebar ──
    with st.sidebar:
        st.markdown("## ⚡ Career Command Centre")
        target_role   = st.text_input("🎯 Target Role", placeholder="e.g. Senior Data Analyst")
        location_opt  = st.selectbox("📍 Location", ["Global Remote","North America","Europe","Asia Pacific","India","Custom"])
        location      = st.text_input("Specify Location") if location_opt == "Custom" else location_opt
        job_description = st.text_area("📋 Paste Job Description (optional)", height=150,
                                        placeholder="Paste the target job description here for best results...")
        resume_file   = st.file_uploader("📄 Upload Resume", type=['pdf','docx','txt'])

        if resume_file:
            original_text = extract_text_from_upload(resume_file)
            if original_text:
                st.success(f"✅ Resume loaded ({len(original_text.split())} words)")

        st.markdown("---")
        optimize_btn = st.button("🚀 Launch Analysis", type="primary", use_container_width=True)
        st.markdown("<small style='color:#aaa'>Powered by Gemini AI</small>", unsafe_allow_html=True)

    # ── Main area ──
    if optimize_btn and resume_file:
        with st.spinner("🔄 AI is analysing and optimising your resume…"):
            try:
                # Save to temp file for FileProcessor
                suffix = os.path.splitext(resume_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(resume_file.getvalue())
                    temp_path = tmp.name

                orchestrator = FastOrchestrator()
                result = asyncio.run(orchestrator.process_resume(
                    temp_path, job_description, target_role, location
                ))
                os.unlink(temp_path)

                if 'error' in result and not result.get('optimized_resume'):
                    st.error(f"❌ {result['error']}")
                else:
                    st.success("✅ Analysis complete! Your resume has been AI-optimised.")
                    display_features(result, original_text)

            except Exception as e:
                st.error(f"❌ System error: {e}")
                import traceback
                st.code(traceback.format_exc())

    elif optimize_btn and not resume_file:
        st.warning("⚠️ Please upload your resume first.")

    else:
        # Welcome screen
        st.markdown("### 👋 Welcome to CareerCatalyst AI")
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='premium-card'><h3>🤖 AI Optimisation</h3><p>ATS-ready, keyword-optimised resume tailored to your target role</p></div>", unsafe_allow_html=True)
        c2.markdown("<div class='premium-card'><h3>📊 Deep Analytics</h3><p>Radar scoring, gap analysis, health tracking and market intelligence</p></div>", unsafe_allow_html=True)
        c3.markdown("<div class='premium-card'><h3>💼 Career Intelligence</h3><p>Real job listings, learning paths and interview prep — all in one place</p></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.info("👈 Upload your resume and target job description in the sidebar, then click **Launch Analysis**.")


if __name__ == "__main__":
    main()