import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="CLM & SDIV Calculator",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("CLM & SDIV Monthly Income Calculator")
st.markdown("""
This app helps you calculate and visualize the monthly income from CLM and SDIV investments.
Enter your investment details below to see projected monthly income.
""")

# Create two columns for CLM and SDIV inputs
col1, col2 = st.columns(2)

# CLM Inputs
with col1:
    st.subheader("CLM Investment Details")
    clm_investment = st.number_input("Total CLM Investment ($)", min_value=0.0, value=10000.0, step=1000.0, key="clm_investment")
    clm_price = st.number_input("CLM Share Price ($)", min_value=0.01, value=7.95, step=0.01, key="clm_price")
    clm_dividend = st.number_input("CLM Monthly Dividend per Share ($)", min_value=0.0, value=0.1257, step=0.0001, key="clm_dividend")
    
    # Calculate CLM values
    clm_shares = clm_investment / clm_price if clm_price > 0 else 0
    clm_monthly_income = clm_shares * clm_dividend
    clm_annual_income = clm_monthly_income * 12
    clm_yield = (clm_annual_income / clm_investment) * 100 if clm_investment > 0 else 0

    # Display CLM results
    st.metric("Number of CLM Shares", f"{clm_shares:.2f}")
    st.metric("Monthly Income from CLM", f"${clm_monthly_income:.2f}")
    st.metric("Annual Income from CLM", f"${clm_annual_income:.2f}")
    st.metric("CLM Yield", f"{clm_yield:.2f}%")

# SDIV Inputs
with col2:
    st.subheader("SDIV Investment Details")
    sdiv_investment = st.number_input("Total SDIV Investment ($)", min_value=0.0, value=10000.0, step=1000.0, key="sdiv_investment")
    sdiv_price = st.number_input("SDIV Share Price ($)", min_value=0.01, value=23.27, step=0.01, key="sdiv_price")
    sdiv_dividend = st.number_input("SDIV Monthly Dividend per Share ($)", min_value=0.0, value=0.1292, step=0.0001, key="sdiv_dividend")
    
    # Calculate SDIV values
    sdiv_shares = sdiv_investment / sdiv_price if sdiv_price > 0 else 0
    sdiv_monthly_income = sdiv_shares * sdiv_dividend
    sdiv_annual_income = sdiv_monthly_income * 12
    sdiv_yield = (sdiv_annual_income / sdiv_investment) * 100 if sdiv_investment > 0 else 0

    # Display SDIV results
    st.metric("Number of SDIV Shares", f"{sdiv_shares:.2f}")
    st.metric("Monthly Income from SDIV", f"${sdiv_monthly_income:.2f}")
    st.metric("Annual Income from SDIV", f"${sdiv_annual_income:.2f}")
    st.metric("SDIV Yield", f"{sdiv_yield:.2f}%")

# Combined results
st.subheader("Combined Investment Summary")
total_investment = clm_investment + sdiv_investment
total_monthly_income = clm_monthly_income + sdiv_monthly_income
total_annual_income = clm_annual_income + sdiv_annual_income
total_yield = (total_annual_income / total_investment) * 100 if total_investment > 0 else 0

# Display combined metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Investment", f"${total_investment:.2f}")
with col2:
    st.metric("Total Monthly Income", f"${total_monthly_income:.2f}")
with col3:
    st.metric("Total Annual Income", f"${total_annual_income:.2f}")
with col4:
    st.metric("Average Yield", f"{total_yield:.2f}%")

# Monthly income projection
st.subheader("Monthly Income Projection (12 Months)")

# Create monthly projection data
months = [f"Month {i+1}" for i in range(12)]
clm_income = [clm_monthly_income] * 12
sdiv_income = [sdiv_monthly_income] * 12

# Create DataFrame for visualization
projection_df = pd.DataFrame({
    'Month': months,
    'CLM': clm_income,
    'SDIV': sdiv_income
})

# Calculate cumulative income
projection_df['Cumulative'] = (projection_df['CLM'] + projection_df['SDIV']).cumsum()

# Melt the DataFrame for easier plotting
plot_df = pd.melt(projection_df, id_vars=['Month'], value_vars=['CLM', 'SDIV'], 
                  var_name='Investment', value_name='Monthly Income')

# Create two tabs for different visualizations
tab1, tab2 = st.tabs(["Monthly Breakdown", "Cumulative Income"])

with tab1:
    # Create a bar chart for monthly income
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Month', y='Monthly Income', hue='Investment', data=plot_df, ax=ax)
    ax.set_title('Monthly Income Breakdown')
    ax.set_ylabel('Income ($)')
    ax.set_xlabel('Month')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Display monthly breakdown table
    st.dataframe(projection_df[['Month', 'CLM', 'SDIV', 'Cumulative']])

with tab2:
    # Create a line chart for cumulative income
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(months, projection_df['Cumulative'], marker='o', linewidth=2, markersize=8)
    ax.set_title('Cumulative Income Over 12 Months')
    ax.set_ylabel('Cumulative Income ($)')
    ax.set_xlabel('Month')
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

# Add some educational information
st.subheader("About CLM and SDIV")
st.info("""
**CLM (Cornerstone Strategic Value Fund)** is a closed-end fund that primarily invests in equity securities of U.S. and non-U.S. companies. It typically pays monthly dividends.

**SDIV (Global X SuperDividend ETF)** is an exchange-traded fund that invests in 100 of the highest dividend-yielding equity securities in the world. It also typically pays monthly dividends.

*Note: Dividend amounts may vary over time. This calculator assumes constant dividend payments for simplicity.*
""")

# Disclaimer
st.caption("""
Disclaimer: This calculator is for informational purposes only and should not be considered financial advice.
Past performance is not indicative of future results. Dividend rates may change over time.
Always conduct your own research or consult with a financial advisor before making investment decisions.
""")