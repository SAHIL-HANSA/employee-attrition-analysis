-- Department-wise Attrition Analysis SQL Queries
-- Author: Sahil Hansa
-- Email: sahilhansa007@gmail.com
-- Description: Comprehensive SQL analysis focusing on departmental attrition patterns and insights
-- Location: Jammu, J&K, India

-- =============================================
-- Department Overview and Benchmarking
-- =============================================

-- Comprehensive department analysis with benchmarking
SELECT 
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    
    -- Salary and compensation metrics
    AVG(monthly_income) as avg_monthly_salary,
    MEDIAN(monthly_income) as median_monthly_salary,
    MIN(monthly_income) as min_salary,
    MAX(monthly_income) as max_salary,
    
    -- Employee satisfaction metrics
    AVG(job_satisfaction) as avg_job_satisfaction,
    AVG(work_life_balance) as avg_work_life_balance,
    
    -- Performance indicators
    AVG(performance_rating) as avg_performance_rating,
    COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) as high_performers,
    ROUND(
        (COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as high_performer_percentage,
    
    -- Work environment factors
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_employees,
    ROUND(
        (COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as overtime_percentage,
    
    AVG(distance_from_home) as avg_commute_distance,
    AVG(years_at_company) as avg_tenure,
    
    -- Risk assessment
    CASE 
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 THEN 'Critical Risk'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 18 THEN 'High Risk'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 12 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_category,
    
    -- Industry benchmark comparison (assuming 15% industry average)
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) - 15, 2
    ) as variance_from_industry_benchmark
    
FROM employee_data
GROUP BY department
ORDER BY attrition_rate_percent DESC;

-- =============================================
-- Department Role Analysis
-- =============================================

-- Job role analysis within each department
SELECT 
    department,
    job_role,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    AVG(job_satisfaction) as avg_satisfaction,
    AVG(years_at_company) as avg_tenure,
    AVG(performance_rating) as avg_performance,
    
    -- Career level identification
    CASE 
        WHEN job_role LIKE '%Manager%' OR job_role LIKE '%Lead%' OR job_role LIKE '%Director%' THEN 'Leadership'
        WHEN job_role LIKE '%Senior%' THEN 'Senior Level'
        WHEN job_role LIKE '%Junior%' OR job_role LIKE '%Associate%' OR job_role LIKE '%Specialist%' THEN 'Mid Level'
        ELSE 'Entry Level'
    END as career_level
    
FROM employee_data
GROUP BY department, job_role
HAVING COUNT(*) >= 2  -- Only roles with multiple employees for statistical relevance
ORDER BY department, attrition_rate_percent DESC;

-- =============================================
-- Department Satisfaction Deep Dive
-- =============================================

-- Satisfaction drivers by department
SELECT 
    department,
    
    -- Satisfaction breakdown
    AVG(job_satisfaction) as avg_job_satisfaction,
    COUNT(CASE WHEN job_satisfaction <= 2 THEN 1 END) as low_satisfaction_count,
    COUNT(CASE WHEN job_satisfaction >= 4 THEN 1 END) as high_satisfaction_count,
    
    -- Work-life balance analysis
    AVG(work_life_balance) as avg_work_life_balance,
    COUNT(CASE WHEN work_life_balance <= 2 THEN 1 END) as poor_wlb_count,
    COUNT(CASE WHEN work_life_balance >= 4 THEN 1 END) as good_wlb_count,
    
    -- Correlation with attrition
    AVG(CASE WHEN attrition = 'Yes' THEN job_satisfaction END) as avg_satisfaction_departed,
    AVG(CASE WHEN attrition = 'No' THEN job_satisfaction END) as avg_satisfaction_staying,
    
    AVG(CASE WHEN attrition = 'Yes' THEN work_life_balance END) as avg_wlb_departed,
    AVG(CASE WHEN attrition = 'No' THEN work_life_balance END) as avg_wlb_staying,
    
    -- Risk indicators
    ROUND(
        (COUNT(CASE WHEN job_satisfaction <= 2 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as low_satisfaction_percentage,
    
    ROUND(
        (COUNT(CASE WHEN work_life_balance <= 2 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as poor_wlb_percentage
    
FROM employee_data
GROUP BY department
ORDER BY avg_job_satisfaction, avg_work_life_balance;

-- =============================================
-- Department Performance vs Attrition
-- =============================================

-- Performance analysis by department with attrition correlation
SELECT 
    department,
    
    -- Overall performance metrics
    AVG(performance_rating) as avg_performance_rating,
    COUNT(CASE WHEN performance_rating = 5 THEN 1 END) as exceptional_performers,
    COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) as high_performers,
    COUNT(CASE WHEN performance_rating <= 2 THEN 1 END) as underperformers,
    
    -- Performance of departed employees
    AVG(CASE WHEN attrition = 'Yes' THEN performance_rating END) as avg_performance_departed,
    COUNT(CASE WHEN attrition = 'Yes' AND performance_rating >= 4 THEN 1 END) as high_performers_lost,
    
    -- Critical insight: High performer attrition rate
    ROUND(
        (COUNT(CASE WHEN attrition = 'Yes' AND performance_rating >= 4 THEN 1 END) * 100.0 / 
         NULLIF(COUNT(CASE WHEN performance_rating >= 4 THEN 1 END), 0)), 2
    ) as high_performer_attrition_rate,
    
    -- Performance distribution
    ROUND(
        (COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as high_performer_percentage,
    
    ROUND(
        (COUNT(CASE WHEN performance_rating <= 2 THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as underperformer_percentage,
    
    -- Promotion readiness analysis
    COUNT(CASE WHEN performance_rating >= 4 AND years_at_company >= 2 THEN 1 END) as promotion_ready_employees
    
FROM employee_data e
GROUP BY department
ORDER BY high_performer_attrition_rate DESC;

-- =============================================
-- Department Cost Analysis
-- =============================================

-- Financial impact of attrition by department
WITH department_costs AS (
    SELECT 
        department,
        COUNT(*) as total_employees,
        SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
        AVG(monthly_income) as avg_monthly_salary,
        AVG(CASE WHEN attrition = 'Yes' THEN monthly_income END) as avg_salary_departed,
        SUM(CASE WHEN attrition = 'Yes' THEN monthly_income * 12 END) as total_annual_salary_lost
    FROM employee_data
    GROUP BY department
)
SELECT 
    department,
    total_employees,
    departed_employees,
    ROUND(avg_monthly_salary, 0) as avg_monthly_salary,
    ROUND(avg_salary_departed, 0) as avg_salary_departed,
    ROUND(total_annual_salary_lost, 0) as total_annual_salary_lost,
    
    -- Estimated replacement costs (assuming 50% of annual salary per replacement)
    ROUND(total_annual_salary_lost * 0.5, 0) as estimated_replacement_cost,
    
    -- Total estimated cost impact
    ROUND(total_annual_salary_lost + (total_annual_salary_lost * 0.5), 0) as total_estimated_cost_impact,
    
    -- Cost per employee in department
    ROUND(
        (total_annual_salary_lost + (total_annual_salary_lost * 0.5)) / total_employees, 0
    ) as cost_impact_per_employee,
    
    -- ROI of retention (potential savings)
    ROUND(total_annual_salary_lost * 0.5 * 0.25, 0) as potential_retention_investment  -- 25% of replacement cost
    
FROM department_costs
WHERE departed_employees > 0
ORDER BY total_estimated_cost_impact DESC;

-- =============================================
-- Department Manager Analysis
-- =============================================

-- Manager effectiveness analysis (simulated based on team performance)
WITH manager_analysis AS (
    SELECT 
        department,
        -- Assuming managers are identified by job titles
        COUNT(CASE WHEN job_role LIKE '%Manager%' THEN 1 END) as manager_count,
        -- Team size analysis (assuming 5-8 reports per manager is optimal)
        ROUND(COUNT(*) * 1.0 / NULLIF(COUNT(CASE WHEN job_role LIKE '%Manager%' THEN 1 END), 0), 1) as avg_team_size,
        
        -- Team performance metrics
        AVG(job_satisfaction) as team_avg_satisfaction,
        AVG(work_life_balance) as team_avg_wlb,
        AVG(performance_rating) as team_avg_performance,
        
        -- Attrition under management
        ROUND(
            (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
        ) as team_attrition_rate,
        
        -- Manager retention
        SUM(CASE WHEN job_role LIKE '%Manager%' AND attrition = 'Yes' THEN 1 ELSE 0 END) as managers_departed
    FROM employee_data
    GROUP BY department
)
SELECT 
    department,
    manager_count,
    avg_team_size,
    team_avg_satisfaction,
    team_avg_wlb,
    team_avg_performance,
    team_attrition_rate,
    managers_departed,
    
    -- Management effectiveness indicators
    CASE 
        WHEN avg_team_size > 12 THEN 'Managers Overloaded'
        WHEN avg_team_size < 4 THEN 'Managers Underutilized'
        ELSE 'Optimal Team Size'
    END as team_size_assessment,
    
    CASE 
        WHEN team_avg_satisfaction >= 4 AND team_attrition_rate <= 15 THEN 'Excellent Management'
        WHEN team_avg_satisfaction >= 3.5 AND team_attrition_rate <= 20 THEN 'Good Management'
        WHEN team_avg_satisfaction >= 3 AND team_attrition_rate <= 25 THEN 'Average Management'
        ELSE 'Management Development Needed'
    END as management_effectiveness
    
FROM manager_analysis
ORDER BY team_attrition_rate;

-- =============================================
-- Department Comparison Matrix
-- =============================================

-- Comprehensive department comparison for strategic planning
SELECT 
    department,
    
    -- Size and scale
    COUNT(*) as dept_size,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employee_data), 1) as percentage_of_workforce,
    
    -- Attrition metrics
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate,
    
    -- Engagement scores
    ROUND(AVG(job_satisfaction), 2) as satisfaction_score,
    ROUND(AVG(work_life_balance), 2) as wlb_score,
    ROUND(AVG(performance_rating), 2) as performance_score,
    
    -- Compensation metrics
    ROUND(AVG(monthly_income), 0) as avg_salary,
    
    -- Tenure and stability
    ROUND(AVG(years_at_company), 1) as avg_tenure,
    
    -- Risk factors
    ROUND(AVG(distance_from_home), 1) as avg_commute,
    ROUND(
        (COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) * 100.0 / COUNT(*)), 1
    ) as overtime_rate,
    
    -- Overall department health score (weighted calculation)
    ROUND(
        (AVG(job_satisfaction) * 0.3 + 
         AVG(work_life_balance) * 0.2 + 
         AVG(performance_rating) * 0.2 + 
         (5 - (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) / 5) * 0.3), 2
    ) as department_health_score,
    
    -- Priority ranking for intervention
    ROW_NUMBER() OVER (
        ORDER BY 
            (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) DESC,
            AVG(job_satisfaction) ASC,
            AVG(work_life_balance) ASC
    ) as intervention_priority_rank
    
FROM employee_data
GROUP BY department
ORDER BY intervention_priority_rank;

-- =============================================
-- Department Action Planning Queries
-- =============================================

-- Specific recommendations by department based on data analysis
SELECT 
    department,
    
    -- Current state metrics
    COUNT(*) as employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate,
    ROUND(AVG(job_satisfaction), 2) as satisfaction,
    ROUND(AVG(work_life_balance), 2) as work_life_balance,
    
    -- Primary issues identification
    CASE 
        WHEN AVG(job_satisfaction) <= 2.5 THEN 'Job Satisfaction Crisis'
        WHEN AVG(work_life_balance) <= 2.5 THEN 'Work-Life Balance Issues'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 THEN 'Attrition Crisis'
        WHEN AVG(monthly_income) < (SELECT AVG(monthly_income) FROM employee_data) * 0.9 THEN 'Compensation Issues'
        ELSE 'General Retention Focus'
    END as primary_issue,
    
    -- Recommended actions
    CASE 
        WHEN AVG(job_satisfaction) <= 2.5 THEN 'Manager training, role clarity, career development'
        WHEN AVG(work_life_balance) <= 2.5 THEN 'Workload management, flexible arrangements, overtime reduction'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 THEN 'Immediate intervention, stay interviews, retention bonuses'
        WHEN AVG(monthly_income) < (SELECT AVG(monthly_income) FROM employee_data) * 0.9 THEN 'Market salary review, compensation benchmarking'
        ELSE 'Preventive retention programs, engagement initiatives'
    END as recommended_action,
    
    -- Timeline urgency
    CASE 
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 OR AVG(job_satisfaction) <= 2.5 THEN 'Immediate (0-30 days)'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 18 OR AVG(work_life_balance) <= 2.5 THEN 'Urgent (1-3 months)'
        ELSE 'Medium-term (3-6 months)'
    END as timeline_priority
    
FROM employee_data
GROUP BY department
ORDER BY 
    CASE 
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 OR AVG(job_satisfaction) <= 2.5 THEN 1
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 18 OR AVG(work_life_balance) <= 2.5 THEN 2
        ELSE 3
    END;