import streamlit as st
import pandas as pd
import json
import os
import base64

def export_data():
    """Export the current work types and results to a JSON file"""
    if 'work_types' not in st.session_state or len(st.session_state.work_types) == 0:
        st.warning("No data to export. Please add work types first.")
        return
    
    export_data = {
        "work_types": st.session_state.work_types
    }
    
    if 'results' in st.session_state and st.session_state.results:
        export_data["results"] = st.session_state.results
    
    if 'scenarios' in st.session_state and st.session_state.scenarios:
        # Convert DataFrame objects to lists to make them JSON serializable
        scenarios_json = {}
        for name, scenario in st.session_state.scenarios.items():
            scenarios_json[name] = {
                "total_cost": scenario["total_cost"],
                "objective_value": scenario["objective_value"],
                "data": scenario["data"].to_dict('records')
            }
        export_data["scenarios"] = scenarios_json
    
    # Convert to JSON
    json_str = json.dumps(export_data, indent=2)
    
    # Create a download link
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="utility_work_plan.json">Download JSON File</a>'
    
    st.markdown(href, unsafe_allow_html=True)
    
    return json_str

def import_data():
    """Import work types and results from a JSON file"""
    uploaded_file = st.file_uploader("Choose a JSON file", type="json")
    
    if uploaded_file is not None:
        try:
            # Load the JSON data
            data = json.load(uploaded_file)
            
            # Import work types
            if "work_types" in data:
                st.session_state.work_types = data["work_types"]
                
            # Import results if present
            if "results" in data:
                st.session_state.results = data["results"]
                
            # Import scenarios if present
            if "scenarios" in data:
                if 'scenarios' not in st.session_state:
                    st.session_state.scenarios = {}
                    
                for name, scenario in data["scenarios"].items():
                    # Convert data back to DataFrame
                    scenario_data = pd.DataFrame(scenario["data"])
                    
                    st.session_state.scenarios[name] = {
                        "total_cost": scenario["total_cost"],
                        "objective_value": scenario["objective_value"],
                        "data": scenario_data
                    }
                    
            st.success("Data imported successfully!")
            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"Error importing data: {str(e)}")

def load_example_data():
    """Load example data from the data directory"""
    try:
        # Get the directory of the current file
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        example_path = os.path.join(current_dir, "data", "example_data.json")
        
        # Load example data
        with open(example_path, "r") as f:
            data = json.load(f)
        
        # Import work types
        if "work_types" in data:
            st.session_state.work_types = data["work_types"]
            
        # Import budget if present
        if "budget" in data:
            st.session_state.budget = data["budget"]
            
        st.success("Example data loaded successfully!")
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"Error loading example data: {str(e)}")

def render_import_export():
    """Render the import/export page"""
    st.title("Import/Export Data")
    
    tab1, tab2, tab3 = st.tabs(["Export Data", "Import Data", "Load Example"])
    
    with tab1:
        st.subheader("Export Current Data")
        st.write("Export your current work types, results, and scenarios to a JSON file.")
        export_data()
    
    with tab2:
        st.subheader("Import Data")
        st.write("Import work types, results, and scenarios from a JSON file.")
        import_data()
    
    with tab3:
        st.subheader("Load Example Data")
        st.write("Load example data to see how the application works.")
        
        if st.button("Load Example Data"):
            load_example_data()