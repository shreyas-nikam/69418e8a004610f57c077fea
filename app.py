
import streamlit as st
import sys
import os

# Add the directory containing app.py and utils.py to sys.path
# This needs to be done *before* attempting to import utils.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils import initialize_session_state # Import the initialization function

st.set_page_config(page_title="AI Value Creation & Investment Efficiency Planner", layout="wide")

# Corrected URL for the image: quantuniversity.com instead of quantuniversity_com
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.sidebar.title("QuLab: AI Value Creation & Investment Efficiency Planner")

# Initialize session state for the first run or after a restart
if 'initialized' not in st.session_state:
    initialize_session_state()
    st.session_state.initialized = True

# Define page options
PAGES = [
    "Company Selection and Initial Org-AI-R Assessment",
    "Deep Dive: Dimension-Level Assessment & Gap Analysis",
    "Identify High-Value AI Use Cases & Estimate Impact",
    "Build the Multi-Year AI Value Creation Plan",
    "Calculate AI Investment Efficiency & Portfolio Benchmarking",
    "Exit-Readiness Assessment"
]

# Sidebar navigation
st.sidebar.subheader("Navigation")
current_page_idx = st.sidebar.radio(
    label="Go to Step:",
    options=range(len(PAGES)),
    format_func=lambda x: f"Step {x+1}: {PAGES[x]}",
    index=st.session_state.get('current_page_idx', 0),
    key="navigation_radio"
)
st.session_state.current_page_idx = current_page_idx
st.session_state.page = PAGES[current_page_idx]

st.sidebar.divider()

def restart_session():
    # Clear all session state variables except for the 'initialized' flag if needed to prevent infinite loop
    # Or simply call initialize_session_state again to reset to defaults
    for key in list(st.session_state.keys()):
        # Keep 'initialized' to ensure initialize_session_state is called only once after explicit restart
        # 'portfolio_companies_df' is re-initialized by initialize_session_state, so it's safe to delete.
        if key not in ['initialized']:
            del st.session_state[key]
    initialize_session_state()
    st.session_state.page = PAGES[0] # Reset to first page
    st.session_state.current_page_idx = 0
    st.rerun()

if st.sidebar.button("Restart Session", key="sidebar_restart_button"):
    restart_session()

st.title("AI Value Creation & Investment Efficiency Planner")
st.divider()

st.markdown("""
Welcome, Private Equity Professional! As a **Portfolio Manager** at a leading PE firm, you're constantly evaluating
and optimizing your portfolio companies for maximum value creation. In today's landscape, Artificial Intelligence is
a critical lever, but quantifying its impact and building a clear investment roadmap can be complex.

This Streamlit application, the **"AI Value Creation & Investment Efficiency Planner"**, guides you through a structured,
data-driven workflow to assess a portfolio company's AI readiness, identify high-potential initiatives, quantify
their financial impact, and develop a strategic multi-year plan. You'll move from an initial high-level screening to
a detailed dimension-level assessment, project selection, financial modeling, and ultimately, an exit-readiness
projection. The story unfolds as you, the Portfolio Manager, make strategic decisions, evaluate potential returns,
and benchmark your assets to drive superior investment outcomes.

**Your Goal:** Maximize investor returns by strategically deploying AI within your portfolio companies.

**Follow the steps in the navigation sidebar to begin your journey.**
""")

# Page routing logic
if st.session_state.page == PAGES[0]:
    from application_pages.page_1_company_selection import main
    main()
elif st.session_state.page == PAGES[1]:
    from application_pages.page_2_dimension_assessment import main
    main()
elif st.session_state.page == PAGES[2]:
    from application_pages.page_3_use_case_selection import main
    main()
elif st.session_state.page == PAGES[3]:
    from application_pages.page_4_multi_year_plan import main
    main()
elif st.session_state.page == PAGES[4]:
    from application_pages.page_5_portfolio_benchmarking import main
    main()
elif st.session_state.page == PAGES[5]:
    from application_pages.page_6_exit_readiness import main
    main()
