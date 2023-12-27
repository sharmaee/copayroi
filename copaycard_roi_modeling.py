import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lamar Health ROI Calculator", layout="wide")

st.markdown(
    """
    <div style='text-align: center;'>
        <h1>Impact of Copay Accumulators on <br/> Manufacturer Bottomline!</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

df = pd.DataFrame(
    [
        {
            "product": "Product A",
            "avg_wholesale_price": 50000,
            "insured_patients": 700,
            "eligible_enrolled": 650,
        },
        {
            "product": "Product B",
            "avg_wholesale_price": 60000,
            "insured_patients": 500,
            "eligible_enrolled": 450,
        },
    ]
)

# Calculate gross_annual_revenue for each product
df["enrolled_copay_accumulator"] = (df["eligible_enrolled"] * 0.39).astype(int)
df["likely_discontinue_therapy"] = (df["enrolled_copay_accumulator"] * 0.36).astype(int)
df["gross_annual_revenue"] = df["insured_patients"] * df["avg_wholesale_price"]
df["lost_revenue_discontinuation"] = df["avg_wholesale_price"] * df["likely_discontinue_therapy"]

st.data_editor(
    df,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "product": st.column_config.Column(
            "Product Name",
        ),
        "insured_patients": st.column_config.Column(
            "Number of Patients",
            help="The Number of Commercially Insured Patients on Therapy",
        ),
        "eligible_enrolled": st.column_config.Column(
            "Patients with Copay Assistance",
            help="The Number of Patients Eligible and Enrolled into Copay Assistance Program",
        ),
        "avg_wholesale_price": st.column_config.NumberColumn(
            "Price of Product",
            help="Wholesale Acquisition Cost (WAC) of the Therapy",
            format="$%d",
        ),
        "gross_annual_revenue": st.column_config.NumberColumn(
            "Gross Annual Revenue",
            format="$%d",
        ),
        "enrolled_copay_accumulator": st.column_config.Column(
            "Number of Patients in Accumulator Programs",
            help="In 2022, 39 percent of all commercially covered lives are enrolled into accumulator programs: \
            https://www.drugchannels.net/2023/02/copay-accumulator-and-maximizer-update \
            ",
        ),
        "likely_discontinue_therapy": st.column_config.Column(
            "Number of Patients Likely to Discontinue",
            help="36 percent of patients that face a copay accumulator are likely to discontinue therapy: \
            https://phrma.org/-/media/Project/PhRMA/PhRMA-Org/PhRMA-Org/PDF/A-C/Accumulator-adjustment-programs-from-payers-lead-to-surprise-out-of-pocket-costs-and-nonadherence.pdf",
        ),
        "lost_revenue_discontinuation": st.column_config.NumberColumn(
            "Lost Revenue",
            help="The amount of revenue lost to manufacturer due to discontinuation.",
            format="$%d",
        ),
    },
)

st.header("Resources:")
st.image("rise_of_accumulators.jpeg")
st.image("likely_to_discontinue.png")
st.markdown("""
    - [Rise of Copay Accumulators and Maximizers](https://www.drugchannels.net/2023/02/copay-accumulator-and-maximizer-update.html)
    - [Copay Accumulator Effects on Patient Adherence](https://phrma.org/-/media/Project/PhRMA/PhRMA-Org/PhRMA-Org/PDF/A-C/Accumulator-adjustment-programs-from-payers-lead-to-surprise-out-of-pocket-costs-and-nonadherence.pdf)
    - [J&J lawsuit against copay maximizers for $100 million dollars](https://www.example.com)
""")
