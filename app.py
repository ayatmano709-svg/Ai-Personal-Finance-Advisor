import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fpdf import FPDF

# Page Configuration
st.set_page_config(page_title="Smart AI Financial Advisor", layout="centered")
st.title("🧠 AI-Driven Financial Advisor & Planner")

# ==========================================
# STEP 1 & 2: Main Input & Side Panel Setup
# ==========================================
st.sidebar.header("💰 Income & Budget Setup")

income = st.sidebar.number_input(
    "Enter Your Monthly Income (PKR)", 
    min_value=1, # 0 se hata kar 1 kiya taake division error na aaye
    value=50000, 
    step=5000
)

# STEP 3: Monthly Planning Feature Input
savings_goal = st.sidebar.number_input(
    "Target Monthly Savings (PKR)",
    min_value=0,
    value=10000,
    step=1000
)

# ==========================================
# Expense Tracking Section
# ==========================================
st.header("📊 Monthly Expenses")

col1, col2 = st.columns(2)
with col1:
    food = st.number_input("Food Expenses (PKR)", min_value=0, value=12000, step=500)
    rent = st.number_input("Rent/Utilities (PKR)", min_value=0, value=15000, step=1000)
with col2:
    transport = st.number_input("Transport (PKR)", min_value=0, value=5000, step=500)
    other = st.number_input("Shopping & Entertainment (PKR)", min_value=0, value=5000, step=500)

total_expenses = food + rent + transport + other
savings = income - total_expenses

# STEP 4: Daily Budget Calculation
daily_budget = (income - savings_goal) / 30

# ==========================================
# STEP 5: Monthly Planning Show
# ==========================================
st.markdown("---")
if savings >= 0:
    st.info(
        f"""
        📅 **Monthly Financial Plan**
        
        * **Income:** {income:,} PKR
        * **Target Savings:** {savings_goal:,} PKR
        * **Recommended Daily Spending Limit:** {daily_budget:,.0f} PKR
        """
    )
else:
    st.error("⚠️ Your expenses exceed your income! Please review your budget.")

# Basic Metrics & Mean Calculation
st.subheader("📈 Financial Overview")
m_col1, m_col2, m_col3 = st.columns(3)
m_col1.metric("Total Expenses", f"{total_expenses:,} PKR")
m_col2.metric("Actual Savings", f"{savings:,} PKR")
m_col3.metric("Average Expense / Category", f"{total_expenses/4:,.0f} PKR")

# Expense Breakdown Chart
categories = ['Food', 'Rent/Utilities', 'Transport', 'Other']
exp_values = [food, rent, transport, other]

fig, ax = plt.subplots(figsize=(6, 4))
ax.pie(exp_values, labels=categories, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
ax.axis('equal')
st.pyplot(fig)


# ==========================================
# STEP 6: Financial Health Score
# ==========================================
st.markdown("---")
st.subheader("❤️ Financial Health Score")

saving_ratio = (max(savings, 0) / income) * 100
health_score = min(100, saving_ratio * 4)

st.progress(int(health_score))
st.write(f"**Score:** {health_score:.0f}/100")


# ==========================================
# STEP 7: Goal Achievement Predictor
# ==========================================
st.subheader("🎯 Goal Achievement Predictor")

goal_amount = st.number_input(
    "Enter Your Financial Goal (e.g., Bike, Laptop, etc.)",
    min_value=1000,
    value=100000,
    step=5000
)

if savings > 0:
    months_needed = goal_amount / savings
    st.success(
        f"🎯 You can achieve your goal in **{months_needed:.1f} months** with your current savings rate."
    )
else:
    months_needed = 0
    st.warning("⚠️ You need positive monthly savings to predict goal achievement.")


# ==========================================
# STEP 8: K-Means Clustering Section
# ==========================================
st.markdown("---")
st.subheader("🧠 User Financial Behaviour Analysis (ML Clustering)")

# Mock dataset representing [Income, Savings] of different user groups
cluster_data = np.array([
    [60000, 15000],
    [70000, 25000],
    [50000, 5000],
    [90000, 30000],
    [40000, 3000],
    [80000, 10000],
    [55000, 8000]
])

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(cluster_data)

# Current user data
user_data = np.array([[income, max(savings, 0)]])
cluster = kmeans.predict(user_data)[0]

cluster_text = ""
if cluster == 0:
    cluster_text = "High Saver Cluster"
    st.success(f"🏆 **Cluster Category:** You belong to the **{cluster_text}**!")
elif cluster == 1:
    cluster_text = "Moderate Saver Cluster"
    st.warning(f"💰 **Cluster Category:** You belong to the **{cluster_text}**.")
else:
    cluster_text = "High Spending Cluster"
    st.error(f"⚠️ **Cluster Category:** You belong to the **{cluster_text}**! Needs attention.")


# ==========================================
# STEP 9: Smart AI Recommendation Engine
# ==========================================
st.subheader("🤖 Smart AI Recommendations")

recommendations = []

if savings < income * 0.20:
    recommendations.append("Warning: Try increasing your savings to at least 20% of your total income.")
if food > income * 0.30:
    recommendations.append("Warning: Your food expenses are relatively high (>30% of income). Consider meal planning.")
if other > income * 0.20:
    recommendations.append("Warning: Shopping and entertainment spending is on the higher side. Try the 50/30/20 rule.")
if savings > income * 0.30:
    recommendations.append("Success: Excellent saving behaviour! Keep it up and consider investing your surplus.")

if len(recommendations) == 0:
    recommendations.append("Your budget looks stable and well-balanced.")

for rec in recommendations:
    st.write(f"- {rec}")


# ==========================================
# STEP 10: PDF Report Generation
# ==========================================
st.markdown("---")
st.subheader("📄 Export Financial Report")

class FinancialPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 51, 102) 
        self.cell(0, 10, "Smart AI Financial Advisor - Report", ln=True, align="C")
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

if st.button("Generate & Download PDF Report"):
    try:
        pdf = FinancialPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)
        
        # 1. Budget & Overview Section
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "1. Budget & Overview", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, f"Total Income: {income:,} PKR", ln=True)
        pdf.cell(0, 8, f"Total Expenses: {total_expenses:,} PKR", ln=True)
        pdf.cell(0, 8, f"Net Savings: {savings:,} PKR", ln=True)
        pdf.cell(0, 8, f"Target Monthly Savings: {savings_goal:,} PKR", ln=True)
        pdf.cell(0, 8, f"Recommended Daily Spending: {daily_budget:,.0f} PKR", ln=True)
        pdf.ln(5)
        
        # 2. Health & Prediction Analysis
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "2. Health & Prediction Analysis", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, f"Financial Health Score: {health_score:.0f}/100", ln=True)
        if savings > 0:
            pdf.cell(0, 8, f"Goal Achievement ({goal_amount:,} PKR): Achievable in {months_needed:.1f} months", ln=True)
        else:
            pdf.cell(0, 8, "Goal Achievement: Needs positive savings rate.", ln=True)
        pdf.ln(5)
        
        # 3. ML Behavior Analysis
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "3. ML Behavior Analysis", ln=True)
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, f"User Category: {cluster_text}", ln=True)
        pdf.ln(5)
        
        # 4. AI Recommendations Section
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "4. Smart AI Recommendations", ln=True)
        pdf.set_font("Helvetica", size=12)
        
        for rec in recommendations:
            pdf.multi_cell(0, 8, f"- {rec}")
                
        # Output PDF as safe byte stream
        pdf_bytes = pdf.output()
        
        st.download_button(
            label="📥 Click Here to Download PDF",
            data=bytes(pdf_bytes),
            file_name="Financial_Advisor_Report.pdf",
            mime="application/pdf"
        )
        st.success("🎉 PDF generated successfully! Click the button above to save it.")
        
    except Exception as e:
        st.error(f"Failed to generate PDF. Error details: {e}")
