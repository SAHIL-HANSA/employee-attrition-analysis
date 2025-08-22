"""
Data Preprocessing for Employee Attrition Analysis
Author: Sahil Hansa
Email: sahilhansa007@gmail.com
Description: Comprehensive data cleaning and preparation pipeline for HR analytics
Location: Jammu, J&K, India
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class HRDataPreprocessor:
    """
    HR Data Preprocessing and Cleaning Pipeline
    
    Handles data validation, cleaning, feature engineering, and preparation
    for employee attrition analysis
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    
    def __init__(self):
        self.employee_data = None
        self.performance_data = None
        self.exit_survey_data = None
        self.processed_data = None
        self.data_quality_report = {}
        
    def load_raw_data(self, employee_file='data/sample/employee_data.csv',
                     performance_file='data/sample/performance_data.csv',
                     exit_survey_file='data/sample/exit_survey_data.csv'):
        """Load raw HR datasets"""
        try:
            logging.info("Loading raw HR datasets...")
            
            self.employee_data = pd.read_csv(employee_file)
            self.performance_data = pd.read_csv(performance_file)
            self.exit_survey_data = pd.read_csv(exit_survey_file)
            
            logging.info(f"Loaded employee data: {len(self.employee_data)} records")
            logging.info(f"Loaded performance data: {len(self.performance_data)} records")
            logging.info(f"Loaded exit survey data: {len(self.exit_survey_data)} records")
            
            return True
        except Exception as e:
            logging.error(f"Error loading data: {str(e)}")
            return False
    
    def validate_data_quality(self):
        """Comprehensive data quality assessment"""
        logging.info("Performing data quality validation...")
        
        quality_report = {}
        
        # Employee data validation
        if self.employee_data is not None:
            emp_quality = {
                'total_records': len(self.employee_data),
                'duplicate_employees': self.employee_data['employee_id'].duplicated().sum(),
                'missing_values': self.employee_data.isnull().sum().to_dict(),
                'invalid_ages': len(self.employee_data[
                    (self.employee_data['age'] < 18) | (self.employee_data['age'] > 70)
                ]),
                'invalid_salaries': len(self.employee_data[
                    (self.employee_data['monthly_income'] < 1000) | 
                    (self.employee_data['monthly_income'] > 20000)
                ]),
                'invalid_tenure': len(self.employee_data[
                    (self.employee_data['years_at_company'] < 0) | 
                    (self.employee_data['years_at_company'] > 50)
                ]),
                'invalid_ratings': len(self.employee_data[
                    (self.employee_data['performance_rating'] < 1) | 
                    (self.employee_data['performance_rating'] > 5)
                ])
            }
            quality_report['employee_data'] = emp_quality
        
        # Performance data validation
        if self.performance_data is not None:
            perf_quality = {
                'total_records': len(self.performance_data),
                'missing_values': self.performance_data.isnull().sum().to_dict(),
                'invalid_ratings': len(self.performance_data[
                    (self.performance_data['performance_rating'] < 1) | 
                    (self.performance_data['performance_rating'] > 5)
                ]),
                'invalid_goals': len(self.performance_data[
                    (self.performance_data['goals_met'] < 0) | 
                    (self.performance_data['goals_met'] > 100)
                ])
            }
            quality_report['performance_data'] = perf_quality
        
        # Exit survey validation
        if self.exit_survey_data is not None:
            exit_quality = {
                'total_records': len(self.exit_survey_data),
                'missing_values': self.exit_survey_data.isnull().sum().to_dict(),
                'invalid_ratings': len(self.exit_survey_data[
                    (self.exit_survey_data['overall_satisfaction'] < 1) | 
                    (self.exit_survey_data['overall_satisfaction'] > 5)
                ])
            }
            quality_report['exit_survey_data'] = exit_quality
        
        self.data_quality_report = quality_report
        
        # Log quality issues
        for dataset, issues in quality_report.items():
            logging.info(f"\n{dataset.upper()} Quality Report:")
            for metric, value in issues.items():
                if isinstance(value, dict):
                    total_missing = sum(value.values())
                    logging.info(f"  Total missing values: {total_missing}")
                else:
                    logging.info(f"  {metric}: {value}")
        
        return quality_report
    
    def clean_employee_data(self):
        """Clean and standardize employee data"""
        if self.employee_data is None:
            return None
        
        logging.info("Cleaning employee data...")
        
        df = self.employee_data.copy()
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['employee_id'])
        if len(df) < initial_count:
            logging.info(f"Removed {initial_count - len(df)} duplicate employee records")
        
        # Clean and standardize text fields
        text_columns = ['first_name', 'last_name', 'department', 'job_role', 'gender', 
                       'education_level', 'marital_status', 'attrition', 'exit_reason']
        
        for col in text_columns:
            if col in df.columns:
                # Standardize text case and remove extra whitespace
                df[col] = df[col].astype(str).str.strip().str.title()
                
                # Specific standardizations
                if col == 'gender':
                    df[col] = df[col].str.upper()
                elif col == 'attrition':
                    df[col] = df[col].str.capitalize()
                elif col == 'department':
                    # Standardize department names
                    dept_mapping = {
                        'It': 'IT',
                        'Hr': 'HR', 
                        'R&D': 'R&D',
                        'Research & Development': 'R&D'
                    }
                    df[col] = df[col].replace(dept_mapping)
        
        # Validate and clean numeric fields
        numeric_validations = {
            'age': (18, 70),
            'monthly_income': (1000, 20000),
            'years_at_company': (0, 50),
            'performance_rating': (1, 5),
            'job_satisfaction': (1, 5),
            'work_life_balance': (1, 5),
            'distance_from_home': (0, 100)
        }
        
        for col, (min_val, max_val) in numeric_validations.items():
            if col in df.columns:
                # Flag outliers
                outliers = (df[col] < min_val) | (df[col] > max_val)
                if outliers.sum() > 0:
                    logging.warning(f"Found {outliers.sum()} outliers in {col}")
                    # Cap outliers at reasonable bounds
                    df.loc[df[col] < min_val, col] = min_val
                    df.loc[df[col] > max_val, col] = max_val
        
        # Handle date fields
        if 'attrition_date' in df.columns:
            df['attrition_date'] = pd.to_datetime(df['attrition_date'], errors='coerce')
        
        # Fill missing values with appropriate defaults
        fill_values = {
            'job_satisfaction': df['job_satisfaction'].median(),
            'work_life_balance': df['work_life_balance'].median(),
            'performance_rating': df['performance_rating'].median(),
            'distance_from_home': df['distance_from_home'].median()
        }
        
        for col, fill_val in fill_values.items():
            if col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    df[col] = df[col].fillna(fill_val)
                    logging.info(f"Filled {missing_count} missing values in {col} with {fill_val}")
        
        self.employee_data = df
        logging.info("Employee data cleaning completed")
        return df
    
    def clean_performance_data(self):
        """Clean and standardize performance data"""
        if self.performance_data is None:
            return None
        
        logging.info("Cleaning performance data...")
        
        df = self.performance_data.copy()
        
        # Convert date column
        if 'review_date' in df.columns:
            df['review_date'] = pd.to_datetime(df['review_date'], errors='coerce')
        
        # Validate numeric ratings
        rating_columns = ['performance_rating', 'competency_score', 'leadership_score', 
                         'teamwork_score', 'innovation_score', 'manager_rating', 
                         'peer_feedback_score', 'self_assessment_score']
        
        for col in rating_columns:
            if col in df.columns:
                # Ensure ratings are within 1-5 range
                df[col] = df[col].clip(1, 5)
        
        # Clean goals_met percentage
        if 'goals_met' in df.columns:
            df['goals_met'] = df['goals_met'].clip(0, 100)
        
        # Clean text fields
        text_columns = ['improvement_areas', 'strengths', 'promotion_ready']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # Handle promotion readiness
        if 'promotion_ready' in df.columns:
            df['promotion_ready'] = df['promotion_ready'].str.capitalize()
            df['promotion_ready'] = df['promotion_ready'].map({'Yes': True, 'No': False})
        
        self.performance_data = df
        logging.info("Performance data cleaning completed")
        return df
    
    def clean_exit_survey_data(self):
        """Clean and standardize exit survey data"""
        if self.exit_survey_data is None:
            return None
        
        logging.info("Cleaning exit survey data...")
        
        df = self.exit_survey_data.copy()
        
        # Convert date column
        if 'exit_date' in df.columns:
            df['exit_date'] = pd.to_datetime(df['exit_date'], errors='coerce')
        
        # Validate rating columns (1-5 scale)
        rating_columns = ['would_recommend_company', 'overall_satisfaction', 
                         'manager_satisfaction', 'compensation_satisfaction',
                         'growth_opportunities', 'work_life_balance_rating',
                         'job_role_clarity', 'training_adequacy', 
                         'company_culture_rating', 'likelihood_to_return']
        
        for col in rating_columns:
            if col in df.columns:
                df[col] = df[col].clip(1, 5)
        
        # Clean text fields
        text_columns = ['exit_reason_primary', 'exit_reason_secondary', 'feedback_comments']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        self.exit_survey_data = df
        logging.info("Exit survey data cleaning completed")
        return df
    
    def engineer_features(self):
        """Create derived features for analysis"""
        if self.employee_data is None:
            return None
        
        logging.info("Engineering features for analysis...")
        
        df = self.employee_data.copy()
        
        # Age-based features
        df['age_group'] = pd.cut(df['age'], 
                               bins=[0, 25, 30, 35, 40, 50, 100],
                               labels=['Under_25', '25_29', '30_34', '35_39', '40_49', 'Over_50'])
        
        # Tenure-based features
        df['tenure_group'] = pd.cut(df['years_at_company'],
                                  bins=[0, 1, 3, 5, 10, 100],
                                  labels=['New_0_1', 'Early_1_3', 'Mid_3_5', 'Senior_5_10', 'Veteran_10plus'])
        
        # Salary-based features
        df['salary_quartile'] = pd.qcut(df['monthly_income'], 4, labels=['Q1_Low', 'Q2_Medium', 'Q3_High', 'Q4_Top'])
        
        # Commute-based features
        df['commute_category'] = pd.cut(df['distance_from_home'],
                                      bins=[0, 10, 20, 30, 100],
                                      labels=['Close', 'Moderate', 'Far', 'Very_Far'])
        
        # Performance categories
        if 'performance_rating' in df.columns:
            df['performance_category'] = df['performance_rating'].map({
                1: 'Poor', 2: 'Below_Average', 3: 'Average', 4: 'Good', 5: 'Excellent'
            })
        
        # Satisfaction risk score
        df['satisfaction_risk_score'] = (
            (5 - df['job_satisfaction']) * 2 +
            (5 - df['work_life_balance']) * 1.5
        )
        
        # Overall engagement score
        df['engagement_score'] = (
            df['job_satisfaction'] * 0.4 +
            df['work_life_balance'] * 0.3 +
            df['performance_rating'] * 0.3
        )
        
        # Attrition risk flags
        df['high_risk_employee'] = (
            (df['job_satisfaction'] <= 2) |
            (df['work_life_balance'] <= 2) |
            (df['years_at_company'].between(1, 3)) |
            (df['performance_rating'] >= 4)  # High performers at risk
        )
        
        # Career progression indicators
        df['leadership_role'] = df['job_role'].str.contains(
            'Manager|Lead|Director|Senior', case=False, na=False
        )
        
        # Overtime impact
        if 'overtime' in df.columns:
            df['overtime_binary'] = df['overtime'].map({'Yes': 1, 'No': 0})
        
        # Generate employee tenure at exit (for departed employees)
        if 'attrition_date' in df.columns:
            df['tenure_at_exit'] = df.apply(
                lambda row: row['years_at_company'] if row['attrition'] == 'Yes' else None, 
                axis=1
            )
        
        self.employee_data = df
        logging.info("Feature engineering completed")
        return df
    
    def merge_datasets(self):
        """Merge all datasets into a comprehensive analysis dataset"""
        logging.info("Merging datasets for comprehensive analysis...")
        
        if self.employee_data is None:
            logging.error("Employee data not available for merging")
            return None
        
        # Start with employee data as base
        merged_df = self.employee_data.copy()
        
        # Merge with performance data
        if self.performance_data is not None:
            perf_cols = ['employee_id', 'performance_rating', 'goals_met', 'competency_score',
                        'leadership_score', 'teamwork_score', 'innovation_score', 
                        'promotion_ready', 'strengths', 'improvement_areas']
            
            # Select available columns
            available_perf_cols = [col for col in perf_cols if col in self.performance_data.columns]
            
            merged_df = merged_df.merge(
                self.performance_data[available_perf_cols],
                on='employee_id',
                how='left',
                suffixes=('', '_perf')
            )
            logging.info(f"Merged performance data: {len(available_perf_cols)} columns")
        
        # Add exit survey insights for departed employees
        if self.exit_survey_data is not None:
            exit_cols = ['employee_id', 'exit_reason_primary', 'overall_satisfaction', 
                        'compensation_satisfaction', 'growth_opportunities', 
                        'work_life_balance_rating', 'would_recommend_company']
            
            # Select available columns
            available_exit_cols = [col for col in exit_cols if col in self.exit_survey_data.columns]
            
            merged_df = merged_df.merge(
                self.exit_survey_data[available_exit_cols],
                on='employee_id',
                how='left',
                suffixes=('', '_exit')
            )
            logging.info(f"Merged exit survey data: {len(available_exit_cols)} columns")
        
        self.processed_data = merged_df
        logging.info(f"Dataset merging completed. Final dataset: {len(merged_df)} rows, {len(merged_df.columns)} columns")
        
        return merged_df
    
    def generate_data_summary(self):
        """Generate comprehensive data summary statistics"""
        if self.processed_data is None:
            logging.warning("No processed data available for summary")
            return None
        
        logging.info("Generating data summary statistics...")
        
        df = self.processed_data
        
        summary_stats = {
            'dataset_overview': {
                'total_employees': len(df),
                'total_columns': len(df.columns),
                'departed_employees': len(df[df['attrition'] == 'Yes']),
                'current_employees': len(df[df['attrition'] == 'No']),
                'overall_attrition_rate': round(len(df[df['attrition'] == 'Yes']) / len(df) * 100, 2)
            },
            'demographic_summary': {
                'avg_age': round(df['age'].mean(), 1),
                'age_range': f"{df['age'].min()} - {df['age'].max()}",
                'gender_distribution': df['gender'].value_counts().to_dict(),
                'department_distribution': df['department'].value_counts().to_dict(),
                'education_distribution': df['education_level'].value_counts().to_dict()
            },
            'compensation_summary': {
                'avg_monthly_income': round(df['monthly_income'].mean(), 0),
                'median_monthly_income': round(df['monthly_income'].median(), 0),
                'salary_range': f"${df['monthly_income'].min():,.0f} - ${df['monthly_income'].max():,.0f}",
                'salary_std': round(df['monthly_income'].std(), 0)
            },
            'performance_summary': {
                'avg_performance_rating': round(df['performance_rating'].mean(), 2),
                'avg_job_satisfaction': round(df['job_satisfaction'].mean(), 2),
                'avg_work_life_balance': round(df['work_life_balance'].mean(), 2),
                'high_performers_count': len(df[df['performance_rating'] >= 4])
            },
            'tenure_summary': {
                'avg_years_at_company': round(df['years_at_company'].mean(), 1),
                'median_tenure': round(df['years_at_company'].median(), 1),
                'tenure_range': f"{df['years_at_company'].min()} - {df['years_at_company'].max()} years"
            }
        }
        
        # Print summary
        print("\n" + "="*60)
        print("HR DATA PREPROCESSING SUMMARY")
        print("="*60)
        print(f"Author: Sahil Hansa (sahilhansa007@gmail.com)")
        print(f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        for category, stats in summary_stats.items():
            print(f"\n{category.upper().replace('_', ' ')}:")
            for metric, value in stats.items():
                print(f"  {metric.replace('_', ' ').title()}: {value}")
        
        return summary_stats
    
    def save_processed_data(self, output_dir='data/processed/'):
        """Save cleaned and processed datasets"""
        if self.processed_data is None:
            logging.error("No processed data to save")
            return False
        
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Save main processed dataset
            output_file = os.path.join(output_dir, 'attrition_analysis_clean.csv')
            self.processed_data.to_csv(output_file, index=False)
            logging.info(f"Saved processed dataset to {output_file}")
            
            # Save individual cleaned datasets
            if self.employee_data is not None:
                emp_file = os.path.join(output_dir, 'employee_data_clean.csv')
                self.employee_data.to_csv(emp_file, index=False)
                logging.info(f"Saved cleaned employee data to {emp_file}")
            
            if self.performance_data is not None:
                perf_file = os.path.join(output_dir, 'performance_data_clean.csv')
                self.performance_data.to_csv(perf_file, index=False)
                logging.info(f"Saved cleaned performance data to {perf_file}")
            
            if self.exit_survey_data is not None:
                exit_file = os.path.join(output_dir, 'exit_survey_data_clean.csv')
                self.exit_survey_data.to_csv(exit_file, index=False)
                logging.info(f"Saved cleaned exit survey data to {exit_file}")
            
            # Save data quality report
            import json
            quality_file = os.path.join(output_dir, 'data_quality_report.json')
            with open(quality_file, 'w') as f:
                json.dump(self.data_quality_report, f, indent=2, default=str)
            logging.info(f"Saved data quality report to {quality_file}")
            
            return True
            
        except Exception as e:
            logging.error(f"Error saving processed data: {str(e)}")
            return False
    
    def run_full_preprocessing_pipeline(self):
        """Execute the complete data preprocessing pipeline"""
        print("="*60)
        print("HR DATA PREPROCESSING PIPELINE")
        print("="*60)
        print(f"Author: Sahil Hansa")
        print(f"Email: sahilhansa007@gmail.com")
        print(f"Location: Jammu, J&K, India")
        print("="*60)
        
        # Step 1: Load data
        if not self.load_raw_data():
            logging.error("Failed to load raw data. Pipeline terminated.")
            return False
        
        # Step 2: Validate data quality
        self.validate_data_quality()
        
        # Step 3: Clean individual datasets
        self.clean_employee_data()
        self.clean_performance_data()
        self.clean_exit_survey_data()
        
        # Step 4: Engineer features
        self.engineer_features()
        
        # Step 5: Merge datasets
        self.merge_datasets()
        
        # Step 6: Generate summary
        self.generate_data_summary()
        
        # Step 7: Save processed data
        self.save_processed_data()
        
        print("\n" + "="*60)
        print("DATA PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        return True

def main():
    """
    Main execution function for HR data preprocessing
    
    Author: Sahil Hansa
    Contact: sahilhansa007@gmail.com
    """
    preprocessor = HRDataPreprocessor()
    success = preprocessor.run_full_preprocessing_pipeline()
    
    if success:
        print("\n✅ Preprocessing completed successfully!")
        print("📁 Cleaned data saved to 'data/processed/' directory")
        print("📊 Ready for analysis and visualization")
    else:
        print("\n❌ Preprocessing failed. Check logs for details.")

if __name__ == "__main__":
    main()