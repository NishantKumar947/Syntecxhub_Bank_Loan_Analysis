import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_advanced_analytics():
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, '..', 'data', 'cleaned_loan_data.csv')
    report_dir = os.path.join(base_dir, '..', 'dashboard')
    os.makedirs(report_dir, exist_ok=True)
    
    if not os.path.exists(data_path):
        print("❌ Error: Cleaned data file nahi mili! Pehle data_cleaning.py chalayein.")
        return
        
    print("📊 Python Advanced Analytics aur Insights generation shuru ho raha hai...")
    df = pd.read_csv(data_path)
    df['issue_date'] = pd.to_datetime(df['issue_date'])
    
    # 1. State-wise (Region) Trend Analysis
    state_analysis = df.groupby('state').agg(
        Total_Applications=('loan_id', 'count'),
        Total_Funded=('funded_amount', 'sum'),
        Bad_Loan_Count=('loan_category', lambda x: (x == 'Bad Loan').sum())
    ).reset_index()
    state_analysis['Bad_Loan_Rate (%)'] = round((state_analysis['Bad_Loan_Count'] / state_analysis['Total_Applications']) * 100, 2)
    top_state = state_analysis.sort_values(by='Total_Applications', ascending=False).iloc[0]
    
    # 2. Risk Factor Analysis (Grade vs Loan Category)
    grade_risk = pd.crosstab(df['grade'], df['loan_category'], normalize='index') * 100
    
    # 3. Chart 1: Grade wise Bad Loan Risk Visualization
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='grade', hue='loan_category', palette='Set2', order=sorted(df['grade'].unique()))
    plt.title('Loan Category Distribution by Grade (Risk Analysis)')
    plt.xlabel('Loan Grade (A=Highest Quality, F=High Risk)')
    plt.ylabel('Number of Applications')
    chart1_path = os.path.join(report_dir, 'grade_risk_analysis.png')
    plt.savefig(chart1_path)
    plt.close()
    
    # 4. Automated Insights Text Report Generation
    report_path = os.path.join(report_dir, 'python_insights_report.txt')
    with open(report_path, 'w') as f:
        f.write("==================================================\n")
        f.write("      BANK LOAN ANALYSIS - AUTOMATED INSIGHTS     \n")
        f.write("==================================================\n\n")
        f.write(f"1. REGIONAL HIGHLIGHTS:\n")
        f.write(f"   - Sabse zyada loan applications {top_state['state']} state se aaye hain ({top_state['Total_Applications']:,} apps).\n")
        f.write(f"   - {top_state['state']} me total funded amount ${top_state['Total_Funded']:,.2f} raha.\n\n")
        f.write(f"2. RISK & REPAYMENT FACTORS:\n")
        for g in sorted(df['grade'].unique()):
            bad_rate = grade_risk.loc[g, 'Bad_Loan_Rate'] if 'Bad_Loan_Rate' in grade_risk.columns else grade_risk.loc[g, 'Bad Loan']
            f.write(f"   - Grade {g} Loans ka Default (Bad Loan) Rate: {bad_rate:.2f}%\n")
        f.write("\n3. CONCLUSION FOR MANAGEMENT:\n")
        f.write("   - Lower grades (E, F) me interest rates high hain par default risk bhi zyada hai.\n")
        f.write("   - Risk mitigation ke liye E aur F grade ke loan approvals par strict guidelines chahiye.\n")

    print("✅ Python Analysis Complete!")
    print(f"📍 Chart saved at: {os.path.abspath(chart1_path)}")
    print(f"📍 Insights Report saved at: {os.path.abspath(report_path)}")

if __name__ == "__main__":
    run_advanced_analytics()