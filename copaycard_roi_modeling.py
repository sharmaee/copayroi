import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(page_title="Lamar Health ROI Calculator")

st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Impact of Copay Accumulators on <br/> Manufacturer Bottomline</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Function to calculate gross and net revenue for each category
def calculate_revenues(num_patients, price, manufacturer_copay, percent_accumulator, num_cannot_afford):
    # Placeholder for calculation logic
    # Replace this with your actual calculation logic for each category
    revenues = {
        "Category": ["No accumulator/maximizer", "Accumulator", "With Lamar Health"],
        "Gross Revenue": [0, 0, 0], 
        "Lost Revenue": [0, 0, 0]
    }
    # Perform calculations here based on the inputs and update the values in 'revenues'

    num_lost_patients = (manufacturer_copay)*(percent_accumulator/100)*(num_cannot_afford/100)

    revenue_gross = num_patients*price
    revenue_lost = num_lost_patients*price
    revenue_accumulator = revenue_gross-revenue_lost


    revenues["Gross Revenue"] = [revenue_gross, revenue_accumulator, revenue_gross]
    revenues["Lost Revenue"] = [0, revenue_lost, 0]


    return pd.DataFrame(revenues)

# Main function for the Streamlit app
def main():

    # Input fields
    with st.form("input_form"):
        num_patients = st.number_input("Number of Commercially Insured Patients on Therapy", value=10000)
        price = st.number_input("Price of the Product", value = 50000)
        manufacturer_copay = st.number_input("Patients Enrolled in Copay Assistance", value=7000)
        percent_accumulator = st.number_input("Percent of Patients Enrolled in Accumulators (%)", value=83)
        num_cannot_afford = st.number_input("Percent of Patients That Discontinue Due to OOP after 6 months (%)", value=36)

        submit_button = st.form_submit_button("Calculate Revenues", type="primary")

        if submit_button:
            # Perform calculations
            revenue_df = calculate_revenues(num_patients, price, manufacturer_copay, percent_accumulator, num_cannot_afford)
    
            # Format the numbers in the DataFrame
            formatted_df = revenue_df.copy()
            formatted_df["Gross Revenue"] = formatted_df["Gross Revenue"].apply(lambda x: f"${x:,.0f}")
            formatted_df["Lost Revenue"] = formatted_df["Lost Revenue"].apply(lambda x: f"${x:,.0f}")

            # Reset and drop the index
            # formatted_df.reset_index(drop=True, inplace=True)
            
            # Display the DataFrame using st.dataframe
            st.dataframe(formatted_df.style.highlight_between(left="$0", inclusive="neither", subset=["Lost Revenue"], color="red"));

    st.header("References:")
    st.image("rise_of_accumulators.jpeg")
    st.image("likely_to_discontinue.png")
    st.markdown("""
    - [Rise of Copay Accumulators and Maximizers](https://www.drugchannels.net/2023/02/copay-accumulator-and-maximizer-update.html)
    - [Copay Accumulator Effects on Patient Adherence](https://phrma.org/-/media/Project/PhRMA/PhRMA-Org/PhRMA-Org/PDF/A-C/Accumulator-adjustment-programs-from-payers-lead-to-surprise-out-of-pocket-costs-and-nonadherence.pdf)
    - [J&J lawsuit against copay maximizers for $100 million dollars](https://www.example.com)
    """)


if __name__ == "__main__":
    main()