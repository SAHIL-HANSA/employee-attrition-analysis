"""
Employee Attrition Analysis and Visualization
Author: Sahil Hansa
Email: sahilhansa007@gmail.com
Description: Comprehensive Python analysis for employee attrition patterns and trends
Location: Jammu, J&K, India
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class EmployeeAttritionAnalyzer:
    """
    Employee Attrition Analysis Class
    
    Comprehensive analysis of employee turnover patterns and retention insights
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    
    def __init__(self):
        self.employee_data = None
        self.performance_data = None
        self.exit_survey_data = None
        self.analysis_results = {}
        
    def load_data(self, employee_file='data/sample/employee_data.csv', 
                  performance_file='data/sample/performance_data.csv',
                  exit_survey_file='data/sample/exit_survey_data.csv'):
        """Load all HR datasets"""
        try:
            self.employee_data = pd.read_csv(employee_file)
            self.performance_data = pd.read_csv(performance_file)
            self.exit_survey_data = pd.read_csv(exit_survey_file)
            
            print(f"Loaded employee data: {len(self.employee_data)} records")
            print(f"Loaded performance data: {len(self.performance_data)} records")  
            print(f"Loaded exit survey data: {len(self.exit_survey_data)} records")
            
            return True
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def calculate_attrition_rates(self):
        """Calculate overall and departmental attrition rates"""
        if self.employee_data is None:
            print("No employee data loaded")
            return None
        
        # Overall attrition rate
        total_employees = len(self.employee_data)
        departed_employees = len(self.employee_data[self.employee_data['attrition'] == 'Yes'])
        overall_rate = (departed_employees / total_employees) * 100
        
        print(f"=== ATTRITION ANALYSIS RESULTS ===")
        print(f"Total Employees: {total_employees}")
        print(f"Departed Employees: {departed_employees}")
        print(f"Overall Attrition Rate: {overall_rate:.2f}%")
        
        # Department-wise attrition
        dept_attrition = self.employee_data.groupby('department').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum()
        }).rename(columns={'employee_id': 'total_employees', 'attrition': 'departed'})
        
        dept_attrition['attrition_rate'] = (dept_attrition['departed'] / dept_attrition['total_employees']) * 100
        dept_attrition = dept_attrition.sort_values('attrition_rate', ascending=False)
        
        print(f"\n=== DEPARTMENT ATTRITION RATES ===")
        for dept, row in dept_attrition.iterrows():
            print(f"{dept}: {row['attrition_rate']:.1f}% ({row['departed']}/{row['total_employees']})")
        
        self.analysis_results['overall_rate'] = overall_rate
        self.analysis_results['department_rates'] = dept_attrition
        
        return dept_attrition
    
    def analyze_demographics(self):
        """Analyze attrition by demographic factors"""
        if self.employee_data is None:
            return None
        
        print(f"\n=== DEMOGRAPHIC ANALYSIS ===")
        
        # Age group analysis
        self.employee_data['age_group'] = pd.cut(self.employee_data['age'], 
                                               bins=[0, 25, 30, 35, 40, 100],
                                               labels=['Under 25', '25-30', '31-35', '36-40', 'Over 40'])
        
        age_attrition = self.employee_data.groupby('age_group').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum()
        })
        age_attrition['attrition_rate'] = (age_attrition['attrition'] / age_attrition['employee_id']) * 100
        
        print("Age Group Attrition Rates:")
        for age_group, row in age_attrition.iterrows():
            print(f"  {age_group}: {row['attrition_rate']:.1f}%")
        
        # Gender analysis
        gender_attrition = self.employee_data.groupby('gender').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum()
        })
        gender_attrition['attrition_rate'] = (gender_attrition['attrition'] / gender_attrition['employee_id']) * 100
        
        print(f"\nGender Attrition Rates:")
        for gender, row in gender_attrition.iterrows():
            print(f"  {gender}: {row['attrition_rate']:.1f}%")
        
        self.analysis_results['age_analysis'] = age_attrition
        self.analysis_results['gender_analysis'] = gender_attrition
        
        return age_attrition, gender_attrition
    
    def analyze_tenure_impact(self):
        """Analyze the impact of tenure on attrition"""
        if self.employee_data is None:
            return None
        
        print(f"\n=== TENURE ANALYSIS ===")
        
        # Tenure group analysis
        self.employee_data['tenure_group'] = pd.cut(self.employee_data['years_at_company'],
                                                  bins=[0, 1, 3, 7, 12, 100],
                                                  labels=['<1 year', '1-3 years', '4-7 years', '8-12 years', '>12 years'])
        
        tenure_attrition = self.employee_data.groupby('tenure_group').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum(),
            'monthly_income': 'mean'
        })
        tenure_attrition['attrition_rate'] = (tenure_attrition['attrition'] / tenure_attrition['employee_id']) * 100
        
        print("Tenure Group Attrition Rates:")
        for tenure, row in tenure_attrition.iterrows():
            print(f"  {tenure}: {row['attrition_rate']:.1f}% (Avg Salary: ${row['monthly_income']:.0f})")
        
        # Critical first 3 years analysis
        early_tenure = self.employee_data[self.employee_data['years_at_company'] <= 3]
        early_attrition_rate = (len(early_tenure[early_tenure['attrition'] == 'Yes']) / len(early_tenure)) * 100
        
        print(f"\nCritical Insight: {early_attrition_rate:.1f}% attrition rate in first 3 years")
        
        self.analysis_results['tenure_analysis'] = tenure_attrition
        
        return tenure_attrition
    
    def analyze_compensation_satisfaction(self):
        """Analyze relationship between compensation and attrition"""
        if self.employee_data is None:
            return None
        
        print(f"\n=== COMPENSATION & SATISFACTION ANALYSIS ===")
        
        # Salary range analysis
        self.employee_data['salary_range'] = pd.cut(self.employee_data['monthly_income'],
                                                  bins=[0, 4000, 5500, 7000, 10000],
                                                  labels=['<$4K', '$4K-$5.5K', '$5.5K-$7K', '>$7K'])
        
        salary_attrition = self.employee_data.groupby('salary_range').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum(),
            'job_satisfaction': 'mean',
            'work_life_balance': 'mean'
        })
        salary_attrition['attrition_rate'] = (salary_attrition['attrition'] / salary_attrition['employee_id']) * 100
        
        print("Salary Range Attrition Analysis:")
        for salary_range, row in salary_attrition.iterrows():
            print(f"  {salary_range}: {row['attrition_rate']:.1f}% (Satisfaction: {row['job_satisfaction']:.1f})")
        
        # Job satisfaction correlation
        satisfaction_attrition = self.employee_data.groupby('job_satisfaction').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum()
        })
        satisfaction_attrition['attrition_rate'] = (satisfaction_attrition['attrition'] / satisfaction_attrition['employee_id']) * 100
        
        print(f"\nJob Satisfaction vs Attrition:")
        for satisfaction, row in satisfaction_attrition.iterrows():
            print(f"  Satisfaction {satisfaction}: {row['attrition_rate']:.1f}% attrition rate")
        
        self.analysis_results['salary_analysis'] = salary_attrition
        self.analysis_results['satisfaction_analysis'] = satisfaction_attrition
        
        return salary_attrition, satisfaction_attrition
    
    def analyze_performance_impact(self):
        """Analyze relationship between performance and attrition"""
        if self.employee_data is None or self.performance_data is None:
            return None
        
        print(f"\n=== PERFORMANCE ANALYSIS ===")
        
        # Merge employee and performance data
        merged_data = self.employee_data.merge(self.performance_data, on='employee_id', how='left')
        
        # Performance rating vs attrition
        perf_attrition = merged_data.groupby('performance_rating').agg({
            'employee_id': 'count',
            'attrition': lambda x: (x == 'Yes').sum(),
            'monthly_income': 'mean',
            'goals_met': 'mean'
        })
        perf_attrition['attrition_rate'] = (perf_attrition['attrition'] / perf_attrition['employee_id']) * 100
        
        print("Performance Rating vs Attrition:")
        for rating, row in perf_attrition.iterrows():
            if not pd.isna(rating):
                print(f"  Rating {rating}: {row['attrition_rate']:.1f}% (Goals Met: {row['goals_met']:.1f}%)")
        
        # High performers who left
        high_performers_left = merged_data[
            (merged_data['attrition'] == 'Yes') & 
            (merged_data['performance_rating'] >= 4)
        ]
        
        print(f"\nCritical Insight: {len(high_performers_left)} high performers (rating 4+) left the company")
        
        if len(high_performers_left) > 0:
            print("High Performers Who Left:")
            for _, emp in high_performers_left.iterrows():
                print(f"  {emp['first_name']} {emp['last_name']} - {emp['department']} - Rating: {emp['performance_rating']}")
        
        self.analysis_results['performance_analysis'] = perf_attrition
        self.analysis_results['high_performers_left'] = high_performers_left
        
        return perf_attrition
    
    def analyze_exit_reasons(self):
        """Analyze exit survey data and departure reasons"""
        if self.exit_survey_data is None:
            return None
        
        print(f"\n=== EXIT REASONS ANALYSIS ===")
        
        # Primary exit reasons
        exit_reasons = self.exit_survey_data['exit_reason_primary'].value_counts()
        total_exits = len(self.exit_survey_data)
        
        print("Top Exit Reasons:")
        for reason, count in exit_reasons.head(5).items():
            percentage = (count / total_exits) * 100
            print(f"  {reason}: {count} ({percentage:.1f}%)")
        
        # Exit satisfaction analysis
        avg_satisfaction = self.exit_survey_data.groupby('exit_reason_primary').agg({
            'overall_satisfaction': 'mean',
            'compensation_satisfaction': 'mean',
            'growth_opportunities': 'mean',
            'work_life_balance_rating': 'mean',
            'would_recommend_company': 'mean'
        }).round(2)
        
        print(f"\nExit Satisfaction by Reason (1-5 scale):")
        for reason, row in avg_satisfaction.iterrows():
            print(f"  {reason}:")
            print(f"    Overall: {row['overall_satisfaction']}, Growth: {row['growth_opportunities']}")
        
        self.analysis_results['exit_reasons'] = exit_reasons
        self.analysis_results['exit_satisfaction'] = avg_satisfaction
        
        return exit_reasons, avg_satisfaction
    
    def identify_high_risk_employees(self):
        """Identify current employees at high risk of leaving"""
        if self.employee_data is None:
            return None
        
        print(f"\n=== HIGH RISK EMPLOYEE IDENTIFICATION ===")
        
        # Current employees only
        current_employees = self.employee_data[self.employee_data['attrition'] == 'No'].copy()
        
        # Calculate risk score based on multiple factors
        def calculate_risk_score(row):
            score = 0
            
            # Job satisfaction (higher weight)
            if row['job_satisfaction'] <= 2:
                score += 3
            elif row['job_satisfaction'] == 3:
                score += 2
            
            # Work-life balance
            if row['work_life_balance'] <= 2:
                score += 3
            elif row['work_life_balance'] == 3:
                score += 2
            
            # Tenure (1-3 years are highest risk)
            if 1 <= row['years_at_company'] <= 3:
                score += 2
            elif row['years_at_company'] < 1:
                score += 3
            
            # High performers without growth (based on performance rating)
            if row['performance_rating'] >= 4:
                score += 1  # High performers are valuable but at risk
            
            return score
        
        current_employees['risk_score'] = current_employees.apply(calculate_risk_score, axis=1)
        
        # High risk employees (score >= 6)
        high_risk = current_employees[current_employees['risk_score'] >= 6].sort_values('risk_score', ascending=False)
        
        print(f"Identified {len(high_risk)} high-risk employees (risk score >= 6):")
        
        for _, emp in high_risk.head(10).iterrows():  # Show top 10
            print(f"  {emp['first_name']} {emp['last_name']} - {emp['department']}")
            print(f"    Risk Score: {emp['risk_score']}, Satisfaction: {emp['job_satisfaction']}, Tenure: {emp['years_at_company']} years")
        
        # Department risk summary
        dept_risk = current_employees.groupby('department').agg({
            'risk_score': 'mean',
            'job_satisfaction': 'mean',
            'work_life_balance': 'mean',
            'employee_id': 'count'
        }).round(2)
        
        print(f"\nDepartment Risk Summary (Current Employees):")
        for dept, row in dept_risk.sort_values('risk_score', ascending=False).iterrows():
            risk_level = 'High' if row['risk_score'] >= 4 else 'Medium' if row['risk_score'] >= 2.5 else 'Low'
            print(f"  {dept}: Risk Score {row['risk_score']} ({risk_level}) - {row['employee_id']} employees")
        
        self.analysis_results['high_risk_employees'] = high_risk
        self.analysis_results['department_risk'] = dept_risk
        
        return high_risk, dept_risk
    
    def generate_retention_recommendations(self):
        """Generate actionable retention recommendations based on analysis"""
        print(f"\n=== RETENTION RECOMMENDATIONS ===")
        print("Author: Sahil Hansa (sahilhansa007@gmail.com)")
        print("="*50)
        
        recommendations = []
        
        # Based on department analysis
        if 'department_rates' in self.analysis_results:
            highest_attrition_dept = self.analysis_results['department_rates'].index[0]
            highest_rate = self.analysis_results['department_rates'].iloc[0]['attrition_rate']
            
            recommendations.append({
                'priority': 'High',
                'area': 'Department Focus',
                'action': f'Immediate intervention needed in {highest_attrition_dept} department',
                'details': f'Attrition rate of {highest_rate:.1f}% requires urgent attention',
                'timeline': '0-3 months'
            })
        
        # Based on tenure analysis
        recommendations.append({
            'priority': 'High',
            'area': 'Early Career Support',
            'action': 'Implement comprehensive onboarding and 1-3 year retention program',
            'details': 'Focus on first 3 years when attrition risk is highest',
            'timeline': '0-6 months'
        })
        
        # Based on satisfaction analysis
        recommendations.append({
            'priority': 'Medium',
            'area': 'Job Satisfaction',
            'action': 'Regular satisfaction surveys and manager training',
            'details': 'Address low satisfaction scores through better management practices',
            'timeline': '3-6 months'
        })
        
        # Based on performance analysis
        if 'high_performers_left' in self.analysis_results:
            recommendations.append({
                'priority': 'Critical',
                'area': 'High Performer Retention',
                'action': 'Career development and recognition programs for top performers',
                'details': 'Prevent loss of high-performing employees through better career pathing',
                'timeline': '0-3 months'
            })
        
        # Based on compensation analysis
        recommendations.append({
            'priority': 'Medium',
            'area': 'Compensation Review',
            'action': 'Market salary analysis and adjustment for key roles',
            'details': 'Ensure competitive compensation especially for high-risk departments',
            'timeline': '3-12 months'
        })
        
        print("Recommended Actions:")
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. {rec['area']} ({rec['priority']} Priority)")
            print(f"   Action: {rec['action']}")
            print(f"   Details: {rec['details']}")
            print(f"   Timeline: {rec['timeline']}")
        
        return recommendations
    
    def create_visualizations(self, save_plots=True):
        """Create comprehensive visualization charts"""
        if self.employee_data is None:
            return None
        
        print(f"\n=== CREATING VISUALIZATIONS ===")
        
        # Set up the plot style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # 1. Department Attrition Rates
        if 'department_rates' in self.analysis_results:
            plt.figure(figsize=(12, 6))
            dept_rates = self.analysis_results['department_rates']
            
            bars = plt.bar(dept_rates.index, dept_rates['attrition_rate'], 
                          color=['#ff4444' if x > 20 else '#ffaa00' if x > 15 else '#44aa44' 
                                for x in dept_rates['attrition_rate']])
            
            plt.title('Employee Attrition Rate by Department', fontsize=16, fontweight='bold')
            plt.xlabel('Department', fontsize=12)
            plt.ylabel('Attrition Rate (%)', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for bar, rate in zip(bars, dept_rates['attrition_rate']):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            if save_plots:
                plt.savefig('assets/department_attrition_chart.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 2. Age Group Analysis
        if 'age_analysis' in self.analysis_results:
            plt.figure(figsize=(10, 6))
            age_analysis = self.analysis_results['age_analysis']
            
            plt.pie(age_analysis['employee_id'], labels=age_analysis.index, autopct='%1.1f%%',
                   startangle=90, colors=sns.color_palette('husl', len(age_analysis)))
            plt.title('Employee Distribution by Age Group', fontsize=16, fontweight='bold')
            plt.axis('equal')
            
            if save_plots:
                plt.savefig('assets/age_distribution_chart.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        # 3. Tenure vs Attrition
        if 'tenure_analysis' in self.analysis_results:
            plt.figure(figsize=(12, 6))
            tenure_analysis = self.analysis_results['tenure_analysis']
            
            bars = plt.bar(tenure_analysis.index, tenure_analysis['attrition_rate'],
                          color='skyblue', edgecolor='navy', linewidth=1.2)
            
            plt.title('Attrition Rate by Years at Company', fontsize=16, fontweight='bold')
            plt.xlabel('Years at Company', fontsize=12)
            plt.ylabel('Attrition Rate (%)', fontsize=12)
            
            # Add value labels
            for bar, rate in zip(bars, tenure_analysis['attrition_rate']):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            if save_plots:
                plt.savefig('assets/tenure_attrition_chart.png', dpi=300, bbox_inches='tight')
            plt.show()
        
        print("Visualizations created successfully!")
    
    def generate_executive_summary(self):
        """Generate executive summary of findings"""
        print(f"\n" + "="*60)
        print("EMPLOYEE ATTRITION ANALYSIS - EXECUTIVE SUMMARY")
        print("="*60)
        print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Analyst: Sahil Hansa (sahilhansa007@gmail.com)")
        print(f"Location: Jammu, J&K, India")
        print("="*60)
        
        if 'overall_rate' in self.analysis_results:
            print(f"\n📊 KEY FINDINGS:")
            print(f"• Overall Attrition Rate: {self.analysis_results['overall_rate']:.1f}%")
            
            if 'department_rates' in self.analysis_results:
                highest_dept = self.analysis_results['department_rates'].index[0]
                highest_rate = self.analysis_results['department_rates'].iloc[0]['attrition_rate']
                print(f"• Highest Risk Department: {highest_dept} ({highest_rate:.1f}%)")
            
            if 'high_risk_employees' in self.analysis_results:
                high_risk_count = len(self.analysis_results['high_risk_employees'])
                print(f"• High-Risk Current Employees: {high_risk_count}")
            
            if 'exit_reasons' in self.analysis_results:
                top_reason = self.analysis_results['exit_reasons'].index[0]
                print(f"• Top Exit Reason: {top_reason}")
        
        print(f"\n💡 BUSINESS IMPACT:")
        total_employees = len(self.employee_data) if self.employee_data is not None else 0
        departed = len(self.employee_data[self.employee_data['attrition'] == 'Yes']) if self.employee_data is not None else 0
        
        # Estimated costs (industry averages)
        avg_salary = self.employee_data['monthly_income'].mean() * 12 if self.employee_data is not None else 60000
        replacement_cost = avg_salary * 0.5  # 50% of annual salary
        total_cost = departed * replacement_cost
        
        print(f"• Estimated Annual Turnover Cost: ${total_cost:,.0f}")
        print(f"• Average Replacement Cost per Employee: ${replacement_cost:,.0f}")
        
        print(f"\n🎯 RECOMMENDED ACTIONS:")
        print("1. Immediate intervention in high-attrition departments")
        print("2. Enhanced onboarding and early-career support programs")
        print("3. Manager training on employee engagement and retention")
        print("4. Compensation review and market alignment")
        print("5. Career development programs for high performers")
        
        print("="*60)

def main():
    """
    Main execution function for employee attrition analysis
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    print("=== Employee Attrition Analysis System ===")
    print("Author: Sahil Hansa")
    print("Email: sahilhansa007@gmail.com")
    print("GitHub: https://github.com/SAHIL-HANSA")
    print("Location: Jammu, J&K, India")
    print("=" * 45)
    
    # Initialize analyzer
    analyzer = EmployeeAttritionAnalyzer()
    
    # Load data
    if not analyzer.load_data():
        print("Failed to load data. Please check file paths.")
        return
    
    # Perform comprehensive analysis
    print(f"\nPerforming comprehensive attrition analysis...")
    
    analyzer.calculate_attrition_rates()
    analyzer.analyze_demographics()
    analyzer.analyze_tenure_impact()
    analyzer.analyze_compensation_satisfaction()
    analyzer.analyze_performance_impact()
    analyzer.analyze_exit_reasons()
    analyzer.identify_high_risk_employees()
    
    # Generate recommendations
    recommendations = analyzer.generate_retention_recommendations()
    
    # Create visualizations
    analyzer.create_visualizations()
    
    # Generate executive summary
    analyzer.generate_executive_summary()
    
    print(f"\n=== Analysis Complete ===")
    print("Check the generated visualizations and recommendations.")
    print("All insights have been compiled for HR strategic planning.")

if __name__ == "__main__":
    main()