import numpy as np
import pandas as pd
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, value

def optimize_work_allocation(work_df, total_budget):
    """
    Optimize work allocation based on priorities, costs, and constraints.
    
    Args:
        work_df (pd.DataFrame): DataFrame containing work types with columns:
            - name: Name of the work type
            - cost: Cost per unit
            - priority: Priority score (1-10)
            - min_units: Minimum required units
            - max_units: Maximum possible units
        total_budget (float): Total available budget
    
    Returns:
        dict: Optimization results containing:
            - status: Optimization status
            - allocation: List of allocated units for each work type
            - objective_value: Total priority value achieved
    """
    # Create the optimization problem
    prob = LpProblem("Utility_Work_Optimization", LpMaximize)
    
    # Extract data from DataFrame
    work_types = work_df['name'].tolist()
    costs = work_df['cost'].tolist()
    priorities = work_df['priority'].tolist()
    min_units = work_df['min_units'].tolist()
    max_units = work_df['max_units'].tolist()
    
    # Create decision variables (number of units for each work type)
    work_vars = {
        work_type: LpVariable(f"Units_{i}", 
                              lowBound=min_unit, 
                              upBound=max_unit, 
                              cat='Integer')
        for i, (work_type, min_unit, max_unit) in enumerate(zip(work_types, min_units, max_units))
    }
    
    # Objective function: Maximize priority-weighted work
    prob += sum(priority * work_vars[work_type] 
                for work_type, priority in zip(work_types, priorities))
    
    # Constraint: Budget limitation
    prob += sum(cost * work_vars[work_type] 
                for work_type, cost in zip(work_types, costs)) <= total_budget, "Budget_Constraint"
    
    # Solve the problem
    prob.solve()
    
    # Get results
    status = LpStatus[prob.status]
    allocation = [int(value(work_vars[work_type])) for work_type in work_types]
    objective_value = value(prob.objective)
    
    return {
        'status': status,
        'allocation': allocation,
        'objective_value': objective_value
    }

def analyze_sensitivity(work_df, total_budget, steps=10):
    """
    Perform sensitivity analysis by varying the budget and observing changes.
    
    Args:
        work_df (pd.DataFrame): DataFrame containing work types
        total_budget (float): Current total budget
        steps (int): Number of budget steps to analyze
    
    Returns:
        pd.DataFrame: Results of sensitivity analysis
    """
    budget_range = np.linspace(total_budget * 0.5, total_budget * 1.5, steps)
    results = []
    
    for budget in budget_range:
        result = optimize_work_allocation(work_df, budget)
        
        # Calculate total cost
        total_cost = sum(alloc * cost for alloc, cost in zip(result['allocation'], work_df['cost']))
        
        results.append({
            'budget': budget,
            'objective_value': result['objective_value'],
            'budget_utilization': total_cost / budget if budget > 0 else 0
        })
    
    return pd.DataFrame(results)