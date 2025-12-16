
import streamlit as st
import pandas as pd
import numpy as np

# Import all shared functions and data
# This import assumes the 'application_pages' directory exists and contains
# an '__init__.py' file (making it a Python package) and a 'shared_functions.py' module.
from application_pages.shared_functions import (
    initialize_session_state,
    go_to_page,
    pages_config, # To get the list of page labels
)

st.set_page_config(page_title="AI Value Creation & Investment Efficiency Planner", layout="wide")

# Initialize session state for all relevant variables at the start of the app
# This needs to be done on every rerun if the key 'session_initialized' is not present.
# It ensures all necessary variables are set up.
if 'session_initialized' not in st.session_state or not st.session_state['session_initialized']:
    initialize_session_state()
    st.session_state['session_initialized'] = True

# --- Sidebar ---
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.title("AI Value Creation & Investment Efficiency Planner")
st.sidebar.divider()

# Restart Session button
if st.sidebar.button("Restart Session"):
    # Clear all session state variables except the 'session_initialized' flag
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    # Set the flag to False so initialize_session_state runs on the next rerun
    st.session_state['session_initialized'] = False
    st.rerun()

# Navigation dropdown
page_labels = list(pages_config.keys())
# Ensure 'current_page' is always in session_state, initialized by initialize_session_state
current_page_index = page_labels.index(st.session_state['current_page']) if st.session_state['current_page'] in page_labels else 0

selected_page_label = st.sidebar.selectbox(
    label="Navigation",
    options=page_labels,
    index=current_page_index,
    key='sidebar_navigation_select' # Unique key for this widget
)

# Update session state and query params if sidebar selection changes
# This check prevents unnecessary reruns if the page is already selected
if selected_page_label != st.session_state['current_page']:
    go_to_page(selected_page_label) # Uses the helper to set page and rerun

# Display current step progress
step_index = page_labels.index(st.session_state['current_page']) + 1
total_steps = len(page_labels)
st.sidebar.markdown(f"**Step {step_index} of {total_steps}: {st.session_state['current_page']}**")
st.sidebar.divider()

# --- Main Content Area ---
st.title("QuLab: AI Value Creation & Investment Efficiency Planner")
st.divider()

# Overall business scenario and story explanation
st.markdown("""
In this lab, you step into the shoes of a **Private Equity Portfolio Manager** responsible for maximizing value
across a diverse portfolio of companies. Your mission is to strategically leverage Artificial Intelligence
to drive growth, improve operational efficiency, and ultimately, enhance exit valuations for your assets.

This application provides a structured, step-by-step workflow to:
1.  **Screen potential AI opportunities** within a portfolio company.
2.  Conduct a **deep-dive assessment** of current AI capabilities and identify key gaps.
3.  **Strategically select** AI initiatives that address these gaps and drive measurable value.
4.  **Quantify** the projected financial impact (EBITDA) and organizational AI readiness (Org-AI-R) over a multi-year horizon.
5.  **Benchmark** the company's AI performance and investment efficiency against the rest of your portfolio.
6.  **Assess** how these AI investments contribute to a compelling exit narrative and enhanced valuation multiples.

Each page represents a critical decision point or analytical task in your journey. Interact with the inputs, review the
outputs, and observe how your strategic choices influence the company's AI trajectory and financial outcomes.
Use the 'Navigation' sidebar to move between steps or the 'Continue' button at the bottom of each section.
""")

st.markdown("---") # Visual separator

# Load and run the selected page's main function
# The `pages_config` dict maps page labels (e.g., "Company Selection") to their
# corresponding module names (e.g., "page_1_company_selection").
page_module_name = pages_config[st.session_state['current_page']]
try:
    # Dynamically import the main function from the selected page module
    # 'fromlist=["main"]' is crucial for relative imports and to ensure 'main' is directly accessible.
    module = __import__(f"application_pages.{page_module_name}", fromlist=["main"])
    module.main()
except ImportError:
    st.error(f"Could not load page: '{st.session_state['current_page']}'. This might happen if page files are missing or the 'application_pages' directory is not a valid Python package.")
    st.info("Please ensure all page files (e.g., `application_pages/page_1_company_selection.py`) are created and the `application_pages` directory contains an `__init__.py` file.")
except Exception as e:
    st.error(f"An unexpected error occurred on page '{st.session_state['current_page']}': {e}")
    st.exception(e) # Display full traceback for debugging
