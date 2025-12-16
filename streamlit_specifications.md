
# Streamlit Application Specification: AI Value Creation & Investment Efficiency Planner

## 1. Application Overview

### Narrative-Aligned Overview

Welcome, Private Equity Professional! As a **Portfolio Manager** at a leading PE firm, you're constantly evaluating and optimizing your portfolio companies for maximum value creation. In today's landscape, Artificial Intelligence is a critical lever, but quantifying its impact and building a clear investment roadmap can be complex.

This Streamlit application, the **"AI Value Creation & Investment Efficiency Planner"**, guides you through a structured, data-driven workflow to assess a portfolio company's AI readiness, identify high-potential initiatives, quantify their financial impact, and develop a strategic multi-year plan. You'll move from an initial high-level screening to a detailed dimension-level assessment, project selection, financial modeling, and ultimately, an exit-readiness projection. The story unfolds as you, the Portfolio Manager, make strategic decisions, evaluate potential returns, and benchmark your assets to drive superior investment outcomes.

The application reflects a realistic scenario where you need to:
1.  **Rapidly screen** potential AI opportunities within a portfolio company.
2.  Conduct a **deep-dive assessment** to understand current AI capabilities and identify key gaps.
3.  **Strategically select** AI initiatives that address these gaps and drive value.
4.  **Quantify** the projected EBITDA impact and Org-AI-R improvement over a multi-year horizon.
5.  **Benchmark** the company's AI performance and investment efficiency against the rest of your portfolio.
6.  **Assess** how these AI investments contribute to a compelling exit narrative and enhanced valuation multiples.

Through interactive components, the app demonstrates how you can leverage AI models and data analytics to transform qualitative assessments into measurable, actionable insights, directly supporting your mandate to maximize investor returns.

### Learning Goals (Persona-Aligned Applied Skills)

By interacting with this application, the Portfolio Manager will gain applied skills in:

*   **Strategic AI Screening:** Rapidly evaluating a company's systemic AI opportunity and idiosyncratic readiness for initial deal prioritization using quantitative metrics.
*   **Detailed AI Readiness Assessment:** Performing a granular, dimension-level analysis to pinpoint specific AI capability gaps and prioritize investment areas.
*   **Value Creation Planning:** Structuring a multi-year AI roadmap by selecting high-value use cases and estimating their investment, probability of success, and expected financial impact.
*   **Investment Efficiency Analysis:** Quantifying the return on AI investment using a fund-level metric ($AIE$) and benchmarking it across portfolio companies.
*   **Portfolio Optimization:** Understanding a company's AI standing relative to the broader portfolio using percentile and Z-score metrics to identify best practices and areas for intervention.
*   **Exit Strategy Development:** Projecting the impact of embedded AI capabilities on a company's valuation and crafting a data-backed exit narrative.
*   **Data-Driven Decision Making:** Translating analytical outputs (scores, gaps, projections, benchmarks) into actionable investment and operational strategies.

## 2. User Interface Requirements

The UI will follow a chronological, narrative-driven flow. Each section represents a distinct stage in the Portfolio Manager's workflow, building upon previous decisions and insights.

#### Layout & Navigation Structure

*   **Page Structure:** The application will be a single-page Streamlit app. Content will be organized into distinct, scrollable sections, each representing a step in the story.
*   **Navigation Flow:** Users will progress through the story sequentially. A "Continue" button at the bottom of each section will guide them to the next stage. A "Back" button could also be implemented within each section (except the first) to allow revisiting previous inputs, ensuring state preservation. A "Restart Session" button in the sidebar will clear all `st.session_state` variables and return to the initial state.
*   **Overall Layout:**
    *   **Sidebar (`st.sidebar`):**
        *   Application Title: "AI Value Creation & Investment Efficiency Planner"
        *   Global controls (e.g., "Restart Session" button).
        *   Optional: A progress indicator (e.g., "Step 1 of 6: Company Selection").
    *   **Main Content Area (`st.main`):**
        *   Each section will begin with a clear, narrative-driven heading and brief explanatory text, setting the context for the persona's task.
        *   Interactive widgets (sliders, dropdowns, multi-selects) will be presented clearly.
        *   Calculated results and visualizations will be displayed immediately below relevant inputs.
        *   Annotations and tooltips will provide contextual help.

#### Input Widgets and Controls

**Step 1: Company Selection and Initial Org-AI-R Assessment**
*   **Narrative:** "Our first step is to identify which portfolio company we're evaluating. Let's get an initial sense of its AI potential."
*   **Widget:** `st.selectbox`
    *   **Label:** "Select Portfolio Company"
    *   **Purpose:** To choose the target company for analysis.
    *   **Real-world Action:** Initiating a formal AI readiness assessment for a specific asset in the fund.
    *   **Parameters:**
        *   `options`: Derived from `portfolio_companies_df['Company']`.
        *   `default`: 'Alpha Manufacturing'.
        *   `key`: `'selected_company'`
*   **Widget:** `st.number_input`
    *   **Label:** "Simulated Baseline Idiosyncratic Readiness ($V_{org,j}^R$)"
    *   **Purpose:** To allow the Portfolio Manager to input a baseline readiness score, representing initial, rough internal capabilities.
    *   **Real-world Action:** Providing a preliminary estimate of a company's internal AI capabilities based on initial observations or limited data.
    *   **Parameters:**
        *   `min_value`: `0`
        *   `max_value`: `100`
        *   `value`: `36` (default from notebook)
        *   `step`: `1`
        *   `key`: `'baseline_v_org_r'`
*   **Widget:** `st.number_input`
    *   **Label:** "Simulated External Signals Score"
    *   **Purpose:** To input external market intelligence regarding a company's AI visibility.
    *   **Real-world Action:** Incorporating public data (e.g., job postings, news mentions) into the preliminary screening.
    *   **Parameters:**
        *   `min_value`: `0`
        *   `max_value`: `100`
        *   `value`: `45` (default from notebook)
        *   `step`: `1`
        *   `key`: `'external_signals_score'`

**Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis**
*   **Narrative:** "Now, let's conduct a detailed due diligence. Your expert assessment of the company's current capabilities across 7 key AI dimensions is crucial for understanding specific strengths and weaknesses."
*   **Widgets (14 x `st.slider`):**
    *   **Labels:** "Current Rating (1-5) for [Dimension Name]", "Target Rating (1-5) for [Dimension Name]" (for each of the 7 dimensions: Data Infrastructure, AI Governance, Technology Stack, Talent, Leadership, Use Case Portfolio, Culture).
    *   **Purpose:** To capture the Portfolio Manager's assessment of the company's current and desired (target) AI readiness across each dimension.
    *   **Real-world Action:** Performing a comprehensive capability assessment based on interviews, data reviews, and strategic objectives.
    *   **Parameters:**
        *   `min_value`: `1`
        *   `max_value`: `5`
        *   `value`: (Defaults dynamically generated by `simulate_dimension_ratings` from notebook for current/target)
        *   `step`: `1`
        *   `key`: e.g., `'current_rating_data_infra'`, `'target_rating_data_infra'`

**Step 3: Identify High-Value AI Use Cases & Estimate Impact**
*   **Narrative:** "With a clear understanding of the gaps, let's identify specific AI initiatives. Which high-value use cases will directly address the identified gaps and create the most significant impact for the company?"
*   **Widget:** `st.multiselect`
    *   **Label:** "Select High-Value AI Use Cases"
    *   **Purpose:** To choose potential AI projects from a sector-specific library.
    *   **Real-world Action:** Prioritizing and selecting strategic AI initiatives for implementation.
    *   **Parameters:**
        *   `options`: Derived from `high_value_use_cases[selected_sector]['Use Case']`.
        *   `default`: `['Predictive Maintenance', 'Demand Forecasting', 'Supply Chain Optimization']` (dynamic based on initial company selection/sector).
        *   `key`: `'selected_use_cases'`
*   **Widgets (for EACH selected use case, dynamically generated):**
    *   **Label (for Investment):** "Estimated Investment Cost for [Use Case] ($M$)"
        *   **Purpose:** To input or adjust the estimated financial outlay for a specific AI project.
        *   **Real-world Action:** Budgeting and resource allocation.
        *   **Parameters:** `min_value`: `0.1`, `max_value`: `10.0`, `value`: (Default from `estimate_project_parameters`), `step`: `0.1`, `key`: e.g., `'investment_predictive_maintenance'`
    *   **Label (for Probability):** "Probability of Success for [Use Case] (0-1)"
        *   **Purpose:** To input or adjust the likelihood of successful implementation of the AI project.
        *   **Real-world Action:** Risk assessment and scenario planning.
        *   **Parameters:** `min_value`: `0.0`, `max_value`: `1.0`, `value`: (Default from `estimate_project_parameters`), `step`: `0.01`, `format`: `%.2f`, `key`: e.g., `'prob_success_predictive_maintenance'`
    *   **Label (for Quality):** "Execution Quality Factor for [Use Case] (0-1)"
        *   **Purpose:** To input or adjust the expected quality of project execution, impacting the realized benefits.
        *   **Real-world Action:** Reflecting confidence in the company's ability to deliver high-quality AI solutions.
        *   **Parameters:** `min_value`: `0.0`, `max_value`: `1.0`, `value`: (Default from `estimate_project_parameters`), `step`: `0.01`, `format`: `%.2f`, `key`: e.g., `'exec_quality_predictive_maintenance'`

**Step 4: Build the Multi-Year AI Value Creation Plan**
*   **Narrative:** "Now, let's integrate these initiatives into a cohesive multi-year plan, projecting the financial and strategic trajectory for the company under your guidance."
*   **Widget:** `st.slider`
    *   **Label:** "Planning Horizon (Years)"
    *   **Purpose:** To define the time frame over which the AI value creation plan will be projected.
    *   **Real-world Action:** Aligning the AI roadmap with typical PE investment horizons and exit strategies.
    *   **Parameters:**
        *   `min_value`: `1`
        *   `max_value`: `5`
        *   `value`: `3` (default from notebook)
        *   `step`: `1`
        *   `key`: `'planning_horizon'`

**Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking**
*   **Narrative:** "With the plan defined, it's time to evaluate its efficiency and see how it benchmarks against other companies in our portfolio. This informs fund-level strategy and resource allocation."
*   **No specific inputs in this step; it's output-focused based on previous inputs.**

**Step 6: Exit-Readiness Assessment**
*   **Narrative:** "Finally, let's project how these AI investments enhance the company's appeal to potential buyers and impact its exit valuation. Crafting a compelling AI narrative is key to maximizing our returns."
*   **Widgets (3 x `st.slider`):**
    *   **Label:** "Visible AI Capabilities Score (0-100)"
        *   **Purpose:** To assess how easily apparent the company's AI features and technology stack are to an external buyer.
        *   **Real-world Action:** Evaluating market perception and the ease of demonstrating AI value.
        *   **Parameters:** `min_value`: `0`, `max_value`: `100`, `value`: `75` (default from notebook), `step`: `1`, `key`: `'visible_score'`
    *   **Label:** "Documented AI Impact Score (0-100)"
        *   **Purpose:** To assess the availability and quality of auditable data demonstrating AI's financial impact.
        *   **Real-world Action:** Preparing evidence-based ROI documentation for due diligence.
        *   **Parameters:** `min_value`: `0`, `max_value`: `100`, `value`: `80` (default from notebook), `step`: `1`, `key`: `'documented_score'`
    *   **Label:** "Sustainable AI Capabilities Score (0-100)"
        *   **Purpose:** To assess if AI capabilities are embedded processes, talent, and infrastructure versus one-off projects.
        *   **Real-world Action:** Proving long-term, defensible AI advantage to potential acquirers.
        *   **Parameters:** `min_value`: `0`, `max_value`: `100`, `value`: `70` (default from notebook), `step`: `1`, `key`: `'sustainable_score'`
*   **Widget:** `st.number_input`
    *   **Label:** "Baseline Exit Multiple (e.g., for selected sector)"
    *   **Purpose:** To input the assumed pre-AI or industry-average valuation multiple.
    *   **Real-world Action:** Setting a baseline for projecting AI-driven multiple expansion.
    *   **Parameters:**
        *   `min_value`: `1.0`
        *   `max_value`: `20.0`
        *   `value`: `6.5` (default from notebook, dynamic based on sector if available)
        *   `step`: `0.1`
        *   `key`: `'base_exit_multiple'`

#### Visualization Components

All visualizations will be rendered using Matplotlib/Seaborn or Plotly, tailored for clarity within the narrative.

1.  **Radar Chart:** "AI Readiness Dimension Scores for [Company Name]"
    *   **Location:** Step 2.
    *   **Purpose:** Visually compare the `Current Score (0-100)` and `Target Score (0-100)` across the 7 AI readiness dimensions.
    *   **Format:** Spider/Radar chart with dimensions on axes and two lines/fills for current vs. target.
    *   **Expected Output:** Clear polygonal shapes highlighting gaps and strengths.
2.  **Bar Chart:** "AI Readiness Gap Analysis for [Company Name]"
    *   **Location:** Step 2.
    *   **Purpose:** Display the `Gap (Target - Current Score)` for each dimension, sorted from largest to smallest.
    *   **Format:** Vertical bar chart, dimensions on x-axis, gap score on y-axis.
    *   **Expected Output:** Quick identification of priority areas for investment.
3.  **Line Plot:** "Cumulative EBITDA Impact for [Company Name] AI Plan"
    *   **Location:** Step 4.
    *   **Purpose:** Illustrate the projected cumulative EBITDA impact ($M$) over the defined planning horizon.
    *   **Format:** Line plot, Year on x-axis, Cumulative EBITDA Impact ($M$) on y-axis.
    *   **Expected Output:** Visualization of the financial value accretion over time.
4.  **Line Plot:** "PE Org-AI-R Progression for [Company Name] AI Plan"
    *   **Location:** Step 4.
    *   **Purpose:** Show the progression of the `Org-AI-R Score` over the multi-year plan.
    *   **Format:** Line plot, Year on x-axis, Org-AI-R Score on y-axis, with y-axis limits 0-100.
    *   **Expected Output:** Clear trajectory of capability improvement.
5.  **Bar Chart:** "Current PE Org-AI-R Scores Across Portfolio Companies"
    *   **Location:** Step 5.
    *   **Purpose:** Compare the `Current Org-AI-R` scores for all portfolio companies, with bars colored by sector.
    *   **Format:** Vertical bar chart, Company on x-axis, Current Org-AI-R on y-axis, hue by Sector.
    *   **Expected Output:** Relative positioning of the selected company against peers in terms of AI readiness.
6.  **Bar Chart:** "AI Investment Efficiency Across Portfolio Companies"
    *   **Location:** Step 5.
    *   **Purpose:** Compare the `AI Investment Efficiency (AIE)` for all portfolio companies, with bars colored by sector.
    *   **Format:** Vertical bar chart, Company on x-axis, AIE (pts*$M$/$M$) on y-axis, hue by Sector.
    *   **Expected Output:** Benchmarking of investment effectiveness across the portfolio.

#### Interactive Elements & Feedback Mechanisms

*   **Continue Buttons:** A prominent button at the end of each section, labeled "Continue to [Next Step Name]", will advance the user through the narrative.
*   **Dynamic Updates:** All numerical outputs, tables, and visualizations will react immediately and automatically to user input changes in sliders, number inputs, and selectboxes. For example, changing a "Target Rating" slider in Step 2 will instantly update the `Gap` table, the Radar Chart, and the Bar Chart. Adjusting "Probability of Success" for a use case in Step 3 will update the `EBITDA Impact ($M)` and `Delta Org-AI-R` for that use case, which in turn will update the multi-year plan and AIE in subsequent sections.
*   **Recommendations/Insights:** Key conclusions (e.g., screening recommendation, priority dimensions, AIE score, predicted exit multiple) will be displayed as clear text alongside numerical results, guiding the persona's interpretation.
*   **Calculations Trigger:** In some sections (e.g., after selecting use cases and adjusting parameters), a "Calculate Plan" or "Generate Report" button might be used to explicitly trigger complex multi-step calculations and plot generation, providing control and clear feedback that processing is occurring.

## 3. Additional Requirements

#### Annotations & Tooltips

*   **Contextual Explanations:** For every interactive input widget, a small info icon ($\text{ⓘ}$) will provide a tooltip (on hover) explaining its purpose in the scenario and its impact on the calculations.
    *   Example for `st.slider` "Current Rating (1-5) for Data Infrastructure": "Your assessment of the company's current data infrastructure maturity. A higher rating indicates robust data governance, catalogs, and accessibility, crucial for AI deployment."
*   **Output Interpretations:** Below each calculated score or visualization, a brief `st.info` or `st.write` statement will interpret the result in the context of the Portfolio Manager's role.
    *   Example for Screening Recommendation: "The Screening Recommendation guides your initial due diligence focus. A 'Strong AI candidate' suggests high potential and justifies deeper investigation."
    *   Example for Radar Chart: "This Radar Chart visually highlights the 'gaps' between current and target AI readiness. Large gaps represent critical areas requiring strategic investment and focus in your value creation plan."
*   **Formula References:** Where complex formulas are presented in the output, a tooltip or footnote will concisely explain the variables involved.

#### State Management Requirements

*   **`st.session_state`:** All user inputs (selected company, dimension ratings, use case parameters, planning horizon, exit readiness scores, etc.) and dynamically generated data (e.g., `planned_initiatives_df`, `ai_plan_trajectory_df`, updated `portfolio_companies_df`) must be stored in `st.session_state`.
*   **Persistence Across Interactions:** Changes to any input widget should trigger recalculations and UI updates while ensuring all other form inputs and application states remain preserved. This prevents data loss as the user interacts with different parts of the application or navigates between logical steps (if any non-linear navigation is introduced, though the primary flow is linear).
*   **Initialization and Reset:** `st.session_state` variables will be initialized upon the first run or when the "Restart Session" button is clicked in the sidebar, providing sensible defaults for a new workflow.

## 4. Notebook Content and Code Requirements

All relevant code stubs and markdown content from the provided Jupyter Notebook will be meticulously integrated into the Streamlit application. Each section of the notebook corresponds directly to an interactive section or component in the Streamlit app.

### **Initial Setup and Data Loading (Corresponding to Notebook Section 2)**

*   **Code:**
    ```python
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    import streamlit as st

    # Suppress warnings for cleaner output
    warnings.filterwarnings('ignore')

    # Model Coefficients and Constants (Hardcoded based on document priors)
    model_coefficients = {
        'alpha': 0.65,  # Weight on idiosyncratic readiness
        'beta': 0.15,   # Synergy coefficient
        'gamma': 0.035, # Value creation coefficient for Org-AI-R to EBITDA mapping
        'epsilon': 0.30, # Screening score weight for external signals
        'w1_exit': 0.35, # Exit-Readiness: Visible weight
        'w2_exit': 0.40, # Exit-Readiness: Documented weight
        'w3_exit': 0.25, # Exit-Readiness: Sustainable weight
        'delta_exit': 2.0 # AI premium coefficient for exit multiple
    }

    # Systematic Opportunity (H_org,k^R) scores by sector
    systematic_opportunity_scores = {
        'Manufacturing': 72, 'Healthcare': 78, 'Retail': 75,
        'Business Services': 80, 'Technology': 85
    }

    # General Dimension Weights
    general_dimension_weights = {
        'Data Infrastructure': 0.25, 'AI Governance': 0.20, 'Technology Stack': 0.15,
        'Talent': 0.15, 'Leadership': 0.10, 'Use Case Portfolio': 0.10, 'Culture': 0.05
    }

    # Sector-Specific Dimension Weight Adjustments
    sector_dimension_weight_adjustments = {
        'Manufacturing': {
            'Data Infrastructure': 0.28, 'AI Governance': 0.15, 'Technology Stack': 0.18,
            'Talent': 0.15, 'Leadership': 0.08, 'Use Case Portfolio': 0.12, 'Culture': 0.04
        },
        'Healthcare': {
            'Data Infrastructure': 0.28, 'AI Governance': 0.25, 'Technology Stack': 0.12,
            'Talent': 0.15, 'Leadership': 0.08, 'Use Case Portfolio': 0.08, 'Culture': 0.04
        },
        'Retail': {
            'Data Infrastructure': 0.28, 'AI Governance': 0.12, 'Technology Stack': 0.18,
            'Talent': 0.14, 'Leadership': 0.10, 'Use Case Portfolio': 0.13, 'Culture': 0.05
        },
        'Business Services': {
            'Data Infrastructure': 0.22, 'AI Governance': 0.18, 'Technology Stack': 0.15,
            'Talent': 0.20, 'Leadership': 0.10, 'Use Case Portfolio': 0.10, 'Culture': 0.05
        },
        'Technology': {
            'Data Infrastructure': 0.22, 'AI Governance': 0.15, 'Technology Stack': 0.20,
            'Talent': 0.22, 'Leadership': 0.08, 'Use Case Portfolio': 0.10, 'Culture': 0.03
        }
    }

    # Combine weights into a DataFrame (cached)
    @st.cache_data
    def get_all_dimension_weights_df():
        df = pd.DataFrame(general_dimension_weights, index=['General']).T
        for sector, weights in sector_dimension_weight_adjustments.items():
            df[sector] = pd.Series(weights)
        return df
    all_dimension_weights_df = get_all_dimension_weights_df()

    # High-Value Use Cases by Sector (cached)
    @st.cache_data
    def get_high_value_use_cases():
        return {
            'Manufacturing': pd.DataFrame([
                {'Use Case': 'Predictive Maintenance', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4, 'Description': 'AI-driven equipment monitoring reducing unplanned downtime 15-25%'},
                {'Use Case': 'Quality Control (CV)', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 3, 'Description': 'Computer vision defect detection improving yield 5-10%'},
                {'Use Case': 'Demand Forecasting', 'Complexity': 'Low-Medium', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'ML-based demand planning reducing inventory costs 10-20%'},
                {'Use Case': 'Supply Chain Optimization', 'Complexity': 'High', 'Timeline (months)': '12-18', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 3, 'Description': 'AI route optimization and supplier risk monitoring'},
            ]),
            'Healthcare': pd.DataFrame([
                {'Use Case': 'Revenue Cycle Management', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 3, 'EBITDA Impact (max%)': 5, 'Description': 'AI-driven claims processing reducing denials 15-25%'},
                {'Use Case': 'Clinical Documentation', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'NLP-powered coding improving accuracy and speed'},
                {'Use Case': 'Patient Scheduling', 'Complexity': 'Low-Medium', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 3, 'Description': 'Predictive scheduling reducing wait times, improving utilization'},
                {'Use Case': 'Diagnostic AI', 'Complexity': 'High', 'Timeline (months)': '12-24', 'EBITDA Impact (min%)': 0, 'EBITDA Impact (max%)': 0, 'Description': 'AI imaging analysis (radiology, pathology). Variable impact.'},
            ]),
            'Retail': pd.DataFrame([
                {'Use Case': 'Demand Forecasting', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 3, 'Description': 'ML-powered inventory optimization'},
                {'Use Case': 'Personalization', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 0.5, 'EBITDA Impact (max%)': 1, 'Description': 'AI-driven product recommendations'},
                {'Use Case': 'Dynamic Pricing', 'Complexity': 'High', 'Timeline (months)': '9-15', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'Real-time price optimization'},
                {'Use Case': 'Customer Service Chatbot', 'Complexity': 'Low', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 0.5, 'EBITDA Impact (max%)': 1, 'Description': 'AI chatbots reducing contact center costs'},
            ]),
            'Business Services': pd.DataFrame([
                {'Use Case': 'Document Processing', 'Complexity': 'Low-Medium', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4, 'Description': 'AI extraction and analysis'},
                {'Use Case': 'Knowledge Worker Tools', 'Complexity': 'Low', 'Timeline (months)': '1-3', 'EBITDA Impact (min%)': 3, 'EBITDA Impact (max%)': 5, 'Description': 'Gen AI tools improving output'},
                {'Use Case': 'Sales Enablement', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 3, 'Description': 'AI-powered proposal generation'},
                {'Use Case': 'Contract Analysis', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'AI review of legal/procurement documents'},
            ]),
            'Technology': pd.DataFrame([
                {'Use Case': 'Product AI Embedding', 'Complexity': 'High', 'Timeline (months)': '12-24', 'EBITDA Impact (min%)': 5, 'EBITDA Impact (max%)': 10, 'Description': 'Embedding AI as core product features'},
                {'Use Case': 'Automated Code Generation', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 3, 'EBITDA Impact (max%)': 6, 'Description': 'AI assistance for software development'},
                {'Use Case': 'Predictive Cybersecurity', 'Complexity': 'High', 'Timeline (months)': '9-18', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4, 'Description': 'AI for threat detection and prevention'},
                {'Use Case': 'ML-driven DevOps', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 3, 'Description': 'AI for optimizing deployment pipelines'},
            ])
        }
    high_value_use_cases = get_high_value_use_cases()

    # Synthetic Portfolio Companies Data (dynamic, not cached as it will be updated)
    initial_portfolio_companies_data = [
        {'Company': 'Alpha Manufacturing', 'Sector': 'Manufacturing', 'Baseline Org-AI-R': 42, 'Current Org-AI-R': 68, 'Delta Org-AI-R': 26, 'Investment ($M)': 2.8, 'EBITDA Impact (%)': 6, 'EBITDA ($M)': 9.0},
        {'Company': 'Beta Healthcare', 'Sector': 'Healthcare', 'Baseline Org-AI-R': 48, 'Current Org-AI-R': 71, 'Delta Org-AI-R': 23, 'Investment ($M)': 3.2, 'EBITDA Impact (%)': 5, 'EBITDA ($M)': 8.0},
        {'Company': 'Gamma Retail', 'Sector': 'Retail', 'Baseline Org-AI-R': 44, 'Current Org-AI-R': 62, 'Delta Org-AI-R': 18, 'Investment ($M)': 2.4, 'EBITDA Impact (%)': 3, 'EBITDA ($M)': 12.0},
        {'Company': 'Delta Services', 'Sector': 'Business Services', 'Baseline Org-AI-R': 62, 'Current Org-AI-R': 79, 'Delta Org-AI-R': 17, 'Investment ($M)': 2.1, 'EBITDA Impact (%)': 8, 'EBITDA ($M)': 7.5},
        {'Company': 'Epsilon Tech', 'Sector': 'Technology', 'Baseline Org-AI-R': 75, 'Current Org-AI-R': 86, 'Delta Org-AI-R': 11, 'Investment ($M)': 1.5, 'EBITDA Impact (%)': 4, 'EBITDA ($M)': 15.0},
        {'Company': 'Zeta Logistics', 'Sector': 'Manufacturing', 'Baseline Org-AI-R': 38, 'Current Org-AI-R': 58, 'Delta Org-AI-R': 20, 'Investment ($M)': 1.9, 'EBITDA Impact (%)': 4, 'EBITDA ($M)': 6.0},
        {'Company': 'Eta Food', 'Sector': 'Retail', 'Baseline Org-AI-R': 35, 'Current Org-AI-R': 52, 'Delta Org-AI-R': 17, 'Investment ($M)': 2.0, 'EBITDA Impact (%)': 3, 'EBITDA ($M)': 10.0},
        {'Company': 'Theta Finance', 'Sector': 'Business Services', 'Baseline Org-AI-R': 68, 'Current Org-AI-R': 82, 'Delta Org-AI-R': 14, 'Investment ($M)': 1.8, 'EBITDA Impact (%)': 5, 'EBITDA ($M)': 11.0}
    ]

    # Initialize portfolio_companies_df in session state
    if 'portfolio_companies_df' not in st.session_state:
        st.session_state.portfolio_companies_df = pd.DataFrame(initial_portfolio_companies_data)
        st.session_state.portfolio_companies_df['EBITDA Impact ($M)'] = st.session_state.portfolio_companies_df['EBITDA ($M)'] * (st.session_state.portfolio_companies_df['EBITDA Impact (%)'] / 100)
        st.session_state.portfolio_companies_df['Efficiency (pts/$M)'] = (st.session_state.portfolio_companies_df['Delta Org-AI-R'] / st.session_state.portfolio_companies_df['Investment ($M)']) * st.session_state.portfolio_companies_df['EBITDA Impact ($M)']
        st.session_state.portfolio_companies_df = st.session_state.portfolio_companies_df[['Company', 'Sector', 'Baseline Org-AI-R', 'Current Org-AI-R', 'Delta Org-AI-R', 'Investment ($M)', 'Efficiency (pts/$M)', 'EBITDA Impact (%)', 'EBITDA ($M)', 'EBITDA Impact ($M)']]

    # Core Functions
    def calculate_org_ai_r(V_org_R, H_org_k_R, synergy_score, alpha, beta):
        return round((alpha * V_org_R) + ((1 - alpha) * H_org_k_R) + (beta * synergy_score), 2)

    def calculate_screening_score(H_org_k_R, external_signals_score, epsilon):
        return round(H_org_k_R + (epsilon * external_signals_score), 2)

    def simulate_dimension_ratings(company_name, sector, is_target=False):
        # Using a deterministic seed for consistent defaults
        seed_val = hash(company_name + sector + str(is_target)) % (2**32 - 1)
        rng = np.random.default_rng(seed_val)
        ratings = {}
        for dim in general_dimension_weights.keys():
            if is_target:
                ratings[dim] = rng.integers(3, 6) # Target ratings tend to be higher
            else:
                ratings[dim] = rng.integers(1, 4) # Current ratings for baseline
        return pd.Series(ratings, name='Rating (1-5)')

    def calculate_dimension_score(ratings):
        return ((ratings / 5) * 100).round(2)

    def calculate_V_org_R(dimension_scores, sector_weights):
        # Ensure alignment of indices
        aligned_scores = dimension_scores.reindex(sector_weights.index, fill_value=0)
        weighted_sum = (aligned_scores * sector_weights).sum()
        return round(weighted_sum, 2)

    def calculate_synergy(V_org_R, H_org_k_R):
        return min(V_org_R, H_org_k_R)

    def estimate_project_parameters(use_case_data, current_V_org_R, H_org_k_R, initial_ebitda_M, user_investment=None, user_prob_success=None, user_exec_quality=None):
        complexity_map = {'Low': 0.7, 'Low-Medium': 0.6, 'Medium': 0.5, 'High': 0.3}
        timeline_map_avg = {'1-3': 2, '3-6': 4.5, '6-9': 7.5, '6-12': 9, '9-15': 12, '12-18': 15, '12-24': 18} # Use average of range

        complexity_factor = complexity_map.get(use_case_data['Complexity'], 0.5)
        timeline_months_str = str(use_case_data['Timeline (months)'])
        timeline_months = timeline_map_avg.get(timeline_months_str, 6) # Default 6 months if range not found

        # Deterministic random generation for defaults based on use case name
        seed_val = hash(use_case_data['Use Case']) % (2**32 - 1)
        rng = np.random.default_rng(seed_val)
        
        # Calculate default values
        default_investment_cost_M = round(0.2 * complexity_factor * (timeline_months / 6) * rng.uniform(0.8, 1.2) + 0.1, 2)
        default_prob_success = round(np.clip(0.6 + (current_V_org_R / 100 * 0.2) - (complexity_factor * 0.3), 0.5, 0.95), 2)
        default_exec_quality = round(np.clip(current_V_org_R / 100 * 0.8, 0.6, 0.9), 2)
        
        # Use user-provided values if available, otherwise use defaults
        investment_cost_M = user_investment if user_investment is not None else default_investment_cost_M
        prob_success = user_prob_success if user_prob_success is not None else default_prob_success
        exec_quality = user_exec_quality if user_exec_quality is not None else default_exec_quality

        # Base EBITDA impact from use case definition, adjusted for H_org_k_R and V_org_R for realism
        ebitda_impact_pct_base = rng.uniform(use_case_data['EBITDA Impact (min%)'], use_case_data['EBITDA Impact (max%)'])
        if use_case_data['Use Case'] == 'Diagnostic AI' and ebitda_impact_pct_base == 0:
            ebitda_impact_pct_base = rng.uniform(1, 3) # Re-simulate for Diagnostic AI if base is 0

        # Adjust EBITDA impact for company-specific context (Systematic Opportunity & Idiosyncratic Readiness)
        ebitda_impact_pct_contextual = ebitda_impact_pct_base * (H_org_k_R / 100) * (current_V_org_R / 100 * 0.5 + 0.5)

        # Apply user-influenced probability and quality to the potential impact
        ebitda_impact_pct_adjusted = round(ebitda_impact_pct_contextual * prob_success * exec_quality, 2)
        ebitda_impact_M = round(initial_ebitda_M * (ebitda_impact_pct_adjusted / 100), 2)
        
        # Delta Org-AI-R also influenced by user inputs and base factors
        delta_org_ai_r_base = round(rng.uniform(5, 15) * complexity_factor * (ebitda_impact_pct_base / 2), 2)
        delta_org_ai_r_adjusted = round(delta_org_ai_r_base * prob_success * exec_quality, 2)
        if delta_org_ai_r_adjusted < 1: delta_org_ai_r_adjusted = 1
        
        return {
            'Investment ($M)': investment_cost_M,
            'Probability of Success': prob_success,
            'Execution Quality': exec_quality,
            'EBITDA Impact (%)': ebitda_impact_pct_adjusted, # This is the final percentage impact
            'EBITDA Impact ($M)': ebitda_impact_M,
            'Delta Org-AI-R': delta_org_ai_r_adjusted,
            'Timeline (months)': timeline_months
        }

    def create_multi_year_plan(company_name, initial_org_ai_r, initial_ebitda_M, planned_initiatives_df, H_org_k_R, total_years=3):
        current_org_ai_r = initial_org_ai_r
        current_ebitda_M_base = initial_ebitda_M # Base EBITDA for calculating year-on-year impact
        cumulative_ebitda_impact_M = 0
        cumulative_investment_M = 0
        
        plan_trajectory = []
        planned_initiatives_df_sorted = planned_initiatives_df.sort_values(by='Timeline (months)')
        completed_initiatives = [] # To track initiatives that have finished their timeline

        for year in range(1, total_years + 1):
            year_ebitda_impact_M = 0
            year_org_ai_r_delta = 0
            year_investment_M = 0
            
            # Add benefits from initiatives that completed in *previous* years and are still active
            # For simplicity, assume all initiatives, once "completed", contribute their full annual impact
            # (EBITDA_Impact_M * Prob_Success * Exec_Quality) for the remainder of the plan.
            # Here we define "completed" as their timeline being met.
            
            # Initiatives that have finished their timeline and contribute *this year*
            for index, initiative in planned_initiatives_df_sorted.iterrows():
                if initiative['Timeline (months)'] <= year * 12: # Initiative timeline is within or before current year
                    # Ensure we only count its delta_org_ai_r and investment once
                    if initiative['Use Case'] not in [i['Use Case'] for i in completed_initiatives]:
                        year_org_ai_r_delta += initiative['Delta Org-AI-R']
                        year_investment_M += initiative['Investment ($M)']
                        completed_initiatives.append(initiative)
                    
                    # Contribution to EBITDA each year, assuming persistent impact after completion
                    # We are summing the *full potential* impact of each *completed* project for this year
                    # This implies projects add their full annual benefit once implemented.
                    year_ebitda_impact_M += initiative['EBITDA Impact ($M)']
                    
            # Update scores for the year
            current_org_ai_r += year_org_ai_r_delta
            cumulative_ebitda_impact_M += year_ebitda_impact_M # This is cumulative impact from all projects
            cumulative_investment_M += year_investment_M # Sum of all investment made up to this point

            plan_trajectory.append({
                'Year': year,
                'Org-AI-R': round(current_org_ai_r, 2),
                'EBITDA Impact ($M) - Year': round(year_ebitda_impact_M, 2),
                'Cumulative EBITDA Impact ($M)': round(cumulative_ebitda_impact_M, 2),
                'Investment ($M) - Year': round(year_investment_M, 2),
                'Cumulative Investment ($M)': round(cumulative_investment_M, 2)
            })

        return pd.DataFrame(plan_trajectory)

    def calculate_ai_investment_efficiency(delta_org_ai_r, total_ai_investment_M, total_ebitda_impact_M):
        if total_ai_investment_M <= 0:
            return 0.0 # Handle division by zero
        aie_score = (delta_org_ai_r / total_ai_investment_M) * total_ebitda_impact_M
        return round(aie_score, 2)

    def calculate_within_portfolio_percentile(company_org_ai_r, portfolio_org_ai_rs):
        if not portfolio_org_ai_rs: return 0.0
        sorted_scores = sorted(portfolio_org_ai_rs)
        rank = sum(1 for score in sorted_scores if score <= company_org_ai_r) # Count scores less than or equal
        percentile = (rank / len(portfolio_org_ai_rs)) * 100
        return round(percentile, 2)

    def calculate_cross_portfolio_z_score(company_org_ai_r, industry_mean, industry_std):
        if industry_std == 0 or np.isnan(industry_std):
            return 0.0 # Handle division by zero or NaN std
        z_score = (company_org_ai_r - industry_mean) / industry_std
        return round(z_score, 2)

    def assess_exit_readiness(visible_score, documented_score, sustainable_score, w1, w2, w3):
        return round((w1 * visible_score) + (w2 * documented_score) + (w3 * sustainable_score), 2)

    def predict_exit_multiple(base_multiple, exit_ai_r, delta):
        return round(base_multiple + (delta * exit_ai_r / 100), 2)
    ```

### **Streamlit Application Flow and Component Mapping**

The Streamlit app will use `st.session_state` extensively to maintain progress.

#### **Section 1: Company Selection and Initial Org-AI-R Assessment (Notebook Section 3)**

*   **Markdown:** "Welcome, Private Equity Professional! This planner helps you assess AI readiness, identify initiatives, and quantify financial impact. Our first step is to identify which portfolio company we're evaluating. Let's get an initial sense of its AI potential."
*   **Input:** `st.selectbox` for company selection.
*   **Outputs:**
    *   Display `selected_sector`, `H_{org,k}^R` (from `systematic_opportunity_scores`), `baseline_V_org_R` (from `st.number_input`), `calculated_baseline_org_ai_r` (using `calculate_org_ai_r`), `external_signals_score` (from `st.number_input`), `screening_score` (using `calculate_screening_score`).
    *   **Formula (Display):** PE Org-AI-R: $$PE~Org-AI-R_{j,t} = \alpha \cdot V_{org,j}^R(t) + (1 - \alpha) \cdot H_{org,k}^R(t) + \beta \cdot Synergy(V_{org,j}^R, H_{org,k}^R)$$
    *   **Formula (Display):** Screening Score: $$Screen_{j} = H_{org,k}^R + \epsilon \cdot ExternalSignals_j$$
    *   **Formula (Display):** Synergy: $$Synergy = min(V_{org,j}^R, H_{org,k}^R)$$
    *   Screening Recommendation logic as in the notebook.
*   **Navigation:** "Continue to Dimension-Level Assessment" button.

#### **Section 2: Deep Dive: Dimension-Level Assessment & Gap Analysis (Notebook Section 4)**

*   **Markdown:** "Now, let's conduct a detailed due diligence. Your expert assessment of the company's current capabilities across 7 key AI dimensions is crucial for understanding specific strengths and weaknesses."
*   **Inputs:** `st.slider` widgets for 'Current Rating (1-5)' and 'Target Rating (1-5)' for each of the 7 dimensions. Initial values derived from `simulate_dimension_ratings`.
*   **Processing:** Calls `calculate_dimension_score`, `calculate_V_org_R`, `calculate_synergy`, `calculate_org_ai_r` to generate intermediate scores.
    *   **Formula (Display):** Dimension Score: $$D_k = \frac{\sum_i w_i \cdot Rating_{i,k}}{5} \times 100$$
    *   **Formula (Display):** Gap Score: $$Gap_k = D_k^{target} - D_k^{current}$$
*   **Outputs:**
    *   `dimension_assessment_df` displayed as `st.dataframe` or `st.table`.
    *   Display `current_V_org_R_alpha`, `recalculated_current_org_ai_r_alpha`.
    *   **Visualization:** Radar Chart and Bar Chart from the notebook.
*   **Navigation:** "Continue to Use Case Identification" button.

#### **Section 3: Identify High-Value AI Use Cases & Estimate Impact (Notebook Section 5)**

*   **Markdown:** "With a clear understanding of the gaps, let's identify specific AI initiatives. Which high-value use cases will directly address the identified gaps and create the most significant impact for the company?"
*   **Input:** `st.multiselect` for `selected_use_case_names`.
*   **Dynamic Inputs for Each Selected Use Case:**
    *   `st.number_input` for 'Investment ($M$)'.
    *   `st.slider` for 'Probability of Success'.
    *   `st.slider` for 'Execution Quality'.
*   **Processing:** For each selected use case, call `estimate_project_parameters` (adapted to take user inputs for investment, probability, and quality) to project `EBITDA Impact ($M)` and `Delta Org-AI-R`.
    *   **Formula (Conceptual, inline):** EBITDA Impact ($M$) for a use case is conceptually derived from a base impact percentage, adjusted by the company's systematic opportunity and idiosyncratic readiness, then scaled by the user's `Probability of Success` and `Execution Quality` factors: $Base\_Impact \times (H_{org,k}^R/100) \times (V_{org,j}^R/100 \times 0.5 + 0.5) \times Probability\_Success \times Execution\_Quality$.
    *   **Formula (Conceptual, inline):** Delta Org-AI-R for a use case is also scaled by user's `Probability of Success` and `Execution Quality` factors from its base potential.
*   **Outputs:** `planned_initiatives_df` displayed as `st.dataframe`, including user-adjusted parameters and derived impacts.
*   **Navigation:** "Continue to Build Multi-Year Plan" button.

#### **Section 4: Build the Multi-Year AI Value Creation Plan (Notebook Section 6)**

*   **Markdown:** "Now, let's integrate these initiatives into a cohesive multi-year plan, projecting the financial and strategic trajectory for the company under your guidance."
*   **Input:** `st.slider` for `Planning Horizon (Years)`.
*   **Processing:** Calls `create_multi_year_plan` with all collected data.
*   **Outputs:**
    *   `ai_plan_trajectory_df` displayed as `st.dataframe`.
    *   **Visualization:** Line Plot for "Cumulative EBITDA Impact".
    *   **Visualization:** Line Plot for "PE Org-AI-R Progression".
*   **Navigation:** "Continue to Portfolio Benchmarking" button.

#### **Section 5: Calculate AI Investment Efficiency & Portfolio Benchmarking (Notebook Section 7 & 8)**

*   **Markdown:** "With the plan defined, it's time to evaluate its efficiency and see how it benchmarks against other companies in our portfolio. This informs fund-level strategy and resource allocation."
*   **Processing:**
    *   Extracts `total_delta_org_ai_r_plan`, `total_investment_plan_M`, `total_ebitda_impact_plan_M` from `ai_plan_trajectory_df`.
    *   Calls `calculate_ai_investment_efficiency`.
    *   Updates `st.session_state.portfolio_companies_df` with the results for the `selected_company`.
    *   Calls `calculate_within_portfolio_percentile` and `calculate_cross_portfolio_z_score`.
*   **Outputs:**
    *   Display `Total Projected Delta Org-AI-R`, `Total Projected AI Investment`, `Total Projected EBITDA Impact`, and `AI Investment Efficiency (AIE)`.
    *   **Formula (Display):** AI Investment Efficiency: $$AIE = \left(\frac{\Delta Org-AI-R}{AI~Investment}\right) \times EBITDA~Impact$$
    *   Updated `portfolio_companies_df` with benchmarking metrics (`Org-AI-R Percentile`, `Org-AI-R Z-Score`) displayed as `st.dataframe`.
    *   **Visualization:** Bar Chart for "Current PE Org-AI-R Scores Across Portfolio Companies".
    *   **Visualization:** Bar Chart for "AI Investment Efficiency Across Portfolio Companies".
*   **Navigation:** "Continue to Exit-Readiness Assessment" button.

#### **Section 6: Exit-Readiness Assessment (Notebook Section 9)**

*   **Markdown:** "Finally, let's project how these AI investments enhance the company's appeal to potential buyers and impact its exit valuation. Crafting a compelling AI narrative is key to maximizing our returns."
*   **Inputs:** `st.slider` widgets for `visible_score`, `documented_score`, `sustainable_score`, and `st.number_input` for `base_multiple`.
*   **Processing:** Calls `assess_exit_readiness` and `predict_exit_multiple`.
*   **Outputs:**
    *   Display `Calculated Exit-AI-R Score`.
    *   Display `Predicted Exit Multiple with AI Premium`.
    *   **Formula (Display):** Exit-AI-R Score: $$Exit-AI-R_j = w_1 \cdot Visible_j + w_2 \cdot Documented_j + w_3 \cdot Sustainable_j$$
    *   **Formula (Display):** Predicted Exit Multiple: $$Multiple_j = Multiple_{base,k} + \delta \cdot \frac{Exit-AI-R_j}{100}$$
*   **Navigation:** "Restart Session" button (or a "View Summary" page with all key results).

