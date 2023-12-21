import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.title('Understand how accumulators and maximizers impact your bottomline.')

# Function to calculate gross and net revenue for each category
def calculate_revenues(num_patients, price, manufacturer_copay, max_copay, num_cannot_afford):
    # Placeholder for calculation logic
    # Replace this with your actual calculation logic for each category
    revenues = {
        "Category": ["No accumulator/maximizer", "Accumulator", "Maximizer", "With Lamar Health"],
        "Gross Revenue": [0, 0, 0, 0], 
        "Manufacturer Costs": [0, 0, 0, 0],
        "Net Revenue": [0, 0, 0, 0],    
        "Lost Revenue": [0, 0, 0, 0] 
    }
    # Perform calculations here based on the inputs and update the values in 'revenues'
    nothing_gross = num_patients*price
    nothing_net = num_patients*(price-manufacturer_copay)
    nothing_cost = nothing_gross - nothing_net

    accumulator_gross = (num_patients-num_cannot_afford)*price
    accumulator_net = accumulator_gross-(num_patients-num_cannot_afford)*(manufacturer_copay)
    accumulator_cost = accumulator_gross - accumulator_net

    maximizer_gross = (num_patients-num_cannot_afford)*price
    maximizer_net = maximizer_gross-(num_patients-num_cannot_afford)*(max_copay)
    maximizer_cost = maximizer_gross - maximizer_net

    lh_gross = num_patients*price
    lh_net = num_patients*(price-manufacturer_copay)
    lh_cost = lh_gross - lh_net

    revenues["Gross Revenue"] = [nothing_gross, accumulator_gross, maximizer_gross, lh_gross]
    revenues["Manufacturer Costs"] = [nothing_cost, accumulator_cost, maximizer_cost, lh_cost]
    revenues["Net Revenue"] = [nothing_net, accumulator_net, maximizer_net, lh_net]
    revenues["Lost Revenue"] = [nothing_net-nothing_net, nothing_net-accumulator_net, nothing_net-maximizer_net, nothing_net-lh_net]

    return pd.DataFrame(revenues)

# Main function for the Streamlit app
def main():

    # Input fields
    with st.form("input_form"):
        num_patients = st.number_input("Number of Patients", value=1000)
        price = st.number_input("Price of the Product", value = 24000)
        manufacturer_copay = st.number_input("Manufacturer Copay (based on patient out-of-pocket costs, deductible)", value=6000)
        max_copay = st.number_input("Maximum Copay", value=16000)
        num_cannot_afford = st.number_input("Number of Patients Who Can't Afford Out-of-Pocket Costs", value=100)

        submit_button = st.form_submit_button("Calculate Revenues")

        if submit_button:
            # Perform calculations
            revenue_df = calculate_revenues(num_patients, price, manufacturer_copay, max_copay, num_cannot_afford)
    
            # Format the numbers in the DataFrame
            formatted_df = revenue_df.copy()
            formatted_df["Gross Revenue"] = formatted_df["Gross Revenue"].apply(lambda x: f"${x:,.2f}")
            formatted_df["Manufacturer Costs"] = formatted_df["Manufacturer Costs"].apply(lambda x: f"${x:,.2f}")
            formatted_df["Net Revenue"] = formatted_df["Net Revenue"].apply(lambda x: f"${x:,.2f}")
            formatted_df["Lost Revenue"] = formatted_df["Lost Revenue"].apply(lambda x: f"${x:,.2f}")

            # Reset and drop the index
            formatted_df.reset_index(drop=True, inplace=True)
            
            # Display the DataFrame using st.dataframe
            st.dataframe(formatted_df)

if __name__ == "__main__":
    main()
