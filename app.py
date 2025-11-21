# app.py
import streamlit as st
import asyncio
import os
import tempfile
from datetime import datetime
import plotly.graph_objects as go
import difflib

from orchestrator import FastOrchestrator

# --- Page Configuration ---
st.set_page_config(
    page_title="CareerCatalyst AI | Resume Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .premium-card, .job-card, .metric-card {
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin: 1rem 0;
    }
    .premium-card { background:white; border:1px solid #e0e0e0; text-align:center;}
    .metric-card { background: linear-gradient(135deg, #667eea, #764ba2); color:white; text-align:center;}
    .job-card { background:white; border-left:4px solid #667eea;}
    .diff-added { background-color: #d4edda; padding: 2px 4px; border-radius: 3px;}
    .diff-removed { background-color: #f8d7da; padding: 2px 4px; border-radius: 3px; text-decoration: line-through;}
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def display_real_jobs(jobs):
    """Display job listings with Apply buttons."""
    if not jobs:
        st.info("🔍 No real-time jobs found. Check company career pages.")
        return
    st.markdown("### 🎯 Curated Career Opportunities")
    for job in jobs:
        st.markdown("<div class='job-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"#### {job.get('title','Professional Position')}")
            st.markdown(f"**🏛️ {job.get('company','Top Company')}** • 📍 {job.get('location','Remote')}")
            st.markdown(f"**💰 Compensation:** {job.get('salary','Competitive Package')}")
            st.markdown(f"*{job.get('description','Exciting opportunity.')}*")
        with col2:
            apply_url = job.get('apply_url') or job.get('fallback_url') or "#"
            st.markdown(f"""<a href="{apply_url}" target="_blank"><button style='background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:0.75rem 1rem;border:none;border-radius:6px;width:100%;font-weight:600;'>⚡ Apply Now</button></a>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

def create_competitive_radar(score_data):
    categories = ['Technical Alignment', 'Strategic Impact', 'Career Narrative', 'Market Relevance', 'ATS Compliance']
    scores = [
        score_data.get('skills_alignment',0),
        score_data.get('impact_presentation',0),
        score_data.get('career_narrative',0),
        score_data.get('keyword_match',0),
        score_data.get('ats_optimization',0)
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores+[scores[0]],
        theta=categories+[categories[0]],
        fill='toself',
        line=dict(color='#667eea', width=3),
        fillcolor='rgba(102,126,234,0.3)',
        name='Profile'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,100])), showlegend=False, height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def create_performance_gauge(current_score, improvement):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_score,
        delta={'reference': current_score-improvement,'increasing':{'color':'#00d26a'}},
        title={'text':'Competitive Score'},
        gauge={'axis':{'range':[None,100]}, 'bar':{'color':'#667eea'}, 'steps':[{'range':[0,60],'color':'#ff6b6b'},{'range':[60,80],'color':'#ffd93d'},{'range':[80,100],'color':'#00d26a'}]}
    ))
    fig.update_layout(height=300)
    return fig

def create_improvement_chart(comparison_data):
    if not comparison_data or 'metrics' not in comparison_data:
        return None
    metrics = comparison_data['metrics']
    categories = ['Content Volume','Achievements','Skills','Impact']
    original = [metrics.get('word_count',{}).get('original',0), metrics.get('achievement_count',{}).get('original',0), metrics.get('skill_mentions',{}).get('original',0), metrics.get('action_verbs',{}).get('original',0)]
    optimized = [metrics.get('word_count',{}).get('optimized',0), metrics.get('achievement_count',{}).get('optimized',0), metrics.get('skill_mentions',{}).get('optimized',0), metrics.get('action_verbs',{}).get('optimized',0)]
    fig = go.Figure(data=[
        go.Bar(name='Before', x=categories, y=original, marker_color='#95a5a6'),
        go.Bar(name='After', x=categories, y=optimized, marker_color='#667eea')
    ])
    fig.update_layout(barmode='group', title="Content Enhancement Analysis", height=400)
    return fig

def show_resume_changes(original_text, optimized_text):
    st.markdown("### 📝 Content Enhancements Preview")
    tab1, tab2 = st.tabs(["🔍 Side-by-Side Diff", "🎯 Key Improvements"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Original Resume")
            diff_html = ""
            for line in difflib.ndiff(original_text.splitlines(), optimized_text.splitlines()):
                if line.startswith('-'):
                    diff_html += f"<div class='diff-removed'>{line[2:]}</div>"
                elif line.startswith('+'):
                    diff_html += f"<div class='diff-added'>{line[2:]}</div>"
                else:
                    diff_html += f"<div>{line[2:]}</div>"
            st.markdown(f"<div style='max-height:400px; overflow-y:auto; font-family:monospace;'>{diff_html}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("#### Optimized Resume")
            st.text_area("Optimized Resume", optimized_text, height=400, key="optimized_resume", label_visibility="visible")
    
    with tab2:
        st.markdown("#### Strategic Enhancements Applied")
        improvements = [
            "✅ ATS-optimized formatting",
            "✅ Keyword integration for target role",
            "✅ Action-oriented language enhancement",
            "✅ Achievements emphasized",
            "✅ Professional summary optimization",
            "✅ Skills section reorganized",
            "✅ Quantifiable results added"
        ]
        for imp in improvements:
            st.write(imp)

def display_all_features(result, original_resume_text=""):
    st.markdown("## 📊 Executive Summary Dashboard")
    
    # Metrics cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{result.get('final_score',{}).get('overall_score',0)}%</div>Overall Score</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>+{result.get('improvement_percentage',0):.1f}%</div>Performance Gain</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{result.get('final_score',{}).get('ats_optimization',0)}%</div>ATS Ready</div>", unsafe_allow_html=True)
    with col4:
        confidence = result.get('final_score',{}).get('confidence_level','medium').title()
        st.markdown(f"<div class='metric-card'><div style='font-size:2rem;font-weight:bold'>{confidence}</div>Confidence Level</div>", unsafe_allow_html=True)
    
    # Charts
    viz_col1, viz_col2 = st.columns(2)
    with viz_col1:
        fig_radar = create_competitive_radar(result.get('final_score',{}))
        st.plotly_chart(fig_radar, width='stretch')
    with viz_col2:
        fig_gauge = create_performance_gauge(result.get('final_score',{}).get('overall_score',0), result.get('improvement_percentage',0))
        st.plotly_chart(fig_gauge, width='stretch')
    
    # Improvement chart
    if 'resume_comparison' in result:
        fig_imp = create_improvement_chart(result['resume_comparison'])
        if fig_imp:
            st.plotly_chart(fig_imp, width='stretch')
    
    # Job opportunities
    st.markdown("## 💼 Strategic Opportunity Pipeline")
    if 'job_listings' in result:
        display_real_jobs(result['job_listings'])
    
    # Optimized resume & diff
    if 'optimized_resume' in result and original_resume_text:
        col1, col2 = st.columns([1,4])
        with col1:
            st.download_button("📥 Download Enhanced Resume", result['optimized_resume'], file_name=f"enhanced_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", mime="text/plain")
        with col2:
            show_resume_changes(original_resume_text, result['optimized_resume'])

# --- Main Application ---
def main():
    st.markdown("<h1 class='main-header'>CareerCatalyst AI</h1>", unsafe_allow_html=True)
    original_resume_text = ""

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚡ Career Command Center")
        target_role = st.text_input("Target Role", placeholder="e.g., Senior Data Analyst")
        location = st.selectbox("Location", ["Global Remote","North America","Europe","Asia Pacific","Custom"])
        if location=="Custom":
            location = st.text_input("Specify Location")
        job_description = st.text_area("Paste Target Job Description", height=120)
        resume_file = st.file_uploader("Upload Your Resume", type=['pdf','docx','txt'])
        if resume_file:
            ext = os.path.splitext(resume_file.name)[1].lower()
            if ext == '.txt':
                original_resume_text = resume_file.getvalue().decode('utf-8')
            elif ext == '.pdf':
                import pdfplumber
                with pdfplumber.open(resume_file) as pdf:
                    original_resume_text = "\n".join([p.extract_text() or "" for p in pdf.pages])
            elif ext == '.docx':
                from docx import Document
                doc = Document(resume_file)
                original_resume_text = "\n".join([p.text for p in doc.paragraphs])
            else:
                original_resume_text = "Resume loaded for analysis"
        optimize_btn = st.button("🚀 Launch Analysis", type="primary")

    if optimize_btn and resume_file:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[1]) as tmp_file:
                tmp_file.write(resume_file.getvalue())
                temp_path = tmp_file.name
            orchestrator = FastOrchestrator()
            result = asyncio.run(orchestrator.process_resume(temp_path, job_description, target_role, location))
            os.unlink(temp_path)

            st.success("✅ Analysis Complete! Advanced AI has optimized your profile.")
            display_all_features(result, original_resume_text)
        except Exception as e:
            st.error(f"❌ System Error: {str(e)}")
    elif optimize_btn and not resume_file:
        st.warning("⚠️ Please upload your resume to start analysis")
    else:
        # Welcome Cards
        col1, col2, col3 = st.columns(3)
        col1.markdown("<div class='premium-card'><h3>🤖 AI-Powered Optimization</h3><p>ATS-ready & keyword optimized</p></div>", unsafe_allow_html=True)
        col2.markdown("<div class='premium-card'><h3>📊 Advanced Analytics</h3><p>Performance metrics & benchmarking</p></div>", unsafe_allow_html=True)
        col3.markdown("<div class='premium-card'><h3>💼 Career Intelligence</h3><p>Job matching & skill roadmap</p></div>", unsafe_allow_html=True)

if __name__=="__main__":
    main()
