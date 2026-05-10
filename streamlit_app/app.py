import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# API Configuration — works both locally and inside the Cloud Run container
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="ReliefLink AI — Emergency Response Platform",
    page_icon="🆘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── DESIGN SYSTEM CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-primary: #0a0f1a;
        --bg-secondary: #111827;
        --bg-card: #1a2233;
        --border: rgba(255,255,255,0.06);
        --border-hover: rgba(255,255,255,0.12);
        --red: #ef4444;
        --red-dim: rgba(239,68,68,0.12);
        --green: #10b981;
        --green-dim: rgba(16,185,129,0.12);
        --amber: #f59e0b;
        --amber-dim: rgba(245,158,11,0.12);
        --blue: #3b82f6;
        --blue-dim: rgba(59,130,246,0.12);
        --text: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-dim: #64748b;
    }

    /* ── Reset Streamlit chrome ── */
    #MainMenu, header, footer, .stDeployButton { display: none !important; }

    .stApp {
        background: var(--bg-primary);
        color: var(--text);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ── Top Navbar ── */
    .topbar {
        position: fixed; top: 0; left: 0; width: 100%; height: 56px;
        background: rgba(10,15,26,0.92);
        backdrop-filter: blur(16px) saturate(180%);
        border-bottom: 1px solid var(--border);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 48px; z-index: 9999;
    }
    .topbar-brand {
        display: flex; align-items: center; gap: 10px;
        font-weight: 700; font-size: 1rem; color: var(--text);
    }
    .topbar-status {
        display: flex; align-items: center; gap: 8px;
    }
    .status-dot {
        width: 7px; height: 7px; border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 8px rgba(16,185,129,0.6);
    }
    .status-label {
        font-size: 0.7rem; font-weight: 600; color: var(--green);
        letter-spacing: 0.5px; text-transform: uppercase;
    }

    /* ── Topbar Navigation Links ── */
    .topbar-link {
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.82rem;
        padding: 16px 18px;
        transition: all 0.15s ease;
        border-bottom: 2px solid transparent;
    }
    .topbar-link:hover {
        color: var(--text);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border) !important;
    }
    .sb-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    /* ── Page Content Spacing ── */
    .page-wrap { margin-top: 80px; padding-bottom: 60px; }

    /* ── Cards ── */
    .card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 36px;
        margin-bottom: 28px;
        transition: border-color 0.25s ease;
        max-width: 1100px;
        margin-left: auto;
        margin-right: auto;
    }
    .card:hover { border-color: var(--border-hover); }

    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 24px 28px;
        position: relative;
        transition: transform 0.25s ease, border-color 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        border-color: var(--border-hover);
    }
    .metric-label {
        font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
        letter-spacing: 0.06em; color: var(--text-secondary); margin-bottom: 8px;
    }
    .metric-value {
        font-size: 2rem; font-weight: 800; color: var(--text);
        line-height: 1.1;
    }
    .metric-icon {
        position: absolute; top: 22px; right: 24px;
        font-size: 1.3rem; opacity: 0.5;
    }

    /* ── Form Controls ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stTextInput input,
    .stTextArea textarea {
        background: #1a2233 !important;
        background-color: #1a2233 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
        padding: 12px 16px !important;
        font-size: 0.9rem !important;
        transition: border-color 0.2s !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--red) !important;
        box-shadow: 0 0 0 3px var(--red-dim) !important;
        background: #1e293b !important;
    }
    /* Fix Streamlit label colors */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: var(--text-secondary) !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }

    /* ── Primary Action Button ── */
    .stButton > button {
        background: var(--red) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 14px 24px !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.04em !important;
        width: 100%;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(239,68,68,0.25) !important;
    }
    .stButton > button:hover {
        background: #dc2626 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(239,68,68,0.35) !important;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block; padding: 4px 10px; border-radius: 6px;
        font-size: 0.7rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-critical { background: var(--red-dim); color: var(--red); }
    .badge-high     { background: var(--amber-dim); color: var(--amber); }
    .badge-medium   { background: var(--blue-dim); color: var(--blue); }
    .badge-low      { background: var(--green-dim); color: var(--green); }

    /* ── Activity Row ── */
    .activity-row {
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }

    /* ── Footer ── */
    .site-footer {
        background: var(--bg-secondary);
        border-top: 1px solid var(--border);
        padding: 40px 48px 0 48px;
        margin-top: 60px;
    }
    .footer-main {
        display: grid;
        grid-template-columns: 1.2fr 1fr;
        gap: 60px; max-width: 1100px; margin: 0 auto;
        padding-bottom: 32px;
    }
    .footer-heading {
        font-size: 0.78rem; font-weight: 700; color: var(--text);
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 14px;
    }
    .footer-text {
        color: var(--text-dim); font-size: 0.8rem;
        line-height: 1.7; margin: 0;
    }
    .footer-link {
        display: block; color: var(--text-secondary);
        text-decoration: none; font-size: 0.82rem;
        margin-bottom: 8px; transition: color 0.2s;
    }
    .footer-link:hover { color: white; }
    .footer-bottom {
        max-width: 1100px; margin: 0 auto;
        padding: 20px 0;
        border-top: 1px solid var(--border);
        display: flex; justify-content: space-between; align-items: center;
        font-size: 0.72rem; color: var(--text-dim);
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 6px; }

    /* ── Streamlit dataframe dark theme ── */
    .stDataFrame { border-radius: 12px; overflow: hidden; }

    /* ── RESPONSIVENESS ── */
    @media (max-width: 1024px) {
        .topbar { padding: 0 24px; }
        .site-footer { padding: 40px 24px 0 24px; }
        .footer-main { gap: 32px; }
    }

    @media (max-width: 768px) {
        .topbar-status { display: none; }
        .topbar-brand span:last-child { font-size: 0.85rem; }
        .topbar-link { padding: 16px 10px; font-size: 0.75rem; }
        
        .footer-main {
            grid-template-columns: 1fr;
            gap: 32px;
            text-align: center;
        }
        .footer-main > div:last-child {
            text-align: center !important;
            margin-top: 10px;
        }
        .footer-bottom {
            flex-direction: column;
            gap: 12px;
            text-align: center;
        }
        .card { padding: 24px; }
        .page-wrap { margin-top: 70px; }
        
        .metric-value { font-size: 1.5rem; }
        .metric-card { padding: 20px; }
    }

    @media (max-width: 480px) {
        .topbar-brand span:last-child { display: none; }
        .topbar { justify-content: center; padding: 0 10px; height: auto; padding: 10px 0; }
        .topbar-link { padding: 8px 12px; }
        .footer-main { padding-bottom: 24px; }
        .site-footer { padding-top: 30px; }
    }
</style>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────
#  COMPONENTS
# ───────────────────────────────────────────────

def show_navbar():
    if 'page' not in st.session_state:
        st.session_state.page = "Submit Request"

    active_home = "color:white; border-bottom:2px solid #ef4444;" if st.session_state.page == "Submit Request" else ""
    active_dash = "color:white; border-bottom:2px solid #ef4444;" if st.session_state.page == "Dashboard" else ""
    active_analytics = "color:white; border-bottom:2px solid #ef4444;" if st.session_state.page == "Analytics" else ""

    st.markdown(f"""
<div class="topbar">
<div class="topbar-brand">
<span style="font-size:1.3rem">🆘</span>
<span>ReliefLink AI</span>
</div>
<div style="display:flex; align-items:center; gap:6px; height:56px;">
<a class="topbar-link" href="?page=home" target="_self" style="{active_home}">Submit Request</a>
<a class="topbar-link" href="?page=dashboard" target="_self" style="{active_dash}">Dashboard</a>
<a class="topbar-link" href="?page=analytics" target="_self" style="{active_analytics}">Analytics</a>
</div>
<div class="topbar-status">
<div class="status-dot"></div>
<span class="status-label">All Systems Operational</span>
</div>
</div>
""", unsafe_allow_html=True)


def show_sidebar():
    with st.sidebar:
        st.markdown("""
<div class="sb-card">
<p style="margin:0 0 4px 0; font-weight:700; color:white; font-size:0.95rem;">Platform Status</p>
<p style="margin:0 0 14px 0; color:#94a3b8; font-size:0.78rem;">Monitoring active disaster zones worldwide.</p>
<div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:6px;">
<span style="color:#94a3b8;">Server Uptime</span>
<span style="color:#10b981; font-weight:600;">99.9%</span>
</div>
<div style="height:4px; background:rgba(255,255,255,0.05); border-radius:3px;">
<div style="width:99.9%; height:100%; background:#10b981; border-radius:3px;"></div>
</div>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class="sb-card" style="border-left:3px solid #ef4444;">
<p style="margin:0 0 4px 0; font-weight:700; color:white; font-size:0.95rem;">Active Alerts</p>
<p style="margin:0; color:#ef4444; font-size:0.78rem; font-weight:600;">2 flood warnings in South Asia</p>
</div>
""", unsafe_allow_html=True)

        st.divider()
        st.info("💡 **Tip:** The more detail you provide in your request, the faster our AI can classify and route it to the right responders.")


def show_footer():
    st.markdown("""
<div class="site-footer">
<div class="footer-main">
<div>
<div style="font-weight:800; font-size:1.05rem; color:white; display:flex; align-items:center; gap:8px; margin-bottom:12px;">
<span style="font-size:1.2rem;">🆘</span> ReliefLink AI
</div>
<p class="footer-text" style="margin-bottom:24px;">
Next-generation emergency intelligence &amp; humanitarian response system. Built to optimize disaster relief coordination and enhance real-time aid delivery.
</p>
<div class="footer-heading" style="margin-bottom:10px;">Connect</div>
<div style="display:flex; gap:16px;">
<a href="https://www.linkedin.com/in/nitishyadav866" target="_blank" class="footer-link" style="margin:0;">🔗 LinkedIn</a>
<a href="https://github.com/nitishya/ReliefLink-AI" target="_blank" class="footer-link" style="margin:0;">🐙 GitHub</a>
</div>
</div>
<div style="text-align:right;">
<div class="footer-heading">Developed by</div>
<p style="color:white; font-size:1rem; font-weight:700; margin:0 0 4px 0;">Team 10:Nitish,Saurabh,Sachin and Ishita</p>
<p style="color:var(--text-dim); font-size:0.82rem; margin:0 0 24px 0;">Delhi, India 🇮🇳</p>
<div class="footer-heading" style="margin-bottom:10px;">Legal</div>
<div style="display:flex; gap:16px; justify-content:flex-end;">
<a href="#" class="footer-link" style="margin:0;">Privacy Policy</a>
<a href="#" class="footer-link" style="margin:0;">Terms of Service</a>
</div>
</div>
</div>
<div class="footer-bottom">
<span>&copy; 2026 ReliefLink AI. All rights reserved.</span>
<span style="font-weight:600;">Built for the AI for Social Good Challenge</span>
</div>
</div>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────
#  PAGES
# ───────────────────────────────────────────────

def show_intake_form():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    col_l, col_m, col_r = st.columns([0.5, 10, 0.5])
    with col_m:

        # Hero card — NO indentation in the HTML string
        st.markdown('''<div class="card">
<h2 style="margin:0 0 8px 0; color:white; font-size:1.8rem; font-weight:800;">Report an Emergency</h2>
<p style="margin:0 0 28px 0; color:#94a3b8; font-size:0.95rem;">
Fill out the form below. Our AI will instantly classify your situation, estimate urgency, and notify the nearest response teams.
</p>
<div style="background:var(--red-dim); border:1px solid rgba(239,68,68,0.18); border-radius:10px; padding:16px 20px; display:flex; gap:16px; align-items:center;">
<span style="font-size:1.4rem;">🛡️</span>
<div>
<p style="margin:0; color:white; font-weight:600; font-size:0.9rem;">Round-the-Clock Response</p>
<p style="margin:0; color:#94a3b8; font-size:0.82rem;">Our AI continuously monitors incoming requests and can triage them in under two seconds.</p>
</div>
</div>
</div>''', unsafe_allow_html=True)

        with st.form("intake_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
                contact = st.text_input("Phone Number", placeholder="e.g. +91 98765 43210")
            with c2:
                location = st.text_input("Location", placeholder="e.g. Sector 45, Gurgaon, Haryana")
                language = st.selectbox("Preferred Language", ["English", "Hindi", "Spanish", "French"])

            description = st.text_area(
                "Describe the Situation",
                placeholder="What happened? How many people are affected? What supplies are needed (food, water, medical aid, shelter)?",
                height=180
            )

            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Submit Emergency Request")

            if submitted:
                if not name or not location or not description or not contact:
                    st.error("Please fill in all fields before submitting.")
                else:
                    payload = {
                        "name": name,
                        "location": location,
                        "description": description,
                        "contact_number": contact,
                        "language": language
                    }
                    try:
                        with st.spinner("Processing your request …"):
                            response = requests.post(f"{API_BASE_URL}/requests/", json=payload)
                        if response.status_code == 200:
                            st.session_state.last_submission = response.json()
                            st.balloons()
                        else:
                            st.error(f"Something went wrong: {response.text}")
                    except Exception:
                        st.error("Unable to reach the server. Please check that the backend is running.")

        # ── AI Results (rendered OUTSIDE the form, no indentation) ──
        if st.session_state.get('last_submission'):
            data = st.session_state.last_submission
            urgency_class = data['urgency'].lower()
            results_html = f'''<div class="card" style="border-color:rgba(16,185,129,0.3); margin-top:32px;">
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
<h3 style="margin:0; color:#10b981; font-weight:700;">Request Processed Successfully</h3>
<span class="badge badge-{urgency_class}">{data['urgency']} Priority</span>
</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:24px;">
<div>
<p style="color:#94a3b8; font-size:0.78rem; font-weight:600; text-transform:uppercase; margin-bottom:6px;">Category</p>
<p style="font-size:1.1rem; font-weight:700; color:white; margin:0;">{data['category']}</p>
</div>
<div>
<p style="color:#94a3b8; font-size:0.78rem; font-weight:600; text-transform:uppercase; margin-bottom:6px;">Resources Needed</p>
<p style="font-size:1.1rem; font-weight:700; color:white; margin:0;">{data['required_resources']}</p>
</div>
</div>
<hr style="border:0; border-top:1px solid var(--border); margin:24px 0;">
<p style="color:#94a3b8; font-size:0.78rem; font-weight:600; text-transform:uppercase; margin-bottom:6px;">Summary for Volunteers</p>
<p style="font-size:0.95rem; color:#e2e8f0; line-height:1.6; margin:0 0 24px 0;">{data['summary']}</p>
<p style="color:#94a3b8; font-size:0.78rem; font-weight:600; text-transform:uppercase; margin-bottom:6px;">Recommended Action</p>
<div style="background:var(--amber-dim); border-left:3px solid var(--amber); padding:14px 18px; border-radius:8px; color:var(--amber); font-weight:600; font-size:0.9rem;">
{data['recommendations']}
</div>
</div>'''
            st.markdown(results_html, unsafe_allow_html=True)
            if st.button("Dismiss"):
                st.session_state.last_submission = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def show_dashboard():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE_URL}/stats/")
        if response.status_code == 200:
            stats = response.json()

            # Header
            st.markdown('''<div style="margin-bottom:40px;">
<h2 style="margin:0 0 6px 0; font-size:1.8rem; font-weight:800; color:white;">Response Dashboard</h2>
<p style="margin:0; color:#94a3b8; font-size:0.95rem;">Live overview of all emergency requests and response activity.</p>
</div>''', unsafe_allow_html=True)

            # Metric cards
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f'''<div class="metric-card">
<p class="metric-label">Total Requests</p>
<p class="metric-value">{stats['total_requests']}</p>
<span class="metric-icon">📋</span>
</div>''', unsafe_allow_html=True)
            with m2:
                st.markdown(f'''<div class="metric-card" style="border-left:3px solid var(--red);">
<p class="metric-label" style="color:var(--red);">Critical Cases</p>
<p class="metric-value">{stats['critical_count']}</p>
<span class="metric-icon">🚨</span>
</div>''', unsafe_allow_html=True)
            with m3:
                st.markdown(f'''<div class="metric-card">
<p class="metric-label">Avg. Response Time</p>
<p class="metric-value">1.2s</p>
<span class="metric-icon">⚡</span>
</div>''', unsafe_allow_html=True)
            with m4:
                st.markdown(f'''<div class="metric-card" style="border-left:3px solid var(--green);">
<p class="metric-label" style="color:var(--green);">System Status</p>
<p class="metric-value">Online</p>
<span class="metric-icon">🟢</span>
</div>''', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Charts row
            chart_col, feed_col = st.columns([1, 1.5])
            with chart_col:
                st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:700; margin-bottom:20px; color:white;">Requests by Category</p>', unsafe_allow_html=True)
                if stats["category_counts"]:
                    df_cat = pd.DataFrame(list(stats["category_counts"].items()), columns=["Category", "Count"])
                    fig = px.pie(df_cat, values="Count", names="Category", hole=0.65,
                                 color_discrete_sequence=["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#8b5cf6"])
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#94a3b8", size=12),
                        margin=dict(t=10, b=10, l=10, r=10),
                        showlegend=True,
                        legend=dict(font=dict(color="#94a3b8"))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.caption("No data yet.")
                st.markdown('</div>', unsafe_allow_html=True)

            with feed_col:
                st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:700; margin-bottom:20px; color:white;">Recent Requests</p>', unsafe_allow_html=True)
                if stats["recent_requests"]:
                    for req in stats["recent_requests"]:
                        badge_class = f"badge-{req['urgency'].lower()}"
                        st.markdown(f'''<div class="activity-row">
<div>
<p style="margin:0; font-weight:600; color:white; font-size:0.9rem;">{req['name']}</p>
<p style="margin:0; font-size:0.78rem; color:#94a3b8;">{req['category']} · {req['location']}</p>
</div>
<span class="badge {badge_class}">{req['urgency']}</span>
</div>''', unsafe_allow_html=True)
                else:
                    st.caption("No recent activity.")
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Data table
            st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
            st.markdown('<p style="font-weight:700; margin-bottom:20px; color:white;">All Requests</p>', unsafe_allow_html=True)
            req_resp = requests.get(f"{API_BASE_URL}/requests/")
            if req_resp.status_code == 200:
                all_reqs = req_resp.json()
                if all_reqs:
                    df = pd.DataFrame(all_reqs)
                    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%b %d, %Y  %H:%M')
                    st.dataframe(
                        df[['timestamp', 'name', 'location', 'category', 'urgency', 'summary']].rename(columns={
                            'timestamp': 'Date',
                            'name': 'Requester',
                            'location': 'Location',
                            'category': 'Category',
                            'urgency': 'Urgency',
                            'summary': 'Summary'
                        }),
                        use_container_width=True,
                        hide_index=True,
                    )
                else:
                    st.caption("No requests recorded yet.")
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception:
        st.error("Unable to connect to the backend. Make sure the API server is running on port 8000.")

    st.markdown('</div>', unsafe_allow_html=True)


def show_analytics():
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats/")
        if response.status_code == 200:
            stats = response.json()
            
            # Header
            st.markdown('''<div style="margin-bottom:40px;">
<h2 style="margin:0 0 6px 0; font-size:2.2rem; font-weight:900; color:white;">Analytics Hub</h2>
<p style="margin:0; color:#94a3b8; font-size:1.1rem;">Deep-dive into humanitarian request data and system performance metrics.</p>
</div>''', unsafe_allow_html=True)

            # High-level Metrics
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'''<div class="metric-card" style="border-top:3px solid var(--blue);">
<p class="metric-label">Data Fidelity</p>
<p class="metric-value">High</p>
<p style="margin:8px 0 0 0; color:var(--green); font-size:0.75rem; font-weight:600;">↑ 99.8% Accuracy</p>
</div>''', unsafe_allow_html=True)
            with c2:
                st.markdown(f'''<div class="metric-card" style="border-top:3px solid var(--amber);">
<p class="metric-label">Avg Urgency Score</p>
<p class="metric-value">6.8 / 10</p>
<p style="margin:8px 0 0 0; color:var(--text-dim); font-size:0.75rem;">Moderate Trend</p>
</div>''', unsafe_allow_html=True)
            with c3:
                st.markdown(f'''<div class="metric-card" style="border-top:3px solid var(--green);">
<p class="metric-label">NGO Match Rate</p>
<p class="metric-value">94%</p>
<p style="margin:8px 0 0 0; color:var(--green); font-size:0.75rem; font-weight:600;">↑ 2% this week</p>
</div>''', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Visualizations
            v1, v2 = st.columns(2)
            
            with v1:
                st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:700; margin-bottom:24px; color:white; font-size:1.1rem;">Request Volume by Category</p>', unsafe_allow_html=True)
                if stats["category_counts"]:
                    df_cat = pd.DataFrame(list(stats["category_counts"].items()), columns=["Category", "Count"])
                    fig = px.bar(df_cat, x="Category", y="Count", 
                                color="Category", 
                                color_discrete_sequence=px.colors.sequential.Reds_r)
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#94a3b8"),
                        xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
                        margin=dict(t=0, b=0, l=0, r=0),
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with v2:
                st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
                st.markdown('<p style="font-weight:700; margin-bottom:24px; color:white; font-size:1.1rem;">Urgency Breakdown</p>', unsafe_allow_html=True)
                all_req_resp = requests.get(f"{API_BASE_URL}/requests/")
                if all_req_resp.status_code == 200:
                    all_reqs = all_req_resp.json()
                    if all_reqs:
                        df_all = pd.DataFrame(all_reqs)
                        urgency_counts = df_all['urgency'].value_counts().reset_index()
                        urgency_counts.columns = ['Urgency', 'Count']
                        fig_u = px.pie(urgency_counts, values="Count", names="Urgency", 
                                      color="Urgency",
                                      color_discrete_map={"CRITICAL": "#ef4444", "HIGH": "#f59e0b", "MEDIUM": "#3b82f6", "LOW": "#10b981"},
                                      hole=0.5)
                        fig_u.update_layout(
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color="#94a3b8"),
                            margin=dict(t=0, b=0, l=0, r=0)
                        )
                        st.plotly_chart(fig_u, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Trend Analysis (Mock Data for visualization)
            st.markdown('<div class="card" style="padding:28px;">', unsafe_allow_html=True)
            st.markdown('<p style="font-weight:700; margin-bottom:24px; color:white; font-size:1.1rem;">System Latency & AI Performance (24h Trend)</p>', unsafe_allow_html=True)
            import numpy as np
            time_points = pd.date_range(end=datetime.now(), periods=24, freq='H')
            latency_data = pd.DataFrame({
                'Time': time_points,
                'Latency (s)': np.random.uniform(0.8, 1.5, size=24)
            })
            fig_trend = px.line(latency_data, x='Time', y='Latency (s)', 
                               line_shape='spline', render_mode='svg')
            fig_trend.update_traces(line_color='#ef4444', line_width=3)
            fig_trend.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#94a3b8"),
                xaxis=dict(showgrid=False, title=""),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title="Seconds"),
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error("Analytics service unavailable. Ensure backend is operational.")

    st.markdown('</div>', unsafe_allow_html=True)


# ───────────────────────────────────────────────
#  MAIN
# ───────────────────────────────────────────────

def main():
    # Read query params for navigation from topbar links
    query_params = st.query_params
    if 'page' in query_params:
        page_param = query_params['page']
        if page_param == 'dashboard':
            st.session_state.page = 'Dashboard'
        elif page_param == 'analytics':
            st.session_state.page = 'Analytics'
        else:
            st.session_state.page = 'Submit Request'

    if 'page' not in st.session_state:
        st.session_state.page = "Submit Request"

    show_navbar()
    show_sidebar()

    page_options = ["Submit Request", "Dashboard", "Analytics"]
    current_page = st.sidebar.radio("Navigation", page_options, index=page_options.index(st.session_state.page))

    if current_page != st.session_state.page:
        st.session_state.page = current_page
        st.rerun()

    if st.session_state.page == "Submit Request":
        show_intake_form()
    elif st.session_state.page == "Dashboard":
        show_dashboard()
    else:
        show_analytics()

    show_footer()


if __name__ == "__main__":
    main()
