id: 69418e8a004610f57c077fea_documentation
summary: AI Value Creation & Investment Efficiency Planner Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Value Creation & Investment Efficiency Planner: A Developer's Guide

## Step 1: Understanding the AI Value Creation & Investment Efficiency Planner
Duration: 0:05:00

Welcome to the **"AI Value Creation & Investment Efficiency Planner"** codelab! This guide provides a comprehensive walkthrough of a Streamlit application designed for Private Equity (PE) professionals, specifically Portfolio Managers, to strategically assess, plan, and optimize AI investments within their portfolio companies.

<aside class="positive">
This application empowers PE professionals to move beyond qualitative discussions to a **data-driven approach** for quantifying AI's impact, identifying high-potential initiatives, and developing actionable multi-year investment plans. Understanding this application will equip you with insights into building interactive, data-intensive tools with Streamlit for complex business workflows.
</aside>

**Why is this application important?**
In today's competitive landscape, Artificial Intelligence (AI) is a critical driver for value creation. However, many organizations struggle with:
1.  **Quantifying AI Impact:** How much value can AI truly unlock?
2.  **Strategic Alignment:** Which AI initiatives align best with company goals?
3.  **Investment Efficiency:** Are AI investments delivering optimal returns?
4.  **Benchmarking:** How does one company's AI readiness compare to others in the portfolio or market?
This application provides a structured framework to address these challenges, guiding users from initial assessment to final exit-readiness projections.

**Core Concepts Explained:**
*   **Streamlit Fundamentals:** Building interactive web applications with Python.
*   **Session State Management:** Persisting data across user interactions and page navigations in Streamlit.
*   **Modular Application Design:** Organizing a Streamlit application into multiple Python files for better maintainability and scalability.
*   **Data-Driven Decision Making:** Using quantitative and qualitative inputs to drive strategic planning.
*   **Financial Modeling:** Estimating AI's impact on revenue, cost savings, and ultimately, company valuation.

**Application Workflow:**
The application follows a logical, step-by-step workflow mirroring a PE professional's journey:
1.  **Company Selection & Initial Assessment:** Select or add a portfolio company and perform a high-level "Org-AI-R" assessment.
2.  **Deep Dive Assessment:** Conduct a detailed dimension-level assessment of the company's AI readiness.
3.  **Use Case Identification & Impact Estimation:** Identify specific AI use cases and estimate their potential financial impact.
4.  **Multi-Year Plan Development:** Build a strategic multi-year plan for AI investments and expected value creation.
5.  **Investment Efficiency & Benchmarking:** Analyze the efficiency of AI investments and benchmark against other portfolio companies.
6.  **Exit-Readiness Assessment:** Project the impact of AI initiatives on the company's valuation and exit potential.

**Overall Application Architecture:**

The application utilizes a modular architecture to manage complexity. The main `app.py` acts as the entry point, handling global configurations, session state initialization, sidebar navigation, and routing to specific page implementations. Each page's logic resides in its own Python file within the `application_pages` directory, enhancing readability and maintainability. `utils.py` handles common utilities, primarily session state initialization.

```mermaid
graph TD
    A[app.py - Main Entry Point] --> B{st.set_page_config()}
    A --> C{sys.path Setup}
    A --> D{Sidebar: Navigation & Restart}
    A --> E{Session State Initialization}
    A --> F{Main Content Area}
    E -- Persists Data --> G[st.session_state]
    F -- Routes based on st.session_state.page --> H[application_pages/page_1_company_selection.py]
    F -- Routes based on st.session_state.page --> I[application_pages/page_2_dimension_assessment.py]
    F -- Routes based on st.session_state.page --> J[application_pages/page_3_use_case_selection.py]
    F -- Routes based on st.session_state.page --> K[application_pages/page_4_multi_year_plan.py]
    F -- Routes based on st.session_state.page --> L[application_pages/page_5_portfolio_benchmarking.py]
    F -- Routes based on st.session_state.page --> M[application_pages/page_6_exit_readiness.py]
    H --> G
    I --> G
    J --> G
    K --> G
    L --> G
    M --> G
    E -- Calls --> N[utils.py: initialize_session_state()]
```

This structure allows different parts of the application to operate independently while sharing data through Streamlit's `st.session_state` mechanism.

## Step 2: Setting Up the Development Environment and Project Structure
Duration: 0:08:00

Before diving into the code, let's ensure your development environment is correctly set up and you understand the project's file structure.

**Prerequisites:**
*   Python 3.8+ installed.
*   `pip` (Python package installer).

**1. Create a Project Directory:**
Start by creating a main directory for your project.
```bash
mkdir ai_planner_app
cd ai_planner_app
```

**2. Install Dependencies:**
The core dependency is Streamlit. You might also need `pandas` for data handling, which is often a good practice in such applications.
```bash
pip install streamlit pandas
```

**3. Recreate the File Structure:**
The application uses a modular structure. Create the following files and directories:
```
ai_planner_app/
├── app.py
├── utils.py
└── application_pages/
    ├── __init__.py
    ├── page_1_company_selection.py
    ├── page_2_dimension_assessment.py
    ├── page_3_use_case_selection.py
    ├── page_4_multi_year_plan.py
    ├── page_5_portfolio_benchmarking.py
    └── page_6_exit_readiness.py
```
You can create these using your terminal:
```bash
touch app.py utils.py
mkdir application_pages
touch application_pages/__init__.py application_pages/page_1_company_selection.py \
      application_pages/page_2_dimension_assessment.py application_pages/page_3_use_case_selection.py \
      application_pages/page_4_multi_year_plan.py application_pages/page_5_portfolio_benchmarking.py \
      application_pages/page_6_exit_readiness.py
```

**4. Populate `app.py`:**
Copy the provided `app.py` content into your `app.py` file.

**5. Populate `utils.py`:**
For `utils.py`, we need a function to initialize the session state variables.

```python
# utils.py
import streamlit as st
import pandas as pd
import numpy as np

def initialize_session_state():
    """
    Initializes or resets Streamlit session state variables for the AI Planner application.
    This function sets up default values for all key data structures and application state.
    """
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False # Flag to ensure this runs only once per session or explicit restart

    if not st.session_state.initialized:
        # General App State
        st.session_state.page = "Company Selection and Initial Org-AI-R Assessment"
        st.session_state.current_page_idx = 0

        # Company Data
        if 'portfolio_companies_df' not in st.session_state:
            st.session_state.portfolio_companies_df = pd.DataFrame(
                columns=[
                    "Company Name", "Industry", "Revenue ($M)", "EBITDA ($M)",
                    "Org-AI-R Score", "Data_Maturity", "Tech_Infra", "Talent_Capability",
                    "Strategy_Vision", "Culture_Adaptability", "Regulatory_Compliance",
                    "Selected Use Cases", "AI Investment ($M) Y1", "AI Investment ($M) Y2", "AI Investment ($M) Y3",
                    "Projected Value Add ($M) Y1", "Projected Value Add ($M) Y2", "Projected Value Add ($M) Y3",
                    "AI Efficiency Score"
                ]
            )

        # Default sample company data for initial demonstration
        if st.session_state.portfolio_companies_df.empty:
            sample_data = {
                "Company Name": ["Tech Innovations Inc.", "Global Logistics Co.", "Healthcare Solutions Ltd."],
                "Industry": ["Software", "Logistics", "Healthcare"],
                "Revenue ($M)": [500, 300, 700],
                "EBITDA ($M)": [100, 45, 120],
                "Org-AI-R Score": [3.5, 2.8, 3.9],
                "Data_Maturity": [4, 3, 4],
                "Tech_Infra": [4, 3, 4],
                "Talent_Capability": [3, 2, 4],
                "Strategy_Vision": [4, 3, 4],
                "Culture_Adaptability": [3, 2, 4],
                "Regulatory_Compliance": [4, 3, 4],
                "Selected Use Cases": [
                    "Predictive Analytics, Automated Customer Support",
                    "Route Optimization, Inventory Forecasting",
                    "Diagnostic Imaging, Personalized Treatment Plans"
                ],
                "AI Investment ($M) Y1": [5, 3, 7],
                "AI Investment ($M) Y2": [7, 4, 9],
                "AI Investment ($M) Y3": [8, 5, 10],
                "Projected Value Add ($M) Y1": [15, 8, 20],
                "Projected Value Add ($M) Y2": [25, 12, 35],
                "Projected Value Add ($M) Y3": [35, 18, 50],
                "AI Efficiency Score": [3.0, 2.7, 3.2] # Example calculated score
            }
            st.session_state.portfolio_companies_df = pd.DataFrame(sample_data)

        # Selected company for detailed view
        if 'selected_company_name' not in st.session_state:
            st.session_state.selected_company_name = (
                st.session_state.portfolio_companies_df["Company Name"].iloc[0]
                if not st.session_state.portfolio_companies_df.empty
                else None
            )

        # Detailed Assessment Data (for the currently selected company)
        if 'assessment_scores' not in st.session_state:
            st.session_state.assessment_scores = {
                "Data Maturity": {"score": 3, "insights": ""},
                "Technology Infrastructure": {"score": 3, "insights": ""},
                "Talent & Capabilities": {"score": 3, "insights": ""},
                "Strategy & Vision": {"score": 3, "insights": ""},
                "Culture & Adaptability": {"score": 3, "insights": ""},
                "Regulatory & Compliance": {"score": 3, "insights": ""},
            }

        # Use Case Data
        if 'use_cases_df' not in st.session_state:
            st.session_state.use_cases_df = pd.DataFrame(
                columns=[
                    "Use Case", "Description", "Business Impact ($M/year)",
                    "Complexity", "Feasibility", "Alignment with Strategy", "Selected"
                ]
            )

        # Multi-Year Plan Data (for the currently selected company's plan)
        if 'ai_plan_df' not in st.session_state:
            st.session_state.ai_plan_df = pd.DataFrame(
                columns=[
                    "Year", "AI Investment ($M)", "Projected Value Add ($M)", "Cumulative Investment ($M)", "Cumulative Value Add ($M)"
                ]
            )
            # Initialize with default years and zero values
            for i in range(1, 4): # Plan for 3 years
                st.session_state.ai_plan_df = pd.concat([
                    st.session_state.ai_plan_df,
                    pd.DataFrame([{"Year": f"Year {i}", "AI Investment ($M)": 0, "Projected Value Add ($M)": 0, "Cumulative Investment ($M)": 0, "Cumulative Value Add ($M)": 0}])
                ], ignore_index=True)


        # Exit-Readiness Data
        if 'exit_readiness_data' not in st.session_state:
            st.session_state.exit_readiness_data = {
                "AI-Driven Valuation Uplift ($M)": 0,
                "Improved Multiplier (x)": 0,
                "Total Exit Value Impact ($M)": 0,
                "Key Strengths": [],
                "Areas for Improvement": []
            }

        st.session_state.initialized = True # Mark as initialized

```

**6. Populate Placeholder Page Files:**
For the `application_pages` files, for now, you can just put a simple `main()` function to demonstrate the routing. We'll conceptualize their content in later steps.

```python
# application_pages/page_1_company_selection.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("Step 1: Company Selection and Initial Org-AI-R Assessment")
    st.write("This page allows you to select a company, add a new one, and perform a high-level Org-AI-R assessment.")
    
    # Placeholder for company selection
    if not st.session_state.portfolio_companies_df.empty:
        company_names = st.session_state.portfolio_companies_df["Company Name"].tolist()
        st.session_state.selected_company_name = st.selectbox(
            "Select Company",
            options=company_names,
            index=company_names.index(st.session_state.selected_company_name) if st.session_state.selected_company_name in company_names else 0,
            key="page1_company_select"
        )
        current_company_data = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df["Company Name"] == st.session_state.selected_company_name].iloc[0]
        st.metric(label="Selected Company Revenue", value=f"${current_company_data['Revenue ($M)']:,}M")
        st.metric(label="Selected Company Org-AI-R Score", value=f"{current_company_data['Org-AI-R Score']:.1f}")
    else:
        st.warning("No companies added yet. Please add a new company below.")

    with st.expander("Add New Company"):
        new_company_name = st.text_input("New Company Name", key="new_company_name_input")
        new_company_industry = st.text_input("Industry", key="new_company_industry_input")
        new_company_revenue = st.number_input("Revenue ($M)", min_value=0.0, value=0.0, key="new_company_revenue_input")
        new_company_ebitda = st.number_input("EBITDA ($M)", min_value=0.0, value=0.0, key="new_company_ebitda_input")
        
        if st.button("Add Company", key="add_company_button"):
            if new_company_name and new_company_name not in st.session_state.portfolio_companies_df["Company Name"].values:
                new_row = pd.DataFrame([{
                    "Company Name": new_company_name,
                    "Industry": new_company_industry,
                    "Revenue ($M)": new_company_revenue,
                    "EBITDA ($M)": new_company_ebitda,
                    "Org-AI-R Score": 0, # Initial score
                    "Data_Maturity": 0, "Tech_Infra": 0, "Talent_Capability": 0,
                    "Strategy_Vision": 0, "Culture_Adaptability": 0, "Regulatory_Compliance": 0,
                    "Selected Use Cases": "",
                    "AI Investment ($M) Y1": 0, "AI Investment ($M) Y2": 0, "AI Investment ($M) Y3": 0,
                    "Projected Value Add ($M) Y1": 0, "Projected Value Add ($M) Y2": 0, "Projected Value Add ($M) Y3": 0,
                    "AI Efficiency Score": 0
                }])
                st.session_state.portfolio_companies_df = pd.concat([st.session_state.portfolio_companies_df, new_row], ignore_index=True)
                st.session_state.selected_company_name = new_company_name
                st.success(f"Company '{new_company_name}' added!")
                st.rerun()
            else:
                st.error("Company name is required or already exists.")

    st.write("")
    st.write("Perform initial Org-AI-R (Organizational AI Readiness) assessment:")
    if st.session_state.selected_company_name:
        current_company_index = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df["Company Name"] == st.session_state.selected_company_name].index[0]
        
        col1, col2 = st.columns(2)
        with col1:
            data_maturity = st.slider("Data Maturity (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Data_Maturity'], key=f"data_maturity_{st.session_state.selected_company_name}")
            tech_infra = st.slider("Technology Infrastructure (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Tech_Infra'], key=f"tech_infra_{st.session_state.selected_company_name}")
            talent_capability = st.slider("Talent & Capabilities (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Talent_Capability'], key=f"talent_capability_{st.session_state.selected_company_name}")
        with col2:
            strategy_vision = st.slider("Strategy & Vision (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Strategy_Vision'], key=f"strategy_vision_{st.session_state.selected_company_name}")
            culture_adaptability = st.slider("Culture & Adaptability (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Culture_Adaptability'], key=f"culture_adaptability_{st.session_state.selected_company_name}")
            regulatory_compliance = st.slider("Regulatory & Compliance (1-5)", 1, 5, st.session_state.portfolio_companies_df.loc[current_company_index, 'Regulatory_Compliance'], key=f"regulatory_compliance_{st.session_state.selected_company_name}")

        avg_score = (data_maturity + tech_infra + talent_capability + strategy_vision + culture_adaptability + regulatory_compliance) / 6
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Org-AI-R Score'] = avg_score
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Data_Maturity'] = data_maturity
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Tech_Infra'] = tech_infra
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Talent_Capability'] = talent_capability
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Strategy_Vision'] = strategy_vision
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Culture_Adaptability'] = culture_adaptability
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Regulatory_Compliance'] = regulatory_compliance

        st.info(f"Current **Org-AI-R Score** for {st.session_state.selected_company_name}: **{avg_score:.2f}**")
    else:
        st.info("Please select or add a company to perform assessment.")

```
The other page files (`page_2_dimension_assessment.py`, `page_3_use_case_selection.py`, etc.) will have similar `main()` functions. For now, you can just add a placeholder `main()` function printing the page title for each, e.g.:

```python
# application_pages/page_X_YOUR_PAGE.py
import streamlit as st

def main():
    st.subheader("Step X: [Your Page Title]")
    st.write("Content for this page will go here.")
```
Replace `X` and `[Your Page Title]` with the actual step number and title.

**7. Run the Application:**
Navigate to the `ai_planner_app` directory in your terminal and run the Streamlit application:
```bash
streamlit run app.py
```
This should open the application in your web browser, displaying the main page with the sidebar navigation.

## Step 3: Exploring the Main Application (`app.py`)
Duration: 0:10:00

The `app.py` file is the heart of the Streamlit application. It handles the overall structure, navigation, and initial setup. Let's break down its components.

```python
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
```

**1. System Path Modification and Imports:**
```python
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
from utils import initialize_session_state
```
This crucial block ensures that Python can find modules in the `application_pages` directory and `utils.py`. By adding the `current_dir` to `sys.path`, Python's interpreter knows where to look for local modules, allowing `from utils import initialize_session_state` to work correctly. This is particularly important for modular Streamlit apps.

**2. Page Configuration:**
```python
st.set_page_config(page_title="AI Value Creation & Investment Efficiency Planner", layout="wide")
```
`st.set_page_config` is called once at the very beginning of your script to set up global configurations for your Streamlit app, such as the browser tab title (`page_title`) and the layout style (`layout="wide"` for more horizontal space).

**3. Sidebar Elements:**
The sidebar is a key navigation component.
```python
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.sidebar.title("QuLab: AI Value Creation & Investment Efficiency Planner")
```
These lines add a logo image, a visual divider, and the application's main title to the sidebar.

**4. Session State Initialization:**
```python
if 'initialized' not in st.session_state:
    initialize_session_state()
    st.session_state.initialized = True
```
This block checks if the session state has been initialized for the current user session. If not, it calls `initialize_session_state()` from `utils.py` to set up all default data structures and flags. This ensures that the application always starts with a consistent state, or resets to one after an explicit restart.

**5. Page Definition and Navigation:**
```python
PAGES = [
    "Company Selection and Initial Org-AI-R Assessment",
    # ... other pages ...
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
```
The `PAGES` list defines the titles of all the steps in the application. `st.sidebar.radio` creates a set of radio buttons in the sidebar, allowing users to navigate between these steps. The `format_func` customizes how the options are displayed (e.g., "Step 1: ..."). The `st.session_state.page` and `st.session_state.current_page_idx` variables store the user's current page selection, ensuring state persistence across reruns.

**6. Restart Session Functionality:**
```python
def restart_session():
    # ... logic to clear session state and re-initialize ...
    st.rerun()

if st.sidebar.button("Restart Session", key="sidebar_restart_button"):
    restart_session()
```
The `restart_session` function clears most of the `st.session_state` variables and then re-calls `initialize_session_state()`. This provides users with a way to reset the application to its default state, akin to starting fresh. `st.rerun()` forces Streamlit to re-execute the entire script from top to bottom, applying the reset state.

**7. Main Content Introduction:**
```python
st.title("AI Value Creation & Investment Efficiency Planner")
st.divider()
st.markdown("""
Welcome, Private Equity Professional! ...
""")
```
This section sets the main title of the application and provides an introductory text using `st.markdown`, explaining the purpose and target audience of the tool.

**8. Page Routing Logic:**
```python
if st.session_state.page == PAGES[0]:
    from application_pages.page_1_company_selection import main
    main()
elif st.session_state.page == PAGES[1]:
    # ...
```
This is the core routing mechanism. Based on the value of `st.session_state.page` (which is updated by the sidebar navigation), the application dynamically imports and calls the `main()` function of the corresponding page file from the `application_pages` directory. This pattern allows for a clean separation of concerns, where each page's logic is self-contained.

## Step 4: Mastering Streamlit Session State (`utils.py`)
Duration: 0:07:00

Streamlit's `st.session_state` is fundamental for building multi-page or interactive applications where data needs to persist across reruns or different views. The `utils.py` file is dedicated to managing this crucial aspect of our application.

```python
# utils.py
import streamlit as st
import pandas as pd
import numpy as np

def initialize_session_state():
    """
    Initializes or resets Streamlit session state variables for the AI Planner application.
    This function sets up default values for all key data structures and application state.
    """
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False

    if not st.session_state.initialized:
        # General App State
        st.session_state.page = "Company Selection and Initial Org-AI-R Assessment"
        st.session_state.current_page_idx = 0

        # Company Data
        if 'portfolio_companies_df' not in st.session_state:
            st.session_state.portfolio_companies_df = pd.DataFrame(
                columns=[
                    "Company Name", "Industry", "Revenue ($M)", "EBITDA ($M)",
                    "Org-AI-R Score", "Data_Maturity", "Tech_Infra", "Talent_Capability",
                    "Strategy_Vision", "Culture_Adaptability", "Regulatory_Compliance",
                    "Selected Use Cases", "AI Investment ($M) Y1", "AI Investment ($M) Y2", "AI Investment ($M) Y3",
                    "Projected Value Add ($M) Y1", "Projected Value Add ($M) Y2", "Projected Value Add ($M) Y3",
                    "AI Efficiency Score"
                ]
            )

        # Default sample company data for initial demonstration (omitted for brevity in codelab, but present in full code)
        # if st.session_state.portfolio_companies_df.empty:
        #     sample_data = {...}
        #     st.session_state.portfolio_companies_df = pd.DataFrame(sample_data)

        # Selected company for detailed view
        if 'selected_company_name' not in st.session_state:
            st.session_state.selected_company_name = (
                st.session_state.portfolio_companies_df["Company Name"].iloc[0]
                if not st.session_state.portfolio_companies_df.empty
                else None
            )

        # Detailed Assessment Data (for the currently selected company)
        if 'assessment_scores' not in st.session_state:
            st.session_state.assessment_scores = {
                "Data Maturity": {"score": 3, "insights": ""},
                "Technology Infrastructure": {"score": 3, "insights": ""},
                "Talent & Capabilities": {"score": 3, "insights": ""},
                "Strategy & Vision": {"score": 3, "insights": ""},
                "Culture & Adaptability": {"score": 3, "insights": ""},
                "Regulatory & Compliance": {"score": 3, "insights": ""},
            }

        # Use Case Data
        if 'use_cases_df' not in st.session_state:
            st.session_state.use_cases_df = pd.DataFrame(
                columns=[
                    "Use Case", "Description", "Business Impact ($M/year)",
                    "Complexity", "Feasibility", "Alignment with Strategy", "Selected"
                ]
            )

        # Multi-Year Plan Data (for the currently selected company's plan)
        if 'ai_plan_df' not in st.session_state:
            st.session_state.ai_plan_df = pd.DataFrame(
                columns=[
                    "Year", "AI Investment ($M)", "Projected Value Add ($M)", "Cumulative Investment ($M)", "Cumulative Value Add ($M)"
                ]
            )
            for i in range(1, 4): # Plan for 3 years
                st.session_state.ai_plan_df = pd.concat([
                    st.session_state.ai_plan_df,
                    pd.DataFrame([{"Year": f"Year {i}", "AI Investment ($M)": 0, "Projected Value Add ($M)": 0, "Cumulative Investment ($M)": 0, "Cumulative Value Add ($M)": 0}])
                ], ignore_index=True)

        # Exit-Readiness Data
        if 'exit_readiness_data' not in st.session_state:
            st.session_state.exit_readiness_data = {
                "AI-Driven Valuation Uplift ($M)": 0,
                "Improved Multiplier (x)": 0,
                "Total Exit Value Impact ($M)": 0,
                "Key Strengths": [],
                "Areas for Improvement": []
            }

        st.session_state.initialized = True
```

The `initialize_session_state()` function is called conditionally in `app.py`. This function ensures that all necessary variables are present in `st.session_state` with default values, especially when the application starts or is explicitly restarted.

**Key Session State Variables and Their Purpose:**

*   `st.session_state.initialized`: A boolean flag to ensure `initialize_session_state()` runs only once per user session or upon explicit restart.
*   `st.session_state.page`: Stores the current page name (string), used by `app.py` for routing.
*   `st.session_state.current_page_idx`: Stores the index of the current page, used by the sidebar radio button to maintain selection.
*   `st.session_state.portfolio_companies_df`: A Pandas DataFrame that holds data for all portfolio companies. This is a central data store, updated across various pages. It includes initial company details, Org-AI-R scores, detailed dimension scores, selected AI use cases, investment plans, and efficiency metrics.
    *   This DataFrame is crucial for **data persistence and transfer** between pages. For example, a company added on Page 1 is available for detailed assessment on Page 2, and its aggregated data is used for benchmarking on Page 5.
*   `st.session_state.selected_company_name`: The name of the company currently selected by the user for detailed analysis. Most pages operate on this `selected_company_name`.
*   `st.session_state.assessment_scores`: A dictionary holding detailed assessment scores and insights for the *currently selected company*. While some scores are aggregated into `portfolio_companies_df`, this dictionary might hold more granular, temporary, or textual insights specific to the deep dive.
*   `st.session_state.use_cases_df`: A DataFrame to manage potential AI use cases, their estimated impact, and feasibility. This is typically used on Page 3.
*   `st.session_state.ai_plan_df`: A DataFrame outlining the multi-year AI investment and value creation plan for the *selected company*, used on Page 4.
*   `st.session_state.exit_readiness_data`: A dictionary to store aggregated insights and calculated metrics related to the company's exit potential, updated on Page 6.

<aside class="negative">
It's critical to ensure that `st.session_state` variables are consistently named and accessed across all your page files. Inconsistent naming or accidental overwriting can lead to data loss or unexpected application behavior. Always check if a key exists before trying to access it, especially if it's user-modifiable or dependent on previous interactions.
</aside>

By centralizing state management in `utils.py` and using `st.session_state` effectively, the application maintains data integrity and provides a seamless user experience across its various steps.

## Step 5: Page 1 - Company Selection and Initial Org-AI-R Assessment
Duration: 0:15:00

This is the entry point for the user's journey. On this page, a Private Equity professional selects an existing portfolio company or adds a new one. It also facilitates a high-level "Organizational AI Readiness (Org-AI-R)" assessment.

**File:** `application_pages/page_1_company_selection.py`

**Purpose:**
*   Allow users to choose from a list of portfolio companies.
*   Provide functionality to add new companies with basic financial details.
*   Conduct a high-level, multi-dimensional assessment of the selected company's AI readiness.
*   Store company data and initial assessment scores in `st.session_state.portfolio_companies_df`.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_1_company_selection.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("Step 1: Company Selection and Initial Org-AI-R Assessment")
    st.write("This page allows you to select a company, add a new one, and perform a high-level Org-AI-R assessment.")
    
    #  Company Selection 
    if not st.session_state.portfolio_companies_df.empty:
        company_names = st.session_state.portfolio_companies_df["Company Name"].tolist()
        
        # Ensure selected_company_name is in current list of companies
        if st.session_state.selected_company_name not in company_names:
            st.session_state.selected_company_name = company_names[0] # Default to first if not found
        
        st.session_state.selected_company_name = st.selectbox(
            "Select Company",
            options=company_names,
            index=company_names.index(st.session_state.selected_company_name),
            key="page1_company_select"
        )
        current_company_data = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df["Company Name"] == st.session_state.selected_company_name].iloc[0]
        st.metric(label=f"{st.session_state.selected_company_name} Revenue", value=f"${current_company_data['Revenue ($M)']:,}M")
        st.metric(label=f"{st.session_state.selected_company_name} Org-AI-R Score", value=f"{current_company_data['Org-AI-R Score']:.1f}")
    else:
        st.warning("No companies added yet. Please add a new company below.")

    #  Add New Company 
    with st.expander("Add New Company"):
        new_company_name = st.text_input("New Company Name", key="new_company_name_input")
        new_company_industry = st.text_input("Industry", key="new_company_industry_input")
        new_company_revenue = st.number_input("Revenue ($M)", min_value=0.0, value=0.0, key="new_company_revenue_input")
        new_company_ebitda = st.number_input("EBITDA ($M)", min_value=0.0, value=0.0, key="new_company_ebitda_input")
        
        if st.button("Add Company", key="add_company_button"):
            if new_company_name and new_company_name not in st.session_state.portfolio_companies_df["Company Name"].values:
                # Create a new row with default initial values for all columns
                new_row = pd.DataFrame([{
                    "Company Name": new_company_name,
                    "Industry": new_company_industry,
                    "Revenue ($M)": new_company_revenue,
                    "EBITDA ($M)": new_company_ebitda,
                    "Org-AI-R Score": 0, # Initial score
                    "Data_Maturity": 0, "Tech_Infra": 0, "Talent_Capability": 0,
                    "Strategy_Vision": 0, "Culture_Adaptability": 0, "Regulatory_Compliance": 0,
                    "Selected Use Cases": "",
                    "AI Investment ($M) Y1": 0, "AI Investment ($M) Y2": 0, "AI Investment ($M) Y3": 0,
                    "Projected Value Add ($M) Y1": 0, "Projected Value Add ($M) Y2": 0, "Projected Value Add ($M) Y3": 0,
                    "AI Efficiency Score": 0
                }])
                st.session_state.portfolio_companies_df = pd.concat([st.session_state.portfolio_companies_df, new_row], ignore_index=True)
                st.session_state.selected_company_name = new_company_name
                st.success(f"Company '{new_company_name}' added!")
                st.rerun() # Rerun to update the selectbox with the new company
            else:
                st.error("Company name is required or already exists.")

    st.write("")
    st.subheader("Initial Org-AI-R (Organizational AI Readiness) Assessment")
    st.write("Rate the selected company's capabilities across key dimensions (1 = Low Maturity, 5 = High Maturity).")

    #  Org-AI-R Assessment Sliders 
    if st.session_state.selected_company_name:
        current_company_index = st.session_state.portfolio_companies_df[
            st.session_state.portfolio_companies_df["Company Name"] == st.session_state.selected_company_name
        ].index[0]
        
        # Retrieve current scores from session state to pre-fill sliders
        current_data_maturity = st.session_state.portfolio_companies_df.loc[current_company_index, 'Data_Maturity']
        current_tech_infra = st.session_state.portfolio_companies_df.loc[current_company_index, 'Tech_Infra']
        current_talent_capability = st.session_state.portfolio_companies_df.loc[current_company_index, 'Talent_Capability']
        current_strategy_vision = st.session_state.portfolio_companies_df.loc[current_company_index, 'Strategy_Vision']
        current_culture_adaptability = st.session_state.portfolio_companies_df.loc[current_company_index, 'Culture_Adaptability']
        current_regulatory_compliance = st.session_state.portfolio_companies_df.loc[current_company_index, 'Regulatory_Compliance']

        col1, col2 = st.columns(2)
        with col1:
            data_maturity = st.slider("Data Maturity (1-5)", 1, 5, current_data_maturity, key=f"data_maturity_{st.session_state.selected_company_name}")
            tech_infra = st.slider("Technology Infrastructure (1-5)", 1, 5, current_tech_infra, key=f"tech_infra_{st.session_state.selected_company_name}")
            talent_capability = st.slider("Talent & Capabilities (1-5)", 1, 5, current_talent_capability, key=f"talent_capability_{st.session_state.selected_company_name}")
        with col2:
            strategy_vision = st.slider("Strategy & Vision (1-5)", 1, 5, current_strategy_vision, key=f"strategy_vision_{st.session_state.selected_company_name}")
            culture_adaptability = st.slider("Culture & Adaptability (1-5)", 1, 5, current_culture_adaptability, key=f"culture_adaptability_{st.session_state.selected_company_name}")
            regulatory_compliance = st.slider("Regulatory & Compliance (1-5)", 1, 5, current_regulatory_compliance, key=f"regulatory_compliance_{st.session_state.selected_company_name}")

        # Calculate average Org-AI-R score and update DataFrame
        avg_score = (data_maturity + tech_infra + talent_capability + strategy_vision + culture_adaptability + regulatory_compliance) / 6
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Org-AI-R Score'] = avg_score
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Data_Maturity'] = data_maturity
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Tech_Infra'] = tech_infra
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Talent_Capability'] = talent_capability
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Strategy_Vision'] = strategy_vision
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Culture_Adaptability'] = culture_adaptability
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Regulatory_Compliance'] = regulatory_compliance

        st.info(f"Current **Org-AI-R Score** for {st.session_state.selected_company_name}: **{avg_score:.2f}**")
    else:
        st.info("Please select or add a company to perform assessment.")
```

**Widget Breakdown:**
*   `st.selectbox("Select Company", options=company_names, ...)`: Allows selecting an existing company. The `index` parameter ensures the previously selected company remains highlighted. The selected company name is stored in `st.session_state.selected_company_name`.
*   `st.expander("Add New Company")`: Organizes the "Add New Company" form, allowing it to be collapsed to save space.
*   `st.text_input("New Company Name")`, `st.number_input("Revenue ($M)")`: Widgets for inputting new company details.
*   `st.button("Add Company")`: Triggers the logic to add a new company to `st.session_state.portfolio_companies_df` and updates `st.session_state.selected_company_name`.
*   `st.slider("Data Maturity (1-5)", 1, 5, ...)`: Six slider widgets are used for rating the company across different Org-AI-R dimensions (Data Maturity, Tech Infrastructure, etc.). The current scores from `st.session_state.portfolio_companies_df` are used as the default values for these sliders.
*   `st.metric(label, value)`: Displays key metrics like company revenue and the calculated Org-AI-R score.
*   `st.columns(2)`: Used to arrange sliders into two columns for better layout.

**Data Flow:**
1.  **Read:** When the page loads, `st.session_state.portfolio_companies_df` is read to populate the company selection dropdown and to pre-fill the assessment sliders for the `st.session_state.selected_company_name`.
2.  **Write (Add Company):** When a new company is added, a new row is appended to `st.session_state.portfolio_companies_df`.
3.  **Write (Assessment):** As sliders are adjusted, the corresponding dimension scores and the calculated `Org-AI-R Score` for the `st.session_state.selected_company_name` are updated within `st.session_state.portfolio_companies_df`. This data then persists and is accessible to subsequent pages.
4.  `st.rerun()` is used after adding a new company to immediately refresh the `st.selectbox` with the newly added company.

**Mathematical Formula:**
The Org-AI-R Score is a simple average of the six dimension scores:
$$ OrgAI\_R = \frac{\text{Data Maturity} + \text{Tech Infra} + \text{Talent Cap} + \text{Strategy Vision} + \text{Culture Adapt} + \text{Regulatory Comp}}{6} $$

This page provides the foundational data for all subsequent analysis, making robust data handling via `st.session_state.portfolio_companies_df` critical.

## Step 6: Page 2 - Deep Dive: Dimension-Level Assessment & Gap Analysis
Duration: 0:12:00

Following the initial high-level assessment, this page allows for a more detailed "deep dive" into each organizational dimension, identifying specific strengths, weaknesses, and potential gaps.

**File:** `application_pages/page_2_dimension_assessment.py`

**Purpose:**
*   Provide a structured interface for detailed assessment of each AI readiness dimension.
*   Allow PE professionals to add qualitative insights and observations for each dimension.
*   Further refine and document the company's AI readiness profile.
*   Store these detailed insights (scores and text) in `st.session_state`.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_2_dimension_assessment.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis")
    st.write("Perform a detailed assessment across key AI readiness dimensions for the selected company. Add specific insights and identify gaps.")

    if st.session_state.selected_company_name is None:
        st.warning("Please select a company in 'Step 1: Company Selection' to proceed with the detailed assessment.")
        return

    st.info(f"Currently assessing: **{st.session_state.selected_company_name}**")

    company_name = st.session_state.selected_company_name
    current_company_index = st.session_state.portfolio_companies_df[
        st.session_state.portfolio_companies_df["Company Name"] == company_name
    ].index[0]

    # Initialize assessment_scores for the selected company if not already detailed
    # We'll assume page_1 already has basic scores, and this page deepens them.
    # A more robust approach might be to have a nested dict in session_state,
    # or separate DF per company for detailed text. For simplicity, we update main DF here.

    dimension_names = {
        "Data Maturity": 'Data_Maturity',
        "Technology Infrastructure": 'Tech_Infra',
        "Talent & Capabilities": 'Talent_Capability',
        "Strategy & Vision": 'Strategy_Vision',
        "Culture & Adaptability": 'Culture_Adaptability',
        "Regulatory & Compliance": 'Regulatory_Compliance',
    }
    
    # Placeholder for detailed insights (could be a separate dataframe or a column in main DF)
    # For now, let's assume we store insights directly in session_state.assessment_scores
    if 'detailed_assessment_insights' not in st.session_state:
        st.session_state.detailed_assessment_insights = {}
    
    if company_name not in st.session_state.detailed_assessment_insights:
        st.session_state.detailed_assessment_insights[company_name] = {dim: "" for dim in dimension_names.keys()}


    for dimension_display, dimension_column in dimension_names.items():
        with st.expander(f"**{dimension_display}** - Current Score: {st.session_state.portfolio_companies_df.loc[current_company_index, dimension_column]:.0f}/5"):
            st.write(f"Refine the score for **{dimension_display}** and add detailed observations.")
            
            # Use the score from page 1 as initial value
            initial_score = st.session_state.portfolio_companies_df.loc[current_company_index, dimension_column]
            
            # Update score using a slider
            new_score = st.slider(
                f"Score for {dimension_display}", 1, 5, int(initial_score), 
                key=f"score_{company_name}_{dimension_column}"
            )
            
            # Update the score in the main portfolio_companies_df
            st.session_state.portfolio_companies_df.loc[current_company_index, dimension_column] = new_score

            # Add text area for detailed insights
            current_insights = st.session_state.detailed_assessment_insights[company_name].get(dimension_display, "")
            insights = st.text_area(
                f"Detailed Insights & Gap Analysis for {dimension_display}",
                value=current_insights,
                height=150,
                key=f"insights_{company_name}_{dimension_column}"
            )
            st.session_state.detailed_assessment_insights[company_name][dimension_display] = insights

    st.markdown("")
    st.subheader("Summary of Detailed Assessment")
    
    # Display the refined Org-AI-R score
    # Recalculate Org-AI-R based on potentially updated scores from this page
    updated_scores = [st.session_state.portfolio_companies_df.loc[current_company_index, col] for col in dimension_names.values()]
    if len(updated_scores) > 0:
        updated_org_ai_r_score = sum(updated_scores) / len(updated_scores)
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Org-AI-R Score'] = updated_org_ai_r_score
        st.metric(f"Refined Org-AI-R Score for {company_name}", f"{updated_org_ai_r_score:.2f}")

    # Display the collected detailed insights
    with st.expander("View All Detailed Insights"):
        for dimension, insights_text in st.session_state.detailed_assessment_insights[company_name].items():
            st.markdown(f"**{dimension}**: {st.session_state.portfolio_companies_df.loc[current_company_index, dimension_names[dimension]]:.0f}/5")
            st.write(insights_text if insights_text else "_No detailed insights provided._")
            st.divider()

    st.success("Detailed assessment data saved to session state.")

```

**Widget Breakdown:**
*   `st.expander(f"**{dimension_display}** - Current Score: {score}/5")`: Each dimension gets its own expandable section. This helps organize a large amount of input fields and text areas, making the page less cluttered. The current score from `st.session_state.portfolio_companies_df` is shown in the expander title.
*   `st.slider(f"Score for {dimension_display}", 1, 5, initial_score, ...)`: Allows adjusting the numerical score for each dimension. The `initial_score` is pre-filled from the previous page's assessment.
*   `st.text_area(f"Detailed Insights & Gap Analysis for {dimension_display}", ...)`: Provides a multi-line input field for the user to write qualitative observations, strengths, weaknesses, and gap analysis specific to that dimension.
*   `st.metric(label, value)`: Displays the refined overall Org-AI-R score after potential adjustments on this page.

**Data Flow:**
1.  **Read:** The page first reads `st.session_state.selected_company_name` to determine which company to assess. It also retrieves the initial Org-AI-R dimension scores from `st.session_state.portfolio_companies_df` to pre-populate the sliders.
2.  **Write:**
    *   Any adjustments to the dimension `st.slider` widgets directly update the corresponding score columns (`Data_Maturity`, `Tech_Infra`, etc.) in `st.session_state.portfolio_companies_df` for the `selected_company_name`.
    *   The textual insights from `st.text_area` are stored in a nested dictionary `st.session_state.detailed_assessment_insights` keyed by company name and dimension. This allows for rich, detailed notes to be preserved.
    *   The overall `Org-AI-R Score` in `st.session_state.portfolio_companies_df` is recalculated and updated based on the potentially refined scores from this page.

This page enriches the initial assessment with more granular detail and qualitative context, forming a solid basis for identifying specific AI use cases.

## Step 7: Page 3 - Identify High-Value AI Use Cases & Estimate Impact
Duration: 0:18:00

This step moves from assessment to opportunity identification. Here, the user can brainstorm, add, and prioritize potential AI use cases relevant to the selected company, along with estimating their financial impact.

**File:** `application_pages/page_3_use_case_selection.py`

**Purpose:**
*   Facilitate the identification and documentation of potential AI use cases.
*   Enable estimation of the business impact (financial and non-financial) for each use case.
*   Allow for scoring use cases based on complexity, feasibility, and strategic alignment.
*   Select high-priority use cases that will form part of the multi-year AI plan.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_3_use_case_selection.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("Step 3: Identify High-Value AI Use Cases & Estimate Impact")
    st.write("Brainstorm, prioritize, and estimate the financial impact of potential AI use cases for the selected company.")

    if st.session_state.selected_company_name is None:
        st.warning("Please select a company in 'Step 1: Company Selection' to identify AI use cases.")
        return

    company_name = st.session_state.selected_company_name
    st.info(f"Identifying use cases for: **{company_name}**")

    # Initialize use_cases_df if not exists or if switching company
    if 'use_cases_df_by_company' not in st.session_state:
        st.session_state.use_cases_df_by_company = {}

    if company_name not in st.session_state.use_cases_df_by_company:
        st.session_state.use_cases_df_by_company[company_name] = pd.DataFrame(
            columns=[
                "Use Case", "Description", "Business Impact ($M/year)",
                "Complexity", "Feasibility", "Alignment with Strategy", "Selected"
            ]
        )
        # Add some sample use cases if the dataframe is empty for a new company
        if st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df["Company Name"] == company_name].empty:
             # Only add samples if the company is not in the portfolio_companies_df (shouldn't happen)
             pass
        else:
             # Add default sample use cases if it's truly a new company in this step
            if st.session_state.use_cases_df_by_company[company_name].empty:
                sample_use_cases = [
                    {"Use Case": "Predictive Maintenance", "Description": "Forecast equipment failures to reduce downtime.", "Business Impact ($M/year)": 5.0, "Complexity": 3, "Feasibility": 4, "Alignment with Strategy": 4, "Selected": False},
                    {"Use Case": "Automated Customer Support", "Description": "Deploy AI chatbots to handle common customer queries.", "Business Impact ($M/year)": 3.0, "Complexity": 4, "Feasibility": 3, "Alignment with Strategy": 3, "Selected": False},
                    {"Use Case": "Personalized Marketing", "Description": "Use AI to tailor marketing campaigns to individual customer preferences.", "Business Impact ($M/year)": 7.0, "Complexity": 4, "Feasibility": 4, "Alignment with Strategy": 5, "Selected": False}
                ]
                st.session_state.use_cases_df_by_company[company_name] = pd.DataFrame(sample_use_cases)


    current_use_cases_df = st.session_state.use_cases_df_by_company[company_name]

    st.subheader("Add or Edit AI Use Cases")
    st.write("Enter details for potential AI initiatives. Adjust impact and readiness scores.")

    edited_df = st.data_editor(
        current_use_cases_df,
        num_rows="dynamic",
        column_config={
            "Use Case": st.column_config.TextColumn("Use Case", help="Name of the AI use case"),
            "Description": st.column_config.TextColumn("Description", help="Brief description of the use case"),
            "Business Impact ($M/year)": st.column_config.NumberColumn(
                "Business Impact ($M/year)",
                help="Estimated annual value creation (revenue increase or cost reduction)",
                min_value=0.0,
                format="$%0.1f"
            ),
            "Complexity": st.column_config.NumberColumn(
                "Complexity (1-5)",
                help="Ease of implementation (1=low, 5=high)",
                min_value=1, max_value=5, step=1,
                format="%d"
            ),
            "Feasibility": st.column_config.NumberColumn(
                "Feasibility (1-5)",
                help="Likelihood of success (1=low, 5=high)",
                min_value=1, max_value=5, step=1,
                format="%d"
            ),
            "Alignment with Strategy": st.column_config.NumberColumn(
                "Alignment with Strategy (1-5)",
                help="How well it aligns with company's strategic goals (1=low, 5=high)",
                min_value=1, max_value=5, step=1,
                format="%d"
            ),
            "Selected": st.column_config.CheckboxColumn("Selected", help="Select this use case for the multi-year plan", default=False)
        },
        height=300,
        use_container_width=True,
        key=f"use_case_editor_{company_name}"
    )

    if edited_df is not None:
        st.session_state.use_cases_df_by_company[company_name] = edited_df

    st.markdown("")
    st.subheader("Selected High-Value Use Cases")
    selected_use_cases = edited_df[edited_df["Selected"] == True]

    if not selected_use_cases.empty:
        st.dataframe(selected_use_cases[["Use Case", "Business Impact ($M/year)", "Complexity", "Feasibility", "Alignment with Strategy"]], use_container_width=True)
        total_potential_impact = selected_use_cases["Business Impact ($M/year)"].sum()
        st.metric("Total Annual Potential Impact (Selected Use Cases)", f"${total_potential_impact:.1f}M")
        
        # Update selected use cases in portfolio_companies_df
        current_company_index = st.session_state.portfolio_companies_df[
            st.session_state.portfolio_companies_df["Company Name"] == company_name
        ].index[0]
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Selected Use Cases'] = ", ".join(selected_use_cases["Use Case"].tolist())
    else:
        st.info("No AI use cases selected yet. Please select them in the table above.")

    st.success("Use case data saved to session state.")
```

**Widget Breakdown:**
*   `st.data_editor(current_use_cases_df, num_rows="dynamic", column_config={...})`: This is the star of the show for this page. It allows users to:
    *   View, add, delete, and edit rows in a DataFrame directly within the Streamlit app.
    *   `num_rows="dynamic"` enables users to add new rows.
    *   `column_config` is used to define the display and input types for each column:
        *   `st.column_config.TextColumn` for text inputs.
        *   `st.column_config.NumberColumn` for numerical inputs with `min_value`, `max_value`, `step`, and `format` for currency.
        *   `st.column_config.CheckboxColumn` for the "Selected" column, allowing users to easily choose which use cases to include in the plan.
*   `st.metric("Total Annual Potential Impact (Selected Use Cases)", f"${total_potential_impact:.1f}M")`: Displays the summed potential financial impact of all selected use cases.
*   `st.dataframe()`: Shows a read-only table of the selected use cases for review.

**Data Flow:**
1.  **Read:** The page fetches the `selected_company_name` from `st.session_state`. It then checks `st.session_state.use_cases_df_by_company` to load the use cases specific to that company. If no use cases exist for the company, it initializes an empty DataFrame (or populates with sample data).
2.  **Write:**
    *   Any changes made in the `st.data_editor` (adding rows, editing values, checking checkboxes) are immediately reflected and updated in `st.session_state.use_cases_df_by_company[company_name]`.
    *   The list of `Selected Use Cases` is also updated in the `st.session_state.portfolio_companies_df` for the current company. This allows for quick reference on other pages.

This interactive data editing capability makes it very easy for users to manage a list of potential projects, making this page highly functional for strategic planning.

## Step 8: Page 4 - Build the Multi-Year AI Value Creation Plan
Duration: 0:20:00

With the high-value AI use cases identified, this page focuses on constructing a multi-year plan, detailing investment allocation and projected value creation over time.

**File:** `application_pages/page_4_multi_year_plan.py`

**Purpose:**
*   Model the financial aspects of implementing the selected AI use cases.
*   Input multi-year investment figures and projected value add (financial returns).
*   Visualize cumulative investment and value creation over time.
*   Enable scenario planning for AI initiatives.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_4_multi_year_plan.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def main():
    st.subheader("Step 4: Build the Multi-Year AI Value Creation Plan")
    st.write("Outline the multi-year investment strategy and quantify projected value creation from selected AI initiatives.")

    if st.session_state.selected_company_name is None:
        st.warning("Please select a company in 'Step 1: Company Selection' to build a multi-year plan.")
        return

    company_name = st.session_state.selected_company_name
    st.info(f"Building plan for: **{company_name}**")

    # Load selected use cases for context
    selected_use_cases_df = pd.DataFrame()
    if company_name in st.session_state.use_cases_df_by_company:
        selected_use_cases_df = st.session_state.use_cases_df_by_company[company_name]
        selected_use_cases_df = selected_use_cases_df[selected_use_cases_df["Selected"] == True]

    if selected_use_cases_df.empty:
        st.warning("No AI use cases selected yet. Please go to 'Step 3: Identify High-Value AI Use Cases' to select initiatives.")
        return

    st.write(f"**Selected AI Use Cases:** {', '.join(selected_use_cases_df['Use Case'].tolist())}")
    st.write(f"**Total Annual Potential Impact (from Step 3):** ${selected_use_cases_df['Business Impact ($M/year)'].sum():.1f}M")

    # Initialize ai_plan_df for the selected company
    if 'ai_plan_df_by_company' not in st.session_state:
        st.session_state.ai_plan_df_by_company = {}

    if company_name not in st.session_state.ai_plan_df_by_company:
        st.session_state.ai_plan_df_by_company[company_name] = pd.DataFrame(
            columns=[
                "Year", "AI Investment ($M)", "Projected Value Add ($M)", "Cumulative Investment ($M)", "Cumulative Value Add ($M)"
            ]
        )
        for i in range(1, 4): # Default to 3 years
            st.session_state.ai_plan_df_by_company[company_name] = pd.concat([
                st.session_state.ai_plan_df_by_company[company_name],
                pd.DataFrame([{"Year": f"Year {i}", "AI Investment ($M)": 0, "Projected Value Add ($M)": 0, "Cumulative Investment ($M)": 0, "Cumulative Value Add ($M)": 0}])
            ], ignore_index=True)

    current_ai_plan_df = st.session_state.ai_plan_df_by_company[company_name].copy()

    st.subheader("Edit Multi-Year Plan")
    st.write("Enter projected AI investments and expected value creation for each year.")

    # Use st.data_editor for multi-year plan input
    edited_plan_df = st.data_editor(
        current_ai_plan_df[['Year', 'AI Investment ($M)', 'Projected Value Add ($M)']],
        column_config={
            "Year": st.column_config.TextColumn("Year", disabled=True),
            "AI Investment ($M)": st.column_config.NumberColumn(
                "AI Investment ($M)",
                help="Total investment in AI initiatives for this year",
                min_value=0.0,
                format="$%0.1f"
            ),
            "Projected Value Add ($M)": st.column_config.NumberColumn(
                "Projected Value Add ($M)",
                help="Expected financial value generated from AI initiatives for this year",
                min_value=0.0,
                format="$%0.1f"
            ),
        },
        hide_index=True,
        use_container_width=True,
        key=f"ai_plan_editor_{company_name}"
    )

    # Update cumulative values and save to session state
    if edited_plan_df is not None:
        edited_plan_df['Cumulative Investment ($M)'] = edited_plan_df['AI Investment ($M)'].cumsum()
        edited_plan_df['Cumulative Value Add ($M)'] = edited_plan_df['Projected Value Add ($M)'].cumsum()
        st.session_state.ai_plan_df_by_company[company_name] = edited_plan_df

        # Update main portfolio_companies_df with total investment and value add for easy access
        current_company_index = st.session_state.portfolio_companies_df[
            st.session_state.portfolio_companies_df["Company Name"] == company_name
        ].index[0]
        st.session_state.portfolio_companies_df.loc[current_company_index, 'AI Investment ($M) Y1'] = edited_plan_df.loc[0, 'AI Investment ($M)'] if len(edited_plan_df) > 0 else 0
        st.session_state.portfolio_companies_df.loc[current_company_index, 'AI Investment ($M) Y2'] = edited_plan_df.loc[1, 'AI Investment ($M)'] if len(edited_plan_df) > 1 else 0
        st.session_state.portfolio_companies_df.loc[current_company_index, 'AI Investment ($M) Y3'] = edited_plan_df.loc[2, 'AI Investment ($M)'] if len(edited_plan_df) > 2 else 0
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Projected Value Add ($M) Y1'] = edited_plan_df.loc[0, 'Projected Value Add ($M)'] if len(edited_plan_df) > 0 else 0
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Projected Value Add ($M) Y2'] = edited_plan_df.loc[1, 'Projected Value Add ($M)'] if len(edited_plan_df) > 1 else 0
        st.session_state.portfolio_companies_df.loc[current_company_index, 'Projected Value Add ($M) Y3'] = edited_plan_df.loc[2, 'Projected Value Add ($M)'] if len(edited_plan_df) > 2 else 0


    st.markdown("")
    st.subheader("Financial Projections")

    if not edited_plan_df.empty:
        # Cumulative Investment vs. Value Add Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=edited_plan_df["Year"], y=edited_plan_df["Cumulative Investment ($M)"], mode='lines+markers', name='Cumulative AI Investment'))
        fig.add_trace(go.Scatter(x=edited_plan_df["Year"], y=edited_plan_df["Cumulative Value Add ($M)"], mode='lines+markers', name='Cumulative Projected Value Add'))
        fig.update_layout(
            title_text='Cumulative AI Investment vs. Projected Value Add Over Time',
            xaxis_title="Year",
            yaxis_title="Amount ($M)",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Summary Metrics")
        total_investment = edited_plan_df["AI Investment ($M)"].sum()
        total_value_add = edited_plan_df["Projected Value Add ($M)"].sum()
        net_value = total_value_add - total_investment

        col1, col2, col3 = st.columns(3)
        col1.metric("Total AI Investment", f"${total_investment:.1f}M")
        col2.metric("Total Projected Value Add", f"${total_value_add:.1f}M")
        col3.metric("Net Value Creation (Projected)", f"${net_value:.1f}M")
        
        if total_investment > 0:
            roi_ratio = total_value_add / total_investment
            st.metric("Projected ROI Ratio (Value Add / Investment)", f"{roi_ratio:.2f}x")
        else:
            st.info("Enter AI Investment to calculate ROI.")

    st.success("Multi-year plan data saved and updated in session state.")

```

**Widget Breakdown:**
*   `st.data_editor(current_ai_plan_df[['Year', 'AI Investment ($M)', 'Projected Value Add ($M)']], ...)`: Used again to allow interactive editing of the multi-year plan. Users can input annual AI investments and the expected value creation. The `Year` column is `disabled=True` as it's typically fixed.
*   `plotly.graph_objects.Figure()`: The Plotly library is used to create interactive charts. Here, a line chart visualizes the cumulative AI investment against the cumulative projected value add over the planned years. This provides a clear visual representation of the financial trajectory.
*   `st.plotly_chart(fig, use_container_width=True)`: Renders the Plotly chart in the Streamlit app.
*   `st.columns(3)` and `st.metric()`: Display summary financial metrics like total investment, total value add, and net value creation, organized in columns for readability.

**Calculations:**
*   **Cumulative Investment ($M)**: Sum of `AI Investment ($M)` up to the current year.
*   **Cumulative Value Add ($M)**: Sum of `Projected Value Add ($M)` up to the current year.
*   **Net Value Creation ($M)**: `Total Projected Value Add - Total AI Investment`.
*   **Projected ROI Ratio**: `Total Projected Value Add / Total AI Investment`.

**Data Flow:**
1.  **Read:** The page reads `st.session_state.selected_company_name` and the previously selected use cases from `st.session_state.use_cases_df_by_company` for context. It also retrieves the company's specific `ai_plan_df` from `st.session_state.ai_plan_df_by_company`.
2.  **Write:**
    *   Changes in the `st.data_editor` for `AI Investment ($M)` and `Projected Value Add ($M)` are stored in `st.session_state.ai_plan_df_by_company[company_name]`.
    *   The `Cumulative Investment ($M)` and `Cumulative Value Add ($M)` columns are calculated and updated within this DataFrame.
    *   Specific year-wise investment and value-add figures (Y1, Y2, Y3) are also updated in the main `st.session_state.portfolio_companies_df` for easy aggregation and benchmarking in later steps.

This page transforms conceptual use cases into a tangible financial roadmap, providing critical input for investment decisions.

## Step 9: Page 5 - Calculate AI Investment Efficiency & Portfolio Benchmarking
Duration: 0:15:00

This step focuses on evaluating the investment efficiency of the selected company's AI initiatives and benchmarking its performance against other companies in the portfolio.

**File:** `application_pages/page_5_portfolio_benchmarking.py`

**Purpose:**
*   Calculate key metrics to assess the efficiency of AI investments (e.g., ROI, Value Add per $1M invested).
*   Compare the selected company's AI performance against a peer group within the portfolio.
*   Identify high-performing and underperforming assets regarding AI strategy.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_5_portfolio_benchmarking.py
import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.subheader("Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking")
    st.write("Analyze the AI investment efficiency of the selected company and benchmark it against other portfolio assets.")

    if st.session_state.selected_company_name is None:
        st.warning("Please select a company in 'Step 1: Company Selection' to perform benchmarking.")
        return

    company_name = st.session_state.selected_company_name
    st.info(f"Benchmarking: **{company_name}**")

    portfolio_df = st.session_state.portfolio_companies_df.copy()

    # Ensure necessary columns exist and handle potential NaN values for calculations
    for col in ['AI Investment ($M) Y1', 'AI Investment ($M) Y2', 'AI Investment ($M) Y3',
                'Projected Value Add ($M) Y1', 'Projected Value Add ($M) Y2', 'Projected Value Add ($M) Y3']:
        if col not in portfolio_df.columns:
            portfolio_df[col] = 0.0
        portfolio_df[col] = pd.to_numeric(portfolio_df[col], errors='coerce').fillna(0)


    # Calculate aggregated metrics
    portfolio_df['Total AI Investment ($M)'] = portfolio_df[['AI Investment ($M) Y1', 'AI Investment ($M) Y2', 'AI Investment ($M) Y3']].sum(axis=1)
    portfolio_df['Total Projected Value Add ($M)'] = portfolio_df[['Projected Value Add ($M) Y1', 'Projected Value Add ($M) Y2', 'Projected Value Add ($M) Y3']].sum(axis=1)

    # Calculate AI Efficiency Score and other derived metrics
    # Handle division by zero
    portfolio_df['AI ROI Ratio'] = portfolio_df.apply(
        lambda row: row['Total Projected Value Add ($M)'] / row['Total AI Investment ($M)'] if row['Total AI Investment ($M)'] != 0 else 0,
        axis=1
    )
    portfolio_df['Value Add per $M Invested'] = portfolio_df.apply(
        lambda row: row['Total Projected Value Add ($M)'] / row['Total AI Investment ($M)'] if row['Total AI Investment ($M)'] != 0 else 0,
        axis=1
    )
    
    # Simple AI Efficiency Score: Can be a weighted average of ROI and Org-AI-R, for instance.
    # For now, let's use a simpler heuristic for demonstration.
    # Example: (Org-AI-R Score * 0.5) + (AI ROI Ratio * 0.5) - normalize ROI ratio if needed
    # A more complex model could involve industry benchmarks or growth factors.
    max_roi_ratio = portfolio_df['AI ROI Ratio'].max() if not portfolio_df['AI ROI Ratio'].empty and portfolio_df['AI ROI Ratio'].max() > 0 else 1
    portfolio_df['Normalized AI ROI'] = portfolio_df['AI ROI Ratio'] / max_roi_ratio
    portfolio_df['AI Efficiency Score'] = (portfolio_df['Org-AI-R Score'] * 0.5) + (portfolio_df['Normalized AI ROI'] * 0.5 * 5) # Scale normalized ROI back to 0-5 range approximately


    # Update the AI Efficiency Score in the main session_state.portfolio_companies_df
    st.session_state.portfolio_companies_df['AI Efficiency Score'] = portfolio_df['AI Efficiency Score']
    
    current_company_data = portfolio_df[portfolio_df["Company Name"] == company_name].iloc[0]

    st.subheader("Selected Company's AI Investment Efficiency")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total AI Investment", f"${current_company_data['Total AI Investment ($M)']:.1f}M")
    col2.metric("Total Projected Value Add", f"${current_company_data['Total Projected Value Add ($M)']:.1f}M")
    col3.metric("AI ROI Ratio", f"{current_company_data['AI ROI Ratio']:.2f}x")
    col4.metric("AI Efficiency Score", f"{current_company_data['AI Efficiency Score']:.2f}/5")

    st.markdown("")
    st.subheader("Portfolio Benchmarking")

    # Benchmarking table
    st.write("Compare the selected company against others in the portfolio:")
    display_cols = [
        "Company Name", "Industry", "Revenue ($M)", "EBITDA ($M)",
        "Org-AI-R Score", "Total AI Investment ($M)", "Total Projected Value Add ($M)",
        "AI ROI Ratio", "AI Efficiency Score"
    ]
    st.dataframe(portfolio_df[display_cols].sort_values(by="AI Efficiency Score", ascending=False), use_container_width=True)

    # Benchmarking charts
    st.write("### Visual Benchmarking")

    # Bar chart for AI Efficiency Score
    fig_efficiency = px.bar(
        portfolio_df.sort_values(by="AI Efficiency Score", ascending=False),
        x="Company Name",
        y="AI Efficiency Score",
        color="Company Name",
        title="AI Efficiency Score Across Portfolio Companies",
        labels={"AI Efficiency Score": "Score (0-5)"}
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)

    # Scatter plot: Org-AI-R vs. AI ROI Ratio
    fig_scatter = px.scatter(
        portfolio_df,
        x="Org-AI-R Score",
        y="AI ROI Ratio",
        size="Total AI Investment ($M)",
        color="Company Name",
        hover_name="Company Name",
        title="Org-AI-R Score vs. AI ROI Ratio (Size: Total Investment)",
        labels={"Org-AI-R Score": "Organizational AI Readiness Score", "AI ROI Ratio": "AI ROI Ratio (X)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.success("Benchmarking complete. Data is ready for executive review.")
```

**Widget Breakdown:**
*   `st.columns(4)` and `st.metric()`: Display key efficiency metrics for the `selected_company_name`, providing a quick overview.
*   `st.dataframe()`: Shows a comparison table of all portfolio companies, highlighting important metrics like `Org-AI-R Score`, `Total AI Investment`, `Total Projected Value Add`, `AI ROI Ratio`, and the calculated `AI Efficiency Score`. The table is sorted by `AI Efficiency Score` to easily identify leaders and laggards.
*   `plotly.express.bar()`: Generates a bar chart visualizing the `AI Efficiency Score` for each company in the portfolio, allowing for easy visual comparison.
*   `plotly.express.scatter()`: Creates a scatter plot comparing `Org-AI-R Score` against `AI ROI Ratio`, with the size of the markers representing `Total AI Investment`. This helps identify correlations and outliers (e.g., companies with high readiness but low ROI, or vice-versa).
*   `st.plotly_chart()`: Renders the generated Plotly charts.

**Calculations:**
1.  **Total AI Investment ($M)$**: Sum of `AI Investment ($M) Y1`, `Y2`, `Y3`.
2.  **Total Projected Value Add ($M)$**: Sum of `Projected Value Add ($M) Y1`, `Y2`, `Y3`.
3.  **AI ROI Ratio**:
    $$ \text{AI ROI Ratio} = \frac{\text{Total Projected Value Add}}{\text{Total AI Investment}} $$
    *   (Includes handling for division by zero).
4.  **Value Add per $M Invested**: Same as AI ROI Ratio in this simple implementation, but could be distinct if `Value Add per $M Invested` meant something like `(Total Projected Value Add / Total AI Investment) * 1,000,000`.
5.  **AI Efficiency Score**: A composite score reflecting overall AI performance. In this example, it's a weighted average of `Org-AI-R Score` and a normalized `AI ROI Ratio`.
    $$ \text{AI Efficiency Score} = (\text{Org-AI-R Score} \times 0.5) + (\text{Normalized AI ROI} \times 0.5 \times 5) $$
    where `Normalized AI ROI` scales the ROI ratio from 0 to 1 based on the maximum ROI in the portfolio.

**Data Flow:**
1.  **Read:** This page primarily reads the entire `st.session_state.portfolio_companies_df`, which contains all the aggregated data from previous steps (Org-AI-R scores, annual investments, and value add).
2.  **Process:** It then calculates `Total AI Investment ($M)`, `Total Projected Value Add ($M)`, `AI ROI Ratio`, and `AI Efficiency Score` for all companies.
3.  **Write:** The calculated `AI Efficiency Score` is updated back into `st.session_state.portfolio_companies_df` so it persists across sessions and can be used for final exit readiness.

This page provides quantitative insights crucial for a Portfolio Manager to evaluate and compare the performance of AI initiatives across their portfolio.

## Step 10: Page 6 - Exit-Readiness Assessment
Duration: 0:10:00

The final step consolidates all the information gathered throughout the application to perform an exit-readiness assessment, projecting how AI initiatives impact a company's potential valuation and attractiveness to buyers.

**File:** `application_pages/page_6_exit_readiness.py`

**Purpose:**
*   Summarize the impact of AI investments on key valuation drivers.
*   Estimate the potential uplift in company valuation due to AI.
*   Identify key strengths and areas for improvement for a successful exit.
*   Provide a final, data-driven assessment of the company's AI-driven exit potential.

**Key Functionalities and Streamlit Widgets:**

```python
# application_pages/page_6_exit_readiness.py
import streamlit as st
import pandas as pd

def main():
    st.subheader("Step 6: Exit-Readiness Assessment")
    st.write("Consolidate all AI-driven insights to assess the selected company's exit readiness and potential valuation uplift.")

    if st.session_state.selected_company_name is None:
        st.warning("Please select a company in 'Step 1: Company Selection' to perform the exit-readiness assessment.")
        return

    company_name = st.session_state.selected_company_name
    st.info(f"Assessing exit readiness for: **{company_name}**")

    # Get data for the selected company
    portfolio_df = st.session_state.portfolio_companies_df.copy()
    current_company_data = portfolio_df[portfolio_df["Company Name"] == company_name].iloc[0]

    st.markdown("")
    st.subheader("AI's Impact on Company Valuation")

    #  Valuation Uplift Calculation 
    # Assumptions for illustrative purposes:
    # 1. AI-driven value add directly translates to EBITDA increase.
    # 2. An improved Org-AI-R Score or AI Efficiency Score can lead to a multiple expansion.
    
    # Financial Impact from AI Value Add (EBITDA growth)
    total_projected_value_add = current_company_data.get('Total Projected Value Add ($M)', 0) # from Page 5
    initial_ebitda = current_company_data.get('EBITDA ($M)', 0)

    ai_driven_ebitda_increase = total_projected_value_add # Assume direct increase for simplicity

    # Multiple Expansion Factor based on AI Readiness
    # Higher Org-AI-R or AI Efficiency Score leads to higher multiplier
    ai_efficiency_score = current_company_data.get('AI Efficiency Score', 0)
    
    # Simple heuristic: for every point in AI Efficiency Score (out of 5), add 0.1 to multiple, capped.
    # Base multiple could be industry average or current. Let's assume a current/industry average of 8.0x
    base_multiple = 8.0
    multiple_uplift_per_point = 0.15 # e.g., 0.15x per point of AI Efficiency Score
    max_multiple_increase = 1.5 # e.g., max additional 1.5x multiple
    
    # Cap the uplift
    potential_multiple_increase = min(ai_efficiency_score * multiple_uplift_per_point, max_multiple_increase)
    improved_multiple = base_multiple + potential_multiple_increase

    # Calculate valuation uplift
    current_valuation_estimate = initial_ebitda * base_multiple
    ai_enhanced_ebitda = initial_ebitda + ai_driven_ebitda_increase
    ai_enhanced_valuation_estimate = ai_enhanced_ebitda * improved_multiple

    ai_driven_valuation_uplift = ai_enhanced_valuation_estimate - current_valuation_estimate
    
    # Store these in session state for potential summary if needed
    st.session_state.exit_readiness_data = {
        "AI-Driven Valuation Uplift ($M)": ai_driven_valuation_uplift,
        "Improved Multiple (x)": improved_multiple,
        "Total Exit Value Impact ($M)": ai_enhanced_valuation_estimate,
        "Key Strengths": [], # Populated below
        "Areas for Improvement": [] # Populated below
    }

    col1, col2, col3 = st.columns(3)
    col1.metric("Current Valuation (Est.)", f"${current_valuation_estimate:.1f}M")
    col2.metric("AI-Enhanced Valuation (Est.)", f"${ai_enhanced_valuation_estimate:.1f}M")
    col3.metric("AI-Driven Valuation Uplift", f"${ai_driven_valuation_uplift:.1f}M", delta=f"${ai_driven_valuation_uplift:.1f}M")
    
    st.markdown(f"*(Based on initial EBITDA of ${initial_ebitda:.1f}M, a base multiple of {base_multiple:.1f}x, an AI-driven EBITDA increase of ${ai_driven_ebitda_increase:.1f}M, and an improved multiple of {improved_multiple:.1f}x due to AI readiness.)*")

    st.markdown("")
    st.subheader("Key Strengths for Exit")
    st.write("Highlight the company's strong points driven by AI initiatives.")
    
    # Dynamically generate strengths based on scores and use cases
    strengths = []
    if current_company_data.get('Org-AI-R Score', 0) >= 3.5:
        strengths.append(f"High Org-AI-R Score ({current_company_data['Org-AI-R Score']:.1f}), indicating strong foundational capabilities for AI adoption.")
    if current_company_data.get('AI Efficiency Score', 0) >= 3.0:
        strengths.append(f"Strong AI Investment Efficiency Score ({current_company_data['AI Efficiency Score']:.1f}), demonstrating effective value creation from AI.")
    if current_company_data.get('Selected Use Cases', ''):
        strengths.append(f"Implemented/Planned high-value AI use cases: {current_company_data['Selected Use Cases']}.")
    if current_company_data.get('Total Projected Value Add ($M)', 0) > 0:
        strengths.append(f"Projected total AI-driven value add of ${current_company_data['Total Projected Value Add ($M)']:.1f}M over the plan period.")
    
    if strengths:
        for s in strengths:
            st.success(f"✓ {s}")
    else:
        st.info("No major AI-driven strengths identified yet. Consider refining previous steps.")

    st.markdown("")
    st.subheader("Areas for Improvement")
    st.write("Identify areas to focus on to further enhance exit value through AI.")
    
    areas_for_improvement = []
    if current_company_data.get('Org-AI-R Score', 0) < 3.5:
        areas_for_improvement.append(f"Org-AI-R Score ({current_company_data['Org-AI-R Score']:.1f}) is moderate. Focus on strengthening foundational AI capabilities like Data Maturity and Tech Infrastructure (refer to Step 2).")
    if current_company_data.get('AI Efficiency Score', 0) < 3.0:
        areas_for_improvement.append(f"AI Investment Efficiency Score ({current_company_data['AI Efficiency Score']:.1f}) could be improved. Review use case selection and investment/value projections in Steps 3 & 4.")
    if current_company_data.get('Total AI Investment ($M)', 0) == 0:
        areas_for_improvement.append("No AI investment planned. Develop a clear AI investment roadmap to unlock future value.")

    # Check individual dimension scores from portfolio_df if they are low
    dimensions = ["Data_Maturity", "Tech_Infra", "Talent_Capability", "Strategy_Vision", "Culture_Adaptability", "Regulatory_Compliance"]
    for dim in dimensions:
        if current_company_data.get(dim, 0) < 3:
            areas_for_improvement.append(f"Low score in {dim.replace('_', ' ')} ({current_company_data[dim]:.0f}). This is a key area for targeted investment and improvement.")

    if areas_for_improvement:
        for a in areas_for_improvement:
            st.warning(f"⚠️ {a}")
    else:
        st.success("The company shows strong AI readiness and value creation for exit.")

    st.markdown("")
    st.info("This Exit-Readiness Assessment provides a strategic overview. Detailed financial modeling should be performed by an expert.")

```

**Widget Breakdown:**
*   `st.columns(3)` and `st.metric()`: Display the calculated current valuation estimate, AI-enhanced valuation estimate, and the `AI-Driven Valuation Uplift`. The `delta` argument in `st.metric` highlights the positive change.
*   `st.success()` and `st.warning()`: Used to dynamically highlight `Key Strengths` and `Areas for Improvement`. These info boxes provide actionable insights based on the aggregated data.
*   `st.markdown()`: Used for general text and section headers.

**Calculations & Logic (Illustrative):**
This page relies on simplified financial modeling assumptions for demonstration purposes. In a real-world scenario, these would be more complex and validated by financial experts.

1.  **AI-driven EBITDA Increase**: Directly uses `Total Projected Value Add ($M)` from Page 5 as an increase in EBITDA.
2.  **Multiple Expansion Factor**: Assumes that a higher `AI Efficiency Score` (from Page 5) leads to an expansion in the company's valuation multiple.
    *   `Improved Multiple (x)` = `Base Multiple` + (`AI Efficiency Score` $\times$ `Multiple Uplift per Point`) (with a cap).
3.  **Current Valuation (Estimate)**:
    $$ \text{Current Valuation} = \text{Initial EBITDA} \times \text{Base Multiple} $$
4.  **AI-Enhanced Valuation (Estimate)**:
    $$ \text{AI-Enhanced Valuation} = (\text{Initial EBITDA} + \text{AI-driven EBITDA Increase}) \times \text{Improved Multiple} $$
5.  **AI-Driven Valuation Uplift**:
    $$ \text{AI-Driven Valuation Uplift} = \text{AI-Enhanced Valuation} - \text{Current Valuation} $$

**Dynamic Strengths/Improvements:**
The `Key Strengths` and `Areas for Improvement` sections are dynamically generated based on thresholds for `Org-AI-R Score`, `AI Efficiency Score`, and whether use cases or investments are planned. This provides tailored feedback to the user.

**Data Flow:**
1.  **Read:** This page reads all relevant aggregated data directly from `st.session_state.portfolio_companies_df`, including `EBITDA ($M)`, `Org-AI-R Score`, `AI Efficiency Score`, `Total Projected Value Add ($M)`, and `Selected Use Cases`.
2.  **Process:** It performs the valuation uplift calculations and generates the dynamic strengths and improvement points based on the retrieved data.
3.  **Write:** The `exit_readiness_data` (valuation uplift, improved multiple, etc.) is stored in `st.session_state.exit_readiness_data` for completeness, though it's primarily a summary page.

This page brings the entire workflow to a conclusion, providing a critical assessment from the perspective of a Private Equity investor looking towards a profitable exit.

## Step 11: Conclusion and Next Steps
Duration: 0:03:00

Congratulations! You have successfully navigated through the **AI Value Creation & Investment Efficiency Planner** codelab. You've gained an in-depth understanding of how a Streamlit application can be structured to support complex business workflows, from data input and assessment to strategic planning and financial projection.

**What You've Learned:**
*   **Modular Streamlit Development:** How to break down a large application into manageable, reusable components (`app.py`, `utils.py`, `application_pages/`).
*   **Effective Session State Management:** The importance and implementation of `st.session_state` for persisting data across multiple user interactions and application pages.
*   **Interactive Data Handling:** Utilizing `st.data_editor` for dynamic table input and `st.slider`, `st.text_input`, `st.selectbox` for various data collection needs.
*   **Data Visualization:** Employing `plotly.express` and `plotly.graph_objects` to create informative and interactive charts.
*   **Strategic Application Design:** How to translate a multi-step business process (like PE portfolio management) into a user-friendly, data-driven application.
*   **Financial Modeling Integration:** Basic principles of integrating financial calculations and assumptions within a Streamlit app.

**Further Enhancements:**
This application serves as a robust foundation. Here are some ideas for future enhancements:
*   **User Authentication:** Implement login functionality for secure access.
*   **Data Persistence:** Integrate with a backend database (e.g., PostgreSQL, Google Cloud SQL) to save `st.session_state.portfolio_companies_df` and other data beyond the current session.
*   **More Sophisticated Financial Models:** Incorporate advanced valuation techniques (e.g., DCF, Sensitivity Analysis) and customizable assumptions.
*   **Industry Benchmarks:** Allow users to upload or select industry-specific benchmarks for more accurate comparisons.
*   **PDF Report Generation:** Add functionality to export a comprehensive report of the assessment and plan.
*   **Machine Learning Integration:** Potentially integrate ML models for more accurate impact estimations or risk assessments of AI initiatives.
*   **Interactive Dashboards:** Create more complex and customizable dashboards using `streamlit_elements` or similar libraries for enhanced data exploration.

<aside class="positive">
  The power of Streamlit lies in its simplicity and Python-native approach. It allows developers to quickly build and iterate on data applications, bringing complex analytical tools to business users without extensive web development expertise.
</aside>

We encourage you to experiment with the code, modify the calculations, and explore new Streamlit features. Happy coding!
