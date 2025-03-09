import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from optimization import optimize_work_allocation

def main():
    st.title("Utility Work Management Optimization")
    
    with st.sidebar:
        st.header("Configuration")
        total_budget = st.number_input("Total Budget ($)", min_value=0, value=1000000, step=10000)
        
        st.subheader("Add Work Types")
        with st.form("work_type_form"):
            work_name = st.text_input("Work Type Name")
            work_cost = st.number_input("Cost per Unit ($)", min_value=0, value=1000)
            work_priority = st.slider("Priority (1-10)", min_value=1, max_value=10, value=5)
            work_min = st.number_input("Minimum Units Required", min_value=0, value=0)
            work_max = st.number_input("Maximum Units Possible", min_value=0, value=100)
            submitted = st.form_submit_button("Add Work Type")
        
        if submitted and work_name:
            if 'work_types' not in st.session_state:
                st.session_state.work_types = []
            
            st.session_state.work_types.append({
                'name': work_name,
                'cost': work_cost,
                'priority': work_priority,
                'min_units': work_min,
                'max_units': work_max
            })
            st.success(f"Added {work_name}")
    
    # Main content area
    if 'work_types' in st.session_state and len(st.session_state.work_types) > 0:
        work_df = pd.DataFrame(st.session_state.work_types)
        
        st.subheader("Work Types")
        st.dataframe(work_df)
        
        if st.button("Optimize Work Allocation"):
            with st.spinner("Optimizing work allocation..."):
                try:
                    result = optimize_work_allocation(
                        work_df, 
                        total_budget
                    )
                    
                    if 'results' not in st.session_state:
                        st.session_state.results = {}
                    
                    st.session_state.results = result
                    
                except Exception as e:
                    st.error(f"Optimization failed: {str(e)}")
        
        if 'results' in st.session_state and st.session_state.results:
            st.subheader("Optimization Results")
            
            results_df = pd.DataFrame({
                'Work Type': [w['name'] for w in st.session_state.work_types],
                'Units Allocated': st.session_state.results['allocation'],
                'Cost': [u * w['cost'] for u, w in zip(st.session_state.results['allocation'], st.session_state.work_types)]
            })
            
            st.dataframe(results_df)
            
            # Budget utilization
            total_cost = results_df['Cost'].sum()
            st.metric("Total Budget", f"${total_budget:,.2f}")
            st.metric("Total Cost", f"${total_cost:,.2f}")
            st.metric("Remaining Budget", f"${total_budget - total_cost:,.2f}")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Units by Work Type")
                fig1 = px.bar(
                    results_df, 
                    x='Work Type', 
                    y='Units Allocated',
                    color='Work Type',
                    title="Allocation of Work Units"
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.subheader("Budget Allocation")
                fig2 = px.pie(
                    results_df,
                    names='Work Type',
                    values='Cost',
                    title="Cost Distribution"
                )
                st.plotly_chart(fig2, use_container_width=True)
                
        # Option to clear data
        if st.button("Clear All Data"):
            st.session_state.clear()
            st.experimental_rerun()
    else:
        st.info("Add work types using the sidebar to begin optimization.")

if __name__ == "__main__":
    main()