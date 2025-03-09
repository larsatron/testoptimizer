import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from optimization import analyze_sensitivity

def render_sensitivity_analysis():
    """Render a sensitivity analysis page that shows how changing budget affects optimization."""
    st.title("Sensitivity Analysis")
    
    if 'work_types' not in st.session_state or len(st.session_state.work_types) == 0:
        st.warning("Please add work types on the main page before running sensitivity analysis.")
        return
    
    st.subheader("Budget Sensitivity Analysis")
    
    work_df = pd.DataFrame(st.session_state.work_types)
    
    budget_base = st.number_input(
        "Reference Budget ($)", 
        min_value=10000, 
        value=1000000, 
        step=10000
    )
    
    steps = st.slider(
        "Number of Analysis Points", 
        min_value=5, 
        max_value=20, 
        value=10
    )
    
    if st.button("Run Sensitivity Analysis"):
        with st.spinner("Running sensitivity analysis..."):
            sensitivity_results = analyze_sensitivity(work_df, budget_base, steps)
            
            # Plot results
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sensitivity_results['budget'],
                y=sensitivity_results['objective_value'],
                mode='lines+markers',
                name='Priority Value',
                line=dict(color='blue')
            ))
            
            # Add a secondary y-axis for budget utilization
            fig.add_trace(go.Scatter(
                x=sensitivity_results['budget'],
                y=sensitivity_results['budget_utilization'] * 100,  # Convert to percentage
                mode='lines+markers',
                name='Budget Utilization (%)',
                line=dict(color='green'),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='Budget Sensitivity Analysis',
                xaxis_title='Budget ($)',
                yaxis_title='Priority Value',
                yaxis2=dict(
                    title='Budget Utilization (%)',
                    titlefont=dict(color='green'),
                    tickfont=dict(color='green'),
                    anchor='x',
                    overlaying='y',
                    side='right'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show data table
            st.subheader("Detailed Results")
            display_df = sensitivity_results.copy()
            display_df['budget'] = display_df['budget'].map('${:,.2f}'.format)
            display_df['budget_utilization'] = (display_df['budget_utilization'] * 100).map('{:.1f}%'.format)
            display_df.columns = ['Budget', 'Priority Value', 'Budget Utilization']
            st.dataframe(display_df)

def render_scenario_comparison():
    """Render a scenario comparison tool that allows comparing different work mixes."""
    st.title("Scenario Comparison")
    
    if 'scenarios' not in st.session_state:
        st.session_state.scenarios = {}
    
    # Current scenario section
    st.subheader("Current Scenario")
    
    if 'results' in st.session_state and st.session_state.results and 'work_types' in st.session_state:
        results_df = pd.DataFrame({
            'Work Type': [w['name'] for w in st.session_state.work_types],
            'Units Allocated': st.session_state.results['allocation'],
            'Cost': [u * w['cost'] for u, w in zip(st.session_state.results['allocation'], st.session_state.work_types)]
        })
        
        st.dataframe(results_df)
        
        scenario_name = st.text_input("Scenario Name", "Scenario " + str(len(st.session_state.scenarios) + 1))
        
        if st.button("Save Current Scenario"):
            st.session_state.scenarios[scenario_name] = {
                'data': results_df.copy(),
                'total_cost': results_df['Cost'].sum(),
                'objective_value': st.session_state.results['objective_value']
            }
            st.success(f"Saved scenario: {scenario_name}")
    else:
        st.info("Run an optimization on the main page to create a scenario for comparison.")
    
    # Scenarios comparison section
    if st.session_state.scenarios:
        st.subheader("Compare Scenarios")
        
        scenarios_to_compare = st.multiselect(
            "Select Scenarios to Compare",
            options=list(st.session_state.scenarios.keys()),
            default=list(st.session_state.scenarios.keys())
        )
        
        if scenarios_to_compare:
            # Create comparison metrics
            metrics_df = pd.DataFrame({
                'Scenario': scenarios_to_compare,
                'Total Cost': [st.session_state.scenarios[s]['total_cost'] for s in scenarios_to_compare],
                'Priority Value': [st.session_state.scenarios[s]['objective_value'] for s in scenarios_to_compare]
            })
            
            st.dataframe(metrics_df)
            
            # Create comparison chart
            fig = go.Figure()
            
            for scenario in scenarios_to_compare:
                scenario_data = st.session_state.scenarios[scenario]['data']
                
                fig.add_trace(go.Bar(
                    name=scenario,
                    x=scenario_data['Work Type'],
                    y=scenario_data['Units Allocated'],
                    text=scenario_data['Cost'].map('${:,.2f}'.format),
                    textposition='auto'
                ))
            
            fig.update_layout(
                title='Work Allocation Comparison by Scenario',
                xaxis_title='Work Type',
                yaxis_title='Units Allocated',
                barmode='group',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Option to delete scenarios
            to_delete = st.multiselect("Select Scenarios to Delete", options=list(st.session_state.scenarios.keys()))
            
            if to_delete and st.button("Delete Selected Scenarios"):
                for scenario in to_delete:
                    if scenario in st.session_state.scenarios:
                        del st.session_state.scenarios[scenario]
                st.success("Deleted selected scenarios")
                st.experimental_rerun()
    else:
        st.info("Save scenarios to enable comparison.")