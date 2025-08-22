"""
HR Data Visualization Module
Author: Sahil Hansa
Email: sahilhansa007@gmail.com
Description: Comprehensive visualization suite for employee attrition analysis
Location: Jammu, J&K, India
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

class HRDataVisualizer:
    """
    Comprehensive HR Data Visualization Suite
    
    Creates professional charts and interactive dashboards for employee attrition analysis
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    
    def __init__(self, data_path='data/processed/attrition_analysis_clean.csv'):
        self.data = None
        self.load_data(data_path)
        
    def load_data(self, data_path):
        """Load processed HR data"""
        try:
            self.data = pd.read_csv(data_path)
            print(f"✅ Loaded HR data: {len(self.data)} employees")
            return True
        except FileNotFoundError:
            print(f"⚠️ File not found: {data_path}")
            print("Using sample data generation...")
            self.generate_sample_data()
            return False
        except Exception as e:
            print(f"❌ Error loading data: {str(e)}")
            return False
    
    def generate_sample_data(self):
        """Generate sample data if processed data not available"""
        np.random.seed(42)
        n_employees = 500
        
        departments = ['IT', 'Sales', 'Marketing', 'Finance', 'HR', 'Operations']
        
        self.data = pd.DataFrame({
            'department': np.random.choice(departments, n_employees),
            'age': np.random.normal(35, 8, n_employees).astype(int),
            'years_at_company': np.random.exponential(3, n_employees),
            'monthly_income': np.random.normal(5500, 1500, n_employees),
            'job_satisfaction': np.random.randint(1, 6, n_employees),
            'work_life_balance': np.random.randint(1, 6, n_employees),
            'performance_rating': np.random.choice([2, 3, 4, 5], n_employees, p=[0.1, 0.3, 0.4, 0.2]),
            'attrition': np.random.choice(['Yes', 'No'], n_employees, p=[0.18, 0.82]),
            'gender': np.random.choice(['Male', 'Female'], n_employees),
            'distance_from_home': np.random.exponential(12, n_employees),
            'overtime': np.random.choice(['Yes', 'No'], n_employees, p=[0.3, 0.7])
        })
        
        # Ensure realistic bounds
        self.data['age'] = self.data['age'].clip(22, 65)
        self.data['years_at_company'] = self.data['years_at_company'].clip(0, 40)
        self.data['monthly_income'] = self.data['monthly_income'].clip(2500, 15000)
        self.data['distance_from_home'] = self.data['distance_from_home'].clip(1, 50)
        
        print("📊 Generated sample data for visualization")
    
    def create_attrition_overview_dashboard(self, save_path='assets/attrition_overview.png'):
        """Create comprehensive attrition overview dashboard"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Employee Attrition Analysis Dashboard\nAuthor: Sahil Hansa', 
                     fontsize=16, fontweight='bold', y=0.95)
        
        # 1. Overall Attrition Rate
        attrition_counts = self.data['attrition'].value_counts()
        colors = ['#ff6b6b', '#4ecdc4']
        axes[0, 0].pie(attrition_counts.values, labels=attrition_counts.index, autopct='%1.1f%%',
                       colors=colors, startangle=90)
        axes[0, 0].set_title('Overall Attrition Rate', fontweight='bold')
        
        # 2. Department Attrition
        dept_attrition = self.data.groupby('department')['attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        ).sort_values(ascending=False)
        
        bars = axes[0, 1].bar(dept_attrition.index, dept_attrition.values, 
                             color=plt.cm.Set3(np.linspace(0, 1, len(dept_attrition))))
        axes[0, 1].set_title('Attrition Rate by Department', fontweight='bold')
        axes[0, 1].set_ylabel('Attrition Rate (%)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar, rate in zip(bars, dept_attrition.values):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                           f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # 3. Age Distribution
        age_groups = pd.cut(self.data['age'], bins=[20, 30, 40, 50, 70], 
                           labels=['20-30', '30-40', '40-50', '50+'])
        age_attrition = self.data.groupby(age_groups)['attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        axes[0, 2].bar(age_attrition.index.astype(str), age_attrition.values, 
                      color='skyblue', alpha=0.8)
        axes[0, 2].set_title('Attrition Rate by Age Group', fontweight='bold')
        axes[0, 2].set_ylabel('Attrition Rate (%)')
        
        # 4. Tenure vs Attrition
        tenure_groups = pd.cut(self.data['years_at_company'], 
                              bins=[0, 1, 3, 5, 10, 50], 
                              labels=['0-1', '1-3', '3-5', '5-10', '10+'])
        tenure_attrition = self.data.groupby(tenure_groups)['attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        axes[1, 0].bar(tenure_attrition.index.astype(str), tenure_attrition.values,
                      color='lightcoral', alpha=0.8)
        axes[1, 0].set_title('Attrition Rate by Years at Company', fontweight='bold')
        axes[1, 0].set_xlabel('Years at Company')
        axes[1, 0].set_ylabel('Attrition Rate (%)')
        
        # 5. Satisfaction vs Attrition
        satisfaction_data = self.data.groupby('job_satisfaction')['attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        axes[1, 1].plot(satisfaction_data.index, satisfaction_data.values, 
                       marker='o', linewidth=3, markersize=8, color='#e74c3c')
        axes[1, 1].set_title('Attrition Rate by Job Satisfaction', fontweight='bold')
        axes[1, 1].set_xlabel('Job Satisfaction Level')
        axes[1, 1].set_ylabel('Attrition Rate (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Salary vs Attrition
        salary_quartiles = pd.qcut(self.data['monthly_income'], 4, 
                                  labels=['Q1 (Low)', 'Q2 (Med-Low)', 'Q3 (Med-High)', 'Q4 (High)'])
        salary_attrition = self.data.groupby(salary_quartiles)['attrition'].apply(
            lambda x: (x == 'Yes').mean() * 100
        )
        
        axes[1, 2].bar(salary_attrition.index.astype(str), salary_attrition.values,
                      color='gold', alpha=0.8)
        axes[1, 2].set_title('Attrition Rate by Salary Quartile', fontweight='bold')
        axes[1, 2].set_ylabel('Attrition Rate (%)')
        axes[1, 2].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Attrition overview dashboard saved to {save_path}")
    
    def create_demographic_analysis_charts(self, save_path='assets/demographic_analysis.png'):
        """Create demographic analysis visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('HR Demographic Analysis\nAuthor: Sahil Hansa (sahilhansa007@gmail.com)', 
                     fontsize=16, fontweight='bold')
        
        # 1. Gender Analysis
        gender_data = self.data.groupby(['gender', 'attrition']).size().unstack()
        gender_pct = gender_data.div(gender_data.sum(axis=1), axis=0) * 100
        
        gender_pct.plot(kind='bar', ax=axes[0, 0], color=['#3498db', '#e74c3c'])
        axes[0, 0].set_title('Attrition by Gender', fontweight='bold')
        axes[0, 0].set_ylabel('Percentage')
        axes[0, 0].legend(['Stayed', 'Left'])
        axes[0, 0].tick_params(axis='x', rotation=0)
        
        # 2. Age Distribution with Attrition
        age_bins = np.arange(20, 70, 5)
        for attrition_status in ['No', 'Yes']:
            subset = self.data[self.data['attrition'] == attrition_status]
            axes[0, 1].hist(subset['age'], bins=age_bins, alpha=0.7, 
                           label=f'Attrition: {attrition_status}',
                           color='green' if attrition_status == 'No' else 'red')
        
        axes[0, 1].set_title('Age Distribution by Attrition Status', fontweight='bold')
        axes[0, 1].set_xlabel('Age')
        axes[0, 1].set_ylabel('Number of Employees')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Department Size and Attrition
        dept_stats = self.data.groupby('department').agg({
            'attrition': lambda x: (x == 'Yes').sum(),
            'employee_id': 'count' if 'employee_id' in self.data.columns else lambda x: len(x)
        })
        
        if 'employee_id' not in dept_stats.columns:
            dept_stats['employee_id'] = self.data.groupby('department').size()
        
        # Create bubble chart
        x = dept_stats['employee_id']
        y = (dept_stats['attrition'] / dept_stats['employee_id'] * 100)
        sizes = dept_stats['employee_id'] * 5  # Scale for bubble size
        
        scatter = axes[1, 0].scatter(x, y, s=sizes, alpha=0.6, c=range(len(x)), cmap='viridis')
        
        # Add department labels
        for i, dept in enumerate(dept_stats.index):
            axes[1, 0].annotate(dept, (x.iloc[i], y.iloc[i]), 
                              xytext=(5, 5), textcoords='offset points', fontsize=10)
        
        axes[1, 0].set_title('Department Size vs Attrition Rate', fontweight='bold')
        axes[1, 0].set_xlabel('Number of Employees')
        axes[1, 0].set_ylabel('Attrition Rate (%)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Satisfaction Heatmap
        satisfaction_pivot = self.data.pivot_table(
            values='attrition', 
            index='job_satisfaction',
            columns='work_life_balance',
            aggfunc=lambda x: (x == 'Yes').mean() * 100
        )
        
        sns.heatmap(satisfaction_pivot, annot=True, fmt='.1f', cmap='RdYlBu_r',
                   ax=axes[1, 1], cbar_kws={'label': 'Attrition Rate (%)'})
        axes[1, 1].set_title('Attrition Heatmap: Job Satisfaction vs Work-Life Balance', 
                           fontweight='bold')
        axes[1, 1].set_xlabel('Work-Life Balance')
        axes[1, 1].set_ylabel('Job Satisfaction')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Demographic analysis charts saved to {save_path}")
    
    def create_performance_correlation_chart(self, save_path='assets/performance_correlation.png'):
        """Create performance and attrition correlation analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Performance vs Attrition Analysis\nSahil Hansa - HR Analytics', 
                     fontsize=16, fontweight='bold')
        
        # 1. Performance Rating Distribution
        perf_attrition = self.data.groupby(['performance_rating', 'attrition']).size().unstack(fill_value=0)
        perf_attrition.plot(kind='bar', ax=axes[0, 0], color=['#2ecc71', '#e74c3c'])
        axes[0, 0].set_title('Performance Rating vs Attrition', fontweight='bold')
        axes[0, 0].set_xlabel('Performance Rating')
        axes[0, 0].set_ylabel('Number of Employees')
        axes[0, 0].legend(['Stayed', 'Left'])
        axes[0, 0].tick_params(axis='x', rotation=0)
        
        # 2. High Performer Attrition
        high_performers = self.data[self.data['performance_rating'] >= 4]
        if len(high_performers) > 0:
            hp_attrition = high_performers.groupby('department')['attrition'].apply(
                lambda x: (x == 'Yes').mean() * 100
            ).sort_values(ascending=False)
            
            bars = axes[0, 1].bar(hp_attrition.index, hp_attrition.values, color='orange')
            axes[0, 1].set_title('High Performer Attrition by Department', fontweight='bold')
            axes[0, 1].set_ylabel('Attrition Rate (%)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Add value labels
            for bar, rate in zip(bars, hp_attrition.values):
                axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                               f'{rate:.1f}%', ha='center', va='bottom')
        
        # 3. Salary vs Performance Scatter
        colors = ['red' if x == 'Yes' else 'blue' for x in self.data['attrition']]
        scatter = axes[1, 0].scatter(self.data['monthly_income'], self.data['performance_rating'],
                                   c=colors, alpha=0.6, s=30)
        
        axes[1, 0].set_title('Salary vs Performance Rating', fontweight='bold')
        axes[1, 0].set_xlabel('Monthly Income')
        axes[1, 0].set_ylabel('Performance Rating')
        
        # Add legend
        import matplotlib.patches as mpatches
        red_patch = mpatches.Patch(color='red', label='Left')
        blue_patch = mpatches.Patch(color='blue', label='Stayed')
        axes[1, 0].legend(handles=[blue_patch, red_patch])
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Overtime Impact
        overtime_impact = self.data.groupby(['overtime', 'attrition']).size().unstack()
        overtime_pct = overtime_impact.div(overtime_impact.sum(axis=1), axis=0) * 100
        
        overtime_pct.plot(kind='bar', ax=axes[1, 1], color=['#3498db', '#e74c3c'])
        axes[1, 1].set_title('Overtime Impact on Attrition', fontweight='bold')
        axes[1, 1].set_ylabel('Percentage')
        axes[1, 1].legend(['Stayed', 'Left'])
        axes[1, 1].tick_params(axis='x', rotation=0)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Performance correlation chart saved to {save_path}")
    
    def create_retention_strategy_dashboard(self, save_path='assets/retention_dashboard.png'):
        """Create strategic retention recommendations dashboard"""
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        fig.suptitle('Employee Retention Strategy Dashboard\nStrategic Insights by Sahil Hansa', 
                     fontsize=16, fontweight='bold')
        
        # 1. Risk Segmentation
        # Create risk score based on multiple factors
        risk_score = (
            (5 - self.data['job_satisfaction']) * 0.3 +
            (5 - self.data['work_life_balance']) * 0.2 +
            (self.data['years_at_company'].apply(lambda x: 2 if 1 <= x <= 3 else 1)) * 0.3 +
            (self.data['performance_rating'].apply(lambda x: 1 if x >= 4 else 0)) * 0.2
        )
        
        risk_categories = pd.cut(risk_score, bins=[0, 1.5, 2.5, 5], 
                               labels=['Low Risk', 'Medium Risk', 'High Risk'])
        
        risk_counts = risk_categories.value_counts()
        colors = ['green', 'orange', 'red']
        wedges, texts, autotexts = axes[0, 0].pie(risk_counts.values, labels=risk_counts.index, 
                                                 autopct='%1.1f%%', colors=colors, startangle=90)
        axes[0, 0].set_title('Employee Risk Segmentation', fontweight='bold')
        
        # 2. Cost of Attrition by Department
        dept_costs = self.data.groupby('department').agg({
            'monthly_income': 'mean',
            'attrition': lambda x: (x == 'Yes').sum()
        })
        dept_costs['annual_cost_impact'] = dept_costs['monthly_income'] * 12 * dept_costs['attrition'] * 1.5
        
        bars = axes[0, 1].bar(dept_costs.index, dept_costs['annual_cost_impact'] / 1000,
                             color='darkred', alpha=0.7)
        axes[0, 1].set_title('Annual Attrition Cost Impact by Department', fontweight='bold')
        axes[0, 1].set_ylabel('Cost Impact (K$)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, cost in zip(bars, dept_costs['annual_cost_impact'] / 1000):
            if cost > 0:
                axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                               f'${cost:.0f}K', ha='center', va='bottom')
        
        # 3. Tenure Sweet Spot Analysis
        tenure_survival = self.data.groupby('years_at_company')['attrition'].apply(
            lambda x: (x == 'No').mean() * 100
        )
        
        axes[0, 2].plot(tenure_survival.index, tenure_survival.values, 
                       marker='o', linewidth=3, markersize=6, color='#2ecc71')
        axes[0, 2].set_title('Employee Retention Rate by Tenure', fontweight='bold')
        axes[0, 2].set_xlabel('Years at Company')
        axes[0, 2].set_ylabel('Retention Rate (%)')
        axes[0, 2].grid(True, alpha=0.3)
        axes[0, 2].axhline(y=80, color='red', linestyle='--', alpha=0.7, label='Target (80%)')
        axes[0, 2].legend()
        
        # 4. Satisfaction Investment ROI
        satisfaction_bins = pd.cut(self.data['job_satisfaction'], bins=[0, 2, 3, 4, 5],
                                 labels=['Poor (1-2)', 'Average (3)', 'Good (4)', 'Excellent (5)'])
        
        satisfaction_metrics = self.data.groupby(satisfaction_bins).agg({
            'attrition': lambda x: (x == 'Yes').mean() * 100,
            'monthly_income': 'mean'
        })
        
        ax1 = axes[1, 0]
        ax2 = ax1.twinx()
        
        bars1 = ax1.bar(satisfaction_metrics.index.astype(str), satisfaction_metrics['attrition'],
                       alpha=0.7, color='red', label='Attrition Rate')
        line1 = ax2.plot(satisfaction_metrics.index.astype(str), satisfaction_metrics['monthly_income'],
                        color='blue', marker='o', linewidth=3, label='Avg Salary')
        
        ax1.set_title('Satisfaction vs Attrition & Compensation', fontweight='bold')
        ax1.set_ylabel('Attrition Rate (%)', color='red')
        ax2.set_ylabel('Average Salary ($)', color='blue')
        ax1.tick_params(axis='x', rotation=45)
        
        # 5. Manager Effectiveness (Simulated)
        if 'manager_id' not in self.data.columns:
            # Simulate manager data
            self.data['manager_id'] = np.random.randint(1, 11, len(self.data))
        
        manager_effectiveness = self.data.groupby('manager_id').agg({
            'attrition': lambda x: (x == 'Yes').mean() * 100,
            'job_satisfaction': 'mean'
        })
        
        scatter = axes[1, 1].scatter(manager_effectiveness['job_satisfaction'], 
                                   manager_effectiveness['attrition'],
                                   s=100, alpha=0.7, c=range(len(manager_effectiveness)), cmap='viridis')
        
        axes[1, 1].set_title('Manager Effectiveness Matrix', fontweight='bold')
        axes[1, 1].set_xlabel('Team Average Job Satisfaction')
        axes[1, 1].set_ylabel('Team Attrition Rate (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add quadrant lines
        axes[1, 1].axhline(y=manager_effectiveness['attrition'].mean(), color='red', linestyle='--', alpha=0.5)
        axes[1, 1].axvline(x=manager_effectiveness['job_satisfaction'].mean(), color='red', linestyle='--', alpha=0.5)
        
        # 6. Intervention Priority Matrix
        dept_priority = self.data.groupby('department').agg({
            'attrition': lambda x: (x == 'Yes').mean() * 100,
            'employee_id': 'count' if 'employee_id' in self.data.columns else lambda x: len(x)
        })
        
        if 'employee_id' not in dept_priority.columns:
            dept_priority['employee_id'] = self.data.groupby('department').size()
        
        # Create priority matrix
        x = dept_priority['attrition']  # Attrition rate
        y = dept_priority['employee_id']  # Department size
        
        scatter = axes[1, 2].scatter(x, y, s=200, alpha=0.7, 
                                   c=x, cmap='RdYlBu_r')
        
        # Add department labels
        for i, dept in enumerate(dept_priority.index):
            axes[1, 2].annotate(dept, (x.iloc[i], y.iloc[i]), 
                              xytext=(5, 5), textcoords='offset points', fontweight='bold')
        
        axes[1, 2].set_title('Intervention Priority Matrix', fontweight='bold')
        axes[1, 2].set_xlabel('Attrition Rate (%)')
        axes[1, 2].set_ylabel('Department Size')
        axes[1, 2].grid(True, alpha=0.3)
        
        # Add quadrant labels
        axes[1, 2].text(0.95, 0.95, 'High Impact\nHigh Priority', 
                       transform=axes[1, 2].transAxes, ha='right', va='top',
                       bbox=dict(boxstyle='round', facecolor='red', alpha=0.3))
        axes[1, 2].text(0.05, 0.05, 'Low Impact\nLow Priority', 
                       transform=axes[1, 2].transAxes, ha='left', va='bottom',
                       bbox=dict(boxstyle='round', facecolor='green', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Retention strategy dashboard saved to {save_path}")
    
    def generate_all_visualizations(self):
        """Generate complete visualization suite"""
        print("="*60)
        print("HR DATA VISUALIZATION SUITE")
        print("="*60)
        print(f"Author: Sahil Hansa")
        print(f"Email: sahilhansa007@gmail.com")
        print(f"Location: Jammu, J&K, India")
        print(f"Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        if self.data is None:
            print("❌ No data available for visualization")
            return False
        
        # Create output directory
        import os
        os.makedirs('assets', exist_ok=True)
        
        print("\n📊 Generating visualization suite...")
        
        # Generate all dashboard types
        try:
            print("1. Creating attrition overview dashboard...")
            self.create_attrition_overview_dashboard()
            
            print("2. Creating demographic analysis charts...")
            self.create_demographic_analysis_charts()
            
            print("3. Creating performance correlation charts...")
            self.create_performance_correlation_chart()
            
            print("4. Creating retention strategy dashboard...")
            self.create_retention_strategy_dashboard()
            
            print("\n✅ All visualizations generated successfully!")
            print("📁 Charts saved to 'assets/' directory")
            print("🎯 Ready for HR strategic decision making")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating visualizations: {str(e)}")
            return False

def main():
    """
    Main execution function for HR data visualization
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    visualizer = HRDataVisualizer()
    success = visualizer.generate_all_visualizations()
    
    if success:
        print("\n🎨 Visualization suite completed!")
        print("📈 Professional HR analytics dashboards ready")
        print("💼 Suitable for executive presentations")
    else:
        print("\n⚠️ Visualization generation incomplete")

if __name__ == "__main__":
    main()