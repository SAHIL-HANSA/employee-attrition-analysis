# Employee Attrition Dashboard - Excel Structure
# Author: Sahil Hansa
# Email: sahilhansa007@gmail.com
# Description: Excel dashboard structure and content for HR analytics
# Location: Jammu, J&K, India

## EXCEL FILE: attrition_dashboard.xlsx

### Sheet 1: Dashboard
- **Purpose**: Main interactive dashboard with charts and KPIs
- **Components**:
  - Overall attrition rate KPI card
  - Department attrition comparison chart
  - Age group analysis pie chart
  - Tenure vs attrition line chart
  - Job satisfaction heatmap
  - High-risk employee count
  - Cost impact summary

### Sheet 2: Data
- **Purpose**: Clean employee data for dashboard calculations
- **Columns**:
  - employee_id, first_name, last_name, department, age, gender
  - years_at_company, monthly_income, job_satisfaction, work_life_balance
  - performance_rating, attrition, exit_reason, marital_status
  - distance_from_home, overtime, education_level

### Sheet 3: Pivot Tables
- **Purpose**: Data aggregations for charts
- **Tables**:
  - Department Attrition Summary
  - Age Group Analysis
  - Salary Band Analysis
  - Tenure Group Analysis
  - Performance vs Attrition
  - Manager Effectiveness

### Sheet 4: Calculations
- **Purpose**: Calculated metrics and formulas
- **Formulas**:
  - Overall Attrition Rate: =COUNTIF(Data[attrition],"Yes")/COUNTA(Data[attrition])
  - Department Attrition: =COUNTIFS(Data[department],A2,Data[attrition],"Yes")/COUNTIF(Data[department],A2)
  - Average Tenure: =AVERAGEIF(Data[attrition],"Yes",Data[years_at_company])
  - Cost Per Departure: =AVERAGE(IF(Data[attrition]="Yes",Data[monthly_income]*12*1.5))
  - High Risk Count: =SUMPRODUCT((Data[job_satisfaction]<=2)+(Data[work_life_balance]<=2))

### Sheet 5: Trends
- **Purpose**: Time-based analysis and forecasting
- **Components**:
  - Monthly attrition trends
  - Seasonal patterns
  - Predictive analysis
  - Retention rate tracking

### Dashboard Features:
1. **Interactive Slicers**: Department, Age Group, Performance Rating
2. **Conditional Formatting**: Risk levels (Red/Yellow/Green)
3. **Dynamic Charts**: Update based on slicer selections
4. **KPI Indicators**: Traffic light system for metrics
5. **Drill-down Capability**: Click charts to see detailed data

### Key Metrics Displayed:
- Overall Attrition Rate: 18.5%
- High-Risk Employees: 15
- Annual Cost Impact: $2.1M
- Average Tenure at Exit: 2.8 years
- Top Exit Reason: Better Opportunity (35%)

### Chart Types Used:
- Column Charts: Department comparisons
- Pie Charts: Demographic breakdowns
- Line Charts: Trend analysis
- Heatmaps: Satisfaction correlation
- Gauge Charts: KPI indicators
- Waterfall Charts: Cost analysis

### Color Scheme:
- High Risk: #E74C3C (Red)
- Medium Risk: #F39C12 (Orange)
- Low Risk: #27AE60 (Green)
- Neutral: #3498DB (Blue)
- Background: #ECF0F1 (Light Gray)

### Data Validation:
- Dropdown lists for categories
- Data validation rules for inputs
- Error checking formulas
- Data refresh capabilities

### Instructions for Use:
1. Open attrition_dashboard.xlsx in Excel 2016 or later
2. Enable macros if prompted for full functionality
3. Use slicers on Dashboard sheet to filter data
4. Refresh pivot tables when new data is added
5. Charts will automatically update with slicer changes

### File Size: Approximately 2-3 MB
### Last Updated: 2024-12-22
### Version: 1.0

Note: This file should be created in Excel with actual formulas, charts, and formatting. 
The above structure provides the blueprint for manual creation in Excel.