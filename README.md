# QuLab: AI Value Creation & Investment Efficiency Planner

![QuantUniversity Logo](https://www.quantuniversity.com/assets/img/logo5.jpg)

## 🚀 Project Title and Description

This Streamlit application, **"AI Value Creation & Investment Efficiency Planner,"** is an interactive lab project designed for aspiring and current Private Equity Portfolio Managers (or anyone interested in strategic AI adoption). It provides a structured, step-by-step framework to evaluate, plan, and quantify the impact of Artificial Intelligence initiatives within a portfolio company.

The application simulates a real-world scenario where you, as a Portfolio Manager, must strategically leverage AI to drive growth, improve operational efficiency, and ultimately enhance the exit valuation of your portfolio assets. Through a series of interactive pages, you will make strategic decisions, input data, and observe the projected financial and organizational outcomes, benchmarking your company's performance against industry and portfolio standards.

## ✨ Features

The application offers a guided workflow with the following key functionalities:

*   **Company & Scenario Setup**: Define initial company parameters and the investment scenario.
*   **AI Opportunity Screening**: Identify and prioritize potential AI use cases that align with business objectives.
*   **Deep-Dive AI Capability Assessment**: Evaluate the portfolio company's current AI readiness, infrastructure, talent, and data capabilities.
*   **Strategic AI Initiative Selection**: Select specific AI projects that address identified gaps and promise the highest return on investment.
*   **Financial & Organizational Impact Quantification**: Project the multi-year financial impact (EBITDA uplift) and monitor improvements in organizational AI readiness (Org-AI-R) based on selected initiatives.
*   **Benchmarking & Performance Analysis**: Compare the company's AI performance and investment efficiency against other entities in your portfolio or industry benchmarks.
*   **Exit Narrative & Valuation Assessment**: Analyze how AI investments contribute to a stronger exit story and potentially higher valuation multiples.
*   **Dynamic Multi-Page Navigation**: Seamlessly navigate between different stages of the planning process using a sidebar selector or "Continue" buttons.
*   **Session Management**: Persistent state across page interactions with a clear "Restart Session" functionality to reset all inputs and start afresh.
*   **Interactive UI**: Intuitive Streamlit widgets for data input, selections, and dynamic visualization of results.

## 🏁 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need the following installed on your system:

*   **Python 3.8+**
*   **pip** (Python package installer)
*   **git** (for cloning the repository)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name # Replace with your actual repository name
    ```
    *(Please replace `your-username/your-repo-name.git` with the actual path to your repository.)*

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    *(**Note:** Ensure you have a `requirements.txt` file in your project root containing `streamlit`, `pandas`, `numpy`, and any other dependencies used in your pages.)*
    Example `requirements.txt`:
    ```
    streamlit>=1.20.0
    pandas>=1.4.0
    numpy>=1.22.0
    # Add any other libraries your pages might use
    ```

## 🚀 Usage

Once the dependencies are installed, you can run the Streamlit application.

1.  **Ensure your virtual environment is activated.**
2.  **Run the application from the project's root directory:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the application:**
    Your default web browser should automatically open a new tab pointing to the Streamlit application (usually `http://localhost:8501`). If it doesn't, copy and paste the URL provided in your terminal into your browser.

4.  **Interaction:**
    *   Use the **"Navigation" dropdown** in the sidebar to move between different planning steps.
    *   Input data into various fields, select options, and observe the dynamic updates in the main content area.
    *   Click the **"Restart Session" button** in the sidebar to clear all previous inputs and calculations, starting the simulation from scratch.
    *   Follow the **"Continue" button** often found at the bottom of each page to advance to the next recommended step.

## 📁 Project Structure

The project is organized to promote modularity and ease of development for a multi-page Streamlit application.

```
.
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # List of Python dependencies
├── application_pages/          # Directory containing individual Streamlit page modules
│   ├── __init__.py             # Makes 'application_pages' a Python package
│   ├── shared_functions.py     # Contains global utility functions (session state, navigation)
│   ├── page_1_company_selection.py # Example: First page for company setup
│   ├── page_2_ai_assessment.py   # Example: Second page for AI capability assessment
│   ├── page_X_page_name.py       # ...and so on for subsequent pages
│   └── ...
├── data/                       # (Optional) Directory for storing datasets or lookup tables
│   ├── companies.csv           # Example: Sample company data
│   └── benchmarks.json         # Example: Industry benchmarks
└── assets/                     # (Optional) Directory for static assets like images, CSS
    └── logo.jpg                # Example: Project logo
```

*   **`app.py`**: This is the core file that initializes the Streamlit app, sets up the page configuration, manages session state, renders the sidebar, and dynamically loads the content of the currently selected page from the `application_pages` directory.
*   **`application_pages/`**: This directory is central to the application's modularity. Each Python file here represents a distinct "page" or step in the planning workflow.
    *   **`__init__.py`**: An empty file that tells Python `application_pages` is a package, allowing relative imports within it.
    *   **`shared_functions.py`**: Holds functions like `initialize_session_state`, `go_to_page`, and `pages_config` (which maps page names to module files), ensuring consistent behavior across pages.
    *   **`page_X_*.py`**: Each file here defines the `main()` function for a specific page. This function encapsulates all Streamlit UI elements and logic for that particular step of the planner.

## 🛠️ Technology Stack

This application is built using the following technologies and libraries:

*   **Python**: The core programming language.
*   **Streamlit**: The open-source app framework for machine learning and data science teams.
*   **Pandas**: For data manipulation and analysis.
*   **NumPy**: For numerical operations.
*   **Git**: For version control.

## 🤝 Contributing

This is primarily a lab project, but contributions are welcome for improvements, bug fixes, or new feature ideas.

1.  **Fork** the repository.
2.  **Create a new branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit your changes** (`git commit -m 'Add some AmazingFeature'`).
4.  **Push to the branch** (`git push origin feature/AmazingFeature`).
5.  **Open a Pull Request**.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(You should create a `LICENSE` file in your project root with the MIT License text.)*

## ✉️ Contact

For questions, feedback, or collaborations related to this QuLab project, please feel free to:

*   Raise an issue on this GitHub repository.
*   Contact the QuantUniversity Lab team directly via their official channels (e.g., website contact form, specific lab email).

---
**QuantUniversity Lab**
*Innovating at the Intersection of AI, Finance, and Education*
