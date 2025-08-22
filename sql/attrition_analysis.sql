-- Employee Attrition Analysis SQL Queries
-- Author: Sahil Hansa
-- Email: sahilhansa007@gmail.com
-- Description: Comprehensive SQL queries for analyzing employee attrition patterns
-- Location: Jammu, J&K, India

-- =============================================
-- Overall Attrition Rate Analysis
-- =============================================

-- Calculate overall attrition rate
SELECT 
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as overall_attrition_rate_percent
FROM employee_data;

-- Monthly attrition trend
SELECT 
    DATE_FORMAT(attrition_date, '%Y-%m') as month_year,
    COUNT(*) as departures,
    AVG(monthly_income) as avg_income_departed,
    AVG(years_at_company) as avg_tenure_departed
FROM employee_data 
WHERE attrition = 'Yes' 
  AND attrition_date IS NOT NULL
GROUP BY DATE_FORMAT(attrition_date, '%Y-%m')
ORDER BY month_year;

-- =============================================
-- Department-wise Attrition Analysis
-- =============================================

-- Attrition rate by department
SELECT 
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_department_salary,
    AVG(job_satisfaction) as avg_job_satisfaction
FROM employee_data
GROUP BY department
ORDER BY attrition_rate_percent DESC;

-- Department performance correlation
SELECT 
    e.department,
    COUNT(*) as total_employees,
    AVG(p.performance_rating) as avg_performance_rating,
    AVG(CASE WHEN e.attrition = 'Yes' THEN p.performance_rating END) as avg_performance_departed,
    SUM(CASE WHEN e.attrition = 'Yes' THEN 1 ELSE 0 END) as departed_count,
    ROUND(
        (SUM(CASE WHEN e.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate
FROM employee_data e
LEFT JOIN performance_data p ON e.employee_id = p.employee_id
GROUP BY e.department
ORDER BY attrition_rate DESC;

-- =============================================
-- Age and Demographic Analysis
-- =============================================

-- Attrition by age groups
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 30 THEN '25-30'
        WHEN age BETWEEN 31 AND 35 THEN '31-35'
        WHEN age BETWEEN 36 AND 40 THEN '36-40'
        WHEN age > 40 THEN 'Over 40'
    END as age_group,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent
FROM employee_data
GROUP BY 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 30 THEN '25-30'
        WHEN age BETWEEN 31 AND 35 THEN '31-35'
        WHEN age BETWEEN 36 AND 40 THEN '36-40'
        WHEN age > 40 THEN 'Over 40'
    END
ORDER BY attrition_rate_percent DESC;

-- Gender-based attrition analysis
SELECT 
    gender,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    AVG(job_satisfaction) as avg_satisfaction
FROM employee_data
GROUP BY gender
ORDER BY attrition_rate_percent DESC;

-- Marital status impact on attrition
SELECT 
    marital_status,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(distance_from_home) as avg_commute_distance
FROM employee_data
GROUP BY marital_status
ORDER BY attrition_rate_percent DESC;

-- =============================================
-- Tenure and Experience Analysis
-- =============================================

-- Attrition by years at company
SELECT 
    CASE 
        WHEN years_at_company < 1 THEN 'Less than 1 year'
        WHEN years_at_company BETWEEN 1 AND 3 THEN '1-3 years'
        WHEN years_at_company BETWEEN 4 AND 7 THEN '4-7 years' 
        WHEN years_at_company BETWEEN 8 AND 12 THEN '8-12 years'
        WHEN years_at_company > 12 THEN 'More than 12 years'
    END as tenure_group,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary_range
FROM employee_data
GROUP BY 
    CASE 
        WHEN years_at_company < 1 THEN 'Less than 1 year'
        WHEN years_at_company BETWEEN 1 AND 3 THEN '1-3 years'
        WHEN years_at_company BETWEEN 4 AND 7 THEN '4-7 years' 
        WHEN years_at_company BETWEEN 8 AND 12 THEN '8-12 years'
        WHEN years_at_company > 12 THEN 'More than 12 years'
    END
ORDER BY attrition_rate_percent DESC;

-- Critical tenure periods (highest risk)
SELECT 
    years_at_company,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent
FROM employee_data
WHERE years_at_company <= 5  -- Focus on first 5 years
GROUP BY years_at_company
ORDER BY attrition_rate_percent DESC;

-- =============================================
-- Compensation and Satisfaction Analysis
-- =============================================

-- Salary range impact on attrition
SELECT 
    CASE 
        WHEN monthly_income < 4000 THEN 'Under $4,000'
        WHEN monthly_income BETWEEN 4000 AND 5499 THEN '$4,000-$5,499'
        WHEN monthly_income BETWEEN 5500 AND 6999 THEN '$5,500-$6,999'
        WHEN monthly_income >= 7000 THEN '$7,000+'
    END as salary_range,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(job_satisfaction) as avg_job_satisfaction,
    AVG(work_life_balance) as avg_work_life_balance
FROM employee_data
GROUP BY 
    CASE 
        WHEN monthly_income < 4000 THEN 'Under $4,000'
        WHEN monthly_income BETWEEN 4000 AND 5499 THEN '$4,000-$5,499'
        WHEN monthly_income BETWEEN 5500 AND 6999 THEN '$5,500-$6,999'
        WHEN monthly_income >= 7000 THEN '$7,000+'
    END
ORDER BY attrition_rate_percent DESC;

-- Job satisfaction correlation with attrition
SELECT 
    job_satisfaction,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary
FROM employee_data
GROUP BY job_satisfaction
ORDER BY job_satisfaction;

-- Work-life balance impact
SELECT 
    work_life_balance,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as employees_with_overtime
FROM employee_data
GROUP BY work_life_balance
ORDER BY work_life_balance;

-- =============================================
-- Performance and Career Development
-- =============================================

-- Performance rating vs attrition
SELECT 
    e.performance_rating,
    COUNT(*) as total_employees,
    SUM(CASE WHEN e.attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN e.attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(p.goals_met) as avg_goals_achievement,
    AVG(e.monthly_income) as avg_salary
FROM employee_data e
LEFT JOIN performance_data p ON e.employee_id = p.employee_id
GROUP BY e.performance_rating
ORDER BY e.performance_rating DESC;

-- High performers who left
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    e.job_role,
    e.years_at_company,
    e.monthly_income,
    e.performance_rating,
    e.attrition_date,
    e.exit_reason,
    p.promotion_ready
FROM employee_data e
LEFT JOIN performance_data p ON e.employee_id = p.employee_id
WHERE e.attrition = 'Yes' 
  AND e.performance_rating >= 4
ORDER BY e.performance_rating DESC, e.monthly_income DESC;

-- =============================================
-- Exit Reasons Analysis
-- =============================================

-- Primary exit reasons
SELECT 
    exit_reason,
    COUNT(*) as frequency,
    ROUND((COUNT(*) * 100.0 / (SELECT COUNT(*) FROM employee_data WHERE attrition = 'Yes')), 2) as percentage,
    AVG(years_at_company) as avg_tenure_at_exit,
    AVG(monthly_income) as avg_salary_at_exit
FROM employee_data
WHERE attrition = 'Yes' AND exit_reason IS NOT NULL
GROUP BY exit_reason
ORDER BY frequency DESC;

-- Exit survey insights
SELECT 
    ex.exit_reason_primary,
    COUNT(*) as frequency,
    AVG(ex.overall_satisfaction) as avg_satisfaction,
    AVG(ex.compensation_satisfaction) as avg_comp_satisfaction,
    AVG(ex.growth_opportunities) as avg_growth_rating,
    AVG(ex.work_life_balance_rating) as avg_wlb_rating,
    AVG(ex.would_recommend_company) as avg_recommendation_score
FROM exit_survey_data ex
GROUP BY ex.exit_reason_primary
ORDER BY frequency DESC;

-- =============================================
-- Predictive Risk Analysis
-- =============================================

-- High-risk employees (current employees with risk factors)
SELECT 
    e.employee_id,
    e.first_name,
    e.last_name,
    e.department,
    e.job_role,
    e.years_at_company,
    e.monthly_income,
    e.job_satisfaction,
    e.work_life_balance,
    e.performance_rating,
    p.promotion_ready,
    -- Risk score calculation
    CASE 
        WHEN e.job_satisfaction <= 2 THEN 3
        WHEN e.job_satisfaction = 3 THEN 2  
        ELSE 1
    END +
    CASE 
        WHEN e.work_life_balance <= 2 THEN 3
        WHEN e.work_life_balance = 3 THEN 2
        ELSE 1  
    END +
    CASE 
        WHEN e.years_at_company BETWEEN 1 AND 3 THEN 2
        WHEN e.years_at_company < 1 THEN 3
        ELSE 1
    END +
    CASE 
        WHEN e.performance_rating >= 4 AND p.promotion_ready = 'Yes' THEN 2
        ELSE 1
    END as risk_score
FROM employee_data e
LEFT JOIN performance_data p ON e.employee_id = p.employee_id
WHERE e.attrition = 'No'  -- Current employees only
HAVING risk_score >= 6  -- High risk threshold
ORDER BY risk_score DESC, e.performance_rating DESC;

-- Department risk summary for current employees
SELECT 
    department,
    COUNT(*) as current_employees,
    AVG(job_satisfaction) as avg_satisfaction,
    AVG(work_life_balance) as avg_work_life_balance,
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_employees,
    ROUND(
        (COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as overtime_percentage,
    -- Calculate department risk level
    CASE 
        WHEN AVG(job_satisfaction) <= 2.5 OR AVG(work_life_balance) <= 2.5 THEN 'High Risk'
        WHEN AVG(job_satisfaction) <= 3.5 OR AVG(work_life_balance) <= 3.5 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as department_risk_level
FROM employee_data
WHERE attrition = 'No'
GROUP BY department
ORDER BY avg_satisfaction, avg_work_life_balance;