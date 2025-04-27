import streamlit as st
from app_files.calculate import gold_making_charges

st.title("Making Charge Calculator")

# Initialize session state variables if they don't exist
if "gold_rate" not in st.session_state:
    st.session_state.gold_rate = 9000.00
if "gold_weight" not in st.session_state:
    st.session_state.gold_weight = 1.000
if "making_charge_perc" not in st.session_state:
    st.session_state.making_charge_perc = 12.000
if "hm_charges_per_pc" not in st.session_state:
    st.session_state.hm_charges_per_pc = 53
if "extra_charges" not in st.session_state:
    st.session_state.extra_charges = 0.0
if "total_price" not in st.session_state:
    st.session_state.total_price = 11000.00
if "qty" not in st.session_state:
    st.session_state.qty = 1
if "carat" not in st.session_state:
    st.session_state.carat = 22
if "is_22k" not in st.session_state:
    st.session_state.is_22k = True

col1, col2 = st.columns([2, 1], gap="large")

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

# Only update the session state rate if this is the first page load
# or if the user hasn't manually changed the rate
if "user_modified_gold_rate" not in st.session_state:
    if st.session_state.is_22k:
        st.session_state.gold_rate = default_22k_rate
    else:
        st.session_state.gold_rate = default_24k_rate

# Input fields
with col1:
    is_22k = st.toggle(
        "Is the gold rate converted in 22 Carat?",
        value=st.session_state.is_22k,
        key="is_22k_mc",
    )

    # Update gold rate when toggle changes
    if is_22k != st.session_state.is_22k:
        st.session_state.is_22k = is_22k
        if is_22k:
            st.session_state.gold_rate = default_22k_rate
        else:
            st.session_state.gold_rate = default_24k_rate

    def update_gold_rate():
        st.session_state.gold_rate = st.session_state.gold_rate_mc
        # Mark that the user has manually modified the gold rate
        st.session_state.user_modified_gold_rate = True

    if is_22k:
        gold_rate = st.number_input(
            "Enter the gold rate (22k per gram)",
            value=st.session_state.gold_rate,
            step=0.01,
            key="gold_rate_mc",
            on_change=update_gold_rate,
        )
    else:
        gold_rate = st.number_input(
            "Enter the gold rate (24k per gram)",
            value=st.session_state.gold_rate,
            step=0.01,
            key="gold_rate_mc",
            on_change=update_gold_rate,
        )
    gold_weight = st.number_input(
        "Enter the weight of gold (grams)",
        value=st.session_state.gold_weight,
        step=0.001,
        format="%.3f",
        key="gold_weight_mc",
        on_change=lambda: setattr(
            st.session_state, "gold_weight", st.session_state.gold_weight_mc
        ),
    )
    total_price = st.number_input(
        "Enter the total price",
        value=st.session_state.total_price,
        key="total_price_mc",
    )
    hm_charges = st.number_input(
        "Enter the Hallmark charges",
        value=st.session_state.hm_charges_per_pc,
        key="hm_charges_mc",
        on_change=lambda: setattr(
            st.session_state, "hm_charges_per_pc", st.session_state.hm_charges_mc
        ),
    )
    no_pcs = st.number_input(
        "Enter the number of ornament pieces",
        value=st.session_state.qty,
        min_value=1,
        key="no_pcs_mc",
        on_change=lambda: setattr(st.session_state, "qty", st.session_state.no_pcs_mc),
    )
    gst = st.number_input("Enter the GST (in percentage)", value=3)
    extra_charges = st.number_input(
        "Enter the extra charges (if any)",
        value=st.session_state.extra_charges,
        key="extra_charges_mc",
        on_change=lambda: setattr(
            st.session_state, "extra_charges", st.session_state.extra_charges_mc
        ),
    )
    carat = st.slider(
        "Select the final ornament purity (in carat)",
        min_value=1,
        max_value=24,
        step=1,
        value=st.session_state.carat,
        key="carat_mc",
        on_change=lambda: setattr(st.session_state, "carat", st.session_state.carat_mc),
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

    # Update the session state with the recalculated making charge percentage
    # This will be used in the Gold Buy page
    st.session_state.making_charge_perc = making_charge_perc
    # Update the session state with the recalculated making charges
    st.session_state.calculated_making_charges = making_charges

    st.write("Making Charge Percentage:")
    st.markdown(f"## :green[**{making_charge_perc:.3f}%**]")
    st.write("Making Charge INR:")
    st.markdown(f"""## :green[₹ **{making_charges:,.2f}**]""")
