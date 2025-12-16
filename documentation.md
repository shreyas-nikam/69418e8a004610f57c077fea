id: 69418e8a004610f57c077fea_documentation
summary: AI Value Creation & Investment Efficiency Planner Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI Value Creation & Investment Efficiency Planner Codelab

## 1. Introduction: Unlocking Value with AI in Private Equity
Duration: 00:05:00

Welcome to the **AI Value Creation & Investment Efficiency Planner** codelab! In today's competitive landscape, Artificial Intelligence (AI) is not just a technological advantage but a strategic imperative, especially within the Private Equity (PE) sector. This Streamlit application serves as a powerful, structured tool for **Private Equity Portfolio Managers** to systematically identify, assess, quantify, and benchmark AI opportunities across their portfolio companies.

The primary goal of this application is to guide developers through building and understanding a sophisticated analytical tool that helps PE firms:
*   **Strategically leverage AI:** Identify where AI can drive the most significant growth and operational improvements.
*   **Quantify financial impact:** Project the Return on Investment (ROI) of AI initiatives, specifically in terms of EBITDA uplift and organizational AI readiness (Org-AI-R).
*   **Enhance exit valuations:** Build a compelling narrative around AI investments to justify higher exit multiples.
*   **Improve investment efficiency:** Compare and contrast AI performance and investments across a diverse portfolio.

This codelab will provide a comprehensive guide, walking you through the application's architecture, core functionalities, and how to extend it. By the end, you'll have a clear understanding of how this tool empowers strategic decision-making in AI investments.

<aside class="positive">
<b>Key Concepts Explained:</b>
<ul>
    <li><b>Session State Management:</b> How Streamlit's <code>st.session_state</code> is used to maintain application state across user interactions and page navigations.</li>
    <li><b>Dynamic Page Loading:</b> A modular approach to building multi-page Streamlit applications by dynamically importing and executing page-specific logic.</li>
    <li><b>Modular Design:</b> Structuring a complex application into reusable components and functions.</li>
    <li><b>Interactive Data Analysis:</b> Leveraging Streamlit widgets to create an engaging and intuitive user experience for complex analytical workflows.</li>
</ul>
</aside>

### Application Workflow Overview

The application follows a logical, step-by-step process, mirroring a typical PE due diligence and value creation lifecycle:

1.  **Company Selection:** Identify a specific portfolio company for AI assessment.
2.  **AI Capability Assessment:** Evaluate the company's current AI maturity and identify gaps.
3.  **Strategic AI Initiative Selection:** Choose specific AI projects aligned with value creation.
4.  **Financial Impact Quantification:** Model the projected EBITDA and Org-AI-R improvements.
5.  **Portfolio Benchmarking:** Compare the selected company's AI performance against others in the portfolio.
6.  **Exit Narrative & Valuation:** Craft a story around AI investments to maximize exit value.

### High-Level Architecture

The application adopts a modular architecture, separating the core application logic from individual page implementations and shared functionalities. This enhances maintainability and scalability.

```mermaid
graph TD
    A[User Interaction] --> B[Streamlit UI]
    B --> C[app.py (Main Application)]
    C -- Manages Session State --> D[st.session_state]
    C -- Sets Page Config, Sidebar, Overall Layout --> B
    C -- Uses pages_config to Map Labels to Modules --> E[application_pages.shared_functions.py]
    C -- Dynamically Imports & Executes `main()` from --> F[application_pages.<page_module_name>.py]
    F -- Updates/Reads from --> D
    F -- Uses Helper Functions from --> E

    E -- Contains --> G[initialize_session_state()]
    E -- Contains --> H[go_to_page()]
    E -- Contains --> I[pages_config (Dictionary)]

    subgraph application_pages/
        F1[page_1_company_selection.py]
        F2[page_2_ai_capability_assessment.py]
        F3[...]
        F -- Represents any of --> F1 & F2 & F3
    end
```
**Figure 1: High-Level Application Architecture**

## 2. Setting Up the Development Environment
Duration: 00:05:00

Before diving into the code, let's set up your local development environment.

### Prerequisites

*   **Python 3.8+**: Ensure you have a compatible Python version installed.
*   **Git**: For cloning the repository (if applicable).

### Getting the Code

Assuming the provided code snippets are part of a larger project, you would typically clone a repository or create the file structure manually.

1.  **Create the main application file:** Save the main Streamlit code as `app.py`.
2.  **Create the `application_pages` directory:**
    ```bash
    mkdir application_pages
    cd application_pages
    touch __init__.py # This makes it a Python package
    ```
3.  **Create `shared_functions.py` inside `application_pages`:**
    You'll need to populate this file with the functions mentioned in `app.py`. A basic `shared_functions.py` would look like this:

    ```python
    # application_pages/shared_functions.py
    import streamlit as st
    import pandas as pd
    import numpy as np

    # Define the mapping of human-readable page labels to their Python module names
    pages_config = {
        "Company Selection": "page_1_company_selection",
        "AI Capability Assessment": "page_2_ai_capability_assessment",
        "Strategic AI Initiative Selection": "page_3_ai_initiative_selection",
        "Financial Impact Quantification": "page_4_financial_impact",
        "Portfolio Benchmarking": "page_5_portfolio_benchmarking",
        "Exit Narrative & Valuation": "page_6_exit_valuation",
    }

    def initialize_session_state():
        """
        Initializes all necessary session state variables for the application.
        This function is called at the very start of the app or when a session is restarted.
        """
        # Ensure 'current_page' is set to the first page by default
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = list(pages_config.keys())[0]

        # General company data (example: can be loaded from a CSV/DB)
        if 'companies_df' not in st.session_state:
            st.session_state['companies_df'] = pd.DataFrame({
                'CompanyID': ['C001', 'C002', 'C003', 'C004'],
                'CompanyName': ['Tech Innovators Inc.', 'Global Logistics Co.', 'FinServe Solutions', 'HealthTech Innovations'],
                'Sector': ['Technology', 'Logistics', 'Finance', 'Healthcare'],
                'CurrentEBITDA_M': [100.0, 75.0, 120.0, 90.0],
                'Org-AI-R_Score': [3.5, 2.8, 4.1, 3.2], # Organizational AI Readiness Score (1-5)
                'AI_Maturity_Level': ['Advanced', 'Intermediate', 'Expert', 'Intermediate']
            })

        if 'selected_company_id' not in st.session_state:
            st.session_state['selected_company_id'] = st.session_state['companies_df']['CompanyID'].iloc[0]

        if 'selected_company_name' not in st.session_state:
            st.session_state['selected_company_name'] = st.session_state['companies_df']['CompanyName'].iloc[0]

        # Variables for AI Capability Assessment (example initial values)
        if 'ai_capabilities_scores' not in st.session_state:
            st.session_state['ai_capabilities_scores'] = {
                'Data Infrastructure': 3, 'ML Ops': 2, 'Talent Pool': 3,
                'Ethical AI Governance': 4, 'Strategic Alignment': 3
            } # Scores 1-5

        # Variables for AI Initiative Selection
        if 'selected_initiatives' not in st.session_state:
            st.session_state['selected_initiatives'] = []
        if 'initiative_details' not in st.session_state:
            st.session_state['initiative_details'] = {
                'Automated Customer Support': {'cost': 1.5, 'ebitda_impact': 5.0, 'org_ai_r_boost': 0.3},
                'Predictive Maintenance': {'cost': 2.0, 'ebitda_impact': 7.5, 'org_ai_r_boost': 0.4},
                'Personalized Marketing Engine': {'cost': 1.8, 'ebitda_impact': 6.0, 'org_ai_r_boost': 0.35},
                'Fraud Detection System': {'cost': 2.5, 'ebitda_impact': 8.0, 'org_ai_r_boost': 0.5},
            }

        # Variables for Financial Impact Quantification
        if 'projection_years' not in st.session_state:
            st.session_state['projection_years'] = list(range(1, 6)) # 5 years projection
        if 'ai_investment_cost' not in st.session_state:
            st.session_state['ai_investment_cost'] = 0.0 # Total initial cost from initiatives
        if 'projected_ebitda_uplift' not in st.session_state:
            st.session_state['projected_ebitda_uplift'] = [0.0] * len(st.session_state['projection_years'])
        if 'projected_org_ai_r_growth' not in st.session_state:
            st.session_state['projected_org_ai_r_growth'] = [0.0] * len(st.session_state['projection_years'])


        # Variables for Portfolio Benchmarking
        # This will be dynamically generated or loaded in page_5 based on company data

        # Variables for Exit Narrative
        if 'exit_multiple_impact' not in st.session_state:
            st.session_state['exit_multiple_impact'] = 0.0 # % increase
        if 'exit_narrative_points' not in st.session_state:
            st.session_state['exit_narrative_points'] = []

    def go_to_page(page_label):
        """
        Updates the current page in session state and triggers a rerun.
        Also sets query parameters for direct page linking (optional, but good practice).
        """
        if page_label in pages_config:
            st.session_state['current_page'] = page_label
            # st.experimental_set_query_params(page=pages_config[page_label]) # Disabled for simplicity in this codelab's context
            st.rerun() # Reruns the entire application to load the new page

    ```
4.  **Create placeholder page files (e.g., `page_1_company_selection.py`, `page_2_ai_capability_assessment.py`, etc.)**
    For instance, `application_pages/page_1_company_selection.py` would look like:
    ```python
    # application_pages/page_1_company_selection.py
    import streamlit as st
    from application_pages.shared_functions import go_to_page, pages_config

    def main():
        st.subheader("1. Company Selection")
        st.markdown("Select a portfolio company to analyze its AI value creation potential.")

        companies_df = st.session_state['companies_df']
        company_names = companies_df['CompanyName'].tolist()

        # Find the index of the currently selected company for the selectbox
        current_selection_index = 0
        if 'selected_company_name' in st.session_state and st.session_state['selected_company_name'] in company_names:
            current_selection_index = company_names.index(st.session_state['selected_company_name'])

        selected_company_name = st.selectbox(
            "Choose a Company from your Portfolio",
            options=company_names,
            index=current_selection_index,
            key='company_selection_selectbox'
        )

        # Update session state if a different company is selected
        if selected_company_name != st.session_state.get('selected_company_name'):
            st.session_state['selected_company_name'] = selected_company_name
            selected_company_row = companies_df[companies_df['CompanyName'] == selected_company_name].iloc[0]
            st.session_state['selected_company_id'] = selected_company_row['CompanyID']
            st.session_state['selected_company_data'] = selected_company_row.to_dict() # Store full row data

        st.markdown(f"**Selected Company:** {st.session_state['selected_company_name']}")
        st.dataframe(
            companies_df[companies_df['CompanyName'] == st.session_state['selected_company_name']],
            hide_index=True
        )

        # Add a "Continue" button to move to the next page
        next_page_label = "AI Capability Assessment"
        if st.button(f"Continue to {next_page_label}"):
            go_to_page(next_page_label)

    ```
    You would need to create similar `main()` functions for `page_2_ai_capability_assessment.py` through `page_6_exit_valuation.py`. For the purpose of this codelab, their content can be minimal, e.g.:
    ```python
    # application_pages/page_2_ai_capability_assessment.py
    import streamlit as st
    from application_pages.shared_functions import go_to_page, pages_config

    def main():
        st.subheader("2. AI Capability Assessment")
        st.markdown(f"Assessing AI capabilities for **{st.session_state.get('selected_company_name', 'N/A')}**.")
        st.write("This page would contain sliders/inputs for assessing various AI capabilities.")
        # Example: display current scores
        st.json(st.session_state.get('ai_capabilities_scores', {}))

        next_page_label = "Strategic AI Initiative Selection"
        if st.button(f"Continue to {next_page_label}"):
            go_to_page(next_page_label)
    ```

### Installation

Navigate to your project's root directory (where `app.py` is located) and install Streamlit:

```bash
pip install streamlit pandas numpy
```

### Running the Application

Once everything is set up, run the Streamlit application from your terminal:

```bash
streamlit run app.py
```

This command will open the application in your default web browser.

## 3. Understanding the Core Application Structure (`app.py`)
Duration: 00:15:00

The `app.py` file is the entry point of our Streamlit application. It handles global configuration, sidebar navigation, session state management, and the dynamic loading of individual page modules.

```python
import streamlit as st
import pandas as pd
import numpy as np

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

#  Sidebar 
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
current_page_index = page_labels.index(st.session_state['current_page']) if st.session_state['current_page'] in page_labels else 0

selected_page_label = st.sidebar.selectbox(
    label="Navigation",
    options=page_labels,
    index=current_page_index,
    key='sidebar_navigation_select'
)

# Update session state and query params if sidebar selection changes
if selected_page_label != st.session_state['current_page']:
    go_to_page(selected_page_label)

# Display current step progress
step_index = page_labels.index(st.session_state['current_page']) + 1
total_steps = len(page_labels)
st.sidebar.markdown(f"**Step {step_index} of {total_steps}: {st.session_state['current_page']}**")
st.sidebar.divider()

#  Main Content Area 
st.title("QuLab: AI Value Creation & Investment Efficiency Planner")
st.divider()

st.markdown("""
# ... (rest of markdown content for the main overview) ...
""")

st.markdown("")

# Load and run the selected page's main function
page_module_name = pages_config[st.session_state['current_page']]
try:
    module = __import__(f"application_pages.{page_module_name}", fromlist=["main"])
    module.main()
except ImportError:
    st.error(f"Could not load page: '{st.session_state['current_page']}'. This might happen if page files are missing or the 'application_pages' directory is not a valid Python package.")
    st.info("Please ensure all page files (e.g., `application_pages/page_1_company_selection.py`) are created and the `application_pages` directory contains an `__init__.py` file.")
except Exception as e:
    st.error(f"An unexpected error occurred on page '{st.session_state['current_page']}': {e}")
    st.exception(e)
```

### Core Components Explained

1.  **`st.set_page_config`**:
    This function is called once at the very beginning of the script to configure the Streamlit page settings.
    *   `page_title`: Sets the title that appears in the browser tab.
    *   `layout="wide"`: Makes the main content area occupy the full width of the browser window, which is ideal for data-intensive applications.

2.  **Session State Initialization**:
    ```python
    if 'session_initialized' not in st.session_state or not st.session_state['session_initialized']:
        initialize_session_state()
        st.session_state['session_initialized'] = True
    ```
    This block is critical for maintaining application state. Streamlit reruns the entire script from top to bottom whenever there's an interaction. Without proper session state management, all variables would reset.
    *   `st.session_state`: A dictionary-like object that persists data across reruns.
    *   `initialize_session_state()`: A custom function (defined in `shared_functions.py`) that populates `st.session_state` with default values for all necessary variables (e.g., selected company, AI scores, financial projections). This ensures the application has a consistent starting point.
    *   The `'session_initialized'` flag prevents `initialize_session_state()` from running on every rerun, ensuring that user inputs are not overwritten.

3.  **Sidebar (`st.sidebar`)**:
    The sidebar hosts global navigation and control elements.
    *   `st.sidebar.image`, `st.sidebar.title`, `st.sidebar.divider()`: Standard Streamlit widgets for layout and branding.
    *   **Restart Session Button**:
        ```python
        if st.sidebar.button("Restart Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state['session_initialized'] = False
            st.rerun()
        ```
        This button allows users to reset the application to its initial state. It iterates through `st.session_state` and `del`etes all keys, effectively clearing all user inputs and selections. Setting `st.session_state['session_initialized'] = False` ensures that `initialize_session_state()` runs again on the subsequent `st.rerun()`.
    *   **Navigation Dropdown (`st.sidebar.selectbox`)**:
        ```python
        page_labels = list(pages_config.keys())
        selected_page_label = st.sidebar.selectbox(
            label="Navigation",
            options=page_labels,
            index=current_page_index,
            key='sidebar_navigation_select'
        )
        if selected_page_label != st.session_state['current_page']:
            go_to_page(selected_page_label)
        ```
        This dropdown allows users to navigate between the different analytical steps.
        *   `pages_config`: A dictionary (from `shared_functions.py`) mapping user-friendly page names to their corresponding module filenames.
        *   `current_page_index`: Determines the initially selected item in the `selectbox`.
        *   `go_to_page(selected_page_label)`: A helper function (from `shared_functions.py`) that updates `st.session_state['current_page']` and triggers a `st.rerun()`, which is crucial for loading the new page content.
    *   **Progress Display**: `st.sidebar.markdown(f"**Step {step_index} of {total_steps}: {st.session_state['current_page']}**")` provides visual feedback on the user's progress through the workflow.

4.  **Main Content Area - Dynamic Page Loading**:
    ```python
    page_module_name = pages_config[st.session_state['current_page']]
    try:
        module = __import__(f"application_pages.{page_module_name}", fromlist=["main"])
        module.main()
    except ImportError:
        # ... error handling ...
    except Exception as e:
        # ... error handling ...
    ```
    This is the core mechanism for rendering the active page.
    *   It retrieves the Python module name associated with the `current_page` from `pages_config`.
    *   `__import__(f"application_pages.{page_module_name}", fromlist=["main"])`: This Python built-in function dynamically imports the specified module. `fromlist=["main"]` ensures that the `main` function (which each page module is expected to have) is directly accessible.
    *   `module.main()`: After importing, it calls the `main()` function within that module. Each page's Streamlit components and logic are encapsulated within its `main()` function. This modular approach keeps `app.py` clean and separates concerns.
    *   Error Handling: Includes `try-except` blocks to gracefully handle cases where a page module might be missing or an unexpected error occurs within a page's logic.

## 4. Deep Dive into Shared Functions (`shared_functions.py`)
Duration: 00:10:00

The `application_pages/shared_functions.py` file is a central hub for utilities that are used across multiple parts of the application. It promotes code reusability and helps maintain consistency.

```python
# application_pages/shared_functions.py
import streamlit as st
import pandas as pd
import numpy as np

pages_config = {
    "Company Selection": "page_1_company_selection",
    "AI Capability Assessment": "page_2_ai_capability_assessment",
    "Strategic AI Initiative Selection": "page_3_ai_initiative_selection",
    "Financial Impact Quantification": "page_4_financial_impact",
    "Portfolio Benchmarking": "page_5_portfolio_benchmarking",
    "Exit Narrative & Valuation": "page_6_exit_valuation",
}

def initialize_session_state():
    # ... (content as provided in Setup section) ...

def go_to_page(page_label):
    # ... (content as provided in Setup section) ...
```

### Key Functions and Variables

1.  **`pages_config` Dictionary**:
    ```python
    pages_config = {
        "Company Selection": "page_1_company_selection",
        "AI Capability Assessment": "page_2_ai_capability_assessment",
        # ... and so on ...
    }
    ```
    This dictionary is fundamental to the dynamic page loading mechanism. It provides a clear mapping:
    *   **Keys**: User-friendly labels that appear in the sidebar navigation.
    *   **Values**: The actual Python module names (filenames without `.py` extension) located within the `application_pages` directory.
    This separation allows you to easily change page display names without altering the underlying file structure.

2.  **`initialize_session_state()` Function**:
    ```python
    def initialize_session_state():
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = list(pages_config.keys())[0]
        # ... initialize many other variables ...
    ```
    This function is responsible for setting up the initial state of the application. It ensures that critical variables exist in `st.session_state` before any page attempts to access them.
    *   **Data Initialization**: It often initializes DataFrames (like `companies_df`), dictionaries (like `ai_capabilities_scores`), and lists (`selected_initiatives`) that will hold application data. For a real application, this data might be loaded from a database, CSV, or an API.
    *   **Default Values**: Sets default values for inputs, selections, and calculation results, providing a clean slate when the application starts or is reset.
    *   **Consistency**: By centralizing session state initialization, it ensures that all pages operate with a consistent set of available data and parameters.

    <aside class="negative">
    <b>Important:</b> Any variable that a Streamlit component or custom logic relies on, and needs to persist across reruns, <b>must</b> be initialized in <code>st.session_state</code>, typically through this function. Forgetting to initialize a variable can lead to <code>KeyError</code> exceptions or unexpected behavior.
    </aside>

3.  **`go_to_page(page_label)` Function**:
    ```python
    def go_to_page(page_label):
        if page_label in pages_config:
            st.session_state['current_page'] = page_label
            st.rerun()
    ```
    This is a simple yet powerful navigation helper:
    *   It updates `st.session_state['current_page']` to the target page's label. This change is detected by `app.py` during its next rerun.
    *   `st.rerun()`: This command immediately stops the current execution and reruns the entire Streamlit script from the top. When `app.py` reruns, it sees the updated `current_page` in session state and dynamically loads the corresponding page module.
    *   While not explicitly used in the provided `app.py` snippet for actual page loading, `st.experimental_set_query_params` (commented out in the `shared_functions.py` example) is a useful feature for enabling direct URL access to specific pages, making it easier to share links or bookmark sections of the application.

## 5. Exploring Individual Page Modules
Duration: 00:20:00

Each file under `application_pages/` (e.g., `page_1_company_selection.py`) represents a distinct step in the AI value creation workflow. These modules are designed to be self-contained, with their logic encapsulated within a `main()` function.

The structure of a typical page module involves:
1.  **Imports**: Importing `streamlit` and any necessary shared functions or data.
2.  **`main()` Function**:
    *   Setting a subheader (`st.subheader`) for the page.
    *   Displaying instructional `st.markdown`.
    *   Interacting with `st.session_state` to retrieve current data (e.g., selected company).
    *   Using Streamlit widgets (`st.selectbox`, `st.slider`, `st.text_input`, `st.button`, etc.) to get user input.
    *   Performing calculations or data manipulation based on inputs.
    *   Updating `st.session_state` with new results or selections.
    *   Providing a "Continue" button that calls `go_to_page()` to navigate to the next step.

Let's look at the `page_1_company_selection.py` as an example:

```python
# application_pages/page_1_company_selection.py
import streamlit as st
from application_pages.shared_functions import go_to_page, pages_config

def main():
    st.subheader("1. Company Selection")
    st.markdown("Select a portfolio company to analyze its AI value creation potential.")

    companies_df = st.session_state['companies_df']
    company_names = companies_df['CompanyName'].tolist()

    current_selection_index = 0
    if 'selected_company_name' in st.session_state and st.session_state['selected_company_name'] in company_names:
        current_selection_index = company_names.index(st.session_state['selected_company_name'])

    selected_company_name = st.selectbox(
        "Choose a Company from your Portfolio",
        options=company_names,
        index=current_selection_index,
        key='company_selection_selectbox'
    )

    if selected_company_name != st.session_state.get('selected_company_name'):
        st.session_state['selected_company_name'] = selected_company_name
        selected_company_row = companies_df[companies_df['CompanyName'] == selected_company_name].iloc[0]
        st.session_state['selected_company_id'] = selected_company_row['CompanyID']
        st.session_state['selected_company_data'] = selected_company_row.to_dict()

    st.markdown(f"**Selected Company:** {st.session_state['selected_company_name']}")
    st.dataframe(
        companies_df[companies_df['CompanyName'] == st.session_state['selected_company_name']],
        hide_index=True
    )

    next_page_label = "AI Capability Assessment"
    if st.button(f"Continue to {next_page_label}"):
        go_to_page(next_page_label)
```

### Functional Breakdown of `page_1_company_selection.py`

*   **Display Title and Instructions**: Clear context for the user.
*   **Load Data**: Retrieves `companies_df` from `st.session_state`. This DataFrame contains mock data for portfolio companies. In a real-world scenario, this might come from a database query.
*   **`st.selectbox` for Company Selection**:
    *   Presents a dropdown of `CompanyName` values from the `companies_df`.
    *   `index=current_selection_index` ensures that the previously selected company (if any) is pre-selected when the page reloads.
    *   `key='company_selection_selectbox'` is crucial for Streamlit widgets. Every widget needs a unique key if there are multiple instances of the same widget or if its value needs to be retrieved directly from `st.session_state`.
*   **Update `st.session_state`**:
    *   When the user selects a new company from the dropdown, the `if selected_company_name != st.session_state.get('selected_company_name'):` condition triggers.
    *   `st.session_state['selected_company_name']`, `st.session_state['selected_company_id']`, and `st.session_state['selected_company_data']` are updated. This makes the selected company's details available to all subsequent pages.
*   **Display Selected Company Data**: Uses `st.dataframe` to show details of the currently selected company.
*   **Navigation Button**:
    *   `st.button(f"Continue to {next_page_label}")` creates a button to advance to the next step.
    *   Clicking it calls `go_to_page("AI Capability Assessment")`, which updates `st.session_state['current_page']` and triggers a rerun, leading to the loading of `page_2_ai_capability_assessment.py`.

### Overview of Other Pages (Conceptual)

Each subsequent page would build upon the data and selections made in previous steps:

*   **`page_2_ai_capability_assessment.py`**:
    *   Would use `st.slider` or `st.radio` widgets for users to rate a company's capabilities (e.g., Data Infrastructure, ML Ops maturity, Talent Pool) on a scale (e.g., 1-5).
    *   It would store these scores in `st.session_state['ai_capabilities_scores']`.
*   **`page_3_ai_initiative_selection.py`**:
    *   Might display potential AI initiatives (e.g., "Automated Customer Support", "Predictive Maintenance") using `st.checkbox` widgets.
    *   It would store the user's chosen initiatives in `st.session_state['selected_initiatives']` and potentially aggregate their associated costs and impact from `st.session_state['initiative_details']`.
*   **`page_4_financial_impact.py`**:
    *   Takes the selected initiatives and their projected impacts (from `st.session_state`) and calculates the multi-year projected EBITDA uplift and Org-AI-R growth.
    *   This page could display charts (`st.line_chart`, `st.bar_chart`) and summary metrics.
    *   It would update `st.session_state['projected_ebitda_uplift']` and `st.session_state['projected_org_ai_r_growth']`.
*   **`page_5_portfolio_benchmarking.py`**:
    *   Compares the current company's AI performance and investment efficiency (based on calculated metrics) against other companies in `st.session_state['companies_df']`.
    *   Uses `st.dataframe` or plotting libraries (like `matplotlib`, `plotly`, `altair`) to visualize benchmarks.
*   **`page_6_exit_valuation.py`**:
    *   Synthesizes all previous insights to build a narrative.
    *   Might include inputs for adjusting exit multiples based on AI maturity or projected growth.
    *   Calculates and displays the estimated enhanced exit valuation.

## 6. Extending and Customizing the Application
Duration: 00:15:00

The modular design of this application makes it relatively straightforward to extend and customize.

### How to Add a New Page

Adding a new analytical step or a different view involves three main steps:

1.  **Create a New Page Module**:
    *   Create a new Python file (e.g., `page_7_new_analysis.py`) inside the `application_pages` directory.
    *   Ensure it contains a `main()` function:
        ```python
        # application_pages/page_7_new_analysis.py
        import streamlit as st
        from application_pages.shared_functions import go_to_page, pages_config

        def main():
            st.subheader("7. New Analysis Step")
            st.markdown("This is where your new analysis will go.")
            # Your Streamlit widgets, logic, and data interactions here

            # Example: navigate back to the previous page or a custom one
            if st.button("Go Back"):
                go_to_page("Exit Narrative & Valuation")
        ```
2.  **Update `pages_config`**:
    *   Open `application_pages/shared_functions.py`.
    *   Add your new page to the `pages_config` dictionary. The order in this dictionary determines the order in the navigation sidebar.
    ```python
    # in application_pages/shared_functions.py
    pages_config = {
        # ... existing pages ...
        "Exit Narrative & Valuation": "page_6_exit_valuation",
        "New Analysis Step": "page_7_new_analysis", # Add your new page here
    }
    ```
3.  **Update `initialize_session_state` (if necessary)**:
    *   If your new page introduces new variables or requires specific default values in `st.session_state`, add their initialization logic to the `initialize_session_state()` function in `application_pages/shared_functions.py`.
    ```python
    # in application_pages/shared_functions.py
    def initialize_session_state():
        # ... existing initializations ...
        if 'new_analysis_result' not in st.session_state:
            st.session_state['new_analysis_result'] = {}
    ```
4.  **Integrate Navigation**:
    *   Ensure that the previous page (`page_6_exit_valuation.py` in this example) has a "Continue" button or logic to navigate to your new page using `go_to_page("New Analysis Step")`.

### Modifying Existing Logic

*   **Change Data Sources**: Modify `initialize_session_state()` to load `companies_df` or `initiative_details` from a database, API, or external CSV files instead of hardcoding or using dummy data.
*   **Update Calculation Models**: For example, in `page_4_financial_impact.py`, you could alter how EBITDA uplift or Org-AI-R growth is calculated to incorporate more complex financial models, discounting, or risk factors.
*   **Enhance UI/UX**: Experiment with different Streamlit widgets, layout options (`st.columns`, `st.expander`), or integrate custom CSS for a more branded look.

### Best Practices

*   **Modularization**: Keep functions and pages focused on a single responsibility. This enhances readability and testability.
*   **Session State Keys**: Use descriptive and unique keys for all `st.session_state` variables and Streamlit widgets to avoid conflicts.
*   **Error Handling**: Implement `try-except` blocks, especially for data loading, calculations, or external API calls, to provide informative feedback to the user instead of crashing the app.
*   **Comments and Docstrings**: Document your code thoroughly, explaining complex logic, function purposes, and variable meanings.
*   **Performance**: For very large datasets or complex computations, consider caching data with `@st.cache_data` or `@st.cache_resource` to prevent unnecessary re-computations on every rerun.

This comprehensive guide should equip you with the knowledge to understand, run, and further develop the AI Value Creation & Investment Efficiency Planner. Happy coding!
