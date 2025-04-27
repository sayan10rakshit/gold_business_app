import streamlit as st
from app_files.calculate import cost_price_gold

st.title("Cost Price Calculator")

# Initialize session state variables if they don't exist
if "gold_rate" not in st.session_state:
    st.session_state.gold_rate = 9000.00
if "gold_weight" not in st.session_state:
    st.session_state.gold_weight = 1.000
if "extra_charges" not in st.session_state:
    st.session_state.extra_charges = 0.0
if "is_22k" not in st.session_state:
    st.session_state.is_22k = True
if "carat" not in st.session_state:
    st.session_state.carat = 22

col1, col2 = st.columns([1, 1], gap="large")

# Initialize the default rates for 22k and 24k
default_22k_rate = 9000.00
default_24k_rate = 9818.18  # Approximate 24k equivalent

# Update rates if we have the 916 gold rate available
if "gold_rate_916" in st.session_state:
    # Use the 916 (22k) gold rate directly for 22k
    default_22k_rate = float(
        st.session_state["gold_rate_916"] / 10
    )  # Convert from 100g to per gram
    # Calculate 24k rate: (916 rate / 22 * 24)
    default_24k_rate = float((st.session_state["gold_rate_916"] / 10) / 22 * 24)
elif "current_gold_rate_per_gram" in st.session_state:
    # Fallback to the old calculation method
    default_22k_rate = float(
        round((st.session_state["current_gold_rate_per_gram"] / 24.0) * 22.0)
    )
    default_24k_rate = float(st.session_state["current_gold_rate_per_gram"])

with st.container():
    with col1:
        st.subheader("Input Fields")
        is_22k = st.toggle(
            "Is the gold rate converted in 22 Carat?",
            value=st.session_state.is_22k,
            key="is_22k_cp",
            on_change=lambda: setattr(
                st.session_state, "is_22k", st.session_state.is_22k_cp
            ),
        )
        # Update gold rate only if user hasn't manually changed it
        if is_22k != st.session_state.is_22k:
            st.session_state.is_22k = is_22k
            if "user_modified_gold_rate" not in st.session_state:
                if is_22k:
                    st.session_state.gold_rate = default_22k_rate
                else:
                    st.session_state.gold_rate = default_24k_rate

        def update_gold_rate():
            st.session_state.gold_rate = st.session_state.gold_rate_cp
            # Mark that the user has manually modified the gold rate
            st.session_state.user_modified_gold_rate = True

        if is_22k:
            gold_rate = st.number_input(
                "Enter the gold rate (22k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                key="gold_rate_cp",
                on_change=update_gold_rate,
            )
        else:
            gold_rate = st.number_input(
                "Enter the gold rate (24k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                key="gold_rate_cp",
                on_change=update_gold_rate,
            )

        making_perc = st.number_input(
            "Enter the making charge percentage", value=4.00, step=0.01
        )

        total_weight = st.number_input(
            "Enter the weight of gold (grams)",
            value=st.session_state.gold_weight,
            step=0.001,
            format="%.3f",
            key="total_weight_cp",
            on_change=lambda: setattr(
                st.session_state, "gold_weight", st.session_state.total_weight_cp
            ),
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
            value=st.session_state.carat,
            key="carat_cp",
            on_change=lambda: setattr(
                st.session_state, "carat", st.session_state.carat_cp
            ),
        )

        extra_charges = st.number_input(
            "Enter the extra charges (if any)",
            value=st.session_state.extra_charges,
            key="extra_charges_cp",
            on_change=lambda: setattr(
                st.session_state, "extra_charges", st.session_state.extra_charges_cp
            ),
        )

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
