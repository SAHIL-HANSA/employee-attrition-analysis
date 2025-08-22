-- Demographic and Tenure Analysis SQL Queries
-- Author: Sahil Hansa
-- Email: sahilhansa007@gmail.com
-- Description: Focused SQL analysis for demographic patterns and tenure impact on attrition
-- Location: Jammu, J&K, India

-- =============================================
-- Age Demographics and Attrition Analysis
-- =============================================

-- Detailed age group breakdown with statistical significance
SELECT 
    CASE 
        WHEN age < 25 THEN '22-24 (Early Career)'
        WHEN age BETWEEN 25 AND 29 THEN '25-29 (Peak Risk)'
        WHEN age BETWEEN 30 AND 34 THEN '30-34 (Settling)'
        WHEN age BETWEEN 35 AND 39 THEN '35-39 (Mid Career)'
        WHEN age BETWEEN 40 AND 44 THEN '40-44 (Experienced)'
        WHEN age >= 45 THEN '45+ (Senior)'
    END as detailed_age_group,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    AVG(job_satisfaction) as avg_satisfaction,
    AVG(years_at_company) as avg_tenure,
    -- Statistical significance indicators
    COUNT(*) * 0.1 as sample_threshold,  -- 10% threshold for statistical relevance
    CASE 
        WHEN COUNT(*) >= 10 THEN 'Statistically Significant'
        ELSE 'Small Sample Size'
    END as statistical_validity
FROM employee_data
GROUP BY 
    CASE 
        WHEN age < 25 THEN '22-24 (Early Career)'
        WHEN age BETWEEN 25 AND 29 THEN '25-29 (Peak Risk)'
        WHEN age BETWEEN 30 AND 34 THEN '30-34 (Settling)'
        WHEN age BETWEEN 35 AND 39 THEN '35-39 (Mid Career)'
        WHEN age BETWEEN 40 AND 44 THEN '40-44 (Experienced)'
        WHEN age >= 45 THEN '45+ (Senior)'
    END
ORDER BY 
    MIN(age);

-- Age vs. Performance correlation for departed employees
SELECT 
    CASE 
        WHEN age < 30 THEN 'Young Professionals'
        WHEN age BETWEEN 30 AND 40 THEN 'Mid-Career'  
        WHEN age > 40 THEN 'Senior Professionals'
    END as age_category,
    COUNT(*) as departed_count,
    AVG(performance_rating) as avg_performance_rating,
    AVG(monthly_income) as avg_salary_at_exit,
    AVG(years_at_company) as avg_tenure_at_exit,
    -- Top exit reasons for each age group
    MODE() WITHIN GROUP (ORDER BY exit_reason) as most_common_exit_reason
FROM employee_data 
WHERE attrition = 'Yes'
GROUP BY 
    CASE 
        WHEN age < 30 THEN 'Young Professionals'
        WHEN age BETWEEN 30 AND 40 THEN 'Mid-Career'  
        WHEN age > 40 THEN 'Senior Professionals'
    END
ORDER BY departed_count DESC;

-- =============================================
-- Gender Analysis and Pay Equity
-- =============================================

-- Comprehensive gender analysis with pay equity insights
SELECT 
    gender,
    department,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    MEDIAN(monthly_income) as median_salary,
    AVG(years_at_company) as avg_tenure,
    AVG(job_satisfaction) as avg_job_satisfaction,
    AVG(work_life_balance) as avg_work_life_balance,
    -- Performance metrics
    AVG(performance_rating) as avg_performance,
    COUNT(CASE WHEN performance_rating >= 4 THEN 1 END) as high_performers,
    -- Work arrangements
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_workers,
    ROUND(
        (COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as overtime_percentage
FROM employee_data
GROUP BY gender, department
ORDER BY gender, department;

-- Gender pay gap analysis
WITH gender_pay_analysis AS (
    SELECT 
        department,
        job_role,
        AVG(CASE WHEN gender = 'Male' THEN monthly_income END) as male_avg_salary,
        AVG(CASE WHEN gender = 'Female' THEN monthly_income END) as female_avg_salary,
        COUNT(CASE WHEN gender = 'Male' THEN 1 END) as male_count,
        COUNT(CASE WHEN gender = 'Female' THEN 1 END) as female_count
    FROM employee_data
    GROUP BY department, job_role
    HAVING COUNT(CASE WHEN gender = 'Male' THEN 1 END) > 0 
       AND COUNT(CASE WHEN gender = 'Female' THEN 1 END) > 0
)
SELECT 
    department,
    job_role,
    male_avg_salary,
    female_avg_salary,
    ROUND(((male_avg_salary - female_avg_salary) / female_avg_salary * 100), 2) as pay_gap_percentage,
    male_count,
    female_count,
    CASE 
        WHEN ABS((male_avg_salary - female_avg_salary) / female_avg_salary * 100) < 5 THEN 'Pay Equity Achieved'
        WHEN male_avg_salary > female_avg_salary THEN 'Male Pay Advantage'
        ELSE 'Female Pay Advantage'
    END as pay_equity_status
FROM gender_pay_analysis
ORDER BY ABS(pay_gap_percentage) DESC;

-- =============================================
-- Marital Status and Family Impact Analysis
-- =============================================

-- Marital status impact on attrition with family considerations
SELECT 
    marital_status,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(distance_from_home) as avg_commute_distance,
    AVG(work_life_balance) as avg_work_life_balance,
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_employees,
    ROUND(
        (COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as overtime_percentage,
    -- Exit reasons analysis for married vs single employees
    AVG(CASE WHEN attrition = 'Yes' THEN years_at_company END) as avg_tenure_at_exit
FROM employee_data
GROUP BY marital_status
ORDER BY attrition_rate_percent DESC;

-- Work-life balance correlation with family status
SELECT 
    marital_status,
    work_life_balance,
    COUNT(*) as employee_count,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as attritions,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate,
    AVG(distance_from_home) as avg_commute,
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_count
FROM employee_data
GROUP BY marital_status, work_life_balance
ORDER BY marital_status, work_life_balance;

-- =============================================
-- Education Level Impact Analysis
-- =============================================

-- Education level vs career progression and attrition
SELECT 
    education_level,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    AVG(years_at_company) as avg_tenure,
    AVG(performance_rating) as avg_performance,
    -- Career advancement indicators
    COUNT(CASE WHEN job_role LIKE '%Manager%' OR job_role LIKE '%Lead%' OR job_role LIKE '%Senior%' THEN 1 END) as leadership_roles,
    ROUND(
        (COUNT(CASE WHEN job_role LIKE '%Manager%' OR job_role LIKE '%Lead%' OR job_role LIKE '%Senior%' THEN 1 END) * 100.0 / COUNT(*)), 2
    ) as leadership_percentage,
    -- Satisfaction metrics
    AVG(job_satisfaction) as avg_job_satisfaction
FROM employee_data
GROUP BY education_level
ORDER BY 
    CASE education_level
        WHEN 'High School' THEN 1
        WHEN 'Bachelor' THEN 2
        WHEN 'Master' THEN 3
        WHEN 'PhD' THEN 4
        ELSE 5
    END;

-- =============================================
-- Tenure Deep Dive Analysis
-- =============================================

-- Year-by-year tenure analysis (first 10 years)
SELECT 
    years_at_company,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(monthly_income) as avg_salary,
    AVG(job_satisfaction) as avg_satisfaction,
    AVG(performance_rating) as avg_performance,
    -- Risk indicators
    CASE 
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 25 THEN 'High Risk'
        WHEN ROUND((SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2) > 15 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END as risk_category
FROM employee_data
WHERE years_at_company <= 10  -- Focus on first decade
GROUP BY years_at_company
ORDER BY years_at_company;

-- Critical tenure periods analysis
WITH tenure_survival AS (
    SELECT 
        years_at_company,
        COUNT(*) as employees_at_tenure,
        SUM(COUNT(*)) OVER (ORDER BY years_at_company DESC) as cumulative_survived
    FROM employee_data
    WHERE attrition = 'No'
    GROUP BY years_at_company
)
SELECT 
    t.years_at_company,
    t.employees_at_tenure,
    t.cumulative_survived,
    ROUND(
        (t.cumulative_survived * 100.0 / 
         (SELECT COUNT(*) FROM employee_data WHERE years_at_company >= t.years_at_company)), 2
    ) as survival_rate_percent,
    -- Identify critical drop-off points
    LAG(t.cumulative_survived) OVER (ORDER BY t.years_at_company) - t.cumulative_survived as tenure_dropoff
FROM tenure_survival t
ORDER BY t.years_at_company;

-- =============================================
-- Commute Distance and Remote Work Analysis
-- =============================================

-- Distance from home impact on attrition
SELECT 
    CASE 
        WHEN distance_from_home <= 5 THEN '0-5 km (Very Close)'
        WHEN distance_from_home BETWEEN 6 AND 15 THEN '6-15 km (Close)'
        WHEN distance_from_home BETWEEN 16 AND 25 THEN '16-25 km (Moderate)'
        WHEN distance_from_home > 25 THEN '25+ km (Far)'
    END as commute_category,
    COUNT(*) as total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) as departed_employees,
    ROUND(
        (SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as attrition_rate_percent,
    AVG(work_life_balance) as avg_work_life_balance,
    COUNT(CASE WHEN overtime = 'Yes' THEN 1 END) as overtime_workers,
    AVG(job_satisfaction) as avg_job_satisfaction
FROM employee_data
GROUP BY 
    CASE 
        WHEN distance_from_home <= 5 THEN '0-5 km (Very Close)'
        WHEN distance_from_home BETWEEN 6 AND 15 THEN '6-15 km (Close)'
        WHEN distance_from_home BETWEEN 16 AND 25 THEN '16-25 km (Moderate)'
        WHEN distance_from_home > 25 THEN '25+ km (Far)'
    END
ORDER BY AVG(distance_from_home);

-- =============================================
-- Demographic Risk Scoring Model
-- =============================================

-- Comprehensive demographic risk assessment for current employees
SELECT 
    employee_id,
    first_name,
    last_name,
    department,
    age,
    gender,
    marital_status,
    education_level,
    years_at_company,
    distance_from_home,
    -- Risk factors scoring
    CASE 
        WHEN age BETWEEN 25 AND 32 THEN 3  -- Peak risk age
        WHEN age < 25 OR age > 45 THEN 1   -- Lower risk
        ELSE 2                             -- Moderate risk
    END +
    CASE 
        WHEN years_at_company BETWEEN 1 AND 3 THEN 3  -- Critical tenure period
        WHEN years_at_company < 1 THEN 2               -- New employee risk
        ELSE 1                                         -- Stable tenure
    END +
    CASE 
        WHEN distance_from_home > 25 THEN 2  -- Long commute
        WHEN distance_from_home > 15 THEN 1  -- Moderate commute
        ELSE 0                               -- Short commute
    END +
    CASE 
        WHEN marital_status = 'Single' THEN 1  -- Single employees higher mobility
        ELSE 0
    END +
    CASE 
        WHEN job_satisfaction <= 2 THEN 3  -- Low satisfaction
        WHEN job_satisfaction = 3 THEN 2   -- Moderate satisfaction  
        ELSE 1                             -- High satisfaction
    END as demographic_risk_score,
    
    job_satisfaction,
    work_life_balance,
    performance_rating
FROM employee_data
WHERE attrition = 'No'  -- Current employees only
HAVING demographic_risk_score >= 7  -- High demographic risk threshold
ORDER BY demographic_risk_score DESC, performance_rating DESC;