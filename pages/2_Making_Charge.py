import streamlit as st
from app_files.calculate import gold_making_charges

st.title("Making Charge Calculator")

col1, col2 = st.columns([2, 1], gap="large")

# Input fields
with col1:
    is_22k = st.toggle("Is the gold rate converted in 22 Carat?", value=True)
    if is_22k:
        gold_rate = st.number_input(
            "Enter the gold rate (22k per gram)",
            value=6500.00,
            step=0.01,
        )
    else:
        gold_rate = st.number_input(
            "Enter the gold rate (24k per gram)",
            value=6500.00,
            step=0.01,
        )
    gold_weight = st.number_input(
        "Enter the weight of gold (grams)", value=1.000, step=0.001
    )
    total_price = st.number_input("Enter the total price", value=7058.55)
    hm_charges = st.number_input("Enter the Hallmark charges", value=45)
    no_pcs = st.number_input(
        "Enter the number of ornament pieces", value=1, min_value=1
    )
    gst = st.number_input("Enter the GST (in percentage)", value=3)
    extra_charges = st.number_input("Enter the extra charges (if any)")
    carat = st.slider(
        "Select the final ornament purity (in carat)",
        min_value=1,
        max_value=24,
        step=1,
        value=22,
    )

# Results
with col2:
    st.subheader("Results:")
    making_charge_perc, making_charges = gold_making_charges(
        gold_rate,
        gold_weight,
        total_price,
        hm_charges,
        no_pcs,
        gst,
        extra_charges,
        carat,
        is_22k,
    )

    st.write("Making Charge Percentage:")
    st.markdown(f"## :green[**{making_charge_perc:.3f}%**]")
    st.write("Making Charge INR:")
    st.markdown(f"""## :green[₹ **{making_charges:,.2f}**]""")
