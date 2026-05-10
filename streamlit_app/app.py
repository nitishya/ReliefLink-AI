import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# API Configuration
API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="ReliefLink AI",
    page_icon="🆘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .priority-critical { color: #ff4b4b; font-weight: bold; }
    .priority-high { color: #ff9f4b; font-weight: bold; }
    .priority-medium { color: #f9d71c; font-weight: bold; }
    .priority-low { color: #28a745; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def main():
    st.sidebar.title("🆘 ReliefLink AI")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigation", ["Submit Request", "Dashboard"])

    if page == "Submit Request":
        show_intake_form()
    else:
        show_dashboard()

def show_intake_form():
    st.title("Emergency Request Intake")
    st.markdown("Please provide details about the emergency. Our AI will process and prioritize your request.")

    with st.form("intake_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            contact = st.text_input("Contact Number")
        with col2:
            location = st.text_input("Location (Area/City)")
            language = st.selectbox("Preferred Language", ["English", "Hindi", "Spanish", "French"])
        
        description = st.text_area("Description of Emergency", height=150)
        
        submitted = st.form_submit_button("Submit Emergency Request")
        
        if submitted:
            if not name or not location or not description or not contact:
                st.error("Please fill in all required fields.")
            else:
                payload = {
                    "name": name,
                    "location": location,
                    "description": description,
                    "contact_number": contact,
                    "language": language
                }
                try:
                    with st.spinner("AI is processing your request..."):
                        response = requests.post(f"{API_BASE_URL}/requests/", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        st.success("Request Submitted Successfully!")
                        
                        # Show AI Analysis Results
                        st.markdown("### AI Analysis Results")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Category", data['category'])
                        c2.metric("Urgency", data['urgency'])
                        
                        st.info(f"**Summary:** {data['summary']}")
                        st.info(f"**Hindi Translation:** {data['hindi_summary']}")
                        st.warning(f"**Recommendations:** {data['recommendations']}")
                    else:
                        st.error(f"Failed to submit request. Error: {response.text}")
                except Exception as e:
                    st.error(f"Could not connect to backend server. {e}")

def show_dashboard():
    st.title("Emergency Response Dashboard")
    
    try:
        response = requests.get(f"{API_BASE_URL}/stats/")
        if response.status_code == 200:
            stats = response.json()
            
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="status-card"><h3>Total Requests</h3><h1>{stats["total_requests"]}</h1></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="status-card"><h3>Critical Issues</h3><h1 style="color:#ff4b4b">{stats["critical_count"]}</h1></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="status-card"><h3>Avg Response Time</h3><h1>< 5m</h1></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Charts Row
            c1, c2 = st.columns(2)
            with c1:
                if stats["category_counts"]:
                    df_cat = pd.DataFrame(list(stats["category_counts"].items()), columns=["Category", "Count"])
                    fig = px.pie(df_cat, values="Count", names="Category", title="Requests by Category", hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No data for category chart.")
            
            with c2:
                st.markdown("### Recent Requests")
                if stats["recent_requests"]:
                    for req in stats["recent_requests"]:
                        urgency_class = f"priority-{req['urgency'].lower()}"
                        st.markdown(f"""
                        **{req['name']}** - {req['category']}  
                        <span class="{urgency_class}">{req['urgency']}</span> | {req['location']}  
                        *{req['summary']}*
                        ---
                        """, unsafe_allow_html=True)
                else:
                    st.write("No recent requests.")
            
            # Full Table
            st.markdown("### All Emergency Requests")
            req_resp = requests.get(f"{API_BASE_URL}/requests/")
            if req_resp.status_code == 200:
                all_reqs = req_resp.json()
                if all_reqs:
                    df = pd.DataFrame(all_reqs)
                    st.dataframe(df[['timestamp', 'name', 'location', 'category', 'urgency', 'summary']])
                else:
                    st.write("No requests found.")

        else:
            st.error("Failed to fetch dashboard stats.")
    except Exception as e:
        st.error(f"Could not connect to backend server. {e}")

if __name__ == "__main__":
    main()
