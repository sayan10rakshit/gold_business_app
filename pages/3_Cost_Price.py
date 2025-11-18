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
if "is_24k_rate" not in st.session_state:
    st.session_state.is_24k_rate = False
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

        # 1) Carat selection slider at the top
        carat = st.slider(
            "Select the ornament purity (in carat)",
            min_value=1,
            max_value=24,
            step=1,
            value=st.session_state.carat,
            key="carat_cp",
            on_change=lambda: setattr(
                st.session_state, "carat", st.session_state.carat_cp
            ),
        )

        # 2) Toggle for gold rate type
        is_24k_rate = st.toggle(
            f"Enter gold rate as 24k (otherwise as per {carat}k)",
            value=st.session_state.is_24k_rate,
            key="is_24k_rate_cp",
            on_change=lambda: setattr(
                st.session_state, "is_24k_rate", st.session_state.is_24k_rate_cp
            ),
        )

        # Update gold rate only if user hasn't manually changed it
        if is_24k_rate != st.session_state.is_24k_rate:
            st.session_state.is_24k_rate = is_24k_rate
            if "user_modified_gold_rate" not in st.session_state:
                if is_24k_rate:
                    st.session_state.gold_rate = default_24k_rate
                else:
                    # Calculate carat-specific rate
                    if "current_gold_rate_per_gram" in st.session_state:
                        st.session_state.gold_rate = float(
                            round(
                                (st.session_state["current_gold_rate_per_gram"] / 24.0)
                                * carat
                            )
                        )
                    else:
                        st.session_state.gold_rate = default_22k_rate

        def update_gold_rate():
            st.session_state.gold_rate = st.session_state.gold_rate_cp
            # Mark that the user has manually modified the gold rate
            st.session_state.user_modified_gold_rate = True

        # 3) Gold rate input - changes based on toggle state
        if is_24k_rate:
            gold_rate = st.number_input(
                "Enter the gold rate (24k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                key="gold_rate_cp",
                on_change=update_gold_rate,
            )
        else:
            gold_rate = st.number_input(
                f"Enter the gold rate ({carat}k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                key="gold_rate_cp",
                on_change=update_gold_rate,
            )

        goldsmith_loss_perc = st.number_input(
            "Enter the goldsmith loss percentage",
            value=4.0000,
            step=0.0001,
            format="%.4f",
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

        baseline = st.number_input(
            "Enter the baseline for making charge",
            value=0.9200,
            step=0.0001,
            format="%.4f",
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
            total_pure_wt,
            total_payable_wt,
            goldsmith_loss_wt,
            goldsmith_loss_wt_24k_price,
            breakeven_making_perc,
            cp_total,
        ) = cost_price_gold(
            gold_rate,
            goldsmith_loss_perc,
            baseline,
            carat,
            extra_charges,
            total_weight,
            is_24k_rate,  # is_22k is opposite of is_24k_rate
        )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.write("Pure Weight:")
            st.markdown(f":green[**{total_pure_wt:,.4f} gm.**]")
        with col2:
            st.write("Goldsmith Loss Wt.:")
            st.markdown(f":green[**{goldsmith_loss_wt:,.4f} gm.**]")

        st.write("### Total Payable Wt.:")
        st.markdown(f"## :orange[**{total_payable_wt:,.4f} gm.**]")
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.write("Excess Wt. (Actual Making Charges):")
            st.markdown(f":green[**{goldsmith_loss_wt:,.4f} gm.**]")
        with col2:
            st.write("Excess Wt. Price:")
            st.markdown(f":green[**₹ {goldsmith_loss_wt_24k_price:,.2f}**]")

        st.write("Breakeven Making Charges (%):")
        st.markdown(f"### :orange[**{breakeven_making_perc:,.2f}%**]")

        st.markdown("### Cost Price:")
        st.markdown(f"## :orange[₹ **{cp_total:,.2f}**]")
