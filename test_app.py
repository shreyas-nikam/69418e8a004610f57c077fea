
import pytest
from streamlit.testing.v1 import AppTest
import pandas as pd
import numpy as np

# Helper function to get default dimension ratings, mirroring utils.py logic
def _get_simulated_dimension_ratings(company_name, sector, is_target=False):
    seed_val = hash(company_name + sector + str(is_target)) % (2**32 - 1)
    rng = np.random.default_rng(seed_val)
    ratings = {}
    general_dimension_weights = {
        'Data Infrastructure': 0.25, 'AI Governance': 0.20, 'Technology Stack': 0.15,
        'Talent': 0.15, 'Leadership': 0.10, 'Use Case Portfolio': 0.10, 'Culture': 0.05
    }
    for dim in general_dimension_weights.keys():
        if is_target:
            ratings[dim] = int(rng.integers(3, 6))  # Target ratings tend to be higher
        else:
            ratings[dim] = int(rng.integers(1, 4))  # Current ratings for baseline
    return pd.Series(ratings, name='Rating (1-5)')

# Helper function to simulate get_initial_portfolio_companies_df for test setup
def _get_initial_portfolio_companies_df_for_test():
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
    df = pd.DataFrame(initial_portfolio_companies_data)
    df['EBITDA Impact ($M)'] = df['EBITDA ($M)'] * (df['EBITDA Impact (%)'] / 100)
    df['Efficiency (pts/$M$)'] = (df['Delta Org-AI-R'] / df['Investment ($M)']) * df['EBITDA Impact ($M)']
    return df[['Company', 'Sector', 'Baseline Org-AI-R', 'Current Org-AI-R', 'Delta Org-AI-R', 'Investment ($M)', 'Efficiency (pts/$M$)', 'EBITDA Impact (%)', 'EBITDA ($M)', 'EBITDA Impact ($M)']]

# Pre-computation of expected values for 'Alpha Manufacturing' defaults
ALPHA_MANUFACTURING_ROW = _get_initial_portfolio_companies_df_for_test()[_get_initial_portfolio_companies_df_for_test()['Company'] == 'Alpha Manufacturing'].iloc[0]
ALPHA_EBITDA_M = ALPHA_MANUFACTURING_ROW['EBITDA ($M)']

# Model coefficients and scores from utils.py
model_coefficients = {
    'alpha': 0.65, 'beta': 0.15, 'gamma': 0.035, 'epsilon': 0.30,
    'w1_exit': 0.35, 'w2_exit': 0.40, 'w3_exit': 0.25, 'delta_exit': 2.0
}
systematic_opportunity_scores = {
    'Manufacturing': 72, 'Healthcare': 78, 'Retail': 75,
    'Business Services': 80, 'Technology': 85
}
sector_dimension_weight_adjustments = {
    'Manufacturing': {
        'Data Infrastructure': 0.28, 'AI Governance': 0.15, 'Technology Stack': 0.18,
        'Talent': 0.15, 'Leadership': 0.08, 'Use Case Portfolio': 0.12, 'Culture': 0.04
    }
}
alpha_sector_weights_series = pd.Series(sector_dimension_weight_adjustments['Manufacturing'])


@pytest.fixture(autouse=True)
def setup_teardown_session_state():
    # Ensure a fresh session state for each test
    at = AppTest.from_file("app.py")
    at.run() # Run once to initialize
    yield at
    # No explicit teardown needed as pytest manages app instances

def test_full_app_flow_and_restart():
    at = AppTest.from_file("app.py").run()
    # --- Initial State & Page 1 Defaults ---
    assert at.sidebar.radio[0].value == 0
    assert at.session_state['selected_company'] == 'Alpha Manufacturing'
    assert at.session_state['baseline_v_org_r'] == 36
    assert at.session_state['external_signals_score'] == 45
    assert at.session_state['H_org_k_R'] == systematic_opportunity_scores['Manufacturing'] # 72
    assert at.session_state['synergy_score'] == 36.0
    assert at.session_state['calculated_baseline_org_ai_r'] == 54.0
    assert at.session_state['screening_score'] == 85.5

    # --- Page 1 Interactions ---
    at.number_input(key='baseline_v_org_r').set_value(50).run()
    at.number_input(key='external_signals_score').set_value(60).run()
    assert at.session_state['baseline_v_org_r'] == 50
    assert at.session_state['external_signals_score'] == 60
    assert at.session_state['synergy_score'] == 50.0 # min(50, 72)
    assert at.session_state['calculated_baseline_org_ai_r'] == 65.2 # (0.65*50) + (0.35*72) + (0.15*50)
    assert at.session_state['screening_score'] == 90.0 # 72 + (0.30*60)
    at.button(key='continue_page1').click().run()
    assert at.sidebar.radio[0].value == 1
    assert at.session_state['page'] == "Deep Dive: Dimension-Level Assessment & Gap Analysis"

    # --- Page 2: Dimension Assessment ---
    assert at.session_state['selected_company'] == 'Alpha Manufacturing'
    assert at.session_state['selected_sector'] == 'Manufacturing'
    
    # Predict default slider values for Page 2
    expected_alpha_current_ratings = _get_simulated_dimension_ratings('Alpha Manufacturing', 'Manufacturing', is_target=False)
    expected_alpha_target_ratings = _get_simulated_dimension_ratings('Alpha Manufacturing', 'Manufacturing', is_target=True)
    assert at.slider(key='current_rating_data_infrastructure').value == expected_alpha_current_ratings['Data Infrastructure']
    assert at.slider(key='target_rating_data_infrastructure').value == expected_alpha_target_ratings['Data Infrastructure']

    # Simulate changing a slider (Data Infrastructure current & target)
    at.slider(key='current_rating_data_infrastructure').set_value(3).run()
    at.slider(key='target_rating_data_infrastructure').set_value(5).run()

    # Calculate expected V_org_R and Org-AI-R based on these changes
    alpha_current_ratings_modified = expected_alpha_current_ratings.copy()
    alpha_current_ratings_modified['Data Infrastructure'] = 3
    alpha_target_ratings_modified = expected_alpha_target_ratings.copy()
    alpha_target_ratings_modified['Data Infrastructure'] = 5

    alpha_current_scores_modified = (alpha_current_ratings_modified / 5 * 100).round(2)
    alpha_target_scores_modified = (alpha_target_ratings_modified / 5 * 100).round(2)
    
    aligned_current_scores_modified = alpha_current_scores_modified.reindex(alpha_sector_weights_series.index, fill_value=0)
    current_V_org_R_expected = (aligned_current_scores_modified * alpha_sector_weights_series).sum().round(2)
    aligned_target_scores_modified = alpha_target_scores_modified.reindex(alpha_sector_weights_series.index, fill_value=0)
    target_V_org_R_expected = (aligned_target_scores_modified * alpha_sector_weights_series).sum().round(2)

    current_synergy_expected = min(current_V_org_R_expected, systematic_opportunity_scores['Manufacturing'])
    recalculated_current_org_ai_r_expected = round(
        (model_coefficients['alpha'] * current_V_org_R_expected) +
        ((1 - model_coefficients['alpha']) * systematic_opportunity_scores['Manufacturing']) +
        (model_coefficients['beta'] * current_synergy_expected), 2
    )
    target_synergy_expected = min(target_V_org_R_expected, systematic_opportunity_scores['Manufacturing'])
    recalculated_target_org_ai_r_expected = round(
        (model_coefficients['alpha'] * target_V_org_R_expected) +
        ((1 - model_coefficients['alpha']) * systematic_opportunity_scores['Manufacturing']) +
        (model_coefficients['beta'] * target_synergy_expected), 2
    )

    assert at.session_state['current_V_org_R'] == current_V_org_R_expected
    assert at.session_state['target_V_org_R'] == target_V_org_R_expected
    assert at.session_state['recalculated_current_org_ai_r'] == recalculated_current_org_ai_r_expected
    assert at.session_state['recalculated_target_org_ai_r'] == recalculated_target_org_ai_r_expected
    assert 'dimension_assessment_df' in at.session_state and not at.session_state['dimension_assessment_df'].empty
    assert len(at.pyplot) == 2 # Radar chart and Bar chart
    at.button(key='continue_page2').click().run()
    assert at.sidebar.radio[0].value == 2
    assert at.session_state['page'] == "Identify High-Value AI Use Cases & Estimate Impact"

    # --- Page 3: Use Case Selection ---
    assert at.session_state['current_V_org_R'] == current_V_org_R_expected
    assert at.session_state['H_org_k_R'] == 72
    assert at.session_state['initial_ebitda_M'] == ALPHA_EBITDA_M
    assert len(at.multiselect[0].value) == 3 # Default selections

    # Test warning for no use cases selected
    at.multiselect(key='selected_use_cases').set_value([]).run()
    at.button(key='continue_page3').click().run()
    assert at.warning[0].value == "Please select at least one AI use case to build the multi-year plan."
    assert at.sidebar.radio[0].value == 2 # Still on page 3

    # Select one use case and adjust parameters
    at.multiselect(key='selected_use_cases').set_value(['Predictive Maintenance']).run()
    # Import `utils` functions for calculating expected values within the test
    from utils import estimate_project_parameters as _ep_
    pred_maint_uc_info = {
        'Use Case': 'Predictive Maintenance', 'Complexity': 'Medium', 'Timeline (months)': '6-12',
        'EBITDA Impact (min%)': 2, 'EBITDA Impact (max%)': 4,
        'Description': 'AI-driven equipment monitoring reducing unplanned downtime 15-25%'
    }
    adjusted_pred_maint_params = _ep_(
        pred_maint_uc_info, current_V_org_R_expected, 72, ALPHA_EBITDA_M,
        user_investment=3.5, user_prob_success=0.9, user_exec_quality=0.85
    )
    at.number_input(key='investment_predictive_maintenance').set_value(3.5).run()
    at.slider(key='prob_success_predictive_maintenance').set_value(0.9).run()
    at.slider(key='exec_quality_predictive_maintenance').set_value(0.85).run()
    
    assert 'planned_initiatives_df' in at.session_state
    planned_df = at.session_state.planned_initiatives_df
    assert not planned_df.empty
    assert len(planned_df) == 1
    assert planned_df.iloc[0]['Use Case'] == 'Predictive Maintenance'
    assert planned_df.iloc[0]['Investment ($M)'] == 3.5
    assert planned_df.iloc[0]['Probability of Success'] == 0.9
    assert planned_df.iloc[0]['Execution Quality'] == 0.85
    assert planned_df.iloc[0]['EBITDA Impact (%)'] == adjusted_pred_maint_params['EBITDA Impact (%)']
    assert planned_df.iloc[0]['EBITDA Impact ($M)'] == adjusted_pred_maint_params['EBITDA Impact ($M)']
    assert planned_df.iloc[0]['Delta Org-AI-R'] == adjusted_pred_maint_params['Delta Org-AI-R']
    at.button(key='continue_page3').click().run()
    assert at.sidebar.radio[0].value == 3
    assert at.session_state['page'] == "Build the Multi-Year AI Value Creation Plan"

    # --- Page 4: Multi-Year Plan ---
    assert at.session_state['recalculated_current_org_ai_r'] == recalculated_current_org_ai_r_expected
    assert at.session_state['initial_ebitda_M'] == ALPHA_EBITDA_M
    assert at.slider(key='planning_horizon').value == 3 # Default
    at.slider(key='planning_horizon').set_value(2).run() # Change to 2 years

    from utils import create_multi_year_plan as _cmyp_
    expected_plan_trajectory_df = _cmyp_(
        company_name='Alpha Manufacturing',
        initial_org_ai_r=recalculated_current_org_ai_r_expected,
        initial_ebitda_M=ALPHA_EBITDA_M,
        planned_initiatives_df=planned_df, # Use the modified planned_df
        H_org_k_R=72,
        total_years=2
    )
    pd.testing.assert_frame_equal(at.session_state.ai_plan_trajectory_df, expected_plan_trajectory_df)
    assert len(at.pyplot) == 2 # EBITDA Impact and Org-AI-R progression charts
    at.button(key='continue_page4').click().run()
    assert at.sidebar.radio[0].value == 4
    assert at.session_state['page'] == "Calculate AI Investment Efficiency & Portfolio Benchmarking"

    # --- Page 5: Portfolio Benchmarking ---
    final_year_data = expected_plan_trajectory_df.iloc[-1]
    total_delta_org_ai_r_plan_expected = final_year_data['Org-AI-R'] - recalculated_current_org_ai_r_expected
    total_investment_plan_M_expected = final_year_data['Investment ($M) - Cumulative']
    total_ebitda_impact_plan_M_expected = final_year_data['Cumulative EBITDA Impact ($M)']

    from utils import calculate_ai_investment_efficiency as _caie_
    aie_expected = _caie_(
        total_delta_org_ai_r_plan_expected, total_investment_plan_M_expected, total_ebitda_impact_plan_M_expected
    )
    assert at.metric[0].value == f"{total_delta_org_ai_r_plan_expected:.2f} pts"
    assert at.metric[1].value == f"${total_investment_plan_M_expected:.2f} M"
    assert at.metric[2].value == f"${total_ebitda_impact_plan_M_expected:.2f} M"
    assert at.metric[3].value == f"{aie_expected:.2f} pts*$M$/$M$"
    
    assert 'portfolio_companies_df' in at.session_state
    updated_portfolio_df = at.session_state.portfolio_companies_df
    alpha_updated_row = updated_portfolio_df[updated_portfolio_df['Company'] == 'Alpha Manufacturing'].iloc[0]
    assert alpha_updated_row['Current Org-AI-R'] == final_year_data['Org-AI-R']
    assert alpha_updated_row['Efficiency (pts/$M$)'] == aie_expected
    assert 'Org-AI-R Percentile' in updated_portfolio_df.columns
    assert 'Org-AI-R Z-Score' in updated_portfolio_df.columns
    assert len(at.pyplot) == 2 # Portfolio Org-AI-R and AIE charts
    at.button(key='continue_page5').click().run()
    assert at.sidebar.radio[0].value == 5
    assert at.session_state['page'] == "Exit-Readiness Assessment"

    # --- Page 6: Exit-Readiness Assessment ---
    assert at.session_state['selected_company'] == 'Alpha Manufacturing'
    assert at.session_state['ai_plan_trajectory_df'].iloc[-1]['Org-AI-R'] == final_year_data['Org-AI-R']
    
    # Default values
    assert at.slider(key='visible_score').value == 75
    assert at.slider(key='documented_score').value == 80
    assert at.slider(key='sustainable_score').value == 70
    assert at.number_input(key='base_exit_multiple').value == 6.5

    from utils import assess_exit_readiness as _aer_, predict_exit_multiple as _pem_
    exit_ai_r_expected_default = _aer_(75, 80, 70, model_coefficients['w1_exit'], model_coefficients['w2_exit'], model_coefficients['w3_exit'])
    predicted_exit_multiple_expected_default = _pem_(6.5, exit_ai_r_expected_default, model_coefficients['delta_exit'])
    assert at.metric[0].value == f"{exit_ai_r_expected_default:.2f}"
    assert at.metric[1].value == f"{predicted_exit_multiple_expected_default:.2f}x"

    # Simulate changing inputs
    at.slider(key='visible_score').set_value(90).run()
    at.slider(key='documented_score').set_value(95).run()
    at.number_input(key='base_exit_multiple').set_value(7.0).run()

    exit_ai_r_expected_changed = _aer_(90, 95, 70, model_coefficients['w1_exit'], model_coefficients['w2_exit'], model_coefficients['w3_exit'])
    predicted_exit_multiple_expected_changed = _pem_(7.0, exit_ai_r_expected_changed, model_coefficients['delta_exit'])
    assert at.metric[0].value == f"{exit_ai_r_expected_changed:.2f}"
    assert at.metric[1].value == f"{predicted_exit_multiple_expected_changed:.2f}x"

    # --- Test Restart Session ---
    # Store a unique value in session_state to verify it's cleared
    at.session_state['test_key_to_be_cleared'] = "Should be gone"
    at.button(key='restart_final').click().run()

    assert 'test_key_to_be_cleared' not in at.session_state # Verify cleared
    assert at.sidebar.radio[0].value == 0 # Back to page 1
    assert at.session_state['page'] == "Company Selection and Initial Org-AI-R Assessment"
    assert at.session_state['selected_company'] == 'Alpha Manufacturing' # Re-initialized
    assert at.session_state['baseline_v_org_r'] == 36 # Re-initialized (back to 36, not 50 from previous interaction)
