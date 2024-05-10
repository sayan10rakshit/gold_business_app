import streamlit as st
from app_files.calculate import cost_price_gold

st.title("Cost Price Calculator")

col1, col2 = st.columns([1, 1], gap="large")

with st.container():
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
        making_perc = st.number_input(
            "Enter the making charge percentage", value=4.00, step=0.01
        )
        total_weight = st.number_input(
            "Enter the weight of gold (grams)", value=1.000, step=0.001
        )
        keep_baseline_916 = st.toggle(
            "Keep the baseline as 0.9166",
            value=False,
        )
        if keep_baseline_916:
            baseline = 22 / 24
        else:
            baseline = st.number_input(
                "Enter the baseline for making charge",
                value=0.920,
                step=0.001,
            )
        carat = st.slider(
            "Select the final ornament purity (in carat)",
            min_value=1,
            max_value=24,
            step=1,
            value=22,
        )
        extra_charges = st.number_input("Enter the extra charges (if any)")

    with col2:
        st.subheader("Results")
        (
            pure_wt,
            making_charge_wt,
            actual_making_perc,
            making_charges,
            cp,
        ) = cost_price_gold(
            gold_rate,
            making_perc,
            baseline,
            carat,
            extra_charges,
            total_weight,
            is_22k,
        )

        st.write("Pure Weight:")
        st.markdown(f":green[**{pure_wt:,.5f} gm.**]")

        st.write("Making Charge Wt.:")
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown(f":green[**{making_charge_wt:,.5f} gm.**]")
        with col2:
            if keep_baseline_916:
                pass
            else:
                default_making_charge_wt = (baseline - (carat / 24.0)) * total_weight
                st.markdown(
                    f"**({making_charge_wt - default_making_charge_wt:,.5f}gm + {default_making_charge_wt:,.5f}gm)**"
                )
        if not keep_baseline_916:
            st.caption("Making Charge Wt. + Default Making Charge Wt.")

        st.write("Actual Making Charge Perc.:")
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown(f":green[**{actual_making_perc * 100:.4f}%**]")
        with col2:
            if keep_baseline_916:
                pass
            else:
                st.markdown(
                    f"**({making_perc:,.3f}% + {(baseline - (carat / 24.0))*100:,.3f}%)**"
                )
        if not keep_baseline_916:
            st.caption("Making Perc. + Default Perc.")

        st.write("Actual Making Charges:")
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown(f":green[₹ **{making_charges:,.2f}**]")
        with col2:
            if keep_baseline_916:
                pass
            else:
                if is_22k:
                    gold_rate_24k = gold_rate * (24 / 22.0)
                else:
                    gold_rate_24k = gold_rate
                default_making_charges = (
                    making_charges
                    - gold_rate_24k * total_weight * (making_perc / 100.0)
                )
                st.markdown(
                    f"**(₹ {making_charges - default_making_charges:,.2f} + ₹ {default_making_charges:,.2f})**"
                )
        if not keep_baseline_916:
            st.caption("Making Charges + Default Making Charges")

        st.markdown("### Cost Price:")
        st.markdown(f"## :orange[₹ **{cp:,.2f}**]")
