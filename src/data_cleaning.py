import os
import pandas as pd

def clean_and_process_data():
    # Paths define kar rahe hain
    base_dir = os.path.dirname(__file__)
    input_path = os.path.join(base_dir, '..', 'data', 'raw_loan_data.csv')
    output_path = os.path.join(base_dir, '..', 'data', 'cleaned_loan_data.csv')
    
    if not os.path.exists(input_path):
        print("❌ Error: Raw data file nahi mili! Pehle generate_data.py chalayein.")
        return
        
    print("🧹 Data Cleaning aur Processing shuru ho rahi hai...")
    
    # Data load karna
    df = pd.read_csv(input_path)
    
    # 1. Missing Values Handle karna
    # Jo emplyment length missing hai use 'Unknown' se fill karenge
    df['emp_length'] = df['emp_length'].fillna('Unknown')
    
    # 2. Date Column ko proper DateTime format me convert karna
    df['issue_date'] = pd.to_datetime(df['issue_date'])
    
    # 3. Good vs Bad Loan Classification (Requirement - Classify loans into good vs bad loans)
    # Fully Paid aur Current = Good Loan
    # Charged Off = Bad Loan
    def classify_loan(status):
        if status in ['Fully Paid', 'Current']:
            return 'Good Loan'
        else:
            return 'Bad Loan'
            
    df['loan_category'] = df['loan_status'].apply(classify_loan)
    
    # 4. Kuch Basic KPIs Python me hi verify kar lena (Verification purpose)
    total_apps = len(df)
    total_funded = df['funded_amount'].sum()
    total_received = df['total_payment'].sum()
    
    print("\n--- 📊 Python Verification KPIs ---")
    print(f"🔹 Total Applications: {total_apps:,}")
    print(f"🔹 Total Funded Amount: ${total_funded:,.2f}")
    print(f"🔹 Total Received Amount: ${total_received:,.2f}")
    print(f"🔹 Good Loans Count: {len(df[df['loan_category'] == 'Good Loan']):,}")
    print(f"🔹 Bad Loans Count: {len(df[df['loan_category'] == 'Bad Loan']):,}")
    print("-----------------------------------\n")
    
    # Cleaned data ko save karna
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned dataset successfully save ho gaya hai!")
    print(f"📍 Cleaned File Path: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    clean_and_process_data()