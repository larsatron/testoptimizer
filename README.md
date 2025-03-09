# Utility Work Management Optimization

A Streamlit web application that helps utility planning teams optimize their work allocation based on budget constraints, priorities, and operational requirements.

## Features

- **Work Type Management**: Add different types of work with associated costs, priorities, and constraints.
- **Budget-Constrained Optimization**: Maximize priority-based objectives while staying within budget limits.
- **Sensitivity Analysis**: Analyze how changing the budget affects the optimal work mix.
- **Scenario Comparison**: Save and compare different allocation scenarios.
- **Interactive Visualizations**: Visualize work allocation and budget distribution with interactive charts.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/utility-work-planner.git
cd utility-work-planner
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd app
python3 -m streamlit run app.py
```
This will launch the Streamlit app directly. Make sure you've installed the required dependencies first with `pip install -r requirements.txt`.

## Usage

1. **Add Work Types**:
   - Enter work type name, cost per unit, priority, and min/max constraints
   - Click "Add Work Type" to add it to the optimization list

2. **Run Optimization**:
   - Set the total budget
   - Click "Optimize Work Allocation" to run the optimization algorithm
   - View results in tables and charts

3. **Analyze Sensitivity**:
   - Navigate to the Sensitivity Analysis page
   - Set the reference budget and number of analysis points
   - Click "Run Sensitivity Analysis" to see how the budget affects outcomes

4. **Compare Scenarios**:
   - Save different optimization results as named scenarios
   - Compare scenarios side-by-side to evaluate different approaches

## Technical Details

- **Optimization Engine**: Uses PuLP, a linear programming library, to solve the optimization problem
- **Frontend**: Streamlit for the interactive web interface
- **Data Visualization**: Plotly for interactive charts and graphs
- **Data Processing**: Pandas and NumPy for data manipulation

## License

This project is licensed under the MIT License - see the LICENSE file for details.