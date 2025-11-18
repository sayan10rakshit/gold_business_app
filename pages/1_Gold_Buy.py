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
if "total_before_tax" not in st.session_state:
    st.session_state.total_before_tax = 0.0
if "total_price" not in st.session_state:
    st.session_state.total_price = 0.0
if "qty" not in st.session_state:
    st.session_state.qty = 1
if "carat" not in st.session_state:
    st.session_state.carat = 22
if "is_24k_rate" not in st.session_state:
    st.session_state.is_24k_rate = False
if "user_modified_gold_rate" not in st.session_state:
    st.session_state.user_modified_gold_rate = False
if "calculate_with_tax" not in st.session_state:
    st.session_state.calculate_with_tax = True


# Input fields
with st.container():
    # Create a two-column layout for input fields and results
    col1, col2 = st.columns([2, 1], gap="large")

    with col1:
        st.subheader("Input Fields")

        # 1) Carat selection slider at the top
        carat = st.slider(
            "Select the ornament purity (in carat)",
            min_value=1,
            max_value=24,
            step=1,
            value=st.session_state.carat,
            key="carat_slider",
        )
        st.session_state.carat = carat

        # 2) Toggle for gold rate type
        is_24k_rate = st.toggle(
            f"Enter gold rate as 24k (otherwise as per {carat}k)",
            value=st.session_state.is_24k_rate,
            key="is_24k_rate_toggle",
        )
        st.session_state.is_24k_rate = is_24k_rate

        # Initialize the default rates
        default_carat_rate = 9000.00
        default_24k_rate = 9818.18  # Approximate 24k equivalent

        # Update rates if we have external gold rate data available
        if "gold_rate_916" in st.session_state:
            default_carat_rate = float(st.session_state["gold_rate_916"] / 10)
            default_24k_rate = float((st.session_state["gold_rate_916"] / 10) / 22 * 24)
        elif "current_gold_rate_per_gram" in st.session_state:
            default_carat_rate = float(
                round((st.session_state["current_gold_rate_per_gram"] / 24.0) * carat)
            )
            default_24k_rate = float(st.session_state["current_gold_rate_per_gram"])

        # Keep gold rate synchronized with live defaults unless the user overrides it manually
        if not st.session_state.user_modified_gold_rate:
            if is_24k_rate:
                st.session_state.gold_rate = default_24k_rate
            else:
                st.session_state.gold_rate = default_carat_rate

        # 3) Gold rate input - changes based on toggle state
        if is_24k_rate:
            gold_rate = st.number_input(
                "Enter the gold rate (24k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                format="%.2f",
                key="gold_rate_input",
            )
        else:
            gold_rate = st.number_input(
                f"Enter the gold rate ({carat}k per gram)",
                value=st.session_state.gold_rate,
                step=0.01,
                format="%.2f",
                key="gold_rate_input",
            )

        # Mark user modified if rate changed
        if gold_rate != st.session_state.gold_rate:
            st.session_state.user_modified_gold_rate = True

        # Update session state with current gold rate
        st.session_state.gold_rate = gold_rate

        # Other inputs with direct assignment
        qty = st.number_input(
            "Enter the quantity of gold (items)",
            min_value=1,
            step=1,
            value=st.session_state.qty,
            key="qty_input",
        )
        st.session_state.qty = qty

        weight = st.number_input(
            "Enter the weight of each item (grams)",
            value=st.session_state.gold_weight,
            step=0.001,
            format="%.3f",
            key="weight_input",
        )
        st.session_state.gold_weight = weight

        making_charge_perc = st.number_input(
            "Making charge percentage",
            value=st.session_state.making_charge_perc,
            step=0.001,
            format="%.3f",
            key="making_charge_input",
        )
        st.session_state.making_charge_perc = making_charge_perc
        hm_charges_per_pc = st.number_input(
            "Hallmark charges per piece",
            value=st.session_state.hm_charges_per_pc,
            key="hm_charges_input",
        )
        st.session_state.hm_charges_per_pc = hm_charges_per_pc

        extra_charges = st.number_input(
            "Extra charges",
            value=st.session_state.extra_charges,
            key="extra_charges_input",
        )
        st.session_state.extra_charges = extra_charges

        # Tax toggle
        calculate_with_tax = st.toggle(
            "Calculate with Tax (GST)",
            value=st.session_state.calculate_with_tax,
            key="calculate_with_tax_toggle",
        )
        st.session_state.calculate_with_tax = calculate_with_tax

        if calculate_with_tax:
            st.caption("GST (3%) will be applied to the calculation")
        else:
            st.caption("No GST will be applied to the calculation")

    # Results section in the second column
    with col2:
        st.subheader("Results")

        # Perform calculation with current values
        (
            hm_rate,
            gold_charges,
            making_charges,
            hm_charges,
            tax,
            total_before_tax,
            total_price,
            pure_gold_weight,
            total_recouped_pure_weight,
            making_charge_wt_pure,
        ) = gold_sell(
            gold_rate,
            qty,
            weight,
            making_charge_perc,
            hm_charges_per_pc,
            extra_charges,
            calculate_with_tax,  # Pass the tax toggle value
            carat,
            is_24k_rate,  # is_22k is opposite of is_24k_rate
        )

        # Update session state with calculated values
        st.session_state.total_before_tax = total_before_tax
        st.session_state.total_price = total_price
        st.session_state.calculated_making_charges = making_charges

        # Display results
        st.markdown("Gold Charges:")
        col1_disp, col2_disp = st.columns([1, 1], gap="small")
        with st.container():
            with col1_disp:
                st.markdown(f""":orange[₹**{gold_charges:,.2f}**]""")
            with col2_disp:
                st.markdown(f"""(₹**{hm_rate:,.2f}/gm.**)""")

        st.write("Making charges:")
        col1_disp, col2_disp = st.columns([1, 1], gap="small")
        with st.container():
            with col1_disp:
                st.markdown(f""":green[₹ **{making_charges:,.2f}**]""")
            with col2_disp:
                st.markdown(f"""**(₹{making_charges/weight:,.2f}/gm.)**""")
            if extra_charges:
                st.caption(
                    f"Making Charges: ₹{(making_charges-extra_charges):,.2f} \
                    + Extra charges: ₹{extra_charges:,.2f}"
                )

        st.write("Hallmark Charges")
        col1_disp, col2_disp = st.columns([1, 1], gap="small")
        with st.container():
            with col1_disp:
                st.markdown(f":green[₹**{hm_charges:,.2f}**]")
            with col2_disp:
                st.markdown(f"""**(₹{hm_charges_per_pc}/pc.)**""")
        if calculate_with_tax:
            st.caption(f"Total before tax: ₹{total_before_tax:,.2f}")
            st.write("Tax (GST):")
            col1_disp, col2_disp = st.columns([1, 1], gap="small")
            with st.container():
                with col1_disp:
                    st.markdown(f""":green[₹ **{tax:,.2f}**]""")
                with col2_disp:
                    st.markdown("""**(3%)**""")
                st.caption(f"SGST: ₹{tax/2:,.2f} + CGST: ₹{tax/2:,.2f}")
        else:
            st.write("Tax (GST):")
            st.markdown(":green[₹ **0.00**] (Tax calculation disabled)")

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
                f"Here we have used **{making_charge_perc:.3f}%** making charges, which is **₹{making_charges:,.2f}** and extra charges of **₹{extra_charges:,.2f}**."
            )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Hallmark Charges]**:")
        with col2:
            st.markdown(
                "The price of testing the purity of the ornament and assigning a unique ID (HUID) to the ornament."
            )
            st.caption(
                f"The standard hallmark charges are **₹{hm_charges_per_pc}/pc.**"
            )

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Tax]**:")
        with col2:
            if calculate_with_tax:
                st.markdown(
                    "State Goods and Services Tax (SGST) & Central Goods and Services Tax (CGST). This tax is levied on **:orange[Gold Charges]** + **:green[Making Charges]** + **:green[Hallmark Charges]**."
                )
                st.caption("The standard GST rate is **3%**. (1.5% SGST + 1.5% CGST)")
                st.caption(
                    f"Here we have used **1.5%** SGST {tax/2:,.2f} + **1.5%** CGST {tax/2:,.2f} = **₹{tax:,.2f}**."
                )
            else:
                st.markdown("Tax calculation is currently disabled.")
                st.caption("No GST is being applied to this calculation.")

        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Total Price]**:")
        with col2:
            st.markdown(
                "The final price of the ornament. This is **:orange[Gold Charges]** + **:green[Making Charges]** + **:green[Hallmark Charges]** + **:green[Tax]**."
            )
        col1, col2 = st.columns([1, 1], gap="small")
        with col1:
            st.markdown("- **:green[Pure Gold Weight Recouped]**:")
        with col2:
            # Add pure weight calculation information
            st.markdown(
                f"**Pure Wt.** ({pure_gold_weight:.4f} gm.) + **Excess Pure M.C. Wt.** ({making_charge_wt_pure:.4f} gm.) = **Total Recouped Pure Wt.** ({total_recouped_pure_weight:.4f} gm.)"
            )
