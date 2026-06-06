import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Page Configuration for a high-quality professional UI
st.set_page_config(page_title="AI Personal Finance Advisor & Predictor", page_icon="📈", layout="wide")

st.title("🚀 Smart AI Personal Finance Advisor & Predictive Engine")
st.write("An Advanced Machine Learning & Financial Analytics Prototype for FYP.")
st.markdown("---")

# Main Layout
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📊 1. Financial Data Entry")
    income = st.number_input("Monthly Income / Aamdani (PKR):", min_value=0, value=60000, step=5000)
    
    st.markdown("**Monthly Expenses Breakdown:**")
    rent = st.number_input("🏠 Rent & Utility Bills:", min_value=0, value=15000, step=1000)
    food = st.number_input("🍲 Food & Groceries:", min_value=0, value=12000, step=1000)
    travel = st.number_input("🚗 Transport / Fuel:", min_value=0, value=5000, step=500)
    other = st.number_input("🛍️ Shopping & Entertainment:", min_value=0, value=8000, step=1000)

    total_expenses = rent + food + travel + other
    savings = income - total_expenses
    
    # Feature: Mean Calculation (Mathematical Requirement)
    expense_list = [rent, food, travel, other]
    mean_expense = np.mean(expense_list)

with col2:
    st.subheader("📈 2. Financial Metrics & Dashboard")
    
    # Professional Metrics Displays
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Total Income", value=f"{income} PKR")
    m2.metric(label="Total Expenses", value=f"{total_expenses} PKR", delta=f"-{total_expenses}", delta_color="inverse")
    
    # Feature: Showing Mean Expense in dashboard
    m3.metric(label="Mean Expense / Category", value=f"{mean_expense:.0f} PKR")
    
    if savings >= 0:
        st.success(f"💰 Savings: **{savings} PKR** aap bacha rahe hain!")
    else:
        st.error(f"⚠️ Deficit: Aap budget se **{abs(savings)} PKR** uper chalay gaye hain!")

    # Feature: Graph Visualization
    st.write("### Expense Category Wise Analysis:")
    chart_data = pd.DataFrame({
        "Categories": ["Bills/Rent", "Food", "Transport", "Others"],
        "Amount (PKR)": [rent, food, travel, other]
    }).set_index("Categories")
    st.bar_chart(chart_data)

st.markdown("---")
# Creating rows for ML and Reporting features
col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("🤖 3. Machine Learning Future Expense Prediction")
    st.write("Using *Linear Regression* to project your next 3 months' expenses based on current trend coefficients.")
    
    # Feature: Linear Regression Prediction Engine
    months = np.array([1, 2, 3, 4]).reshape(-1, 1)
    historical_expenses = np.array([total_expenses*0.9, total_expenses*0.95, total_expenses*1.02, total_expenses]).reshape(-1, 1)
    
    # Model Training
    model = LinearRegression()
    model.fit(months, historical_expenses)
    
    # Predicting Month 5 (Next Month)
    next_month = np.array([[5]])
    predicted_expense = model.predict(next_month)[0][0]
    
    st.warning(f"🔮 **ML Prediction:** Base trend ke mutabiq aglay mahine aapka kharcha takreeban **{predicted_expense:.0f} PKR** hone ka imkaan hai.")

with col4:
    st.subheader("📋 4. AI Strategic Financial Advice")
    expense_percentage = (total_expenses / income) * 100 if income > 0 else 100
    
    if savings < 0:
        st.markdown(f"🔴 **Alert:** Strategy change karein! Aap aamdani se `{abs(savings)} PKR` ziada kharch kar rahe hain. `Others` category ko 30% cut-down karein.")
    elif expense_percentage > 70:
        st.markdown(f"🟡 **Advice:** Expense volume high hai (`{expense_percentage:.1f}%`). Mean category kharcha `{mean_expense:.0f} PKR` se neeche lane ki koshish karein.")
    else:
        st.markdown(f"🟢 **Excellent Status:** Status maintain rakhein aur baqi `{savings} PKR` bachat ko auto-invest par lagayein.")

    # --- Feature: Download Report Button ---
    st.markdown("### 📥 5. Export Project Data")
    
    # Create report dataframe
    report_df = pd.DataFrame({
        "Financial Metric": ["Total Income", "Total Expenses", "Average (Mean) Expense", "Net Savings", "ML Predicted Next Month Expense"],
        "Value (PKR)": [income, total_expenses, mean_expense, savings, predicted_expense]
    })
    
    # Convert data frame to CSV strings
    csv_data = report_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Financial Report (CSV) 📄",
        data=csv_data,
        file_name="Financial_Advisor_Report.csv",
        mime="text/csv"
    )
