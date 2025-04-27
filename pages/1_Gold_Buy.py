import streamlit as st
from app_files.calculate import gold_sell

st.title("Gold Buy Calculator")

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
    st.session_state.total_price = 0.0
if "qty" not in st.session_state:
    st.session_state.qty = 1
if "carat" not in st.session_state:
    st.session_state.carat = 22
if "is_22k" not in st.session_state:
    st.session_state.is_22k = True

# Input fields
with st.container():
    # Create a two-column layout for input fields and results
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("Input Fields")
        is_22k = st.toggle(
            "Is the gold rate converted in 22/18 Carat?",
            value=st.session_state.is_22k,
            key="is_22k_buy",
            on_change=lambda: setattr(
                st.session_state, "is_22k", st.session_state.is_22k_buy
            ),
        )

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

        # Update the session state gold rate based on the toggle
        if is_22k and st.session_state.gold_rate != default_22k_rate:
            st.session_state.gold_rate = default_22k_rate
        elif not is_22k and st.session_state.gold_rate != default_24k_rate:
            st.session_state.gold_rate = default_24k_rate

        if is_22k:
            gold_rate = st.number_input(
                "Enter the gold rate (22k/18k per gram)",
                value=default_22k_rate,
                step=0.01,
                format="%.2f",
                key="gold_rate_buy",
                on_change=lambda: setattr(
                    st.session_state, "gold_rate", st.session_state.gold_rate_buy
                ),
            )
        else:
            gold_rate = st.number_input(
                "Enter the gold rate (24k per gram)",
                value=default_24k_rate,
                step=0.01,
                format="%.2f",
                key="gold_rate_buy",
                on_change=lambda: setattr(
                    st.session_state, "gold_rate", st.session_state.gold_rate_buy
                ),
            )
        qty = st.number_input(
            "Enter the quantity of gold (items)",
            min_value=1,
            step=1,
            placeholder=1,
            value=st.session_state.qty,
            key="qty_buy",
            on_change=lambda: setattr(
                st.session_state, "qty", st.session_state.qty_buy
            ),
        )
        weight = st.number_input(
            "Enter the weight of each item (grams)",
            value=st.session_state.gold_weight,
            step=0.001,
            format="%.3f",
            key="weight_buy",
            on_change=lambda: setattr(
                st.session_state, "gold_weight", st.session_state.weight_buy
            ),
        )
        making_charge_perc = st.number_input(
            "Making charge percentage",
            value=st.session_state.making_charge_perc,
            step=0.001,
            format="%.3f",
            key="making_charge_perc_buy",
            on_change=lambda: setattr(
                st.session_state,
                "making_charge_perc",
                st.session_state.making_charge_perc_buy,
            ),
        )
        hm_charges_per_pc = st.number_input(
            "Hallmark charges per piece",
            value=st.session_state.hm_charges_per_pc,
            key="hm_charges_per_pc_buy",
            on_change=lambda: setattr(
                st.session_state,
                "hm_charges_per_pc",
                st.session_state.hm_charges_per_pc_buy,
            ),
        )
        extra_charges = st.number_input(
            "Extra charges",
            value=st.session_state.extra_charges,
            key="extra_charges_buy",
            on_change=lambda: setattr(
                st.session_state, "extra_charges", st.session_state.extra_charges_buy
            ),
        )
        carat = st.slider(
            "Select the final ornament purity (in carat)",
            min_value=1,
            max_value=24,
            step=1,
            value=22,
        )  # Results
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
            hm_charges_per_pc,
            extra_charges,
            carat,
            is_22k,
        )

        # Update session state with calculated values
        st.session_state.total_price = total_price
        # Store the calculated making charges per gram for reference in other pages
        st.session_state.calculated_making_charges = making_charges
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
                st.markdown("""**(₹53/pc.)**""")

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

    with st.expander("**Show Detailed Info. ℹ️**"):
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:orange[Gold Charges]**:")
        with col2:
            st.markdown("The price of the gold in the ornament as per Carat.")
            st.caption(
                f"Here we have used **{carat} Carat** gold, whose price is **₹{hm_rate:,.2f}** per gram."
            )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Making Charges]**:")
        with col2:
            st.markdown(
                'The cost of making the ornament, levied on the **"Gold Charges"** as percentage. The extra charges are also included in this.'
            )
            st.caption(
                "Extra charges are the charges levied on the ornament for adding extra features like stones, conch bangles etc."
            )
            st.caption(
                f"Here we have used **{making_charge_perc}%** making charges, which is **₹{making_charges:,.2f}** and extra charges of **₹{extra_charges:,.2f}**."
            )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Hallmark Charges]**:")
        with col2:
            st.markdown(
                "The price of testing the purity of the ornament and assigning a unique ID (HUID) to the ornament."
            )
            st.caption("The standard hallmark charges are **₹53/pc.**.")

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Tax]**:")
        with col2:
            st.markdown(
                "State Goods and Services Tax (SGST) & Central Goods and Services Tax (CGST). This tax is levied on **:orange[Gold Charges]** + **:green[Making Charges]** + **:green[Hallmark Charges]**."
            )
            st.caption("The standard GST rate is **3%**. (1.5% SGST + 1.5% CGST)")
            st.caption(
                f"Here we have used **1.5%** SGST {tax/2:,.2f} + **1.5%** CGST {tax/2:,.2f} = **₹{tax:,.2f}**."
            )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Total Price]**:")
        with col2:
            st.markdown(
                "The final price of the ornament. This is **:orange[Gold Charges]** + **:green[Making Charges]** + **:green[Hallmark Charges]** + **:green[Tax]**."
            )
