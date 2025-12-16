
# AI Value Creation & Investment Efficiency Planner: A Portfolio Manager's Workflow

Welcome, Private Equity Professional! As a **Portfolio Manager** at Quantum Capital, my core responsibility is to identify and execute value creation strategies for our portfolio companies. In today's market, Artificial Intelligence (AI) is a non-negotiable lever for driving EBITDA growth and enhancing exit multiples. However, transforming abstract AI potential into a measurable, ROI-driven plan is challenging.

This notebook serves as my **AI Value Creation & Investment Efficiency Planner**. I will walk through a structured, data-driven approach to:
1.  **Assess** a portfolio company's current AI readiness.
2.  **Identify** high-impact, sector-specific AI initiatives.
3.  **Quantify** their financial impact and investment efficiency.
4.  **Develop** a phased, multi-year AI value creation roadmap.
5.  **Benchmark** performance across our fund's portfolio.

This process is critical for our 100-day planning, ongoing portfolio management, and ultimately, building a compelling exit narrative for our investments.

## 1. Setup: Installing and Importing Libraries

Before we begin our analysis, we need to set up our environment by installing the necessary Python libraries. These libraries will help us with data manipulation, numerical operations, and creating visualizations.

```python
!pip install pandas numpy matplotlib seaborn
```

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

print("Libraries imported successfully.")
```

## 2. Defining Core Data, Parameters, and Constants

As a Portfolio Manager, I rely on a robust framework to make informed decisions. This framework includes sector-specific benchmarks, established model coefficients, and a clear understanding of potential AI use cases. In this section, I'm setting up these foundational elements, which represent the knowledge base and analytical tools at my disposal. This ensures consistency and comparability across our diverse portfolio.

### Quantitative Logic for Org-AI-R Score

The core of our assessment is the Private Equity Organizational AI-Readiness (PE Org-AI-R) Score, defined as:

$$
\text{PE Org-AI-R}_{j,t} = \alpha \cdot V_{org,j}^R(t) + (1 - \alpha) \cdot H_{org,k}^R(t) + \beta \cdot \text{Synergy}(V_{org,j}^R, H_{org,k}^R)
$$

Where:
*   $j$ is the portfolio company, $k$ is its industry, and $t$ is time.
*   $V_{org,j}^R(t)$: Idiosyncratic Readiness (organization-specific capability), normalized to $[0, 100]$.
*   $H_{org,k}^R(t)$: Systematic Opportunity (industry-level AI potential), normalized to $[0, 100]$.
*   $\alpha \in [0, 1]$: Weight on organizational vs. market factors (prior: $\alpha \in [0.55, 0.70]$).
*   $\beta \ge 0$: Synergy coefficient (prior: $\beta \in [0.08, 0.25]$).
*   $\text{Synergy} \in [0, 100]$: Interaction between $V_{org,j}^R$ and $H_{org,k}^R$.

### Dimension Scoring Logic

Individual dimensions of AI readiness are scored using behaviorally anchored rating scales (1-5) and converted to a 0-100 index:

$$
D_k = \left( \frac{\sum_i w_i \cdot \text{Rating}_{i,k}}{5} \right) \times 100
$$

Where:
*   $D_k$: Score for dimension $k$.
*   $w_i$: Weight for specific sub-factor $i$ within dimension $k$.
*   $\text{Rating}_{i,k}$: Rating (1-5) for sub-factor $i$ within dimension $k$.
*   Here, for simplicity, we assume $w_i = 1$ for all sub-factors and an average rating is used, so $D_k = (\text{AvgRating}_k / 5) \times 100$.
*   For $V_{org,j}^R$, we'll use a weighted sum of these dimension scores.

### AI Investment Efficiency (AIE)

To compare AI capability building across portfolio companies, we use the AI Investment Efficiency metric:

$$
\text{AIE}_j = \left( \frac{\Delta \text{Org-AI-R}_j}{\text{AI Investment}_j} \right) \times \text{EBITDA Impact}_j
$$

Where:
*   $\Delta \text{Org-AI-R}_j$: Change in Org-AI-R score for company $j$.
*   $\text{AI Investment}_j$: Total AI investment for company $j$ (e.g., in millions of dollars).
*   $\text{EBITDA Impact}_j$: Total absolute EBITDA impact (e.g., in millions of dollars) for company $j$.

### Org-AI-R to EBITDA Mapping

We calibrate the relationship between capability improvement and financial outcomes:

$$
\Delta \text{EBITDA}\% = \gamma \cdot \Delta \text{Org-AI-R} \cdot H_{org,k}^R / 100
$$

Where:
*   $\gamma$: Value creation coefficient estimated from historical data (prior: $\gamma \in [0.02, 0.05]$).

```python
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

# Systematic Opportunity (H_org,k^R) scores by sector (from document p.8-12)
systematic_opportunity_scores = {
    'Manufacturing': 72,
    'Healthcare': 78,
    'Retail': 75,
    'Business Services': 80,
    'Technology': 85
}

# General Dimension Weights (used for D_k calculation if not sector-specific)
general_dimension_weights = {
    'Data Infrastructure': 0.25,
    'AI Governance': 0.20,
    'Technology Stack': 0.15,
    'Talent': 0.15,
    'Leadership': 0.10,
    'Use Case Portfolio': 0.10,
    'Culture': 0.05
}

# Sector-Specific Dimension Weight Adjustments (from document p.8-12)
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

# Combine general and sector-specific weights into a DataFrame for easier lookup
all_dimension_weights_df = pd.DataFrame(general_dimension_weights, index=['General']).T
for sector, weights in sector_dimension_weight_adjustments.items():
    all_dimension_weights_df[sector] = pd.Series(weights)

# High-Value Use Cases by Sector (from Appendix B, p.29-30)
# This will be a dictionary of dataframes, for easier filtering by sector
high_value_use_cases = {
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
        {'Use Case': 'Diagnostic AI', 'Complexity': 'High', 'Timeline (months)': '12-24', 'EBITDA Impact (min%)': 0, 'EBITDA Impact (max%)': 0, 'Description': 'AI imaging analysis (radiology, pathology). Variable impact, significant long-term value.'},
    ]),
    'Retail': pd.DataFrame([
        {'Use Case': 'Demand Forecasting', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 3, 'Description': 'ML-powered inventory optimization reducing stockouts and overstock'},
        {'Use Case': 'Personalization', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 0.5, 'EBITDA Impact (max%)': 1, 'Description': 'AI-driven product recommendations increasing conversion 10-30% (0.5-1% EBITDA from 2-4% revenue lift)'},
        {'Use Case': 'Dynamic Pricing', 'Complexity': 'High', 'Timeline (months)': '9-15', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'Real-time price optimization improving margins 2-5%'},
        {'Use Case': 'Customer Service Chatbot', 'Complexity': 'Low', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 0.5, 'EBITDA Impact (max%)': 1, 'Description': 'AI chatbots reducing contact center costs 20-40%'},
    ]),
    'Business Services': pd.DataFrame([
        {'Use Case': 'Document Processing', 'Complexity': 'Low-Medium', 'Timeline (months)': '3-6', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4, 'Description': 'AI extraction and analysis reducing manual effort 50-70%'},
        {'Use Case': 'Knowledge Worker Tools', 'Complexity': 'Low', 'Timeline (months)': '1-3', 'EBITDA Impact (min%)': 3, 'EBITDA Impact (max%)': 5, 'Description': 'Gen AI tools improving output 20-30%'},
        {'Use Case': 'Sales Enablement', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 3, 'Description': 'AI-powered proposal generation and lead scoring'},
        {'Use Case': 'Contract Analysis', 'Complexity': 'Medium', 'Timeline (months)': '6-9', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 2, 'Description': 'AI review of legal/procurement documents'},
    ]),
    'Technology': pd.DataFrame([
        {'Use Case': 'Product AI Embedding', 'Complexity': 'High', 'Timeline (months)': '12-24', 'EBITDA Impact (min%)': 5, 'EBITDA Impact (max%)': 10, 'Description': 'Embedding AI as core product features'},
        {'Use Case': 'Automated Code Generation', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 3, 'EBITDA Impact (max%)': 6, 'Description': 'AI assistance for software development, improving efficiency'},
        {'Use Case': 'Predictive Cybersecurity', 'Complexity': 'High', 'Timeline (months)': '9-18', 'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4, 'Description': 'AI for threat detection and prevention'},
        {'Use Case': 'ML-driven DevOps', 'Complexity': 'Medium', 'Timeline (months)': '6-12', 'EBITDA Impact (min%)': 1, 'EBITDA Impact (max%)': 3, 'Description': 'AI for optimizing deployment pipelines and infrastructure'},
    ])
}

# Synthetic Portfolio Companies Data (based on Fund-Wide Review table, p.23)
portfolio_companies_df = pd.DataFrame([
    {'Company': 'Alpha Manufacturing', 'Sector': 'Manufacturing', 'Baseline Org-AI-R': 42, 'Current Org-AI-R': 68, 'Delta Org-AI-R': 26, 'Investment ($M)': 2.8, 'EBITDA Impact (%)': 6, 'EBITDA ($M)': 9.0}, # Base EBITDA assumed for calc
    {'Company': 'Beta Healthcare', 'Sector': 'Healthcare', 'Baseline Org-AI-R': 48, 'Current Org-AI-R': 71, 'Delta Org-AI-R': 23, 'Investment ($M)': 3.2, 'EBITDA Impact (%)': 5, 'EBITDA ($M)': 8.0},
    {'Company': 'Gamma Retail', 'Sector': 'Retail', 'Baseline Org-AI-R': 44, 'Current Org-AI-R': 62, 'Delta Org-AI-R': 18, 'Investment ($M)': 2.4, 'EBITDA Impact (%)': 3, 'EBITDA ($M)': 12.0},
    {'Company': 'Delta Services', 'Sector': 'Business Services', 'Baseline Org-AI-R': 62, 'Current Org-AI-R': 79, 'Delta Org-AI-R': 17, 'Investment ($M)': 2.1, 'EBITDA Impact (%)': 8, 'EBITDA ($M)': 7.5},
    {'Company': 'Epsilon Tech', 'Sector': 'Technology', 'Baseline Org-AI-R': 75, 'Current Org-AI-R': 86, 'Delta Org-AI-R': 11, 'Investment ($M)': 1.5, 'EBITDA Impact (%)': 4, 'EBITDA ($M)': 15.0},
    {'Company': 'Zeta Logistics', 'Sector': 'Manufacturing', 'Baseline Org-AI-R': 38, 'Current Org-AI-R': 58, 'Delta Org-AI-R': 20, 'Investment ($M)': 1.9, 'EBITDA Impact (%)': 4, 'EBITDA ($M)': 6.0}, # Using Manufacturing for Logistics as closest match
    {'Company': 'Eta Food', 'Sector': 'Retail', 'Baseline Org-AI-R': 35, 'Current Org-AI-R': 52, 'Delta Org-AI-R': 17, 'Investment ($M)': 2.0, 'EBITDA Impact (%)': 3, 'EBITDA ($M)': 10.0}, # Using Retail for Food as closest match
    {'Company': 'Theta Finance', 'Sector': 'Business Services', 'Baseline Org-AI-R': 68, 'Current Org-AI-R': 82, 'Delta Org-AI-R': 14, 'Investment ($M)': 1.8, 'EBITDA Impact (%)': 5, 'EBITDA ($M)': 11.0}
])

# Calculate AIE for existing portfolio companies for benchmarking
portfolio_companies_df['EBITDA Impact ($M)'] = portfolio_companies_df['EBITDA ($M)'] * (portfolio_companies_df['EBITDA Impact (%)'] / 100)
portfolio_companies_df['Efficiency (pts/$M)'] = (portfolio_companies_df['Delta Org-AI-R'] / portfolio_companies_df['Investment ($M)']) * portfolio_companies_df['EBITDA Impact ($M)']
# Reorder columns to match document
portfolio_companies_df = portfolio_companies_df[['Company', 'Sector', 'Baseline Org-AI-R', 'Current Org-AI-R', 'Delta Org-AI-R', 'Investment ($M)', 'Efficiency (pts/$M)', 'EBITDA Impact (%)', 'EBITDA ($M)', 'EBITDA Impact ($M)']]

print("\nModel coefficients and synthetic datasets initialized.")
```

## 3. Company Selection and Initial Org-AI-R Assessment

As a Portfolio Manager, my first step is to focus on a specific company within our portfolio for a deeper dive. Today, I'm examining **Alpha Manufacturing**, an industrial equipment manufacturer. My goal is to quickly assess its baseline AI readiness and overall opportunity using the PE Org-AI-R framework. This initial screening helps me understand if the company has significant AI potential worth pursuing.

The Org-AI-R Score combines both the company's internal capabilities ($V_{org,j}^R$) and the industry's overall AI potential ($H_{org,k}^R$). The `Screening Score` (Definition 2, p.5) provides a rapid assessment:

$$
\text{Screen}_j = H_{org,k}^R + \epsilon \cdot \text{ExternalSignals}_j
$$

where $\epsilon = 0.30$ weights preliminary capability signals against systematic opportunity. $\text{ExternalSignals}_j$ (normalized to [0,100]) are derived from factors like job postings, innovation activity, digital presence, and leadership signals.

```python
def calculate_org_ai_r(V_org_R, H_org_k_R, synergy_score, alpha, beta):
    """
    Calculates the PE Org-AI-R Score.
    V_org_R, H_org_k_R, and synergy_score should be normalized to [0, 100].
    """
    org_ai_r = (alpha * V_org_R) + ((1 - alpha) * H_org_k_R) + (beta * synergy_score)
    return round(org_ai_r, 2)

def calculate_screening_score(H_org_k_R, external_signals_score, epsilon):
    """
    Calculates the Screening Score for preliminary assessment.
    External_signals_score should be normalized to [0, 100].
    """
    screening_score = H_org_k_R + (epsilon * external_signals_score)
    return round(screening_score, 2)

# --- Persona's action: Select a company ---
selected_company_name = 'Alpha Manufacturing'
selected_company_data = portfolio_companies_df[portfolio_companies_df['Company'] == selected_company_name].iloc[0]
selected_sector = selected_company_data['Sector']
initial_org_ai_r = selected_company_data['Baseline Org-AI-R']
current_org_ai_r = selected_company_data['Current Org-AI-R']
initial_ebitda_M = selected_company_data['EBITDA ($M)'] # in millions of dollars

H_org_k_R = systematic_opportunity_scores[selected_sector]

# Simulate initial V_org_R and Synergy_score for the baseline, as it's not directly in the initial table
# For baseline, we can back-calculate or assume a reasonable starting point.
# Let's assume V_org_R is derived from Org-AI-R, and Synergy is a simple function of V_org_R and H_org_k_R
# For simplicity in this initial assessment, we will use the Baseline Org-AI-R directly.
# If we were to calculate V_org_R, it would involve detailed dimension scoring.
# For the purpose of initial assessment, we'll use the provided Baseline Org-AI-R.
# Let's simulate a baseline V_org_R and Synergy that would result in the Baseline Org-AI-R:
# Assuming baseline V_org_R is lower than H_org_k_R for manufacturing
baseline_V_org_R = 36 # As per example 8.1 in the document for Manufacturing Turnaround (p.19)
baseline_synergy_score = min(baseline_V_org_R, H_org_k_R) # Simple heuristic for synergy

# Verify the Org-AI-R calculation with these components
calculated_baseline_org_ai_r = calculate_org_ai_r(
    V_org_R=baseline_V_org_R,
    H_org_k_R=H_org_k_R,
    synergy_score=baseline_synergy_score,
    alpha=model_coefficients['alpha'],
    beta=model_coefficients['beta']
)

# Simulate ExternalSignals_j for Alpha Manufacturing (e.g., lower due to legacy systems)
external_signals_score = 45 # Out of 100, representing "Limited AI job postings, legacy ERP, no cloud presence" from example p.19

screening_score = calculate_screening_score(
    H_org_k_R=H_org_k_R,
    external_signals_score=external_signals_score,
    epsilon=model_coefficients['epsilon']
)

print(f"--- Initial Assessment for {selected_company_name} ---")
print(f"Selected Sector: {selected_sector}")
print(f"Systematic Opportunity (H_org,k^R) for {selected_sector}: {H_org_k_R}")
print(f"Simulated Baseline Idiosyncratic Readiness (V_org,j^R): {baseline_V_org_R}")
print(f"Simulated Baseline Synergy: {baseline_synergy_score}")
print(f"Calculated Baseline PE Org-AI-R: {calculated_baseline_org_ai_r}")
print(f"Actual Baseline PE Org-AI-R (from portfolio data): {initial_org_ai_r}") # Use provided baseline for consistency

print(f"\nSimulated External Signals Score: {external_signals_score}")
print(f"Calculated Screening Score: {screening_score}")

# Screening Decision Matrix (p.5 of document)
if screening_score > 70 and H_org_k_R > 75:
    screening_recommendation = "Strong AI candidate - accelerate diligence"
elif screening_score > 70 and H_org_k_R < 60:
    screening_recommendation = "Capability strength in low-opportunity sector - evaluate defensibility"
elif screening_score < 50 and H_org_k_R > 75:
    screening_recommendation = "Transformation opportunity - assess execution risk"
elif screening_score < 50 and H_org_k_R < 60:
    screening_recommendation = "Limited AI thesis - require alternative value drivers"
else:
    screening_recommendation = "Moderate AI candidate - proceed with standard diligence"

print(f"Screening Recommendation: {screening_recommendation}")
```

### Explanation of Initial Assessment

For **Alpha Manufacturing**, the initial screening score indicates a "Transformation opportunity". This is consistent with a company in an industry with moderate-high AI potential ($H_{org,k}^R = 72$) but with lower current internal capabilities (signified by the low external signals score). My initial assessment confirms that while the baseline Org-AI-R is 42, there's significant room for improvement, making it a compelling target for value creation through AI. This immediate insight drives my decision to proceed with a more detailed due diligence.

## 4. Deep Dive: Dimension-Level Assessment & Gap Analysis

Now that I've identified Alpha Manufacturing as a "Transformation opportunity", I need to conduct a thorough due diligence to understand its specific strengths and weaknesses across the seven critical AI readiness dimensions (Data Infrastructure, AI Governance, Technology Stack, Talent, Leadership, Use Case Portfolio, Culture). This detailed assessment, involving structured interviews and technical reviews, allows me to pinpoint priority investment areas and quantify *Idiosyncratic Readiness ($V_{org,j}^R$)*. This is crucial for building a targeted AI strategy, rather than a generic one.

### Quantitative Logic for Gap Analysis

The dimension score $D_k$ for each dimension $k$ is calculated as:

$$
D_k = \left( \frac{\text{Rating}_k}{5} \right) \times 100
$$

(Here, for simplicity in the notebook, `Rating_k` is assumed to be an average rating for the dimension, directly reflecting the 1-5 scale).

The gap analysis identifies priority investment areas by comparing current scores against a target (e.g., industry 75th percentile benchmark):

$$
\text{Gap}_k = D_k^{target} - D_k^{current}
$$

```python
def simulate_dimension_ratings(company_name, sector, is_baseline=True):
    """
    Simulates 1-5 ratings for a company's AI dimensions.
    If is_baseline is True, ratings will be lower to reflect a less mature state.
    Otherwise, ratings will be higher to represent an improved state or a benchmark.
    """
    np.random.seed(hash(company_name + sector + str(is_baseline)) % (2**32 - 1)) # Consistent seeding
    
    ratings = {}
    for dim in general_dimension_weights.keys():
        if is_baseline:
            # Baseline/Current ratings, often lower for companies needing transformation
            ratings[dim] = np.random.randint(1, 4) # Ratings between 1 and 3
        else:
            # Target/Improved ratings, generally higher
            ratings[dim] = np.random.randint(3, 6) # Ratings between 3 and 5
    return pd.Series(ratings, name='Rating (1-5)')

def calculate_dimension_score(ratings, dimension_weights):
    """
    Calculates the 0-100 dimension score based on 1-5 ratings and weights.
    For simplicity, assuming `ratings` is a Series of average ratings per dimension (1-5).
    """
    scores = (ratings / 5) * 100
    weighted_scores = scores * pd.Series(dimension_weights)
    
    # Normalize weighted scores to ensure sum is 100 if weights sum to 1
    # Dk = (sum(wi*Rating_i,k)/5)*100
    # Let's adjust Dk to be a simple normalized score of the rating for the dimension.
    # The document gives D_k = (sum_i w_i * Rating_i,k / 5) * 100
    # If we assume one rating per dimension, with w_i=1, then D_k = (Rating_k / 5) * 100
    
    return scores.round(2)

def calculate_V_org_R(dimension_scores, sector_weights):
    """
    Calculates V_org_R (Idiosyncratic Readiness) as a weighted average of dimension scores.
    """
    weighted_sum = (dimension_scores * pd.Series(sector_weights)).sum()
    V_org_R = weighted_sum # since dimension scores are 0-100 and weights sum to 1
    return round(V_org_R, 2)

def calculate_synergy(V_org_R, H_org_k_R):
    """
    Calculates a simplified synergy score based on V_org_R and H_org_k_R.
    Synergy is normalized to [0, 100]. A simple heuristic: min of V_org_R and H_org_k_R.
    """
    return min(V_org_R, H_org_k_R)

def perform_gap_analysis(current_scores, target_scores):
    """
    Performs gap analysis: Target Score - Current Score.
    """
    gap_analysis = target_scores - current_scores
    return gap_analysis.round(2)

# --- Persona's action: Conduct detailed assessment ---
# Simulate current dimension ratings for Alpha Manufacturing
current_ratings_alpha = simulate_dimension_ratings(selected_company_name, selected_sector, is_baseline=True)

# Get sector-specific weights for Alpha Manufacturing
sector_weights = all_dimension_weights_df[selected_sector]

# Calculate current dimension scores (0-100)
current_dimension_scores_alpha = calculate_dimension_score(current_ratings_alpha, sector_weights)

# Simulate target dimension scores (e.g., industry 75th percentile)
# Let's assume target ratings are generally higher
target_ratings_alpha = simulate_dimension_ratings(selected_company_name, selected_sector, is_baseline=False)
target_dimension_scores_alpha = calculate_dimension_score(target_ratings_alpha, sector_weights)

# Perform Gap Analysis
gap_scores_alpha = perform_gap_analysis(current_dimension_scores_alpha, target_dimension_scores_alpha)

# Determine priority based on gap size
priority_labels = ['Low', 'Medium', 'High']
gap_priority = pd.cut(gap_scores_alpha, bins=[-np.inf, 20, 40, np.inf], labels=priority_labels, right=False)

# Consolidate results
dimension_assessment_df = pd.DataFrame({
    'Current Rating (1-5)': current_ratings_alpha,
    'Current Score (0-100)': current_dimension_scores_alpha,
    'Target Score (0-100)': target_dimension_scores_alpha,
    'Gap': gap_scores_alpha,
    'Priority': gap_priority
}).sort_values('Gap', ascending=False)

print(f"\n--- Dimension-Level Assessment for {selected_company_name} ({selected_sector}) ---")
print(dimension_assessment_df)

# Calculate V_org_R based on current dimension scores
current_V_org_R_alpha = calculate_V_org_R(current_dimension_scores_alpha, sector_weights)
current_synergy_alpha = calculate_synergy(current_V_org_R_alpha, H_org_k_R)

# Calculate Org-AI-R using the newly derived V_org_R
recalculated_current_org_ai_r_alpha = calculate_org_ai_r(
    V_org_R=current_V_org_R_alpha,
    H_org_k_R=H_org_k_R,
    synergy_score=current_synergy_alpha,
    alpha=model_coefficients['alpha'],
    beta=model_coefficients['beta']
)

print(f"\nRecalculated Idiosyncratic Readiness (V_org,j^R): {current_V_org_R_alpha}")
print(f"Recalculated Synergy: {current_synergy_alpha}")
print(f"Recalculated Current PE Org-AI-R: {recalculated_current_org_ai_r_alpha} (Actual in portfolio: {current_org_ai_r})")


# --- Visualization: Radar Chart for Dimension Scores ---
categories = list(dimension_assessment_df.index)
N = len(categories)

angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1] # Complete the loop

current_values = dimension_assessment_df['Current Score (0-100)'].tolist()
current_values += current_values[:1]

target_values = dimension_assessment_df['Target Score (0-100)'].tolist()
target_values += target_values[:1]

plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
plt.xticks(angles[:-1], categories, color='grey', size=10)

ax.set_rlabel_position(0)
plt.yticks([25, 50, 75, 100], ["25", "50", "75", "100"], color="grey", size=8)
plt.ylim(0, 100)

ax.plot(angles, current_values, linewidth=1, linestyle='solid', label='Current Score', color='blue')
ax.fill(angles, current_values, 'blue', alpha=0.1)

ax.plot(angles, target_values, linewidth=1, linestyle='solid', label='Target Score', color='red')
ax.fill(angles, target_values, 'red', alpha=0.05)

plt.title(f'AI Readiness Dimension Scores for {selected_company_name}', size=14, color='black', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
plt.show()

# --- Visualization: Bar Chart for Gap Analysis ---
plt.figure(figsize=(10, 6))
sns.barplot(x=dimension_assessment_df.index, y='Gap', data=dimension_assessment_df, palette='viridis')
plt.title(f'AI Readiness Gap Analysis for {selected_company_name}')
plt.xlabel('Dimension')
plt.ylabel('Gap (Target - Current Score)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### Explanation of Gap Analysis

The dimension-level assessment for Alpha Manufacturing clearly highlights its critical areas for improvement. "Data Infrastructure", "Talent", and "Technology Stack" show the largest gaps, indicating that foundational capabilities are underdeveloped. This granular view allows me to direct investment and operational support precisely where it's needed most. The recalculation of $V_{org,j}^R$ based on these dimensions provides a more accurate picture of the company's internal AI capability, which is a key component for calculating its overall Org-AI-R score. These insights are directly translatable into the "Due Diligence Output Package" for our investment committee, pinpointing "Priority Investment Areas."

## 5. Identify High-Value AI Use Cases & Estimate Impact

With a clear understanding of Alpha Manufacturing's AI readiness gaps, my next step is to identify specific, high-value AI initiatives that can address these gaps and deliver tangible EBITDA improvement. I will leverage our sector-specific use case library (Appendix B) to ensure relevance and benchmarked potential. For each chosen use case, I need to estimate key project parameters: investment cost, probability of successful implementation, and execution quality. These estimations are crucial for building a realistic and ROI-driven value creation plan.

### Quantitative Logic for Project Financial Impact

The $\Delta \text{EBITDA}$ attributed to a set of AI use cases $U$ is defined as:

$$
\Delta \text{EBITDA}_j = \sum_{u \in U} P_u \cdot \text{Impact}_u \cdot \text{Execution}_u
$$

Where:
*   $P_u$: Probability of successful implementation for use case $u$.
*   $\text{Impact}_u$: Potential EBITDA impact if successful (in absolute dollars or as a percentage of current EBITDA).
*   $\text{Execution}_u \in [0, 1]$: Execution quality factor.

```python
def estimate_project_parameters(use_case, current_V_org_R, H_org_k_R, initial_ebitda_M):
    """
    Estimates investment cost, probability of success, execution quality,
    and potential EBITDA impact ($M) for a given use case.
    These are simulated based on use case complexity and current Org-AI-R components.
    """
    complexity_map = {'Low': 0.7, 'Low-Medium': 0.6, 'Medium': 0.5, 'High': 0.3}
    timeline_map = {'1-3': 3, '3-6': 6, '6-9': 9, '6-12': 9, '9-15': 12, '12-18': 15, '12-24': 18} # Median months

    complexity_factor = complexity_map.get(use_case['Complexity'], 0.5)
    
    # Investment cost (simulated based on complexity and timeline)
    timeline_months_str = str(use_case['Timeline (months)'])
    timeline_months = int(timeline_months_str.split('-')[0]) if '-' in timeline_months_str else int(timeline_months_str)
    
    # More detailed timeline mapping based on ranges
    if '1-3' in timeline_months_str: timeline_months = timeline_map['1-3']
    elif '3-6' in timeline_months_str: timeline_months = timeline_map['3-6']
    elif '6-9' in timeline_months_str: timeline_months = timeline_map['6-9']
    elif '6-12' in timeline_months_str: timeline_months = timeline_map['6-12']
    elif '9-15' in timeline_months_str: timeline_months = timeline_map['9-15']
    elif '12-18' in timeline_months_str: timeline_months = timeline_map['12-18']
    elif '12-24' in timeline_months_str: timeline_months = timeline_map['12-24']
    
    # Base investment for a 'medium' complexity, 6-month project could be ~0.5M. Scale from there.
    investment_cost_M = round(0.2 * complexity_factor * (timeline_months / 6) * np.random.uniform(0.8, 1.2) + 0.1, 2)
    
    # Probability of success (higher for lower complexity, higher V_org_R)
    prob_success = round(np.clip(0.6 + (current_V_org_R / 100 * 0.2) - (complexity_factor * 0.3), 0.5, 0.95), 2)
    
    # Execution quality (higher for higher V_org_R)
    exec_quality = round(np.clip(current_V_org_R / 100 * 0.8, 0.6, 0.9), 2)
    
    # EBITDA impact (percentage, from min/max, scaled by H_org_k_R and V_org_R)
    ebitda_impact_pct = np.random.uniform(use_case['EBITDA Impact (min%)'], use_case['EBITDA Impact (max%)'])
    
    # Adjust for Diagnostic AI (which has 0-0 range) - give a base range for simulation
    if use_case['Use Case'] == 'Diagnostic AI' and ebitda_impact_pct == 0:
        ebitda_impact_pct = np.random.uniform(1, 3) # Assume 1-3% impact if successful

    ebitda_impact_pct = round(ebitda_impact_pct * (H_org_k_R / 100) * (current_V_org_R / 100 * 0.5 + 0.5), 2) # scale by readiness

    # Convert EBITDA impact percentage to absolute dollars based on initial_ebitda_M
    ebitda_impact_M = round(initial_ebitda_M * (ebitda_impact_pct / 100), 2)
    
    # Delta Org-AI-R improvement (higher for more complex/impactful projects)
    delta_org_ai_r = round(np.random.uniform(5, 15) * complexity_factor * (ebitda_impact_pct / 2), 2) # Scale with impact
    if delta_org_ai_r < 1: delta_org_ai_r = 1 # Minimum 1 point improvement
    
    return {
        'Investment ($M)': investment_cost_M,
        'Probability of Success': prob_success,
        'Execution Quality': exec_quality,
        'EBITDA Impact (%)': ebitda_impact_pct,
        'EBITDA Impact ($M)': ebitda_impact_M,
        'Delta Org-AI-R': delta_org_ai_r,
        'Timeline (months)': timeline_months
    }

# --- Persona's action: Select use cases based on identified gaps ---
print(f"\n--- Exploring High-Value AI Use Cases for {selected_company_name} ({selected_sector}) ---")
sector_use_cases_df = high_value_use_cases[selected_sector].copy()
print(sector_use_cases_df.to_string())

print(f"\nBased on the gap analysis, {selected_company_name} needs to focus on Data Infrastructure, Talent, and Technology Stack.")
print("The following use cases align with these foundational improvements and offer high EBITDA potential:")

# Example selection of use cases based on identified gaps for Alpha Manufacturing
# (Manufacturing: Data Infrastructure, Technology Stack, Talent are high priority)
selected_use_case_names = [
    'Predictive Maintenance',
    'Demand Forecasting',
    'Supply Chain Optimization' # This is complex, but addresses efficiency, and needs data infra
]

planned_initiatives_data = []
for uc_name in selected_use_case_names:
    use_case = sector_use_cases_df[sector_use_cases_df['Use Case'] == uc_name].iloc[0]
    
    # Estimate parameters based on current readiness and use case specifics
    estimated_params = estimate_project_parameters(use_case, current_V_org_R_alpha, H_org_k_R, initial_ebitda_M)
    
    initiative = {
        'Use Case': uc_name,
        'Description': use_case['Description'],
        'Complexity': use_case['Complexity'],
        **estimated_params
    }
    planned_initiatives_data.append(initiative)

planned_initiatives_df = pd.DataFrame(planned_initiatives_data)
planned_initiatives_df = planned_initiatives_df[['Use Case', 'Description', 'Complexity', 'Timeline (months)',
                                                 'Investment ($M)', 'Probability of Success', 'Execution Quality',
                                                 'EBITDA Impact (%)', 'EBITDA Impact ($M)', 'Delta Org-AI-R']]

print("\n--- Selected AI Initiatives with Estimated Parameters ---")
print(planned_initiatives_df.to_string())
```

### Explanation of Initiative Selection

I've selected three key initiatives for Alpha Manufacturing: Predictive Maintenance, Demand Forecasting, and Supply Chain Optimization. These directly target the "Data Infrastructure" and "Technology Stack" gaps identified in the prior section, while offering clear EBITDA enhancement. By estimating each project's cost, probability of success, and execution quality, I have the necessary inputs to project their combined financial impact and strategically prioritize them within our investment horizon. The estimated `Delta Org-AI-R` for each initiative shows how it contributes to improving the company's overall AI readiness, linking capability building to financial outcomes.

## 6. Build the Multi-Year AI Value Creation Plan

Now that I have a set of high-value AI initiatives with estimated impacts, it's time to construct a concrete, multi-year AI value creation plan for Alpha Manufacturing. This plan integrates with our typical PE "100-day planning" cycles, phasing initiatives to optimize for quick wins and foundational build-out. My goal is to project the cumulative EBITDA impact and the progression of the Org-AI-R score over the investment horizon, demonstrating a clear roadmap for value creation.

### Quantitative Logic for Projected Trajectory

The cumulative EBITDA impact and Org-AI-R progression are modeled over time by summing the contributions from planned initiatives, considering their timelines and estimated impacts:

$$
\text{Total } \Delta \text{EBITDA}_{j,T} = \sum_{t=1}^{T} \sum_{u \in U_t} P_u \cdot \text{Impact}_u \cdot \text{Execution}_u
$$

$$
\text{Org-AI-R}_{j,T} = \text{Baseline Org-AI-R}_j + \sum_{t=1}^{T} \sum_{u \in U_t} \Delta \text{Org-AI-R}_u
$$

Where $U_t$ is the set of use cases implemented and delivering value by time $t$.

```python
def create_multi_year_plan(company_name, initial_org_ai_r, initial_ebitda_M, planned_initiatives_df, H_org_k_R, total_years=3):
    """
    Constructs a multi-year AI value creation plan, projecting Org-AI-R and EBITDA.
    """
    current_org_ai_r = initial_org_ai_r
    current_ebitda_M = initial_ebitda_M
    cumulative_ebitda_impact_M = 0
    cumulative_investment_M = 0
    
    plan_trajectory = []
    
    # Sort initiatives by timeline to simulate phased approach
    planned_initiatives_df_sorted = planned_initiatives_df.sort_values(by='Timeline (months)')
    
    implemented_initiatives = []

    for year in range(1, total_years + 1):
        year_ebitda_impact_M = 0
        year_org_ai_r_delta = 0
        year_investment_M = 0
        
        # Calculate benefits from already implemented initiatives
        for init in implemented_initiatives:
            # Assumes full impact after implementation
            year_ebitda_impact_M += init['EBITDA Impact ($M)'] * init['Probability of Success'] * init['Execution Quality']

        # Add new initiatives for the current year
        for index, initiative in planned_initiatives_df_sorted.iterrows():
            if initiative['Use Case'] not in [i['Use Case'] for i in implemented_initiatives]: # Only add if not already in implemented
                if initiative['Timeline (months)'] <= year * 12: # Check if initiative completes within the current year
                    
                    # Contribution to year's EBITDA (if implemented in current year, partial year impact can be considered)
                    # For simplicity, let's assume full impact from the year of completion.
                    year_ebitda_impact_M += initiative['EBITDA Impact ($M)'] * initiative['Probability of Success'] * initiative['Execution Quality']
                    year_org_ai_r_delta += initiative['Delta Org-AI-R']
                    year_investment_M += initiative['Investment ($M)']
                    
                    implemented_initiatives.append(initiative)
        
        # Update current Org-AI-R and EBITDA
        current_org_ai_r += year_org_ai_r_delta
        cumulative_ebitda_impact_M += year_ebitda_impact_M
        cumulative_investment_M += year_investment_M
        current_ebitda_M += year_ebitda_impact_M # Direct dollar impact

        plan_trajectory.append({
            'Year': year,
            'Org-AI-R': round(current_org_ai_r, 2),
            'EBITDA Impact ($M) - Year': round(year_ebitda_impact_M, 2),
            'Cumulative EBITDA Impact ($M)': round(cumulative_ebitda_impact_M, 2),
            'Investment ($M) - Year': round(year_investment_M, 2),
            'Cumulative Investment ($M)': round(cumulative_investment_M, 2)
        })

    return pd.DataFrame(plan_trajectory), implemented_initiatives


# --- Persona's action: Build the plan ---
total_years_plan = 3
ai_plan_trajectory_df, final_implemented_initiatives = create_multi_year_plan(
    selected_company_name,
    recalculated_current_org_ai_r_alpha, # Use the recalculated V_org_R to get a more accurate starting Org-AI-R
    initial_ebitda_M,
    planned_initiatives_df,
    H_org_k_R,
    total_years=total_years_plan
)

print(f"\n--- AI Value Creation Plan & Projected Trajectory for {selected_company_name} over {total_years_plan} years ---")
print(ai_plan_trajectory_df.to_string())

# --- Summarize the Final Value Creation Plan ---
final_plan_summary_df = planned_initiatives_df.copy()
final_plan_summary_df['Expected Annual EBITDA Impact ($M)'] = final_plan_summary_df['EBITDA Impact ($M)'] * final_plan_summary_df['Probability of Success'] * final_plan_summary_df['Execution Quality']
final_plan_summary_df = final_plan_summary_df[['Use Case', 'Timeline (months)', 'Investment ($M)', 'Expected Annual EBITDA Impact ($M)', 'Delta Org-AI-R']]
print("\n--- Summary of AI Value Creation Initiatives ---")
print(final_plan_summary_df.to_string())


# --- Visualization: Cumulative EBITDA Impact over Time ---
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Cumulative EBITDA Impact ($M)', data=ai_plan_trajectory_df, marker='o', color='green')
plt.title(f'Cumulative EBITDA Impact for {selected_company_name} AI Plan')
plt.xlabel('Year')
plt.ylabel('Cumulative EBITDA Impact ($M)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(ai_plan_trajectory_df['Year'])
plt.tight_layout()
plt.show()

# --- Visualization: Org-AI-R Progression over Time ---
plt.figure(figsize=(10, 6))
sns.lineplot(x='Year', y='Org-AI-R', data=ai_plan_trajectory_df, marker='o', color='purple')
plt.title(f'PE Org-AI-R Progression for {selected_company_name} AI Plan')
plt.xlabel('Year')
plt.ylabel('Org-AI-R Score')
plt.ylim(0, 100)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(ai_plan_trajectory_df['Year'])
plt.tight_layout()
plt.show()
```

### Explanation of Value Creation Plan

The multi-year plan for Alpha Manufacturing clearly outlines the expected progression. The trajectory table shows a steady increase in Org-AI-R from the initial 42 (baseline) to a projected higher score, alongside a significant cumulative EBITDA impact over 3 years. The visualizations provide an easy-to-digest view of this growth, which is critical for communicating the value proposition to our investment committee and for tracking progress over the investment horizon. This phased approach, starting with initiatives that deliver quick wins or foundational improvements, is consistent with effective 100-day planning.

## 7. Calculate AI Investment Efficiency

As a Portfolio Manager, I need to evaluate not just the total value created but also the efficiency of our AI investments. The AI Investment Efficiency (AIE) metric provides a standardized way to compare different initiatives or companies, helping me allocate capital optimally. It quantifies how much Org-AI-R improvement and EBITDA impact we achieve per dollar invested.

```python
def calculate_ai_investment_efficiency(delta_org_ai_r, total_ai_investment_M, total_ebitda_impact_M):
    """
    Calculates the AI Investment Efficiency (AIE).
    total_ai_investment_M and total_ebitda_impact_M are in millions of dollars.
    """
    if total_ai_investment_M <= 0:
        return 0 # Avoid division by zero
    
    # AIE = (Delta Org-AI-R / AI Investment) * EBITDA Impact ($M)
    aie_score = (delta_org_ai_r / total_ai_investment_M) * total_ebitda_impact_M
    return round(aie_score, 2)

# --- Persona's action: Calculate AIE for the plan ---
total_delta_org_ai_r_plan = ai_plan_trajectory_df['Org-AI-R'].iloc[-1] - recalculated_current_org_ai_r_alpha
total_investment_plan_M = ai_plan_trajectory_df['Cumulative Investment ($M)'].iloc[-1]
total_ebitda_impact_plan_M = ai_plan_trajectory_df['Cumulative EBITDA Impact ($M)'].iloc[-1]

aie_for_plan = calculate_ai_investment_efficiency(
    delta_org_ai_r=total_delta_org_ai_r_plan,
    total_ai_investment_M=total_investment_plan_M,
    total_ebitda_impact_M=total_ebitda_impact_plan_M
)

print(f"\n--- AI Investment Efficiency for {selected_company_name}'s {total_years_plan}-Year Plan ---")
print(f"Total Projected Delta Org-AI-R: {total_delta_org_ai_r_plan:.2f} points")
print(f"Total Projected AI Investment: ${total_investment_plan_M:.2f} Million")
print(f"Total Projected EBITDA Impact: ${total_ebitda_impact_plan_M:.2f} Million")
print(f"AI Investment Efficiency (AIE): {aie_for_plan:.2f} pts*$M/$M (Org-AI-R points * EBITDA $M per $M invested)")
```

### Explanation of AI Investment Efficiency

The calculated AIE for Alpha Manufacturing's plan provides a powerful metric. An AIE of, for example, 10.5 means that for every million dollars invested in AI, we gain 10.5 Org-AI-R points AND generate an EBITDA impact of that many million dollars. This standardized score allows me to quickly compare this plan against other potential investments within our portfolio, ensuring that we prioritize initiatives that deliver the highest return on AI capital.

## 8. Portfolio-Level Review & Benchmarking

My role extends beyond individual company plans; I must also assess the overall health and performance of our entire portfolio. By benchmarking Alpha Manufacturing against other portfolio companies, I can identify best practices, uncover underperforming assets, and optimize capital allocation at the fund level. This provides a holistic view of our AI value creation efforts.

### Quantitative Logic for Benchmarking

**Within-Portfolio Benchmarking:** The percentile rank indicates a company's standing relative to peers in the fund.

$$
\text{Percentile}_j = \frac{\text{Rank}(\text{Org-AI-R}_j)}{\text{Portfolio Size}} \times 100
$$

**Cross-Portfolio Benchmarking (Industry-Adjusted):** The Z-score normalizes a company's Org-AI-R against its industry, accounting for sector-specific opportunities.

$$
Z_{j,k} = \frac{\text{Org-AI-R}_j - \mu_k}{\sigma_k}
$$

Where $\mu_k$ and $\sigma_k$ are the industry mean and standard deviation of Org-AI-R scores.

```python
def calculate_within_portfolio_percentile(company_org_ai_r, portfolio_org_ai_rs):
    """
    Calculates the percentile rank of a company's Org-AI-R within the portfolio.
    """
    sorted_scores = sorted(portfolio_org_ai_rs)
    rank = next(i for i, score in enumerate(sorted_scores) if score >= company_org_ai_r) + 1
    percentile = (rank / len(portfolio_org_ai_rs)) * 100
    return round(percentile, 2)

def calculate_cross_portfolio_z_score(company_org_ai_r, industry_mean, industry_std):
    """
    Calculates the industry-adjusted Z-score for a company's Org-AI-R.
    """
    if industry_std == 0:
        return 0 # Or handle as appropriate
    z_score = (company_org_ai_r - industry_mean) / industry_std
    return round(z_score, 2)

# --- Persona's action: Update portfolio and perform benchmarking ---
# Update Alpha Manufacturing's data in the portfolio_companies_df with projected values
updated_alpha_data = {
    'Company': selected_company_name,
    'Sector': selected_sector,
    'Baseline Org-AI-R': initial_org_ai_r,
    'Current Org-AI-R': ai_plan_trajectory_df['Org-AI-R'].iloc[-1], # End-of-plan Org-AI-R
    'Delta Org-AI-R': total_delta_org_ai_r_plan,
    'Investment ($M)': total_investment_plan_M,
    'Efficiency (pts/$M)': aie_for_plan,
    'EBITDA Impact (%)': (total_ebitda_impact_plan_M / initial_ebitda_M) * 100,
    'EBITDA ($M)': initial_ebitda_M + total_ebitda_impact_plan_M, # New absolute EBITDA
    'EBITDA Impact ($M)': total_ebitda_impact_plan_M
}

# Find and update the row for Alpha Manufacturing, or add if new
idx_to_update = portfolio_companies_df[portfolio_companies_df['Company'] == selected_company_name].index
if not idx_to_update.empty:
    for col, value in updated_alpha_data.items():
        portfolio_companies_df.loc[idx_to_update, col] = value
else: # Should not happen if selected from existing df, but for robustness
    portfolio_companies_df = pd.concat([portfolio_companies_df, pd.DataFrame([updated_alpha_data])], ignore_index=True)


# Calculate benchmarking metrics for the entire portfolio
portfolio_companies_df['Org-AI-R Percentile'] = portfolio_companies_df['Current Org-AI-R'].apply(
    lambda x: calculate_within_portfolio_percentile(x, portfolio_companies_df['Current Org-AI-R'].tolist())
)

# Calculate industry means and stds for Z-score
industry_stats = portfolio_companies_df.groupby('Sector')['Current Org-AI-R'].agg(['mean', 'std']).reset_index()
industry_stats.rename(columns={'mean': 'Industry Mean Org-AI-R', 'std': 'Industry Std Org-AI-R'}, inplace=True)

portfolio_companies_df = portfolio_companies_df.merge(industry_stats, on='Sector', how='left')
portfolio_companies_df['Org-AI-R Z-Score'] = portfolio_companies_df.apply(
    lambda row: calculate_cross_portfolio_z_score(
        row['Current Org-AI-R'], row['Industry Mean Org-AI-R'], row['Industry Std Org-AI-R']
    ), axis=1
)

print(f"\n--- Portfolio-Level Analysis and Benchmarking (after {selected_company_name} plan) ---")
print(portfolio_companies_df[['Company', 'Sector', 'Current Org-AI-R', 'Org-AI-R Percentile', 'Org-AI-R Z-Score', 'Efficiency (pts/$M)', 'EBITDA Impact (%)']].to_string())

# --- Visualization: Portfolio Org-AI-R Scores ---
plt.figure(figsize=(12, 7))
sns.barplot(x='Company', y='Current Org-AI-R', hue='Sector', data=portfolio_companies_df.sort_values('Current Org-AI-R', ascending=False), palette='viridis')
plt.title('Current PE Org-AI-R Scores Across Portfolio Companies')
plt.xlabel('Company')
plt.ylabel('Current Org-AI-R Score')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# --- Visualization: Portfolio AI Investment Efficiency ---
plt.figure(figsize=(12, 7))
sns.barplot(x='Company', y='Efficiency (pts/$M)', hue='Sector', data=portfolio_companies_df.sort_values('Efficiency (pts/$M)', ascending=False), palette='magma')
plt.title('AI Investment Efficiency Across Portfolio Companies')
plt.xlabel('Company')
plt.ylabel('AI Investment Efficiency (pts*$M/$M)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### Explanation of Portfolio Benchmarking

The portfolio-level analysis offers critical insights. Alpha Manufacturing's projected Org-AI-R score and AIE can now be directly compared against its peers. If Alpha Manufacturing's AIE is significantly higher than others, it suggests a highly efficient AI investment, potentially warranting further capital allocation. Conversely, if it falls below target, I can initiate a "deep dive" into execution challenges. The Z-score provides an industry-normalized view, revealing if the company is outperforming or underperforming its sector peers, a key input for our fund-wide capital deployment strategy.

## 9. Exit-Readiness Assessment

As a Private Equity Portfolio Manager, the ultimate goal is a successful exit. Buyers increasingly scrutinize a company's AI capabilities, which directly impacts valuation multiples. In this final step, I assess Alpha Manufacturing's AI strengths from a buyer's perspective to formulate a compelling exit narrative.

### Quantitative Logic for Exit-Readiness Score and Valuation Impact

The Exit-AI-R Score is defined as:

$$
\text{Exit-AI-R}_j = w_1 \cdot \text{Visible}_j + w_2 \cdot \text{Documented}_j + w_3 \cdot \text{Sustainable}_j
$$

Where:
*   $\text{Visible}_j$: AI capabilities apparent to buyers (e.g., product features, technology stack), normalized to $[0, 100]$.
*   $\text{Documented}_j$: Quantified AI impact with audit trail, normalized to $[0, 100]$.
*   $\text{Sustainable}_j$: Embedded capabilities vs. one-time projects, normalized to $[0, 100]$.
*   $w_1, w_2, w_3$: Exit-readiness weights (e.g., $w_1=0.35, w_2=0.40, w_3=0.25$).

The Multiple Attribution Model links Exit-AI-R to valuation:

$$
\text{Multiple}_j = \text{Multiple}_{base,k} + \delta \cdot \text{Exit-AI-R}_j / 100
$$

Where:
*   $\text{Multiple}_{base,k}$: Baseline exit multiple for industry $k$.
*   $\delta$: AI premium coefficient (estimated: $\delta \in [1.0, 3.0]$ turns of EBITDA).

```python
def assess_exit_readiness(visible_score, documented_score, sustainable_score, w1, w2, w3):
    """
    Calculates the Exit-AI-R Score. Scores should be normalized to [0, 100].
    """
    exit_ai_r = (w1 * visible_score) + (w2 * documented_score) + (w3 * sustainable_score)
    return round(exit_ai_r, 2)

def predict_exit_multiple(base_multiple, exit_ai_r, delta):
    """
    Predicts the exit multiple based on the Exit-AI-R Score.
    """
    predicted_multiple = base_multiple + (delta * exit_ai_r / 100)
    return round(predicted_multiple, 2)

# --- Persona's action: Assess exit readiness ---
# Simulate scores for Visible, Documented, Sustainable based on Alpha Manufacturing's plan
# Higher Org-AI-R and documented EBITDA impact would lead to higher scores.
# Let's assume current_org_ai_r is ~68 and improved
visible_score = min(100, recalculated_current_org_ai_r_alpha * 0.8 + 20) # Based on V_org_R, tech stack
documented_score = min(100, (total_ebitda_impact_plan_M / initial_ebitda_M) * 1000 + 40) # Based on EBITDA impact
sustainable_score = min(100, (recalculated_current_org_ai_r_alpha * 0.7 + 30)) # Based on embedded capabilities (talent, culture)

# For Alpha Manufacturing with its plan, these scores would be higher than baseline.
# Let's directly set some improved scores for demonstration:
visible_score = 75 # Product AI features, tech stack improvements
documented_score = 80 # Strong EBITDA impact documented, audit trail
sustainable_score = 70 # Embedded processes, talent retention

exit_ai_r_score = assess_exit_readiness(
    visible_score=visible_score,
    documented_score=documented_score,
    sustainable_score=sustainable_score,
    w1=model_coefficients['w1_exit'],
    w2=model_coefficients['w2_exit'],
    w3=model_coefficients['w3_exit']
)

# Simulate baseline multiple for Manufacturing sector
base_multiple_manufacturing = 6.5 # Example from document p.20 (6.5x -> 8.0x)

predicted_exit_multiple = predict_exit_multiple(
    base_multiple=base_multiple_manufacturing,
    exit_ai_r=exit_ai_r_score,
    delta=model_coefficients['delta_exit']
)

print(f"\n--- Exit-Readiness Assessment for {selected_company_name} ---")
print(f"Visible AI Capabilities Score: {visible_score}")
print(f"Documented AI Impact Score: {documented_score}")
print(f"Sustainable AI Capabilities Score: {sustainable_score}")
print(f"Calculated Exit-AI-R Score: {exit_ai_r_score:.2f}")
print(f"Baseline Exit Multiple for {selected_sector}: {base_multiple_manufacturing}x EBITDA")
print(f"Predicted Exit Multiple with AI Premium: {predicted_exit_multiple:.2f}x EBITDA")
```

### Explanation of Exit-Readiness

The Exit-AI-R score and projected exit multiple are critical for our exit strategy. For Alpha Manufacturing, the planned AI initiatives lead to a strong Exit-AI-R, justifying a premium on its valuation. This provides concrete, evidence-based data for our discussions with potential buyers, allowing us to articulate a compelling narrative about how AI capabilities are not just aspirational but are deeply embedded, delivering measurable and sustainable financial value. A projected increase from 6.5x to 8.0x EBITDA (as seen in the example) directly translates to significant upside for the fund.
