import streamlit as st
from advanced_features import render_sensitivity_analysis, render_scenario_comparison
from import_export import render_import_export

# Setup page config first - must be the first Streamlit command
st.set_page_config(page_title="Utility Work Planner", layout="wide")

# Import main after set_page_config to avoid the error
from main import main as main_page

# Define the pages
PAGES = {
    "Work Optimization": main_page,
    "Sensitivity Analysis": render_sensitivity_analysis,
    "Scenario Comparison": render_scenario_comparison,
    "Import/Export Data": render_import_export
}

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Display the selected page
PAGES[selection]()

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Utility Work Management Optimization Tool**
    
    This application helps utility planning teams optimize their work allocation 
    to meet budget constraints while maximizing priority-based objectives.
    """
)