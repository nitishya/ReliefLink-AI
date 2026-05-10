import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# API Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="ReliefLink AI | Emergency Response",
    page_icon="🆘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    :root {
        --primary-bg: #0B1120;
        --secondary-bg: #111827;
        --accent-red: #EF4444;
        --text-main: #F9FAFB;
        --text-muted: #9CA3AF;
        --card-bg: #1F2937;
        --card-border: rgba(255, 255, 255, 0.05);
        --success: #22C55E;
        --warning: #F59E0B;
    }

    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* Global App Container */
    .stApp {
        background-color: var(--primary-bg);
        color: var(--text-main);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Navbar Styling */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background: rgba(11, 17, 32, 0.8);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid var(--card-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 40px;
        z-index: 9999;
    }

    .nav-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-weight: 800;
        font-size: 1.4rem;
        color: var(--text-main);
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 30px;
        align-items: center;
    }

    .nav-link {
        color: var(--text-muted);
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .nav-link:hover, .nav-link.active {
        color: var(--accent-red);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #0B1120 100%);
        border-right: 1px solid var(--card-border);
        padding-top: 40px;
    }

    .sidebar-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* Card & Container Styling */
    .main-card {
        background: var(--secondary-bg);
        border: 1px solid var(--card-border);
        border-radius: 24px;
        padding: 40px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 30px;
    }

    .stat-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        padding: 25px;
        text-align: left;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    .stat-card:hover {
        transform: translateY(-5px);
        border-color: rgba(239, 68, 68, 0.3);
        box-shadow: 0 10px 30px -5px rgba(239, 68, 68, 0.1);
    }

    /* Inputs & Forms */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 12px 16px !important;
    }

    .stTextInput>div>div>input:focus {
        border-color: var(--accent-red) !important;
        box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.2) !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #EF4444 0%, #B91C1C 100%);
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(239, 68, 68, 0.4);
    }

    /* Badges */
    .p-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .p-critical { background: rgba(239, 68, 68, 0.1); color: #EF4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    .p-high { background: rgba(245, 158, 11, 0.1); color: #F59E0B; border: 1px solid rgba(245, 158, 11, 0.2); }
    .p-medium { background: rgba(59, 130, 246, 0.1); color: #3B82F6; border: 1px solid rgba(59, 130, 246, 0.2); }
    .p-low { background: rgba(34, 197, 94, 0.1); color: #22C55E; border: 1px solid rgba(34, 197, 94, 0.2); }

    /* Footer */
    .footer-container {
        background: linear-gradient(to bottom, #111827, #0B1120);
        border-top: 1px solid var(--card-border);
        padding: 80px 40px 40px 40px;
        margin-top: 100px;
    }

    .footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 60px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .footer-header {
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        font-size: 1.1rem;
    }

    .footer-link {
        color: var(--text-muted);
        text-decoration: none;
        display: block;
        margin-bottom: 12px;
        font-size: 0.9rem;
        transition: color 0.3s;
    }

    .footer-link:hover { color: white; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: var(--primary-bg); }
    ::-webkit-scrollbar-thumb { background: #374151; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #4B5563; }

    /* Fix spacing for top navbar */
    .main-content {
        margin-top: 100px;
        padding-bottom: 100px;
    }

    /* Target the navigation buttons to be fixed at the top */
    .nav-button-container {
        position: fixed;
        top: 22px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 20px;
        z-index: 10000;
        width: auto !important;
    }

    .nav-btn button {
        background: transparent !important;
        border: none !important;
        color: var(--text-muted) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        padding: 5px 15px !important;
        height: auto !important;
        transition: all 0.3s ease !important;
        box-shadow: none !important;
    }

    .nav-btn button:hover {
        color: white !important;
        background: rgba(255,255,255,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

def show_navbar():
    if 'page' not in st.session_state:
        st.session_state.page = "Submit Request"
        
    # Fixed Background Navbar
    st.markdown(f"""
    <div class="nav-container">
        <div class="nav-logo">
            <span style="font-size: 2rem;">🆘</span>
            <span>ReliefLink AI</span>
        </div>
        <div></div> <!-- Spacer for buttons -->
        <div style="display: flex; align-items: center; gap: 20px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 10px #22C55E;"></div>
                <span style="font-size: 0.7rem; font-weight: 700; color: #22C55E;">SYSTEM ACTIVE</span>
            </div>
            <span style="font-size: 1.1rem; cursor: pointer; color: var(--text-muted);">⚙️</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Functional Buttons overlaid on navbar
    # We use a container to wrap the columns for CSS targeting
    with st.container():
        st.markdown('<div class="nav-button-container">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("HOME", key="nav_home_top"):
                st.session_state.page = "Submit Request"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("DASHBOARD", key="nav_dash_top"):
                st.session_state.page = "Dashboard"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            st.button("ANALYTICS", key="nav_analytics_top")
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_footer():
    st.markdown("""
    <div class="footer-container">
        <div class="footer-grid">
            <div>
                <div style="font-size: 1.5rem; font-weight: 800; color: white; display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                    <span>🆘</span> ReliefLink AI
                </div>
                <p style="color: #9CA3AF; font-size: 0.9rem; line-height: 1.6;">
                    An AI-powered emergency management platform designed for rapid response, intelligent coordination, and humanitarian relief.
                </p>
            </div>
            <div>
                <div class="footer-header">Quick Links</div>
                <a href="#" class="footer-link">Home</a>
                <a href="#" class="footer-link">About Project</a>
                <a href="#" class="footer-link">How it Works</a>
                <a href="#" class="footer-link">NGO Portal</a>
            </div>
            <div>
                <div class="footer-header">Legal</div>
                <a href="#" class="footer-link">Privacy Policy</a>
                <a href="#" class="footer-link">Terms of Service</a>
                <a href="#" class="footer-link">Data Security</a>
            </div>
            <div>
                <div class="footer-header">Contact</div>
                <p style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 12px;">support@relieflink.ai</p>
                <div style="display: flex; gap: 15px; font-size: 1.2rem;">
                    <span>🐦</span> <span>💼</span> <span>🐙</span>
                </div>
            </div>
        </div>
        <div style="max-width: 1200px; margin: 60px auto 0 auto; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; color: #6B7280; font-size: 0.8rem;">
            <div>© 2026 ReliefLink AI. All Rights Reserved.</div>
            <div style="font-weight: 700;">BUILT FOR AI FOR SOCIAL GOOD CHALLENGE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-card">
            <h4 style="margin: 0; color: white;">Global Response</h4>
            <p style="color: #9CA3AF; font-size: 0.8rem;">Monitoring live emergencies worldwide.</p>
            <div style="margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 5px;">
                    <span>Network Integrity</span>
                    <span style="color: #22C55E;">99.9%</span>
                </div>
                <div style="height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px;">
                    <div style="width: 99%; height: 100%; background: #22C55E; border-radius: 2px;"></div>
                </div>
            </div>
        </div>
        
        <div class="sidebar-card" style="border-left: 4px solid #EF4444;">
            <h4 style="margin: 0; color: white;">Critical Alerts</h4>
            <p style="color: #EF4444; font-size: 0.8rem; font-weight: 700;">2 New Flood Warnings</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.info("💡 **AI Tip:** Detailed descriptions help our classification agent prioritize faster.")

def show_intake_form():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        # Emergency Hero Section
        st.markdown('''
            <div class="main-card">
                <div style="text-align: left; margin-bottom: 40px;">
                    <h1 style="font-size: 2.5rem; margin-bottom: 10px; color: white;">Emergency Request Intake</h1>
                    <p style="color: #9CA3AF; font-size: 1.1rem;">Provide information below to trigger our AI Response Workflow.</p>
                </div>
                <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 16px; padding: 20px; display: flex; gap: 20px; align-items: center;">
                    <div style="font-size: 2rem;">🛡️</div>
                    <div>
                        <h4 style="margin: 0; color: white;">24/7 Monitoring Active</h4>
                        <p style="margin: 0; color: #9CA3AF; font-size: 0.9rem;">Our AI agents are standby to prioritize your request within seconds.</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.form("intake_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("FULL NAME", placeholder="John Doe")
                contact = st.text_input("CONTACT NUMBER", placeholder="+1-XXX-XXX-XXXX")
            with c2:
                location = st.text_input("LOCATION", placeholder="Area, City, Province")
                language = st.selectbox("PREFERRED LANGUAGE", ["English", "Hindi", "Spanish", "French"])
            
            description = st.text_area("DETAILED EMERGENCY DESCRIPTION", placeholder="Describe the emergency in detail. Mention resources needed (food, water, medical aid)...", height=200)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("TRIGGER AI RESPONSE WORKFLOW")
            
            if submitted:
                if not name or not location or not description or not contact:
                    st.error("⚠️ All fields are required for emergency processing.")
                else:
                    payload = {
                        "name": name,
                        "location": location,
                        "description": description,
                        "contact_number": contact,
                        "language": language
                    }
                    try:
                        with st.spinner("🚀 AI Multi-Step Workflow Initiated..."):
                            response = requests.post(f"{API_BASE_URL}/requests/", json=payload)
                        if response.status_code == 200:
                            st.session_state.last_submission = response.json()
                            st.balloons()
                        else:
                            st.error(f"❌ Workflow Error: {response.text}")
                    except Exception as e:
                        st.error(f"🔌 Connection Error: Backend server is offline.")

        if st.session_state.get('last_submission'):
            data = st.session_state.last_submission
            st.markdown(f"""
            <div class="main-card" style="border: 1px solid rgba(34, 197, 94, 0.3); background: rgba(34, 197, 94, 0.02);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                    <h2 style="margin: 0; color: #22C55E;">✅ AI Analysis Complete</h2>
                    <span class="p-badge p-{data['urgency'].lower()}">{data['urgency']} PRIORITY</span>
                </div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                    <div>
                        <h4 style="color: #9CA3AF; margin-bottom: 10px;">Classification</h4>
                        <p style="font-size: 1.2rem; font-weight: 700;">{data['category']}</p>
                    </div>
                    <div>
                        <h4 style="color: #9CA3AF; margin-bottom: 10px;">Resources Identified</h4>
                        <p style="font-size: 1.2rem; font-weight: 700;">{data['required_resources']}</p>
                    </div>
                </div>
                <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.05); margin: 30px 0;">
                <h4 style="color: #9CA3AF; margin-bottom: 10px;">Volunteer Summary</h4>
                <p style="font-size: 1.1rem; font-style: italic; color: #E5E7EB;">"{data['summary']}"</p>
                
                <h4 style="color: #9CA3AF; margin-top: 30px; margin-bottom: 10px;">Local NGO Recommendations</h4>
                <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #F59E0B; padding: 15px; border-radius: 8px; color: #F59E0B; font-weight: 600;">
                    {data['recommendations']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("DISMISS ANALYSIS"):
                st.session_state.last_submission = None
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats/")
        if response.status_code == 200:
            stats = response.json()
            
            # Analytics Header
            st.markdown("""
            <div style="margin-bottom: 50px;">
                <h1 style="font-size: 2.5rem;">Response Intelligence Dashboard</h1>
                <p style="color: #9CA3AF; font-size: 1.1rem;">Real-time humanitarian metrics and request tracking.</p>
            </div>
            """, unsafe_allow_html=True)

            # Metrics Grid
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="stat-card">
                    <p style="color: #9CA3AF; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Total Requests</p>
                    <h1>{stats['total_requests']}</h1>
                    <div style="position: absolute; right: 20px; top: 20px; font-size: 1.5rem;">📥</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="stat-card" style="border-left: 4px solid #EF4444;">
                    <p style="color: #EF4444; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Critical Cases</p>
                    <h1>{stats['critical_count']}</h1>
                    <div style="position: absolute; right: 20px; top: 20px; font-size: 1.5rem;">🔥</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="stat-card">
                    <p style="color: #9CA3AF; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Avg AI Time</p>
                    <h1>1.2s</h1>
                    <div style="position: absolute; right: 20px; top: 20px; font-size: 1.5rem;">⚡</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="stat-card" style="border-left: 4px solid #22C55E;">
                    <p style="color: #22C55E; font-size: 0.8rem; font-weight: 700; text-transform: uppercase;">Network Status</p>
                    <h1>ACTIVE</h1>
                    <div style="position: absolute; right: 20px; top: 20px; font-size: 1.5rem;">🌐</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Visuals
            c1, c2 = st.columns([1, 1.5])
            with c1:
                st.markdown('<div class="main-card" style="padding: 30px; height: 100%;">', unsafe_allow_html=True)
                st.markdown('<h4 style="margin-bottom: 30px;">Request Distribution</h4>', unsafe_allow_html=True)
                if stats["category_counts"]:
                    df_cat = pd.DataFrame(list(stats["category_counts"].items()), columns=["Category", "Count"])
                    fig = px.pie(df_cat, values="Count", names="Category", hole=0.7, 
                                color_discrete_sequence=px.colors.sequential.Reds_r)
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="white"),
                        margin=dict(t=0, b=0, l=0, r=0),
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data available.")
                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="main-card" style="padding: 30px; height: 100%;">', unsafe_allow_html=True)
                st.markdown('<h4 style="margin-bottom: 30px;">Live Request Stream</h4>', unsafe_allow_html=True)
                if stats["recent_requests"]:
                    for req in stats["recent_requests"]:
                        p_class = f"p-{req['urgency'].lower()}"
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 12px; border: 1px solid var(--card-border); margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 700;">{req['name']}</div>
                                <div style="font-size: 0.8rem; color: #9CA3AF;">{req['category']} • {req['location']}</div>
                            </div>
                            <span class="p-badge {p_class}">{req['urgency']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No activity.")
                st.markdown('</div>', unsafe_allow_html=True)

            # Table View
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown('<div class="main-card" style="padding: 30px;">', unsafe_allow_html=True)
            st.markdown('<h4 style="margin-bottom: 30px;">Historical Request Audit</h4>', unsafe_allow_html=True)
            req_resp = requests.get(f"{API_BASE_URL}/requests/")
            if req_resp.status_code == 200:
                all_reqs = req_resp.json()
                if all_reqs:
                    df = pd.DataFrame(all_reqs)
                    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
                    st.dataframe(
                        df[['timestamp', 'name', 'location', 'category', 'urgency', 'summary']],
                        use_container_width=True,
                        hide_index=True
                    )
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"🔌 Connection Error: Backend server is offline.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    show_navbar()
    show_sidebar()
    
    # Simple routing
    if 'page' not in st.session_state:
        st.session_state.page = "Submit Request"
        
    # Sync radio with session state
    page_options = ["Submit Request", "Dashboard"]
    current_page = st.sidebar.radio("NAVIGATION", page_options, index=page_options.index(st.session_state.page))
    
    if current_page != st.session_state.page:
        st.session_state.page = current_page
        st.rerun()

    if st.session_state.page == "Submit Request":
        show_intake_form()
    else:
        show_dashboard()
        
    show_footer()

if __name__ == "__main__":
    main()
