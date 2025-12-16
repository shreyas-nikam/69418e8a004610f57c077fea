id: 69418e8a004610f57c077fea_documentation
summary: AI Value Creation & Investment Efficiency Planner Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: AI Value Creation & Investment Efficiency Planner Codelab

## 1. Introduction: Understanding AI Value Creation in Private Equity
Duration: 05:00

Welcome, aspiring Private Equity Professional! This codelab is designed to guide you through the **QuLab: AI Value Creation & Investment Efficiency Planner**, a Streamlit application built to empower PE professionals in evaluating and optimizing their portfolio companies using Artificial Intelligence.

<aside class="positive">
This codelab will provide a comprehensive understanding of the application's functionalities, underlying models, and the strategic insights it offers. By the end, you'll grasp how AI can be systematically integrated into value creation strategies, quantified, and benchmarked.
</aside>

### The Challenge and the Solution

In today's competitive landscape, leveraging AI is no longer optional for private equity firms. It's a critical driver for enhancing operational efficiency, creating new revenue streams, and ultimately, maximizing exit valuations. However, quantifying AI's impact, building actionable investment roadmaps, and demonstrating tangible value can be complex.

This application provides a structured, data-driven workflow to address these challenges. It enables you to:
1.  **Assess AI Readiness**: Understand a portfolio company's current AI capabilities.
2.  **Identify Opportunities**: Pinpoint high-potential AI initiatives.
3.  **Quantify Impact**: Project the financial (EBITDA) and strategic (Org-AI-R) returns.
4.  **Strategic Planning**: Develop multi-year investment plans.
5.  **Benchmarking**: Compare performance against other portfolio assets.
6.  **Exit Strategy**: Understand AI's contribution to enhanced exit multiples.

### Core Concepts Explained

The application revolves around several key concepts and metrics:

*   **PE Org-AI-R Score ($PE~Org-AI-R_{j,t}$)**: A composite score representing an organization's overall AI readiness at a given time ($t$). It combines internal capabilities and external opportunities.
*   **Idiosyncratic Readiness ($V_{org,j}^R(t)$)**: The company's unique, internal AI capabilities and maturity across various dimensions (e.g., data infrastructure, talent, leadership).
*   **Systematic AI Opportunity ($H_{org,k}^R(t)$)**: The general AI opportunity inherent in the company's specific sector ($k$), reflecting external market trends and industry-specific potential.
*   **Synergy**: A measure of alignment between the company's internal readiness and the external systematic opportunity, calculated as the minimum of $V_{org,j}^R$ and $H_{org,k}^R$.
*   **Screening Score**: An initial high-level assessment of AI potential, combining systematic opportunity with external market signals.
*   **AI Investment Efficiency (AIE)**: A metric that quantifies the return on AI investment, considering both the improvement in Org-AI-R and the financial (EBITDA) impact relative to capital deployed.
*   **Exit-AI-R Score**: A specialized score assessing how well a company's AI capabilities are positioned to drive a premium at exit, considering visibility, documentation, and sustainability.

### Application Architecture and Data Flow

The Streamlit application leverages Python for its backend logic and `pandas`, `numpy`, `matplotlib`, and `seaborn` for data manipulation and visualization. It relies heavily on `st.session_state` to maintain the application's state across user interactions, ensuring a consistent and interactive experience.

Here's a conceptual data flow:

1.  **Initialization**: Global model coefficients, systematic opportunity scores, and dimension weights are loaded. A sample portfolio of companies is initialized into `st.session_state`.
2.  **Company Selection**: User selects a company, triggering updates to `st.session_state` with company-specific data (sector, EBITDA, initial ratings).
3.  **Dimension Assessment**: User inputs (or simulated defaults) for AI dimension ratings are processed to calculate Idiosyncratic Readiness.
4.  **Use Case Planning**: Based on sector and readiness, high-value AI use cases are presented. User inputs for investment, probability of success, and execution quality are used to estimate financial and strategic impacts.
5.  **Multi-Year Plan Generation**: Selected initiatives are aggregated over a planning horizon to project cumulative investment, EBITDA impact, and Org-AI-R progression.
6.  **Benchmarking**: Calculated efficiency metrics and Org-AI-R scores for the selected company are compared against the entire portfolio.
7.  **Exit Readiness**: Additional qualitative inputs assess AI's contribution to exit value, projecting an AI premium on the exit multiple.

This iterative process allows for detailed scenario planning and strategic decision-making.

### Running the Streamlit Application

To run the application yourself, save the provided Python code as `app.py` (or any other `.py` file) and execute it from your terminal:

```console
streamlit run app.py
```

This will open the application in your default web browser.



## 2. Step 1: Company Selection and Initial Org-AI-R Assessment
Duration: 07:00

Our journey begins with selecting a portfolio company and conducting a high-level screening. This step provides an initial estimate of the company's AI readiness and potential, guiding whether to pursue a deeper dive.

The primary goal here is to calculate an **Initial PE Org-AI-R Score** and a **Screening Score**.

### How it Works

1.  **Select Portfolio Company**: You choose a company from a pre-defined list. This action updates relevant `st.session_state` variables with the company's sector and initial EBITDA.
2.  **Systematic AI Opportunity ($H_{org,k}^R$)**: This score is automatically retrieved based on the selected company's sector from the `systematic_opportunity_scores` dictionary. It represents the inherent AI potential in that industry.
    ```python
    systematic_opportunity_scores = {
        'Manufacturing': 72, 'Healthcare': 78, 'Retail': 75,
        'Business Services': 80, 'Technology': 85
    }
    ```
3.  **Simulated Baseline Idiosyncratic Readiness ($V_{org,j}^R$)**: This is a preliminary, high-level estimate of the company's internal AI capabilities. In a real-world scenario, this might come from initial due diligence or expert opinion. For this app, it's a simulated input you can adjust.
4.  **Initial PE Org-AI-R Score Calculation**: This is a weighted average of the company's idiosyncratic readiness and the sector's systematic opportunity, with a synergy component. The `calculate_org_ai_r` function performs this:
    ```python
    def calculate_org_ai_r(V_org_R, H_org_k_R, synergy_score, alpha, beta):
        return round((alpha * V_org_R) + ((1 - alpha) * H_org_k_R) + (beta * synergy_score), 2)
    ```
    The coefficients `alpha` (weight on idiosyncratic readiness) and `beta` (synergy coefficient) are defined in `model_coefficients`.
    $$PE~Org-AI-R_{j,t} = \alpha \cdot V_{org,j}^R(t) + (1 - \alpha) \cdot H_{org,k}^R(t) + \beta \cdot Synergy(V_{org,j}^R, H_{org,k}^R)$$
    Where the `Synergy` is defined as:
    $$Synergy = \min(V_{org,j}^R, H_{org,k}^R)$$
5.  **Simulated External Signals Score**: This represents external market intelligence, such as news mentions or job postings related to AI. This is another simulated input.
6.  **Initial Screening Score Calculation**: This score helps prioritize companies for deeper AI evaluation by combining the systematic opportunity with external signals. The `calculate_screening_score` function handles this:
    ```python
    def calculate_screening_score(H_org_k_R, external_signals_score, epsilon):
        return round(H_org_k_R + (epsilon * external_signals_score), 2)
    ```
    Here, `epsilon` (screening score weight for external signals) is also from `model_coefficients`.
    $$Screen_{j} = H_{org,k}^R + \epsilon \cdot ExternalSignals_j$$
7.  **Screening Recommendation**: Based on the calculated scores, the application provides a preliminary recommendation (e.g., "Strong AI candidate," "Promising AI candidate," "Watchlist").

<aside class="positive">
The use of `st.session_state` is critical for maintaining persistence. When you select a company using `st.selectbox` and its `key` is set to `selected_company`, the `st.session_state.selected_company` variable is automatically updated. The `_reset_company_specific_state` function is then called to re-initialize all other company-dependent variables in `st.session_state`.
</aside>

### Your Task

Interact with the `Select Portfolio Company` dropdown and adjust the `Simulated Baseline Idiosyncratic Readiness` and `Simulated External Signals Score`. Observe how the `Initial PE Org-AI-R Score` and `Initial Screening Score` change, and how this influences the `Screening Recommendation`.



## 3. Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis
Duration: 12:00

Having identified a promising candidate in Step 1, this phase delves into a granular assessment of the company's AI capabilities across seven critical dimensions. This deep dive is crucial for understanding specific strengths, weaknesses, and identifying areas for targeted investment.

The core output of this step is a detailed `Dimension-Level Assessment` and a **Recalculated PE Org-AI-R Score** based on your expert inputs.

### How it Works

1.  **Seven Key AI Dimensions**: The assessment covers: `Data Infrastructure`, `AI Governance`, `Technology Stack`, `Talent`, `Leadership`, `Use Case Portfolio`, and `Culture`.
2.  **User Assessment (1-5 Ratings)**: For each dimension, you provide two ratings using sliders:
    *   **Current Rating**: Your assessment of the company's current maturity (1=Novice, 5=Expert).
    *   **Target Rating**: The desired future state for that dimension.
    *   The `simulate_dimension_ratings` function provides initial values, but you can override them. These ratings are stored in `st.session_state` (e.g., `st.session_state.current_rating_data_infrastructure`).
3.  **Dimension Score Calculation**: Each rating is converted to a score out of 100:
    ```python
    def calculate_dimension_score(ratings):
        return ((ratings / 5) * 100).round(2)
    ```
    $$D_k = \frac{Rating_{k}}{5} \times 100$$
4.  **Dimension-Level Assessment Table**: A DataFrame is generated showing current ratings, current scores, target ratings, target scores, and the `Gap` (Target Score - Current Score) for each dimension.
    $$Gap_k = D_k^{target} - D_k^{current}$$
    This table helps visually identify critical areas for improvement, highlighted by a color gradient.
5.  **Idiosyncratic Readiness ($V_{org,j}^R$) Recalculation**: This is a weighted sum of the dimension scores. Crucially, the weights are not uniform; they are adjusted based on the company's sector, reflecting that certain dimensions are more critical in different industries.
    *   `general_dimension_weights`: Baseline weights for all dimensions.
    *   `sector_dimension_weight_adjustments`: Specific adjustments for each sector.
    *   The `get_all_dimension_weights_df` function combines these.
    *   The `calculate_V_org_R` function applies these weights:
        ```python
        def calculate_V_org_R(dimension_scores, sector_weights):
            aligned_scores = dimension_scores.reindex(sector_weights.index, fill_value=0)
            weighted_sum = (aligned_scores * sector_weights).sum()
            return round(weighted_sum, 2)
        ```
6.  **Recalculated PE Org-AI-R Score**: Using the newly calculated `current_V_org_R_alpha` (based on detailed assessment), the PE Org-AI-R score is re-evaluated with the `H_org_k_R` from Step 1 and the synergy factor. This refined score provides a more accurate representation of the company's AI readiness post-deep dive.
7.  **Visual Gap Analysis**:
    *   **Radar Chart**: Compares the `Current Score` vs. `Target Score` across all dimensions, giving an immediate visual overview of gaps and strengths.
    *   **Bar Chart**: Ranks dimensions by `Gap (Target - Current)`, clearly showing priority areas for investment.

### Your Task

Adjust the `Current Rating` and `Target Rating` sliders for the different dimensions. Observe how the `Dimension-Level Assessment` table, `Idiosyncratic Readiness`, and `Recalculated PE Org-AI-R Score` change. Pay close attention to the Radar and Bar charts to identify the most significant gaps that AI initiatives should target.



## 4. Step 3: Identify High-Value AI Use Cases & Estimate Impact
Duration: 10:00

With a detailed understanding of the company's AI readiness and specific capability gaps, the next step is to select high-impact AI initiatives. This phase allows you to identify concrete projects and estimate their potential financial (EBITDA) and strategic (Org-AI-R) returns.

### How it Works

1.  **Sector-Specific Use Cases**: The application presents a list of `High-Value AI Use Cases` relevant to the `selected_sector`. These are loaded from the `high_value_use_cases` dictionary.
    ```python
    high_value_use_cases = {
        'Manufacturing': pd.DataFrame([...]),
        'Healthcare': pd.DataFrame([...]),
        ...
    }
    ```
    Each use case has predefined characteristics like `Complexity`, `Timeline (months)`, and `EBITDA Impact (min%)` / `(max%)`.
2.  **Select Use Cases**: You can select multiple AI use cases using the `st.multiselect` widget.
3.  **Customize Project Parameters**: For each selected use case, you can adjust key parameters that influence its impact:
    *   **Estimated Investment Cost ($M$)**: The capital required for the project.
    *   **Probability of Success (0-1)**: Your confidence in successful implementation.
    *   **Execution Quality Factor (0-1)**: How well the project is expected to be executed, influencing realized benefits.
    *   The `estimate_project_parameters` function provides intelligent defaults for these based on the use case's complexity and the company's current `V_org_R` and `H_org_k_R`.
4.  **Impact Estimation**: The `estimate_project_parameters` function is central to quantifying the project's returns. It calculates:
    *   **EBITDA Impact ($M$)**: The projected increase in EBITDA. This is influenced by the use case's base impact, company's readiness, and your success/quality factors.
        $$EBITDA~Impact~(\$M) = Base\_Impact~(\%) \times \frac{H_{org,k}^R}{100} \times \left(\frac{V_{org,j}^R}{100} \times 0.5 + 0.5\right) \times Probability\_Success \times Execution\_Quality \times Initial\_EBITDA~(\$M)$$
        where $Base\_Impact~(\%)$ is the inherent EBITDA impact of the use case, adjusted by the company's systematic opportunity ($H_{org,k}^R$), idiosyncratic readiness ($V_{org,j}^R$), and scaled by your assessed Probability of Success and Execution Quality, applied to the company's initial EBITDA.
    *   **Delta Org-AI-R**: The projected improvement in the company's overall Org-AI-R score.
        $$\Delta Org-AI-R = Base\_Delta \times Probability\_Success \times Execution\_Quality$$
        where $Base\_Delta$ is the inherent Org-AI-R improvement potential of the use case, scaled by your assessed Probability of Success and Execution Quality.
5.  **Planned AI Initiatives Table**: All selected and estimated use cases are compiled into a DataFrame, providing a clear overview of each project's expected costs and benefits. This DataFrame is stored in `st.session_state.planned_initiatives_df`.

<aside class="negative">
Failing to select any use cases in this step will prevent the generation of a multi-year plan in the subsequent step, limiting the full functionality of the application.
</aside>

### Your Task

Select 2-3 high-value AI use cases relevant to the company and its identified gaps. Experiment with adjusting the `Estimated Investment Cost`, `Probability of Success`, and `Execution Quality Factor` for each. Observe how these changes affect the estimated `EBITDA Impact ($M$)` and `Delta Org-AI-R`.



## 5. Step 4: Build the Multi-Year AI Value Creation Plan
Duration: 08:00

This step integrates your selected AI initiatives into a strategic multi-year plan, projecting the company's financial and strategic trajectory. This provides a clear roadmap for investment and expected returns over time.

### How it Works

1.  **Planning Horizon**: You define the duration of your plan (e.g., 1 to 5 years). This is controlled by the `planning_horizon` slider and stored in `st.session_state`.
2.  **Multi-Year Trajectory Creation**: The `create_multi_year_plan` function takes the initial Org-AI-R, initial EBITDA, and the `planned_initiatives_df` (from Step 3) to generate a year-by-year projection.
    ```python
    def create_multi_year_plan(company_name, initial_org_ai_r, initial_ebitda_M, planned_initiatives_df, H_org_k_R, total_years=3):
        # ... logic to assign project impacts and investments to specific years based on timelines ...
        # ... calculates cumulative Org-AI-R, EBITDA Impact, and Investment per year ...
        return pd.DataFrame(plan_trajectory)
    ```
    The function intelligently distributes the `Investment ($M$)` and `Delta Org-AI-R` from each initiative across the years until its `Timeline (months)` is completed. The `EBITDA Impact ($M$)` starts accruing annually from the completion year of each project.
3.  **Plan Trajectory Table**: The `st.session_state.ai_plan_trajectory_df` DataFrame presents the year-by-year breakdown of:
    *   `Org-AI-R`: The evolving AI readiness score.
    *   `EBITDA Impact ($M$) - Annual`: New EBITDA generated in that year.
    *   `Cumulative EBITDA Impact ($M$)`: Total EBITDA generated up to that year.
    *   `Investment ($M$) - Annual`: Capital deployed in that year.
    *   `Cumulative Investment ($M$)`: Total capital deployed up to that year.
4.  **Visualizations**:
    *   **Cumulative EBITDA Impact Chart**: A line plot showing the projected growth of cumulative EBITDA impact over the planning horizon. This directly visualizes the financial value accretion.
    *   **PE Org-AI-R Progression Chart**: A line plot illustrating the projected improvement of the company's Org-AI-R score over the years, demonstrating strategic capability development.

<aside class="positive">
This step is crucial for communicating the long-term vision and quantifiable returns of your AI strategy to stakeholders. The cumulative charts provide a powerful narrative for value creation.
</aside>

### Your Task

Adjust the `Planning Horizon (Years)` and observe how the `Multi-Year AI Plan Trajectory` table and its associated charts change. Reflect on how this plan aligns with the company's overall strategic goals and potential exit timelines.



## 6. Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking
Duration: 10:00

Now that you have a multi-year plan, it's time to evaluate its effectiveness and compare the company's performance against others in your portfolio. This step provides crucial insights for fund-level strategy, resource allocation, and identifying top-performing assets.

### How it Works

1.  **AI Investment Efficiency (AIE) Calculation**: The AIE metric quantifies the return on your AI investment, considering both the improvement in AI capabilities ($\Delta$ Org-AI-R) and the financial impact (EBITDA) relative to the capital deployed.
    ```python
    def calculate_ai_investment_efficiency(delta_org_ai_r, total_ai_investment_M, total_ebitda_impact_M):
        if total_ai_investment_M <= 0: return 0.0
        aie_score = (delta_org_ai_r / total_ai_investment_M) * total_ebitda_impact_M
        return round(aie_score, 2)
    ```
    $$AIE = \left(\frac{\Delta Org-AI-R}{AI~Investment}\right) \times EBITDA~Impact$$
    where $\Delta Org-AI-R$ is the total change in the Org-AI-R score, $AI~Investment$ is the total capital deployed, and $EBITDA~Impact$ is the total financial gain (all over the planning horizon).
    The `Delta Org-AI-R`, `Total AI Investment`, and `Total Cumulative EBITDA Impact` are taken from the final year of your multi-year plan.
2.  **Portfolio Data Update**: The `portfolio_companies_df` in `st.session_state` is updated with the calculated `Current Org-AI-R`, `Delta Org-AI-R`, `Investment ($M$)`, `EBITDA Impact ($M$)`, and `Efficiency (pts/$M$)` for the selected company.
3.  **Benchmarking Metrics**:
    *   **Within-Portfolio Percentile**: Shows how the selected company's `Current Org-AI-R` ranks among all companies in the portfolio.
        ```python
        def calculate_within_portfolio_percentile(company_org_ai_r, portfolio_org_ai_rs):
            # ... logic to calculate percentile ...
        ```
        $$Percentile_j = \left( \frac{\text{Number of companies with } Org-AI-R \le Org-AI-R_j}{\text{Total number of companies}} \right) \times 100$$
    *   **Cross-Portfolio Z-Score**: Measures how many standard deviations the company's `Current Org-AI-R` is from the portfolio mean, indicating its relative strength or weakness.
        ```python
        def calculate_cross_portfolio_z_score(company_org_ai_r, industry_mean, industry_std):
            # ... logic to calculate z-score ...
        ```
        $$Z-Score_j = \frac{Org-AI-R_j - \mu_{portfolio}}{\sigma_{portfolio}}$$
        where $\mu_{portfolio}$ is the mean and $\sigma_{portfolio}$ is the standard deviation of Org-AI-R scores across the portfolio.
4.  **Benchmarking Visualizations**:
    *   **Current PE Org-AI-R Scores Across Portfolio Companies**: A bar chart comparing the Org-AI-R of all portfolio companies, with the selected company highlighted.
    *   **AI Investment Efficiency Across Portfolio Companies**: A bar chart comparing the AIE scores, highlighting which companies are most efficient in their AI capital deployment.

<aside class="positive">
Benchmarking provides a strategic lens, allowing you to identify which assets are AI leaders, which are laggards, and where to best allocate future fund resources for maximum impact across the entire portfolio.
</aside>

### Your Task

Review the `AI Investment Efficiency` score for your selected company. Compare its `Org-AI-R Percentile` and `Z-Score` to understand its standing. Analyze the benchmarking bar charts to see how your company measures up against its peers in both AI readiness and investment efficiency.



## 7. Step 6: Exit-Readiness Assessment
Duration: 08:00

The final stage of our planner focuses on how AI investments ultimately enhance a company's appeal to potential buyers and impact its exit valuation. Crafting a compelling AI narrative is key to maximizing returns.

### How it Works

1.  **Exit-AI-R Assessment Inputs**: You assess three crucial aspects influencing exit value:
    *   **Visible AI Capabilities Score (0-100)**: How readily apparent are the company's AI features and technology to an external party?
    *   **Documented AI Impact Score (0-100)**: The quality and availability of auditable data demonstrating AI's financial impact (ROI, cost savings).
    *   **Sustainable AI Capabilities Score (0-100)**: Are AI capabilities deeply embedded in the company's processes, talent, and infrastructure, ensuring long-term defensibility?
    These are controlled by sliders and stored in `st.session_state`.
2.  **Exit-AI-R Score Calculation**: These three scores are combined using predefined weights to calculate the `Exit-AI-R Score`.
    ```python
    def assess_exit_readiness(visible_score, documented_score, sustainable_score, w1, w2, w3):
        return round((w1 * visible_score) + (w2 * documented_score) + (w3 * sustainable_score), 2)
    ```
    $$Exit-AI-R_j = w_1 \cdot Visible_j + w_2 \cdot Documented_j + w_3 \cdot Sustainable_j$$
    where $Visible_j$, $Documented_j$, and $Sustainable_j$ are scores reflecting the market-facing aspects of AI, and $w_1, w_2, w_3$ are their respective weights from `model_coefficients` (`w1_exit`, `w2_exit`, `w3_exit`).
3.  **Baseline Exit Multiple**: This is the assumed pre-AI or industry-average valuation multiple for the company's sector. Default values are provided based on the sector from `sector_base_multiples`. You can adjust this input.
4.  **Predicted Exit Multiple with AI Premium**: The `Exit-AI-R Score` is then used to calculate an AI premium, which is added to the `Baseline Exit Multiple`.
    ```python
    def predict_exit_multiple(base_multiple, exit_ai_r, delta):
        return round(base_multiple + (delta * exit_ai_r / 100), 2)
    ```
    $$Multiple_j = Multiple_{base,k} + \delta \cdot \frac{Exit-AI-R_j}{100}$$
    where $Multiple_{base,k}$ is the baseline multiple for the sector, $Exit-AI-R_j$ is the assessed Exit-AI-R score, and $\delta$ is the AI premium coefficient (`delta_exit`) from `model_coefficients`.
5.  **Projected EBITDA at Exit**: This uses the initial EBITDA plus the cumulative EBITDA impact from your multi-year plan (from Step 4, automatically updated in `st.session_state.portfolio_companies_df`).
6.  **Implied Valuation**: The final projected EBITDA is multiplied by the `Predicted Exit Multiple` to give an `Implied Valuation`.

<aside class="positive">
The `Exit-AI-R Score` and the predicted valuation uplift provide a quantifiable narrative for exit. They demonstrate how strategic AI investments can directly translate into enhanced investor returns, a key focus for any PE firm.
</aside>

### Your Task

Adjust the `Visible`, `Documented`, and `Sustainable AI Capabilities Scores`, along with the `Baseline Exit Multiple`. Observe how these influence the `Exit-AI-R Score`, `Predicted Exit Multiple`, and ultimately, the `Implied Valuation`. Reflect on how you would articulate this value creation story to potential buyers.

You have successfully navigated the **QuLab: AI Value Creation & Investment Efficiency Planner**! You've moved from initial screening to detailed assessment, strategic planning, benchmarking, and exit valuation. To explore another company, click the "Restart Session" button in the sidebar.
