
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import streamlit as st

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="QuLab: AI Value Creation & Investment Efficiency Planner", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: AI Value Creation & Investment Efficiency Planner")
st.divider()

# --- Model Coefficients and Constants ---
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

# --- Core Functions ---
def calculate_org_ai_r(V_org_R, H_org_k_R, synergy_score, alpha, beta):
    return round((alpha * V_org_R) + ((1 - alpha) * H_org_k_R) + (beta * synergy_score), 2)

def calculate_screening_score(H_org_k_R, external_signals_score, epsilon):
    return round(H_org_k_R + (epsilon * external_signals_score), 2)

def simulate_dimension_ratings(company_name, sector, is_target=False):
    seed_val = hash(company_name + sector + str(is_target)) % (2**32 - 1)
    rng = np.random.default_rng(seed_val)
    ratings = {}
    for dim in general_dimension_weights.keys():
        if is_target:
            ratings[dim] = rng.integers(3, 6) # Target ratings tend to be higher (3,4,5)
        else:
            ratings[dim] = rng.integers(1, 4) # Current ratings for baseline (1,2,3)
    return pd.Series(ratings, name='Rating (1-5)')

def calculate_dimension_score(ratings):
    return ((ratings / 5) * 100).round(2)

def calculate_V_org_R(dimension_scores, sector_weights):
    aligned_scores = dimension_scores.reindex(sector_weights.index, fill_value=0)
    weighted_sum = (aligned_scores * sector_weights).sum()
    return round(weighted_sum, 2)

def calculate_synergy(V_org_R, H_org_k_R):
    return min(V_org_R, H_org_k_R)

def estimate_project_parameters(use_case_data, current_V_org_R, H_org_k_R, initial_ebitda_M, user_investment=None, user_prob_success=None, user_exec_quality=None):
    complexity_map = {'Low': 0.7, 'Low-Medium': 0.6, 'Medium': 0.5, 'High': 0.3}
    timeline_map_avg = {'1-3': 2, '3-6': 4.5, '6-9': 7.5, '6-12': 9, '9-15': 12, '12-18': 15, '12-24': 18}

    complexity_factor = complexity_map.get(use_case_data['Complexity'], 0.5)
    timeline_months_str = str(use_case_data['Timeline (months)'])
    timeline_months_numeric = timeline_map_avg.get(timeline_months_str, 6)

    seed_val = hash(use_case_data['Use Case']) % (2**32 - 1)
    rng = np.random.default_rng(seed_val)
    
    default_investment_cost_M = round(0.2 * complexity_factor * (timeline_months_numeric / 6) * rng.uniform(0.8, 1.2) + 0.1, 2)
    default_prob_success = round(np.clip(0.6 + (current_V_org_R / 100 * 0.2) - (complexity_factor * 0.3), 0.5, 0.95), 2)
    default_exec_quality = round(np.clip(current_V_org_R / 100 * 0.8, 0.6, 0.9), 2)
    
    investment_cost_M = user_investment if user_investment is not None else default_investment_cost_M
    prob_success = user_prob_success if user_prob_success is not None else default_prob_success
    exec_quality = user_exec_quality if user_exec_quality is not None else default_exec_quality

    ebitda_impact_pct_base = rng.uniform(use_case_data['EBITDA Impact (min%)'], use_case_data['EBITDA Impact (max%)'])
    if use_case_data['Use Case'] == 'Diagnostic AI' and ebitda_impact_pct_base == 0:
        ebitda_impact_pct_base = rng.uniform(1, 3)

    ebitda_impact_pct_contextual = ebitda_impact_pct_base * (H_org_k_R / 100) * (current_V_org_R / 100 * 0.5 + 0.5)
    ebitda_impact_pct_adjusted = round(ebitda_impact_pct_contextual * prob_success * exec_quality, 2)
    ebitda_impact_M = round(initial_ebitda_M * (ebitda_impact_pct_adjusted / 100), 2)
    
    delta_org_ai_r_base = round(rng.uniform(5, 15) * complexity_factor * (ebitda_impact_pct_base / 2), 2)
    delta_org_ai_r_adjusted = round(delta_org_ai_r_base * prob_success * exec_quality, 2)
    if delta_org_ai_r_adjusted < 1: delta_org_ai_r_adjusted = 1
    
    return {
        'Investment ($M)': investment_cost_M,
        'Probability of Success': prob_success,
        'Execution Quality': exec_quality,
        'EBITDA Impact (%)': ebitda_impact_pct_adjusted,
        'EBITDA Impact ($M)': ebitda_impact_M,
        'Delta Org-AI-R': delta_org_ai_r_adjusted,
        'Timeline (months)': timeline_months_numeric
    }

def create_multi_year_plan(company_name, initial_org_ai_r, initial_ebitda_M, planned_initiatives_df, H_org_k_R, total_years=3):
    current_org_ai_r = initial_org_ai_r
    
    plan_trajectory = []
    planned_initiatives_df_sorted = planned_initiatives_df.sort_values(by='Timeline (months)', ascending=True).reset_index(drop=True)
    
    investments_added_per_year = [0] * (total_years + 1)
    org_ai_r_delta_added_per_year = [0] * (total_years + 1)
    annual_ebitda_impact_from_completed_projects = [0] * (total_years + 1) 

    for _, initiative in planned_initiatives_df_sorted.iterrows():
        completion_year = min(total_years, int(np.ceil(initiative['Timeline (months)'] / 12)))
        if completion_year > 0:
            investments_added_per_year[completion_year] += initiative['Investment ($M)']
            org_ai_r_delta_added_per_year[completion_year] += initiative['Delta Org-AI-R']
            
            for year_idx in range(completion_year, total_years + 1):
                annual_ebitda_impact_from_completed_projects[year_idx] += initiative['EBITDA Impact ($M)']

    cumulative_ebitda_impact_M = 0
    cumulative_investment_M = 0
    
    for year in range(1, total_years + 1):
        current_org_ai_r += org_ai_r_delta_added_per_year[year]
        cumulative_investment_M += investments_added_per_year[year]
        cumulative_ebitda_impact_M += annual_ebitda_impact_from_completed_projects[year]

        plan_trajectory.append({
            'Year': year,
            'Org-AI-R': round(current_org_ai_r, 2),
            'EBITDA Impact ($M) - Annual': round(annual_ebitda_impact_from_completed_projects[year], 2),
            'Cumulative EBITDA Impact ($M)': round(cumulative_ebitda_impact_M, 2),
            'Investment ($M) - Annual': round(investments_added_per_year[year], 2),
            'Cumulative Investment ($M)': round(cumulative_investment_M, 2)
        })

    return pd.DataFrame(plan_trajectory)

def calculate_ai_investment_efficiency(delta_org_ai_r, total_ai_investment_M, total_ebitda_impact_M):
    if total_ai_investment_M <= 0:
        return 0.0
    aie_score = (delta_org_ai_r / total_ai_investment_M) * total_ebitda_impact_M
    return round(aie_score, 2)

def calculate_within_portfolio_percentile(company_org_ai_r, portfolio_org_ai_rs):
    if not portfolio_org_ai_rs or len(portfolio_org_ai_rs) == 0: return 0.0
    sorted_scores = sorted(portfolio_org_ai_rs)
    rank = sum(1 for score in sorted_scores if score <= company_org_ai_r)
    percentile = (rank / len(portfolio_org_ai_rs)) * 100
    return round(percentile, 2)

def calculate_cross_portfolio_z_score(company_org_ai_r, industry_mean, industry_std):
    if industry_std == 0 or np.isnan(industry_std):
        return 0.0
    z_score = (company_org_ai_r - industry_mean) / industry_std
    return round(z_score, 2)

def assess_exit_readiness(visible_score, documented_score, sustainable_score, w1, w2, w3):
    return round((w1 * visible_score) + (w2 * documented_score) + (w3 * sustainable_score), 2)

def predict_exit_multiple(base_multiple, exit_ai_r, delta):
    return round(base_multiple + (delta * exit_ai_r / 100), 2)

# --- Session State Initialization and Update Functions ---

def _reset_company_specific_state(company_name):
    # This function updates session state variables that depend on the newly selected company
    
    selected_company_row = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == company_name].iloc[0]
    st.session_state.selected_sector = selected_company_row['Sector']
    st.session_state.initial_ebitda_M = selected_company_row['EBITDA ($M)']

    # Re-simulate dimension ratings and store in session_state
    current_ratings_series = simulate_dimension_ratings(company_name, st.session_state.selected_sector, is_target=False)
    target_ratings_series = simulate_dimension_ratings(company_name, st.session_state.selected_sector, is_target=True)
    for dim in general_dimension_weights.keys():
        st.session_state[f'current_rating_{dim.replace(" ", "_").lower()}'] = current_ratings_series[dim]
        st.session_state[f'target_rating_{dim.replace(" ", "_").lower()}'] = target_ratings_series[dim]
    st.session_state.last_company_for_dim_ratings = company_name

    # Recalculate Org-AI-R based on detailed assessment for the new company
    current_dimension_scores = calculate_dimension_score(current_ratings_series)
    sector_weights = all_dimension_weights_df[st.session_state.selected_sector]
    current_V_org_R_alpha = calculate_V_org_R(current_dimension_scores, sector_weights)
    H_org_k_R_init = systematic_opportunity_scores[st.session_state.selected_sector]
    synergy_score_alpha_init = calculate_synergy(current_V_org_R_alpha, H_org_k_R_init)
    st.session_state.current_org_ai_r_alpha = calculate_org_ai_r(
        current_V_org_R_alpha, H_org_k_R_init, synergy_score_alpha_init,
        model_coefficients['alpha'], model_coefficients['beta']
    )
    st.session_state.current_V_org_R_alpha = current_V_org_R_alpha # Store for later use

    # Update selected use cases and their parameters for the new company/sector
    default_use_cases_for_sector = {
        'Manufacturing': ['Predictive Maintenance', 'Demand Forecasting'],
        'Healthcare': ['Revenue Cycle Management', 'Patient Scheduling'],
        'Retail': ['Demand Forecasting', 'Personalization'],
        'Business Services': ['Document Processing', 'Knowledge Worker Tools'],
        'Technology': ['Product AI Embedding', 'Automated Code Generation']
    }
    st.session_state.selected_use_cases = default_use_cases_for_sector.get(st.session_state.selected_sector, [])
    st.session_state.last_company_for_use_cases = company_name

    planned_initiatives_data_init = []
    selected_sector_use_cases = high_value_use_cases[st.session_state.selected_sector]
    H_org_k_R_temp = systematic_opportunity_scores[st.session_state.selected_sector]
    for uc_name in st.session_state.selected_use_cases:
        uc_data = selected_sector_use_cases[selected_sector_use_cases['Use Case'] == uc_name].iloc[0]
        estimated_params = estimate_project_parameters(
            uc_data, st.session_state.current_V_org_R_alpha, H_org_k_R_temp, st.session_state.initial_ebitda_M
        )
        st.session_state[f'investment_{uc_name.replace(" ", "_").lower()}'] = estimated_params['Investment ($M)']
        st.session_state[f'prob_success_{uc_name.replace(" ", "_").lower()}'] = estimated_params['Probability of Success']
        st.session_state[f'exec_quality_{uc_name.replace(" ", "_").lower()}'] = estimated_params['Execution Quality']
        planned_initiatives_data_init.append({
            'Use Case': uc_name,
            'Complexity': uc_data['Complexity'],
            'Timeline (months)': estimated_params['Timeline (months)'],
            'Investment ($M)': estimated_params['Investment ($M)'],
            'Probability of Success': estimated_params['Probability of Success'],
            'Execution Quality': estimated_params['Execution Quality'],
            'EBITDA Impact (%)': estimated_params['EBITDA Impact (%)'],
            'EBITDA Impact ($M)': estimated_params['EBITDA Impact ($M)'],
            'Delta Org-AI-R': estimated_params['Delta Org-AI-R']
        })
    st.session_state.planned_initiatives_df = pd.DataFrame(planned_initiatives_data_init)

    # Re-initialize plan trajectory
    if not st.session_state.planned_initiatives_df.empty:
        st.session_state.ai_plan_trajectory_df = create_multi_year_plan(
            st.session_state.selected_company,
            st.session_state.current_org_ai_r_alpha,
            st.session_state.initial_ebitda_M,
            st.session_state.planned_initiatives_df,
            H_org_k_R_temp,
            st.session_state.planning_horizon
        )
    else:
        st.session_state.ai_plan_trajectory_df = pd.DataFrame()
        
    sector_base_multiples = {'Manufacturing': 6.0, 'Healthcare': 7.5, 'Retail': 5.5, 'Business Services': 8.0, 'Technology': 10.0}
    st.session_state.base_exit_multiple = sector_base_multiples.get(st.session_state.selected_sector, 6.5)
    st.session_state.last_sector_for_exit = st.session_state.selected_sector

def _initialize_app_state():
    # This function runs only once on app start or full restart.
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
    st.session_state.portfolio_companies_df = pd.DataFrame(initial_portfolio_companies_data)
    st.session_state.portfolio_companies_df['EBITDA Impact ($M)'] = st.session_state.portfolio_companies_df['EBITDA ($M)'] * (st.session_state.portfolio_companies_df['EBITDA Impact (%)'] / 100)
    st.session_state.portfolio_companies_df['Efficiency (pts/$M$)'] = (st.session_state.portfolio_companies_df['Delta Org-AI-R'] / st.session_state.portfolio_companies_df['Investment ($M)']) * st.session_state.portfolio_companies_df['EBITDA Impact ($M)']
    st.session_state.portfolio_companies_df = st.session_state.portfolio_companies_df[['Company', 'Sector', 'Baseline Org-AI-R', 'Current Org-AI-R', 'Delta Org-AI-R', 'Investment ($M)', 'Efficiency (pts/$M$)', 'EBITDA Impact (%)', 'EBITDA ($M)', 'EBITDA Impact ($M)']]

    st.session_state.current_step = 1
    st.session_state.selected_company = 'Alpha Manufacturing' # Default for initial load
    st.session_state.baseline_v_org_r = 36
    st.session_state.external_signals_score = 45
    st.session_state.planning_horizon = 3
    st.session_state.visible_score = 75
    st.session_state.documented_score = 80
    st.session_state.sustainable_score = 70

    # Initialize company-dependent defaults for the initial selected company
    _reset_company_specific_state(st.session_state.selected_company)

if 'current_step' not in st.session_state:
    _initialize_app_state()

def restart_session_callback():
    _initialize_app_state() # Reset everything to initial app state
    st.rerun()

st.sidebar.button("Restart Session", on_click=restart_session_callback)
st.sidebar.subheader("Progress:")
progress_text = {
    1: "1 of 6: Company Selection",
    2: "2 of 6: Dimension Assessment",
    3: "3 of 6: Use Case Planning",
    4: "4 of 6: Multi-Year Plan",
    5: "5 of 6: Benchmarking",
    6: "6 of 6: Exit Readiness"
}
st.sidebar.write(progress_text[st.session_state.current_step])

# --- Navigation Functions ---
def next_step():
    st.session_state.current_step += 1

def prev_step():
    if st.session_state.current_step > 1:
        st.session_state.current_step -= 1

# --- Business Logic & Narrative ---
st.markdown("""
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
""")

st.divider()

# --- Step 1: Company Selection and Initial Org-AI-R Assessment ---
if st.session_state.current_step == 1:
    st.header("Step 1: Company Selection and Initial Org-AI-R Assessment")
    st.markdown("Our first step is to identify which portfolio company we're evaluating. Let's get an initial sense of its AI potential.")
    
    company_options = st.session_state.portfolio_companies_df['Company'].tolist()
    
    # Use the session_state.selected_company directly for index calculation
    selected_company_index = company_options.index(st.session_state.selected_company) if st.session_state.selected_company in company_options else 0

    new_selected_company = st.selectbox(
        "Select Portfolio Company",
        options=company_options,
        index=selected_company_index,
        key='selected_company' # Key directly maps to st.session_state.selected_company
    )

    # If the selected company changes via the widget, update dependent state and rerun
    if new_selected_company != st.session_state.selected_company:
        st.session_state.selected_company = new_selected_company # Update session state after widget interaction
        _reset_company_specific_state(st.session_state.selected_company) # Reset dependent states
        st.session_state.current_step = 1 # Keep on current step for re-evaluation
        st.rerun()

    # Retrieve current values from session state for display and calculation
    current_company_name = st.session_state.selected_company
    current_sector = st.session_state.selected_sector
    current_initial_ebitda_M = st.session_state.initial_ebitda_M

    st.write(f"**Selected Company:** {current_company_name}")
    st.write(f"**Sector:** {current_sector}")

    H_org_k_R = systematic_opportunity_scores[current_sector]
    st.write(f"**Systematic AI Opportunity ($H_{{org,k}}^R$):** {H_org_k_R} (Sector-specific potential)")

    # Widget for baseline_v_org_r. The 'value' is read from session state,
    # and the widget with 'key' will automatically update session_state.baseline_v_org_r.
    st.number_input(
        "Simulated Baseline Idiosyncratic Readiness ($V_{org,j}^R$)",
        min_value=0, max_value=100, value=st.session_state.baseline_v_org_r, step=1,
        key='baseline_v_org_r',
        help="Your preliminary estimate of the company's internal AI capabilities based on initial observations or limited data."
    )
    # Use st.session_state.baseline_v_org_r for calculations
    current_baseline_v_org_r = st.session_state.baseline_v_org_r

    synergy_score_initial = calculate_synergy(current_baseline_v_org_r, H_org_k_R)
    calculated_baseline_org_ai_r = calculate_org_ai_r(
        current_baseline_v_org_r, H_org_k_R, synergy_score_initial,
        model_coefficients['alpha'], model_coefficients['beta']
    )
    st.write(f"**Calculated Initial PE Org-AI-R Score:** {calculated_baseline_org_ai_r} (A high-level combined readiness score)")

    st.markdown(r"$$PE~Org-AI-R_{j,t} = \alpha \cdot V_{org,j}^R(t) + (1 - \alpha) \cdot H_{org,k}^R(t) + \beta \cdot Synergy(V_{org,j}^R, H_{org,k}^R)$$")
    st.markdown(r"where $V_{org,j}^R(t)$ is the company's idiosyncratic readiness, $H_{org,k}^R(t)$ is the systematic AI opportunity for the sector, $\alpha$ is the weight for idiosyncratic readiness, and $\beta$ is the synergy coefficient.")
    st.markdown(r"$$Synergy = \min(V_{org,j}^R, H_{org,k}^R)$$")
    st.markdown(r"where Synergy captures the alignment between internal capabilities and external opportunities.")

    # Widget for external_signals_score
    st.number_input(
        "Simulated External Signals Score",
        min_value=0, max_value=100, value=st.session_state.external_signals_score, step=1,
        key='external_signals_score',
        help="External market intelligence regarding a company's AI visibility, such as job postings or news mentions."
    )
    # Use st.session_state.external_signals_score for calculations
    current_external_signals_score = st.session_state.external_signals_score
    
    screening_score = calculate_screening_score(H_org_k_R, current_external_signals_score, model_coefficients['epsilon'])
    st.write(f"**Calculated Initial Screening Score:** {screening_score}")
    
    st.markdown(r"$$Screen_{j} = H_{org,k}^R + \epsilon \cdot ExternalSignals_j$$")
    st.markdown(rf"where $ExternalSignals_j$ represents external market intelligence, and $\epsilon$ is its weighting coefficient.")

    # Screening Recommendation Logic
    if screening_score > 120 and calculated_baseline_org_ai_r > 60:
        screening_recommendation = "Strong AI candidate: High potential and readiness. Prioritize for deep dive."
    elif screening_score > 100 or calculated_baseline_org_ai_r > 50:
        screening_recommendation = "Promising AI candidate: Investigate further. May have specific strengths."
    else:
        screening_recommendation = "Watchlist: Lower immediate AI priority. Monitor for changes or specific, targeted initiatives."
    
    st.info(f"**Screening Recommendation:** {screening_recommendation}")
    st.info("The Screening Recommendation guides your initial due diligence focus. A 'Strong AI candidate' suggests high potential and justifies deeper investigation.")

    st.button("Continue to Dimension-Level Assessment", on_click=next_step)

# --- Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis ---
elif st.session_state.current_step == 2:
    st.header("Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis")
    st.markdown("Now, let's conduct a detailed due diligence. Your expert assessment of the company's current capabilities across 7 key AI dimensions is crucial for understanding specific strengths and weaknesses.")

    H_org_k_R_step2 = systematic_opportunity_scores[st.session_state.selected_sector]
    sector_weights = all_dimension_weights_df[st.session_state.selected_sector]
    
    current_ratings = {}
    target_ratings = {}

    st.subheader("Your Assessment (1=Novice, 5=Expert)")
    cols = st.columns(2)
    for i, dim in enumerate(general_dimension_weights.keys()):
        with cols[i % 2]:
            st.markdown(f"**{dim}**")
            # Widgets directly update session state keys
            st.slider(
                f"Current Rating for {dim}",
                min_value=1, max_value=5, value=st.session_state[f'current_rating_{dim.replace(" ", "_").lower()}'], step=1,
                key=f'current_rating_{dim.replace(" ", "_").lower()}',
                help=f"Your assessment of the company's current {dim} maturity. A higher rating indicates robust capabilities, crucial for AI deployment."
            )
            st.slider(
                f"Target Rating for {dim}",
                min_value=1, max_value=5, value=st.session_state[f'target_rating_{dim.replace(" ", "_").lower()}'], step=1,
                key=f'target_rating_{dim.replace(" ", "_").lower()}',
                help=f"The desired future state for {dim} to maximize AI value creation."
            )
            # Retrieve values for calculations from session state AFTER widgets are rendered
            current_ratings[dim] = st.session_state[f'current_rating_{dim.replace(" ", "_").lower()}']
            target_ratings[dim] = st.session_state[f'target_rating_{dim.replace(" ", "_").lower()}']
            st.markdown("---")
            
    current_dimension_scores = calculate_dimension_score(pd.Series(current_ratings))
    target_dimension_scores = calculate_dimension_score(pd.Series(target_ratings))

    dimension_assessment_df = pd.DataFrame({
        'Dimension': general_dimension_weights.keys(),
        'Current Rating (1-5)': [current_ratings[d] for d in general_dimension_weights.keys()],
        'Current Score (0-100)': [current_dimension_scores[d] for d in general_dimension_weights.keys()],
        'Target Rating (1-5)': [target_ratings[d] for d in general_dimension_weights.keys()],
        'Target Score (0-100)': [target_dimension_scores[d] for d in general_dimension_weights.keys()]
    })
    dimension_assessment_df['Gap (Target - Current)'] = dimension_assessment_df['Target Score (0-100)'] - dimension_assessment_df['Current Score (0-100)']
    dimension_assessment_df = dimension_assessment_df.set_index('Dimension')

    st.subheader("Dimension-Level Assessment")
    st.dataframe(dimension_assessment_df.style.background_gradient(cmap='RdYlGn', subset=['Gap (Target - Current)']), use_container_width=True)
    
    st.markdown(r"$$D_k = \frac{Rating_{k}}{5} \times 100$$")
    st.markdown(r"where $Rating_k$ is the assigned rating (1-5) for dimension $k$.")
    st.markdown(r"$$Gap_k = D_k^{target} - D_k^{current}$$")
    st.markdown(r"where $D_k^{target}$ is the target score and $D_k^{current}$ is the current score for dimension $k$.")

    current_V_org_R_alpha = calculate_V_org_R(current_dimension_scores, sector_weights)
    target_V_org_R_alpha = calculate_V_org_R(target_dimension_scores, sector_weights)
    
    st.write(f"**Calculated Idiosyncratic Readiness ($V_{{org,j}}^R$) based on Detailed Assessment:** {current_V_org_R_alpha}")
    st.write(f"**Target Idiosyncratic Readiness ($V_{{org,j}}^{{R,target}}$):** {target_V_org_R_alpha}")

    synergy_score_alpha = calculate_synergy(current_V_org_R_alpha, H_org_k_R_step2)
    recalculated_current_org_ai_r_alpha = calculate_org_ai_r(
        current_V_org_R_alpha, H_org_k_R_step2, synergy_score_alpha,
        model_coefficients['alpha'], model_coefficients['beta']
    )
    st.write(f"**Recalculated PE Org-AI-R Score:** {recalculated_current_org_ai_r_alpha}")
    st.session_state.current_org_ai_r_alpha = recalculated_current_org_ai_r_alpha # Store for later use
    st.session_state.current_V_org_R_alpha = current_V_org_R_alpha # Store for later use


    st.subheader(f"AI Readiness Dimension Scores for {st.session_state.selected_company}")
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    categories = dimension_assessment_df.index.tolist()
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1] # Complete the loop

    current_values = dimension_assessment_df['Current Score (0-100)'].tolist()
    target_values = dimension_assessment_df['Target Score (0-100)'].tolist()
    current_values += current_values[:1]
    target_values += target_values[:1]

    ax.plot(angles, current_values, linewidth=1, linestyle='solid', label='Current Score', color='skyblue')
    ax.fill(angles, current_values, 'skyblue', alpha=0.25)
    ax.plot(angles, target_values, linewidth=1, linestyle='solid', label='Target Score', color='lightcoral')
    ax.fill(angles, target_values, 'lightcoral', alpha=0.25)

    ax.set_xticks(angles[:-1], categories, color='grey', size=10)
    ax.set_rlabel_position(0)
    ax.set_yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=8)
    ax.set_ylim(0, 100)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    st.pyplot(fig)
    st.info("This Radar Chart visually highlights the 'gaps' between current and target AI readiness. Large gaps represent critical areas requiring strategic investment and focus in your value creation plan.")

    st.subheader(f"AI Readiness Gap Analysis for {st.session_state.selected_company}")
    gap_df = dimension_assessment_df.sort_values(by='Gap (Target - Current)', ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=gap_df.index, y='Gap (Target - Current)', data=gap_df, palette='viridis', ax=ax)
    ax.set_ylabel('Gap (Target - Current Score)')
    ax.set_xlabel('AI Dimension')
    ax.set_title('AI Readiness Gap Analysis')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    st.info("This bar chart quickly identifies priority areas for investment by displaying the 'Gap' (Target - Current Score) for each dimension, sorted from largest to smallest.")


    cols_nav = st.columns(2)
    with cols_nav[0]:
        st.button("Back to Company Selection", on_click=prev_step)
    with cols_nav[1]:
        st.button("Continue to Use Case Identification", on_click=next_step)

# --- Step 3: Identify High-Value AI Use Cases & Estimate Impact ---
elif st.session_state.current_step == 3:
    st.header("Step 3: Identify High-Value AI Use Cases & Estimate Impact")
    st.markdown("With a clear understanding of the gaps, let's identify specific AI initiatives. Which high-value use cases will directly address the identified gaps and create the most significant impact for the company?")

    selected_sector_use_cases = high_value_use_cases[st.session_state.selected_sector]
    use_case_options = selected_sector_use_cases['Use Case'].tolist()
    
    st.session_state.selected_use_cases = st.multiselect(
        "Select High-Value AI Use Cases",
        options=use_case_options,
        default=[uc for uc in st.session_state.selected_use_cases if uc in use_case_options],
        key='selected_use_cases',
        help="Choose AI projects that align with the company's strategic goals and address identified capability gaps."
    )

    planned_initiatives_data = []
    if st.session_state.selected_use_cases:
        st.subheader("Customize Project Parameters")
        H_org_k_R_step3 = systematic_opportunity_scores[st.session_state.selected_sector]
        current_V_org_R_step3 = st.session_state.get('current_V_org_R_alpha', st.session_state.baseline_v_org_r)

        for uc_name in st.session_state.selected_use_cases:
            uc_data = selected_sector_use_cases[selected_sector_use_cases['Use Case'] == uc_name].iloc[0]
            st.markdown(f"#### {uc_name}")
            st.write(f"Description: *{uc_data['Description']}*")

            # Initialize defaults if not present for a newly selected use case
            investment_key = f'investment_{uc_name.replace(" ", "_").lower()}'
            prob_success_key = f'prob_success_{uc_name.replace(" ", "_").lower()}'
            exec_quality_key = f'exec_quality_{uc_name.replace(" ", "_").lower()}'
            
            if investment_key not in st.session_state:
                defaults = estimate_project_parameters(uc_data, current_V_org_R_step3, H_org_k_R_step3, st.session_state.initial_ebitda_M)
                st.session_state[investment_key] = defaults['Investment ($M)']
            if prob_success_key not in st.session_state:
                defaults = estimate_project_parameters(uc_data, current_V_org_R_step3, H_org_k_R_step3, st.session_state.initial_ebitda_M) # Recalculate or store only if needed
                st.session_state[prob_success_key] = defaults['Probability of Success']
            if exec_quality_key not in st.session_state:
                defaults = estimate_project_parameters(uc_data, current_V_org_R_step3, H_org_k_R_step3, st.session_state.initial_ebitda_M) # Recalculate or store only if needed
                st.session_state[exec_quality_key] = defaults['Execution Quality']


            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input(
                    f"Estimated Investment Cost for {uc_name} ($M$)",
                    min_value=0.1, max_value=10.0, value=st.session_state[investment_key], step=0.1,
                    key=investment_key,
                    help="The estimated financial outlay required for this AI project."
                )
            with col2:
                st.slider(
                    f"Probability of Success for {uc_name} (0-1)",
                    min_value=0.0, max_value=1.0, value=st.session_state[prob_success_key], step=0.01, format="%.2f",
                    key=prob_success_key,
                    help="Your confidence level in the successful implementation and adoption of this project."
                )
            with col3:
                st.slider(
                    f"Execution Quality Factor for {uc_name} (0-1)",
                    min_value=0.0, max_value=1.0, value=st.session_state[exec_quality_key], step=0.01, format="%.2f",
                    key=exec_quality_key,
                    help="Reflects the expected quality of implementation, influencing the realized benefits."
                )
            
            # Recalculate parameters with user inputs (retrieved from updated session state)
            estimated_params = estimate_project_parameters(
                uc_data, current_V_org_R_step3, H_org_k_R_step3, st.session_state.initial_ebitda_M,
                user_investment=st.session_state[investment_key],
                user_prob_success=st.session_state[prob_success_key],
                user_exec_quality=st.session_state[exec_quality_key]
            )
            
            planned_initiatives_data.append({
                'Use Case': uc_name,
                'Complexity': uc_data['Complexity'],
                'Timeline (months)': estimated_params['Timeline (months)'],
                'Investment ($M)': estimated_params['Investment ($M)'],
                'Probability of Success': estimated_params['Probability of Success'],
                'Execution Quality': estimated_params['Execution Quality'],
                'EBITDA Impact (%)': estimated_params['EBITDA Impact (%)'],
                'EBITDA Impact ($M)': estimated_params['EBITDA Impact ($M)'],
                'Delta Org-AI-R': estimated_params['Delta Org-AI-R']
            })
    
    if planned_initiatives_data:
        st.session_state.planned_initiatives_df = pd.DataFrame(planned_initiatives_data)
        st.subheader("Planned AI Initiatives and Estimated Impact")
        st.dataframe(st.session_state.planned_initiatives_df, use_container_width=True)

        st.markdown("Conceptual Formulas for Impact Estimation:")
        st.markdown(r"$$EBITDA~Impact~(\$M) = Base\_Impact~(\%) \times \frac{H_{org,k}^R}{100} \times \left(\frac{V_{org,j}^R}{100} \times 0.5 + 0.5\right) \times Probability\_Success \times Execution\_Quality \times Initial\_EBITDA~(\$M)$$")
        st.markdown(rf"where $Base\_Impact~(\%)$ is the inherent EBITDA impact of the use case, adjusted by the company's systematic opportunity ($H_{org,k}^R$), idiosyncratic readiness ($V_{org,j}^R$), and scaled by your assessed Probability of Success and Execution Quality, applied to the company's initial EBITDA.")
        st.markdown(r"$$\Delta Org-AI-R = Base\_Delta \times Probability\_Success \times Execution\_Quality$$")
        st.markdown(rf"where $Base\_Delta$ is the inherent Org-AI-R improvement potential of the use case, scaled by your assessed Probability of Success and Execution Quality.")

    cols_nav = st.columns(2)
    with cols_nav[0]:
        st.button("Back to Dimension Assessment", on_click=prev_step)
    with cols_nav[1]:
        st.button("Continue to Build Multi-Year Plan", on_click=next_step)

# --- Step 4: Build the Multi-Year AI Value Creation Plan ---
elif st.session_state.current_step == 4:
    st.header("Step 4: Build the Multi-Year AI Value Creation Plan")
    st.markdown("Now, let's integrate these initiatives into a cohesive multi-year plan, projecting the financial and strategic trajectory for the company under your guidance.")

    if st.session_state.planned_initiatives_df.empty:
        st.warning("Please go back to 'Identify High-Value AI Use Cases & Estimate Impact' to select and configure initiatives first. No multi-year plan can be generated without initiatives.")
        
        cols_nav = st.columns(2)
        with cols_nav[0]:
            st.button("Back to Use Case Identification", on_click=prev_step)
        with cols_nav[1]:
            st.button("Continue to Portfolio Benchmarking (No Plan)", on_click=next_step)
    else:
        initial_org_ai_r = st.session_state.get('current_org_ai_r_alpha', st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == st.session_state.selected_company]['Current Org-AI-R'].iloc[0])
        H_org_k_R_step4 = systematic_opportunity_scores[st.session_state.selected_sector]

        st.slider(
            "Planning Horizon (Years)",
            min_value=1, max_value=5, value=st.session_state.planning_horizon, step=1,
            key='planning_horizon',
            help="Define the timeframe for your AI value creation plan."
        )

        st.session_state.ai_plan_trajectory_df = create_multi_year_plan(
            st.session_state.selected_company,
            initial_org_ai_r,
            st.session_state.initial_ebitda_M,
            st.session_state.planned_initiatives_df,
            H_org_k_R_step4,
            st.session_state.planning_horizon
        )

        st.subheader(f"Multi-Year AI Plan Trajectory for {st.session_state.selected_company}")
        st.dataframe(st.session_state.ai_plan_trajectory_df, use_container_width=True)

        st.subheader(f"Cumulative EBITDA Impact for {st.session_state.selected_company} AI Plan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Year', y='Cumulative EBITDA Impact ($M)', data=st.session_state.ai_plan_trajectory_df, marker='o', ax=ax)
        ax.set_title(f'Cumulative EBITDA Impact for {st.session_state.selected_company}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Cumulative EBITDA Impact ($M$)')
        ax.grid(True)
        st.pyplot(fig)
        st.info("This line plot illustrates the projected financial value accretion over the defined planning horizon due to AI initiatives.")


        st.subheader(f"PE Org-AI-R Progression for {st.session_state.selected_company} AI Plan")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='Year', y='Org-AI-R', data=st.session_state.ai_plan_trajectory_df, marker='o', ax=ax)
        ax.set_title(f'PE Org-AI-R Progression for {st.session_state.selected_company}')
        ax.set_xlabel('Year')
        ax.set_ylabel('Org-AI-R Score')
        ax.set_ylim(0, 100)
        ax.grid(True)
        st.pyplot(fig)
        st.info("This line plot shows the clear trajectory of the company's AI capability improvement (Org-AI-R Score) over the multi-year plan.")

        cols_nav = st.columns(2)
        with cols_nav[0]:
            st.button("Back to Use Case Identification", on_click=prev_step)
        with cols_nav[1]:
            st.button("Continue to Portfolio Benchmarking", on_click=next_step)

# --- Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking ---
elif st.session_state.current_step == 5:
    st.header("Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking")
    st.markdown("With the plan defined, it's time to evaluate its efficiency and see how it benchmarks against other companies in our portfolio. This informs fund-level strategy and resource allocation.")

    # Get current values for the selected company from the main portfolio_companies_df
    current_company_df_state = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == st.session_state.selected_company]
    if current_company_df_state.empty:
        st.warning(f"Company {st.session_state.selected_company} not found in portfolio data. Please restart session.")
        st.button("Back to Multi-Year Plan", on_click=prev_step)
        return

    initial_company_row_for_update = current_company_df_state.iloc[0].copy() # Using a copy to store initial state before calculation updates
    
    final_org_ai_r_for_calc = st.session_state.get('current_org_ai_r_alpha', initial_company_row_for_update['Current Org-AI-R'])
    total_delta_org_ai_r_plan = 0.0
    total_investment_plan_M = 0.0
    total_ebitda_impact_plan_M = 0.0
    aie_score = 0.0

    if not st.session_state.ai_plan_trajectory_df.empty:
        final_org_ai_r_for_calc = st.session_state.ai_plan_trajectory_df['Org-AI-R'].iloc[-1]
        total_delta_org_ai_r_plan = final_org_ai_r_for_calc - st.session_state.get('current_org_ai_r_alpha', initial_company_row_for_update['Current Org-AI-R'])
        total_investment_plan_M = st.session_state.ai_plan_trajectory_df['Cumulative Investment ($M)'].iloc[-1]
        total_ebitda_impact_plan_M = st.session_state.ai_plan_trajectory_df['Cumulative EBITDA Impact ($M)'].iloc[-1]
        aie_score = calculate_ai_investment_efficiency(total_delta_org_ai_r_plan, total_investment_plan_M, total_ebitda_impact_plan_M)
        
        total_delta_org_ai_r_plan = max(0.0, total_delta_org_ai_r_plan)
        total_investment_plan_M = max(0.0, total_investment_plan_M)
        total_ebitda_impact_plan_M = max(0.0, total_ebitda_impact_plan_M)

        st.subheader(f"AI Investment Efficiency for {st.session_state.selected_company}")
        st.write(f"**Total Projected Delta Org-AI-R:** {total_delta_org_ai_r_plan:.2f} points")
        st.write(f"**Total Projected AI Investment:** ${total_investment_plan_M:.2f}M")
        st.write(f"**Total Projected Cumulative EBITDA Impact:** ${total_ebitda_impact_plan_M:.2f}M")
        st.markdown(f"**AI Investment Efficiency (AIE):** **{aie_score:.2f} pts*$M$/$M$**")

        st.markdown(r"$$AIE = \left(\frac{\Delta Org-AI-R}{AI~Investment}\right) \times EBITDA~Impact$$")
        st.markdown(rf"where $\Delta Org-AI-R$ is the total change in the Org-AI-R score, $AI~Investment$ is the total capital deployed, and $EBITDA~Impact$ is the total financial gain (all over the planning horizon).")
        st.info("The AI Investment Efficiency (AIE) metric quantifies the return on your AI investment, considering both capability improvement and financial impact. A higher AIE signifies more efficient AI capital deployment.")
    else:
        st.warning("No multi-year plan generated. AI Investment Efficiency will be calculated as zero. Please go back to previous steps to define AI initiatives.")

    # Update the portfolio_companies_df in session state with the new calculated values for the selected company
    selected_company_index = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == st.session_state.selected_company].index
    if not selected_company_index.empty:
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'Current Org-AI-R'] = final_org_ai_r_for_calc
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'Delta Org-AI-R'] = total_delta_org_ai_r_plan
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'Investment ($M)'] = total_investment_plan_M
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'EBITDA Impact ($M)'] = total_ebitda_impact_plan_M
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'Efficiency (pts/$M$)'] = aie_score
        # Update the base EBITDA with the projected initial EBITDA plus the cumulative impact for future steps
        st.session_state.portfolio_companies_df.loc[selected_company_index, 'EBITDA ($M)'] = initial_company_row_for_update['EBITDA ($M)'] + total_ebitda_impact_plan_M # Base EBITDA + cumulative impact

    st.subheader("Portfolio Benchmarking")
    
    all_org_ai_rs = st.session_state.portfolio_companies_df['Current Org-AI-R'].tolist()
    all_aie_scores = st.session_state.portfolio_companies_df['Efficiency (pts/$M$)'].tolist()

    company_current_org_ai_r = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == st.session_state.selected_company]['Current Org-AI-R'].iloc[0]
    company_org_ai_r_percentile = calculate_within_portfolio_percentile(company_current_org_ai_r, all_org_ai_rs)
    
    portfolio_mean_org_ai_r = st.session_state.portfolio_companies_df['Current Org-AI-R'].mean()
    portfolio_std_org_ai_r = st.session_state.portfolio_companies_df['Current Org-AI-R'].std()
    company_org_ai_r_z_score = calculate_cross_portfolio_z_score(company_current_org_ai_r, portfolio_mean_org_ai_r, portfolio_std_org_ai_r)

    st.write(f"**{st.session_state.selected_company} Org-AI-R Percentile (within Portfolio):** {company_org_ai_r_percentile:.2f}% (relative to current state after plan)")
    st.write(f"**{st.session_state.selected_company} Org-AI-R Z-Score (within Portfolio):** {company_org_ai_r_z_score:.2f} (relative to current state after plan)")

    st.markdown(r"$$Percentile_j = \left( \frac{\text{Number of companies with } Org-AI-R \le Org-AI-R_j}{\text{Total number of companies}} \right) \times 100$$")
    st.markdown(r"where $Org-AI-R_j$ is the score for company $j$.")
    st.markdown(r"$$Z-Score_j = \frac{Org-AI-R_j - \mu_{portfolio}}{\sigma_{portfolio}}$$")
    st.markdown(rf"where $\mu_{{portfolio}}$ is the mean and $\sigma_{{portfolio}}$ is the standard deviation of Org-AI-R scores across the portfolio.")
    st.info("These metrics help position your company's AI performance relative to its peers, identifying leaders and laggards.")


    st.subheader("Current PE Org-AI-R Scores Across Portfolio Companies")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Company', y='Current Org-AI-R', hue='Sector', data=st.session_state.portfolio_companies_df, palette='viridis', ax=ax)
    ax.axhline(company_current_org_ai_r, color='red', linestyle='--', label=f'{st.session_state.selected_company} (You)')
    ax.set_title('Current PE Org-AI-R Scores Across Portfolio Companies')
    ax.set_xlabel('Company')
    ax.set_ylabel('Current Org-AI-R Score')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(loc='lower right')
    st.pyplot(fig)
    st.info("This bar chart shows the relative positioning of the selected company against its peers in terms of AI readiness, with your company highlighted.")

    st.subheader("AI Investment Efficiency Across Portfolio Companies")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Company', y='Efficiency (pts/$M$)', hue='Sector', data=st.session_state.portfolio_companies_df, palette='magma', ax=ax)
    ax.axhline(aie_score, color='red', linestyle='--', label=f'{st.session_state.selected_company} (You)')
    ax.set_title('AI Investment Efficiency Across Portfolio Companies')
    ax.set_xlabel('Company')
    ax.set_ylabel('Efficiency (pts*$M$/$M$)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(loc='upper right')
    st.pyplot(fig)
    st.info("This visualization benchmarks the effectiveness of AI capital deployment across the portfolio, highlighting which companies generate the most combined Org-AI-R and EBITDA impact per dollar invested.")
    
    cols_nav = st.columns(2)
    with cols_nav[0]:
        st.button("Back to Multi-Year Plan", on_click=prev_step)
    with cols_nav[1]:
        st.button("Continue to Exit-Readiness Assessment", on_click=next_step)

# --- Step 6: Exit-Readiness Assessment ---
elif st.session_state.current_step == 6:
    st.header("Step 6: Exit-Readiness Assessment")
    st.markdown("Finally, let's project how these AI investments enhance the company's appeal to potential buyers and impact its exit valuation. Crafting a compelling AI narrative is key to maximizing our returns.")

    # Retrieve current_company_row from the updated portfolio_companies_df in session state
    current_company_row = st.session_state.portfolio_companies_df[st.session_state.portfolio_companies_df['Company'] == st.session_state.selected_company].iloc[0]

    st.slider(
        "Visible AI Capabilities Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.visible_score, step=1,
        key='visible_score',
        help="How easily apparent are the company's AI features, technology stack, and demonstrable use cases to an external buyer?"
    )
    st.slider(
        "Documented AI Impact Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.documented_score, step=1,
        key='documented_score',
        help="Availability and quality of auditable data demonstrating AI's financial impact (ROI, cost savings, revenue uplift)."
    )
    st.slider(
        "Sustainable AI Capabilities Score (0-100)",
        min_value=0, max_value=100, value=st.session_state.sustainable_score, step=1,
        key='sustainable_score',
        help="Are AI capabilities embedded in processes, talent, and infrastructure, or are they one-off projects? Indicates long-term defensibility."
    )

    exit_ai_r_score = assess_exit_readiness(
        st.session_state.visible_score, st.session_state.documented_score, st.session_state.sustainable_score,
        model_coefficients['w1_exit'], model_coefficients['w2_exit'], model_coefficients['w3_exit']
    )
    st.write(f"**Calculated Exit-AI-R Score:** {exit_ai_r_score:.2f} (Weighted score of AI attractiveness to buyers)")
    
    st.markdown(r"$$Exit-AI-R_j = w_1 \cdot Visible_j + w_2 \cdot Documented_j + w_3 \cdot Sustainable_j$$")
    st.markdown(r"where $Visible_j$, $Documented_j$, and $Sustainable_j$ are scores reflecting the market-facing aspects of AI, and $w_1, w_2, w_3$ are their respective weights.")

    sector_base_multiples = {'Manufacturing': 6.0, 'Healthcare': 7.5, 'Retail': 5.5, 'Business Services': 8.0, 'Technology': 10.0}
    default_base_multiple_for_sector = sector_base_multiples.get(st.session_state.selected_sector, 6.5)

    # If the base_exit_multiple hasn't been explicitly set by user, or if sector changed, update default
    # The `selected_sector` is part of company-specific state, reset with `_reset_company_specific_state`
    if st.session_state.last_sector_for_exit != st.session_state.selected_sector:
        st.session_state.base_exit_multiple = default_base_multiple_for_sector
        st.session_state.last_sector_for_exit = st.session_state.selected_sector
    
    st.number_input(
        "Baseline Exit Multiple (e.g., for selected sector)",
        min_value=1.0, max_value=20.0, value=st.session_state.base_exit_multiple, step=0.1,
        key='base_exit_multiple',
        help="The assumed pre-AI or industry-average valuation multiple for the company."
    )

    predicted_exit_multiple = predict_exit_multiple(
        st.session_state.base_exit_multiple, exit_ai_r_score, model_coefficients['delta_exit']
    )
    st.write(f"**Predicted Exit Multiple with AI Premium:** {predicted_exit_multiple:.2f}x")
    
    st.markdown(r"$$Multiple_j = Multiple_{base,k} + \delta \cdot \frac{Exit-AI-R_j}{100}$$")
    st.markdown(rf"where $Multiple_{{base,k}}$ is the baseline multiple for the sector, $Exit-AI-R_j$ is the assessed Exit-AI-R score, and $\delta$ is the AI premium coefficient.")
    st.info("The predicted exit multiple indicates the potential valuation uplift due to strategically embedded and demonstrated AI capabilities. A higher multiple reflects a stronger, more defensible asset.")

    st.subheader(f"Projected EBITDA for {st.session_state.selected_company} at Exit")
    # current_company_row already holds the updated EBITDA after the plan from Step 5
    projected_final_ebitda = current_company_row['EBITDA ($M)']
    
    st.write(f"**Projected EBITDA at Exit (after AI plan):** ${projected_final_ebitda:.2f}M")
    st.write(f"**Implied Valuation (EBITDA x Multiple):** ${projected_final_ebitda * predicted_exit_multiple:.2f}M")
    
    st.markdown("---")
    st.success("Congratulations, Portfolio Manager! You've completed the AI Value Creation & Investment Efficiency Planner for this asset. You've gone from initial screening to a detailed plan and exit projection. Click 'Restart Session' in the sidebar to analyze another company.")

    cols_nav = st.columns(2)
    with cols_nav[0]:
        st.button("Back to Portfolio Benchmarking", on_click=prev_step)
    # No 'Continue' button after the final step, as per narrative.
