This is a comprehensive `README.md` file for your Streamlit application lab project.

---

# QuLab: AI Value Creation & Investment Efficiency Planner

![QuantUniversity Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## Project Description

Welcome to the **"AI Value Creation & Investment Efficiency Planner"**, a Streamlit application designed for Private Equity (PE) professionals. As a Portfolio Manager, you are tasked with evaluating and optimizing portfolio companies for maximum value creation, especially in the context of Artificial Intelligence (AI) adoption. This tool provides a structured, data-driven workflow to assess a portfolio company's AI readiness, identify high-potential initiatives, quantify their financial impact, and develop a strategic multi-year plan.

The application simulates a realistic scenario where you, the Portfolio Manager, need to:
1.  **Rapidly screen** potential AI opportunities within a portfolio company.
2.  Conduct a **deep-dive assessment** to understand current AI capabilities and identify key gaps.
3.  **Strategically select** AI initiatives that address these gaps and drive value.
4.  **Quantify** the projected EBITDA impact and `Org-AI-R` improvement over a multi-year horizon.
5.  **Benchmark** the company's AI performance and investment efficiency against the rest of your portfolio.
6.  **Assess** how these AI investments contribute to a compelling exit narrative and enhanced valuation multiples.

Through interactive components, the app demonstrates how to leverage AI models and data analytics to transform qualitative assessments into measurable, actionable insights, directly supporting the mandate to maximize investor returns.

## Features

The application guides you through a 6-step process, each designed to provide crucial insights for AI-driven value creation:

### 1. Company Selection and Initial Org-AI-R Assessment
*   **Select a Portfolio Company**: Choose from a predefined list of portfolio companies.
*   **Initial AI Readiness Scores**: Get a high-level view of the company's `Org-AI-R` (Organizational AI Readiness) based on simulated baseline idiosyncratic readiness and systematic sector opportunity.
*   **AI Screening Score**: Calculate a preliminary screening score by incorporating external AI signals, offering an initial recommendation on AI investment priority.

### 2. Deep Dive: Dimension-Level Assessment & Gap Analysis
*   **Interactive Dimension Ratings**: Assess the company's current and target maturity across 7 key AI dimensions (e.g., Data Infrastructure, AI Governance, Talent) using interactive sliders.
*   **Calculated `V_org_R`**: Derive a detailed `V_org_R` (Idiosyncratic Readiness) score based on your dimension assessments.
*   **Visual Gap Analysis**: Utilize radar charts and bar charts to visualize current vs. target scores and identify critical AI capability gaps.

### 3. Identify High-Value AI Use Cases & Estimate Impact
*   **Sector-Specific Use Cases**: Browse high-value AI use cases tailored to the selected company's industry.
*   **Customizable Project Parameters**: Adjust estimated investment costs, probability of success, and execution quality for chosen initiatives.
*   **Quantified Impact**: Get projected `EBITDA Impact ($M)` and `Delta Org-AI-R` for each selected use case.

### 4. Build the Multi-Year AI Value Creation Plan
*   **Dynamic Planning Horizon**: Define a multi-year planning horizon (1-5 years).
*   **Project Trajectory**: Generate a detailed plan showing the annual progression of `Org-AI-R`, cumulative `EBITDA Impact ($M)`, and cumulative `Investment ($M)`.
*   **Trend Visualizations**: Line plots illustrate the projected financial value accretion and `Org-AI-R` improvement over time.

### 5. Calculate AI Investment Efficiency & Portfolio Benchmarking
*   **AI Investment Efficiency (AIE)**: Calculate a key metric that quantifies the combined return on AI investment in terms of `Org-AI-R` improvement and `EBITDA Impact`.
*   **Portfolio Benchmarking**: Compare the selected company's `Org-AI-R` score and AIE against other companies in your portfolio, including percentile and Z-score analysis.
*   **Comparative Visualizations**: Bar charts provide a clear view of how the company stands relative to its peers.

### 6. Exit-Readiness Assessment
*   **Interactive Exit-AI-R Factors**: Assess `Visible`, `Documented`, and `Sustainable` AI capabilities using sliders.
*   **Calculated Exit-AI-R Score**: Obtain a weighted score reflecting the company's AI attractiveness to potential buyers.
*   **Predicted Exit Multiple**: Project an enhanced exit valuation multiple by incorporating an AI premium based on the `Exit-AI-R` score.
*   **Implied Valuation**: Calculate the overall implied valuation for the company at exit based on projected `EBITDA` and the predicted multiple.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation

1.  **Clone the repository (or download `app.py`):**
    ```bash
    git clone https://github.com/your-username/quolab-ai-planner.git
    cd quolab-ai-planner
    ```
    (Replace `your-username/quolab-ai-planner` with the actual repository link if available, otherwise just place the `app.py` file in a directory).

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    Create a `requirements.txt` file in the project directory with the following content:
    ```
    streamlit
    pandas
    numpy
    matplotlib
    seaborn
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Save the provided Streamlit application code:**
    Save the entire Streamlit application code (as provided in the prompt) into a file named `app.py` within your project directory.

2.  **Run the Streamlit application:**
    Open your terminal or command prompt, navigate to the directory where `app.py` is saved, and execute:
    ```bash
    streamlit run app.py
    ```
    This will open the application in your default web browser (usually at `http://localhost:8501`).

3.  **Navigate the application:**
    *   Use the navigation buttons ("Continue to...", "Back to...") at the bottom of each step to progress or revert.
    *   The sidebar displays your current progress and offers a "Restart Session" button to reset all inputs and start fresh.
    *   Interact with sliders, select boxes, and number inputs to modify parameters and observe real-time recalculations and visualizations.

## Project Structure

This lab project is contained within a single Python file:

```
.
├── app.py          # The main Streamlit application code
└── requirements.txt # List of Python dependencies
```

*   `app.py`: Contains all the application logic, UI components, model coefficients, data definitions (e.g., use cases, weights), and core calculation functions.

## Technology Stack

*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Language**: Python 3.x
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
*   **Numerical Operations**: [NumPy](https://numpy.org/)
*   **Data Visualization**:
    *   [Matplotlib](https://matplotlib.org/)
    *   [Seaborn](https://seaborn.pydata.org/)

## Contributing

This project is primarily a lab exercise to demonstrate the capabilities of Streamlit and AI-driven financial analysis. While direct contributions are not formally managed, feel free to:
*   **Fork** the repository.
*   **Experiment** with the code.
*   **Submit issues** if you encounter bugs or have suggestions for improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (Note: You may need to create a `LICENSE` file if you wish to formally include one).

## Contact

This project is developed as part of **QuantUniversity**'s educational initiatives.

*   **Website**: [QuantUniversity](https://www.quantuniversity.com/)
*   **Support/Inquiries**: info@quantuniversity.com

---