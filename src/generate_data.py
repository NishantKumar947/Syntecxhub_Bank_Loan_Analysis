import os
import random
import pandas as pd
from datetime import datetime, timedelta
from faker import Faker

def generate_bank_loan_dataset(records=30000):
    fake = Faker('en_US')
    random.seed(42) # Consistent data ke liye
    
    print(f"⚙️ {records} Unique aur Realistic Bank Loan records generate ho rahe hain...")
    
    data = []
    
    purposes = ['Debt Consolidation', 'Credit Card Reinvestment', 'Home Improvement', 'Major Purchase', 'Small Business', 'Car Loan']
    home_ownerships = ['RENT', 'MORTGAGE', 'OWN']
    verification_statuses = ['Verified', 'Source Verified', 'Not Verified']
    grades = ['A', 'B', 'C', 'D', 'E', 'F']
    loan_statuses = ['Fully Paid', 'Current', 'Charged Off'] 
    states = ['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(records):
        loan_id = f"LN{100000 + i}"
        customer_name = fake.name()
        state = random.choice(states)
        
        emp_length = random.choice(['< 1 year', '1 year', '3 years', '5 years', '10+ years'])
        annual_income = round(random.uniform(30000, 150000), -2)
        
        funded_amount = round(random.uniform(5000, 35000), -2)
        term = random.choice(['36 months', '60 months'])
        
        grade = random.choice(grades)
        if grade in ['A', 'B']:
            int_rate = round(random.uniform(5.5, 11.5), 2)
            loan_status = random.choices(loan_statuses, weights=[0.85, 0.10, 0.05])[0]
        elif grade in ['C', 'D']:
            int_rate = round(random.uniform(11.6, 18.5), 2)
            loan_status = random.choices(loan_statuses, weights=[0.70, 0.15, 0.15])[0]
        else:
            int_rate = round(random.uniform(18.6, 28.0), 2)
            loan_status = random.choices(loan_statuses, weights=[0.50, 0.20, 0.30])[0]
            
        purpose = random.choice(purposes)
        home_ownership = random.choice(home_ownerships)
        verification_status = random.choice(verification_statuses)
        
        issue_date = start_date + timedelta(days=random.randint(0, 1000))
        issue_date_str = issue_date.strftime('%Y-%m-%d')
        
        # FIX: Variable ka naam sirf 'dti' rakha hai ab
        dti = round(random.uniform(5.0, 35.0), 2)
        
        if loan_status == 'Fully Paid':
            total_payment = round(funded_amount * (1 + (int_rate/100) * (int(term.split()[0])/12) * 0.7), 2)
        elif loan_status == 'Current':
            total_payment = round(funded_amount * random.uniform(0.3, 0.7), 2)
        else: 
            total_payment = round(funded_amount * random.uniform(0.05, 0.4), 2)
            
        if random.random() < 0.02: 
            emp_length = None
            
        data.append({
            'loan_id': loan_id,
            'customer_name': customer_name,
            'emp_length': emp_length,
            'annual_income': annual_income,
            'home_ownership': home_ownership,
            'verification_status': verification_status,
            'issue_date': issue_date_str,
            'purpose': purpose,
            'grade': grade,
            'int_rate': int_rate,
            'term': term,
            'funded_amount': funded_amount,
            'total_payment': total_payment,
            'loan_status': loan_status,
            'dti': dti,
            'state': state
        })
        
    df = pd.DataFrame(data)
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    output_path = os.path.join(data_dir, 'raw_loan_data.csv')
    
    df.to_csv(output_path, index=False)
    print(f"✅ Unique Raw Dataset successfully generate ho gaya hai!")
    print(f"📍 File Path: {os.path.abspath(output_path)}")
    print(f"📊 Total Rows: {df.shape[0]}, Total Columns: {df.shape[1]}")

if __name__ == "__main__":
    generate_bank_loan_dataset(30000)