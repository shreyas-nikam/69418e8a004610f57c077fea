
from streamlit.testing.v1 import AppTest
import pandas as pd
import numpy as np
import warnings

# Suppress warnings that might arise from app's internal logic or test interactions
warnings.filterwarnings('ignore')

# Helper to run to a specific step
def run_to_step(at, target_step, initial_run=True):
    if initial_run:
        at.run()

    while at.session_state.get("current_step", 1) < target_step:
        current_step = at.session_state.get("current_step", 1)
        
        # Determine which button to click based on the current step and available options
        if current_step == 1:
            # "Continue to Dimension-Level Assessment"
            at.button[0].click().run()
        elif current_step == 2:
            # "Continue to Use Case Identification" (second button)
            at.button[1].click().run()
        elif current_step == 3:
            # Ensure some use cases are selected to proceed, otherwise the next button might not appear
            if at.session_state["planned_initiatives_df"].empty:
                # Select a default use case if none are present to enable progression
                # Assuming 'Predictive Maintenance' is a valid option for 'Manufacturing' (default sector)
                if 'Predictive Maintenance' in at.multiselect[0].options:
                    at.multiselect[0].set_values(['Predictive Maintenance']).run()
                else: # Fallback for other sectors
                    at.multiselect[0].set_values([at.multiselect[0].options[0]]).run()
            # "Continue to Build Multi-Year Plan" (second button)
            at.button[1].click().run()
        elif current_step == 4:
            # Handle different button labels for Step 4 depending on whether a plan was built
            if "Continue to Portfolio Benchmarking" in [b.label for b in at.button]:
                at.button[[b.label for b in at.button].index("Continue to Portfolio Benchmarking")].click().run()
            elif "Continue to Portfolio Benchmarking (No Plan)" in [b.label for b in at.button]:
                at.button[[b.label for b in at.button].index("Continue to Portfolio Benchmarking (No Plan)")].click().run()
            else:
                raise Exception(f"Could not find button to proceed from Step 4. Current buttons: {[b.label for b in at.button]}")
        elif current_step == 5:
            # "Continue to Exit-Readiness Assessment" (second button)
            at.button[1].click().run()
        else:
            # Should not happen if target_step is reachable and correctly handled
            break
            
        # Re-run to process the state changes and render the next step
        # AppTest.click().run() already does this, but defensive check
        if at.session_state.get("current_step", 1) == current_step:
            # If step didn't change, something went wrong, or it's the last step
            break
    
    assert at.session_state.get("current_step") == target_step
    return at


def test_app_initial_load_and_restart():
    """
    Tests the initial load of the application, checks default session state,
    and verifies the "Restart Session" functionality.
    """
    at = AppTest.from_file("app.py").run()

    # Initial state checks
    assert at.session_state["current_step"] == 1
    assert "Alpha Manufacturing" in at.session_state["portfolio_companies_df"]["Company"].tolist()
    assert at.session_state["selected_company"] == "Alpha Manufacturing"
    assert at.session_state["selected_sector"] == "Manufacturing"
    assert at.sidebar.button[0].label == "Restart Session" # Assuming it's the first sidebar button

    # Test changing a value and then restarting
    original_baseline_v_org_r = at.session_state["baseline_v_org_r"]
    at.number_input[0].set_value(50).run() # Change baseline_v_org_r
    assert at.session_state["baseline_v_org_r"] == 50

    at.sidebar.button[0].click().run() # Click restart
    assert at.session_state["current_step"] == 1
    assert at.session_state["baseline_v_org_r"] == original_baseline_v_org_r # Should reset to default
    assert at.session_state["selected_company"] == "Alpha Manufacturing" # Restart also resets selected company


def test_step1_company_selection_and_screening():
    """
    Tests Step 1: Company Selection and Initial Org-AI-R Assessment.
    Verifies initial calculations, input changes, and company selection.
    """
    at = AppTest.from_file("app.py").run()

    assert at.session_state["current_step"] == 1
    assert at.selectbox[0].label == "Select Portfolio Company"
    assert at.selectbox[0].value == "Alpha Manufacturing"
    
    # Read model coefficients and systematic opportunity from the app's initial state
    model_coefficients = at.get("model_coefficients", {})
    systematic_opportunity_scores = at.get("systematic_opportunity_scores", {})
    
    alpha = model_coefficients.get('alpha', 0.65)
    beta = model_coefficients.get('beta', 0.15)
    epsilon = model_coefficients.get('epsilon', 0.30)

    # Test initial calculations for Alpha Manufacturing (default values)
    H_org_k_R_alpha = systematic_opportunity_scores.get('Manufacturing', 72)
    baseline_v_org_r = at.session_state["baseline_v_org_r"] # default 36
    synergy_score_initial = min(baseline_v_org_r, H_org_k_R_alpha)
    expected_org_ai_r = round((alpha * baseline_v_org_r) + ((1 - alpha) * H_org_k_R_alpha) + (beta * synergy_score_initial), 2)
    assert at.markdown[4].value == f"**Calculated Initial PE Org-AI-R Score:** {expected_org_ai_r} (A high-level combined readiness score)"

    external_signals_score = at.session_state["external_signals_score"] # default 45
    expected_screening_score = round(H_org_k_R_alpha + (epsilon * external_signals_score), 2)
    assert at.markdown[7].value == f"**Calculated Initial Screening Score:** {expected_screening_score}"
    assert at.info[0].value == "**Screening Recommendation:** Promising AI candidate: Investigate further. May have specific strengths."

    # Test changing inputs and associated calculations/recommendations
    at.number_input[0].set_value(80).run() # baseline_v_org_r
    at.number_input[1].set_value(90).run() # external_signals_score
    
    baseline_v_org_r_new = at.session_state["baseline_v_org_r"]
    external_signals_score_new = at.session_state["external_signals_score"]
    synergy_score_new = min(baseline_v_org_r_new, H_org_k_R_alpha)
    expected_org_ai_r_new = round((alpha * baseline_v_org_r_new) + ((1 - alpha) * H_org_k_R_alpha) + (beta * synergy_score_new), 2)
    expected_screening_score_new = round(H_org_k_R_alpha + (epsilon * external_signals_score_new), 2)

    assert at.markdown[4].value == f"**Calculated Initial PE Org-AI-R Score:** {expected_org_ai_r_new} (A high-level combined readiness score)"
    assert at.markdown[7].value == f"**Calculated Initial Screening Score:** {expected_screening_score_new}"
    assert at.info[0].value == "**Screening Recommendation:** Strong AI candidate: High potential and readiness. Prioritize for deep dive."

    # Test changing selected company
    at.selectbox[0].set_value("Beta Healthcare").run()
    assert at.session_state["selected_company"] == "Beta Healthcare"
    assert at.session_state["selected_sector"] == "Healthcare"
    
    # Verify values dependent on company are reset/updated after _initialize_session_state
    H_org_k_R_beta = systematic_opportunity_scores.get('Healthcare', 78)
    assert at.markdown[2].value == f"**Systematic AI Opportunity ($H_{{org,k}}^R$):** {H_org_k_R_beta} (Sector-specific potential)"
    assert at.session_state["baseline_v_org_r"] == 36 # Default after re-initialization
    assert at.session_state["external_signals_score"] == 45 # Default after re-initialization

    # Navigate to next step
    at.button[0].click().run()
    assert at.session_state["current_step"] == 2


def test_step2_dimension_assessment():
    """
    Tests Step 2: Deep Dive: Dimension-Level Assessment & Gap Analysis.
    Verifies slider interactions, recalculations of Org-AI-R, and chart presence.
    """
    at = AppTest.from_file("app.py")
    at = run_to_step(at, 2)

    assert at.session_state["current_step"] == 2
    assert at.subheader[1].value == "Your Assessment (1=Novice, 5=Expert)"

    # Get the sector and weights for calculations
    selected_sector = at.session_state["selected_sector"]
    all_dimension_weights_df = at.get("all_dimension_weights_df")
    sector_weights = all_dimension_weights_df[selected_sector]
    
    # Read initial current ratings from session state for calculations
    initial_current_ratings = {dim: at.session_state[f'current_rating_{dim.replace(" ", "_").lower()}'] for dim in at.get("general_dimension_weights", {}).keys()}
    current_dimension_scores = {d: round((initial_current_ratings[d] / 5) * 100, 2) for d in initial_current_ratings}
    
    # Manually calculate V_org_R to verify against the app's output
    expected_current_V_org_R = round(pd.Series(current_dimension_scores).reindex(sector_weights.index, fill_value=0).dot(sector_weights), 2)
    assert at.markdown[11].value == f"**Calculated Idiosyncratic Readiness ($V_{{org,j}}^R$) based on Detailed Assessment:** {expected_current_V_org_R}"
    
    # Manipulate a slider (e.g., 'Data Infrastructure' current rating) and check recalculation
    data_infra_current_slider = [s for s in at.slider if s.label == "Current Rating for Data Infrastructure"][0]
    initial_data_infra_current_val = data_infra_current_slider.value
    new_data_infra_current_val = 4 if initial_data_infra_current_val != 4 else 3 # Ensure a change
    data_infra_current_slider.set_value(new_data_infra_current_val).run()

    # Recalculate expected V_org_R based on the changed input
    updated_current_ratings = initial_current_ratings.copy()
    updated_current_ratings['Data Infrastructure'] = new_data_infra_current_val
    updated_current_dimension_scores = {d: round((updated_current_ratings[d] / 5) * 100, 2) for d in updated_current_ratings}
    updated_expected_current_V_org_R = round(pd.Series(updated_current_dimension_scores).reindex(sector_weights.index, fill_value=0).dot(sector_weights), 2)
    
    assert at.markdown[11].value == f"**Calculated Idiosyncratic Readiness ($V_{{org,j}}^R$) based on Detailed Assessment:** {updated_expected_current_V_org_R}"
    assert at.session_state['current_V_org_R_alpha'] == updated_expected_current_V_org_R

    # Check the dataframe output to ensure the change is reflected
    df_output_str = at.dataframe[0].container.text
    assert f"{new_data_infra_current_val}" in df_output_str # Check that the new rating value is in the dataframe string

    # Check that charts are generated
    assert len(at.pyplot) >= 2 # Radar chart and bar chart

    # Navigate to next step
    at.button[1].click().run()
    assert at.session_state["current_step"] == 3


def test_step3_use_case_planning():
    """
    Tests Step 3: Identify High-Value AI Use Cases & Estimate Impact.
    Verifies multiselect interaction, dynamic parameter inputs, and dataframe updates.
    """
    at = AppTest.from_file("app.py")
    at = run_to_step(at, 3)

    assert at.session_state["current_step"] == 3
    assert at.multiselect[0].label == "Select High-Value AI Use Cases"
    
    initial_selected_use_cases = at.session_state["selected_use_cases"]
    assert len(initial_selected_use_cases) > 0 # Should have defaults from _initialize_session_state
    
    # Verify initial parameter inputs are present for a default use case
    first_uc_name = initial_selected_use_cases[0]
    assert at.markdown[3].value == f"#### {first_uc_name}" # The first use case title
    
    investment_input = [n for n in at.number_input if f"Estimated Investment Cost for {first_uc_name}" in n.label][0]
    prob_success_slider = [s for s in at.slider if f"Probability of Success for {first_uc_name}" in s.label][0]
    exec_quality_slider = [s for s in at.slider if f"Execution Quality Factor for {first_uc_name}" in s.label][0]

    # Test changing investment cost for the first use case
    original_investment = investment_input.value
    new_investment = round(original_investment + 0.5, 2) if original_investment < 9.5 else round(original_investment - 0.5, 2)
    investment_input.set_value(new_investment).run()

    # Verify session state and the rendered dataframe reflect the change
    assert at.session_state[f'investment_{first_uc_name.replace(" ", "_").lower()}'] == new_investment
    updated_df = at.session_state.planned_initiatives_df
    assert updated_df[updated_df['Use Case'] == first_uc_name]['Investment ($M)'].iloc[0] == new_investment

    # Select an additional use case
    current_options = at.multiselect[0].options
    # Ensure there's an unselected use case to add
    new_uc_to_add = next((uc for uc in current_options if uc not in initial_selected_use_cases), None)
    if new_uc_to_add:
        at.multiselect[0].set_values(initial_selected_use_cases + [new_uc_to_add]).run()
        assert new_uc_to_add in at.session_state.selected_use_cases
        # Check that new inputs appear for the newly selected use case
        assert [n for n in at.number_input if f"Estimated Investment Cost for {new_uc_to_add}" in n.label]

    # Navigate to next step
    at.button[1].click().run()
    assert at.session_state["current_step"] == 4


def test_step4_multi_year_plan():
    """
    Tests Step 4: Build the Multi-Year AI Value Creation Plan.
    Verifies planning horizon changes, plan generation, and chart presence.
    Also tests the scenario with no planned initiatives.
    """
    at = AppTest.from_file("app.py")
    at = run_to_step(at, 4)

    assert at.session_state["current_step"] == 4
    assert at.slider[0].label == "Planning Horizon (Years)"
    
    # Check initial plan trajectory
    assert not at.session_state.ai_plan_trajectory_df.empty
    assert len(at.session_state.ai_plan_trajectory_df) == at.session_state["planning_horizon"]
    
    # Change planning horizon
    original_horizon = at.session_state["planning_horizon"]
    new_horizon = 4 if original_horizon == 3 else 3 # Toggle between 3 and 4 years
    at.slider[0].set_value(new_horizon).run()

    assert at.session_state["planning_horizon"] == new_horizon
    assert len(at.session_state.ai_plan_trajectory_df) == new_horizon

    # Check chart presence
    assert len(at.pyplot) >= 2 # Cumulative EBITDA Impact and Org-AI-R Progression

    # Test the empty plan scenario: start fresh, go to step 3, deselect all, then go to step 4
    at_empty_plan = AppTest.from_file("app.py")
    at_empty_plan.run() # Initial run for fresh session state
    at_empty_plan = run_to_step(at_empty_plan, 3, initial_run=False) # Go to step 3
    
    # Deselect all use cases
    at_empty_plan.multiselect[0].set_values([]).run()
    assert at_empty_plan.session_state["planned_initiatives_df"].empty

    # Proceed to step 4, expecting a warning and the "No Plan" button
    at_empty_plan.button[1].click().run() # Button to continue
    assert at_empty_plan.session_state["current_step"] == 4
    assert "Please go back to 'Identify High-Value AI Use Cases & Estimate Impact' to select and configure initiatives first." in at_empty_plan.warning[0].value
    assert at_empty_plan.session_state.ai_plan_trajectory_df.empty # DataFrame should be empty

    # Navigate from empty plan to next step using the specific "No Plan" button
    at_empty_plan.button[[b.label for b in at_empty_plan.button].index("Continue to Portfolio Benchmarking (No Plan)")].click().run()
    assert at_empty_plan.session_state["current_step"] == 5

    # Navigate to next step (from a non-empty plan)
    at.button[1].click().run()
    assert at.session_state["current_step"] == 5


def test_step5_benchmarking():
    """
    Tests Step 5: Calculate AI Investment Efficiency & Portfolio Benchmarking.
    Verifies AIE calculation, portfolio DataFrame updates, and benchmarking metrics.
    """
    at = AppTest.from_file("app.py")
    at = run_to_step(at, 5)

    assert at.session_state["current_step"] == 5

    df_plan = at.session_state.ai_plan_trajectory_df
    
    # Check if a plan was generated; if not, AIE should be 0 and a warning present
    if df_plan.empty:
        assert "0.00 pts*$M$/$M$" in at.markdown[3].value
        assert at.warning[0].value == "No multi-year plan generated. AI Investment Efficiency will be calculated as zero. Please go back to previous steps to define AI initiatives."
    else:
        # Expected values from plan
        # The initial_org_ai_r comes from step 2 (current_org_ai_r_alpha)
        initial_org_ai_r = at.session_state.get('current_org_ai_r_alpha')
        final_org_ai_r_for_calc = df_plan['Org-AI-R'].iloc[-1]
        total_delta_org_ai_r_plan = final_org_ai_r_for_calc - initial_org_ai_r
        total_investment_plan_M = df_plan['Cumulative Investment ($M)'].iloc[-1]
        total_ebitda_impact_plan_M = df_plan['Cumulative EBITDA Impact ($M)'].iloc[-1]
        
        expected_aie_score = 0.0
        if total_investment_plan_M > 0:
            expected_aie_score = round((total_delta_org_ai_r_plan / total_investment_plan_M) * total_ebitda_impact_plan_M, 2)

        assert at.markdown[3].value == f"**AI Investment Efficiency (AIE):** **{expected_aie_score:.2f} pts*$M$/$M$**"

        # Verify portfolio_companies_df is updated for the selected company
        selected_company_row = at.session_state.portfolio_companies_df[at.session_state.portfolio_companies_df['Company'] == at.session_state.selected_company].iloc[0]
        assert selected_company_row['Current Org-AI-R'] == final_org_ai_r_for_calc
        # Delta Org-AI-R and Investment can be 0 or small if plan is minimal, ensure robustness
        assert selected_company_row['Delta Org-AI-R'] == max(0.0, total_delta_org_ai_r_plan)
        assert selected_company_row['Investment ($M)'] == max(0.0, total_investment_plan_M)
        assert selected_company_row['Efficiency (pts/$M$)'] == expected_aie_score

        # Verify percentile and z-score are displayed (check prefix and value format)
        assert at.markdown[6].value.startswith(f"**{at.session_state.selected_company} Org-AI-R Percentile (within Portfolio):**")
        assert f"{float(at.markdown[6].value.split(': ')[1].replace('% (relative to current state after plan)', '')):.2f}%"
        assert at.markdown[7].value.startswith(f"**{at.session_state.selected_company} Org-AI-R Z-Score (within Portfolio):**")
        assert f"{float(at.markdown[7].value.split(': ')[1].replace(' (relative to current state after plan)', '')):.2f}"


    # Check chart presence
    assert len(at.pyplot) >= 2 # Current PE Org-AI-R Scores and AI Investment Efficiency charts

    # Navigate to next step
    at.button[1].click().run()
    assert at.session_state["current_step"] == 6


def test_step6_exit_readiness():
    """
    Tests Step 6: Exit-Readiness Assessment.
    Verifies slider interactions, calculations for Exit-AI-R and predicted multiple,
    and implied valuation.
    """
    at = AppTest.from_file("app.py")
    at = run_to_step(at, 6)

    assert at.session_state["current_step"] == 6

    # Get model coefficients from the app's initial state
    model_coefficients = at.get("model_coefficients", {})
    
    w1_exit = model_coefficients.get('w1_exit', 0.35)
    w2_exit = model_coefficients.get('w2_exit', 0.40)
    w3_exit = model_coefficients.get('w3_exit', 0.25)
    delta_exit = model_coefficients.get('delta_exit', 2.0)

    # Test initial values and calculations
    visible_score = at.session_state["visible_score"] # default 75
    documented_score = at.session_state["documented_score"] # default 80
    sustainable_score = at.session_state["sustainable_score"] # default 70

    expected_exit_ai_r = round((w1_exit * visible_score) + (w2_exit * documented_score) + (w3_exit * sustainable_score), 2)
    assert at.markdown[3].value == f"**Calculated Exit-AI-R Score:** {expected_exit_ai_r:.2f} (Weighted score of AI attractiveness to buyers)"

    base_exit_multiple = at.session_state["base_exit_multiple"] # Default for Manufacturing: 6.0
    expected_predicted_multiple = round(base_exit_multiple + (delta_exit * expected_exit_ai_r / 100), 2)
    assert at.markdown[7].value == f"**Predicted Exit Multiple with AI Premium:** {expected_predicted_multiple:.2f}x"
    
    # Change a slider (e.g., 'Visible AI Capabilities Score') and check recalculation
    at.slider[0].set_value(90).run() # visible_score to 90
    visible_score_new = at.session_state["visible_score"] # Should be 90 now
    
    expected_exit_ai_r_new = round((w1_exit * visible_score_new) + (w2_exit * documented_score) + (w3_exit * sustainable_score), 2)
    expected_predicted_multiple_new = round(base_exit_multiple + (delta_exit * expected_exit_ai_r_new / 100), 2)

    assert at.markdown[3].value == f"**Calculated Exit-AI-R Score:** {expected_exit_ai_r_new:.2f} (Weighted score of AI attractiveness to buyers)"
    assert at.markdown[7].value == f"**Predicted Exit Multiple with AI Premium:** {expected_predicted_multiple_new:.2f}x"

    # Check implied valuation (after potential updates from Step 5)
    current_company_row = at.session_state.portfolio_companies_df[at.session_state.portfolio_companies_df['Company'] == at.session_state.selected_company].iloc[0]
    projected_final_ebitda = current_company_row['EBITDA ($M)'] # This is updated in Step 5
    expected_implied_valuation = round(projected_final_ebitda * expected_predicted_multiple_new, 2)
    assert at.markdown[9].value == f"**Implied Valuation (EBITDA x Multiple):** ${expected_implied_valuation:.2f}M"

    # Verify the success message at the end of the app workflow
    assert "Congratulations, Portfolio Manager!" in at.success[0].value

    # Test back button (will go to step 5)
    at.button[0].click().run()
    assert at.session_state["current_step"] == 5

