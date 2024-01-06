import streamlit as st
from app_files.calculate import gold_sell

st.title("Gold Buy Calculator")

# Input fields
with st.container():
    # Create a two-column layout for input fields and results
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("Input Fields")
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
        qty = st.number_input(
            "Enter the quantity of gold (items)",
            min_value=1,
            step=1,
            placeholder=1,
            value=1,
        )
        weight = st.number_input(
            "Enter the weight of each item (grams)", value=1.000, step=0.001
        )
        making_charge_perc = st.number_input(
            "Making charge percentage", value=14.00, step=0.01
        )
        extra_charges = st.number_input("Extra charges")
        carat = st.slider(
            "Select the final ornament purity (in carat)",
            min_value=1,
            max_value=24,
            step=1,
            value=22,
        )

    # Results
    with col2:
        st.subheader("Results")
        (
            hm_rate,
            gold_charges,
            making_charges,
            hm_charges,
            tax,
            total_price,
        ) = gold_sell(
            gold_rate,
            qty,
            weight,
            making_charge_perc,
            extra_charges,
            carat,
            is_22k,
        )
        st.markdown("Gold Charges:")
        col1, col2 = st.columns([1, 1], gap="small")
        with st.container():
            with col1:
                st.markdown(f""":orange[₹**{gold_charges:,.2f}**]""")
            with col2:
                st.markdown(f"""(₹**{hm_rate:,.2f}/gm.**)""")

        st.write("Making charges:")
        col1, col2 = st.columns([1, 1], gap="small")
        with st.container():
            with col1:
                st.markdown(f""":green[₹ **{making_charges:,.2f}**]""")
            with col2:
                st.markdown(f"""**(₹{making_charges/weight:,.2f}/gm.)**""")
            if extra_charges:
                st.caption(
                    f"Making Charges: ₹{(making_charges-extra_charges):,.2f} \
                    + Extra charges: ₹{extra_charges:,.2f}"
                )

        st.write("Hallmark Charges")
        col1, col2 = st.columns([1, 1], gap="small")
        with st.container():
            with col1:
                st.markdown(f":green[₹**{hm_charges:,.2f}**]")
            with col2:
                st.markdown("""**(₹45/pc.)**""")

        st.write("Tax (GST):")
        col1, col2 = st.columns([1, 1], gap="small")
        with st.container():
            with col1:
                st.markdown(f""":green[₹ **{tax:,.2f}**]""")
            with col2:
                st.markdown("""**(3%)**""")
            st.caption(f"SGST: ₹{tax/2:,.2f} + CGST: ₹{tax/2:,.2f}")

        st.markdown("### Total Price:")
        st.markdown(f"""## :green[₹ **{total_price:,.2f}**]""")
