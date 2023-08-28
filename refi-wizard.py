import streamlit as st
import numpy_financial as npf

def monthly_payment(P, r, n):
    """Calculate monthly payment for a mortgage."""
    return -npf.pmt(r, n, P)

def remaining_balance(P, r, n, months_paid):
    """Calculate remaining balance of a mortgage after a certain number of payments."""
    return -npf.fv(r, months_paid, monthly_payment(P, r, n), P)

def main():
    st.title("Mortgage Refinancing Effective Interest Rate Calculator")

    # User inputs with more descriptive labels
    st.sidebar.header("Loan Details")
    P = st.sidebar.number_input("Initial Loan Amount ($):", min_value=1000.0, value=500000.0, step=1000.0)
    r1 = st.sidebar.number_input("Initial Interest Rate (%):", min_value=0.1, value=5.5, step=0.1) / 100 / 12
    n1_years = st.sidebar.number_input("Initial Loan Term (years):", min_value=1, value=30, step=1)
    n1 = n1_years * 12

    st.sidebar.header("Refinancing Details")
    time_before_refinance = st.sidebar.number_input("Time Before Refinancing (years):", min_value=1, value=10, step=1)
    r2 = st.sidebar.number_input("New Interest Rate After Refinancing (%):", min_value=0.1, value=3.5, step=0.1) / 100 / 12
    n2_years = st.sidebar.number_input("New Loan Term After Refinancing (years):", min_value=1, value=30, step=1)
    n2 = n2_years * 12

    # Calculate total interest for the initial loan until refinancing
    M1 = monthly_payment(P, r1, n1)
    total_paid_before_refinance = M1 * time_before_refinance * 12
    balance_before_refinance = remaining_balance(P, r1, n1, time_before_refinance * 12)
    interest_before_refinance = total_paid_before_refinance - (P - balance_before_refinance)

    # Calculate total interest for the refinanced loan
    M2 = monthly_payment(balance_before_refinance, r2, n2)
    interest_after_refinance = M2 * n2 - balance_before_refinance

    # Display results with better formatting
    st.subheader("Results")
    st.write(f"Total interest paid before refinancing: ${interest_before_refinance:,.2f}")
    st.write(f"Total interest paid after refinancing: ${interest_after_refinance:,.2f}")
    
    # Improved effective interest rate calculation
    total_paid = total_paid_before_refinance + M2 * n2
    total_interest = total_paid - P
    effective_rate_annual = (total_interest / (P * (n1_years + n2_years))) * 100
    st.write(f"Effective interest rate over the entire period: {effective_rate_annual:.2f}%")

if __name__ == "__main__":
    main()
