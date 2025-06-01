def gold_sell(
    gold_rate=6500,
    qty=1,
    weight=1,
    making_charge_perc=14,
    hm_charges_per_pc=53,
    extra_charges=0,
    calculate_with_tax=True,
    carat=22,
    is_22k=True,
):
    if calculate_with_tax:
        tax_rate = 0.03
    else:
        tax_rate = 0.0
    if is_22k:
        hm_rate = gold_rate
        carat = 22
    else:
        hm_rate = gold_rate * (carat / 24)
    gold_charges = hm_rate * weight
    making_charges = gold_charges * (making_charge_perc / 100) + extra_charges
    hm_charges = hm_charges_per_pc * qty

    tax = (total_before_tax := gold_charges + making_charges + hm_charges) * tax_rate
    total_price = total_before_tax + tax

    return (
        hm_rate,
        gold_charges,
        making_charges,
        hm_charges,
        tax,
        total_price,
    )


# print(gold_sell())


def gold_making_charges(
    gold_rate=6500,
    gold_weight=1,
    total_price=7415,
    hm_charges=45,
    no_pcs=1,
    gst=3,
    extra_charges=0,
    carat=22,
    is_22k=True,
):
    """
    calculate_making_charges AI is creating summary for calculate_making_charges

    [extended_summary]
    """

    if is_22k:
        pass
    else:
        gold_rate = gold_rate * (carat / 24)

    expr_1 = 1 + gst / 100
    expr_2 = gold_rate * gold_weight
    expr_3 = total_price - expr_1 * (extra_charges + hm_charges * no_pcs)

    making_charge_perc = ((expr_3 / expr_2) - expr_1) * (100 / expr_1)
    making_charges = (making_charge_perc / 100) * expr_2

    return (
        making_charge_perc,
        making_charges,
    )


# print(gold_making_charges())


def cost_price_gold(
    gold_rate=9100,
    goldsmith_loss_perc=3,
    baseline=0.92,
    carat=22,
    extra_charges=0,
    total_weight=1,
    is_22k=True,
):
    """
    The cost price of gold is the following
            cost_of_24k_metal * (baseline * (total_weight + goldsmith_loss))
    Where
    - **"cost_of_24k_metal"** is the gold rate in 24k purity
    - **"baseline"** is the purity level demanded by the goldsmith for making charges
        - For 22k gold, this is 0.92 or 0.9166 (note that 0.92 is excess and is deliberately kept by some goldsmiths to slightly
        hike the making charges; can be negotiated)
        - for 18k gold, this is 0.755 or 0.75 and so on
    - **"total_weight"** is the total weight of the gold in grams (or respective carat/purity)
    - **"goldsmith_loss_perc"** is the percentage of gold (of respective ornament purity) that is charged by the goldsmith for designing the ornament

    Returnables:
    - **"total_pure_wt"**: The total pure weight of gold in grams (of respective carat/purity)
    - **"goldsmith_loss_wt"**: The weight of gold (of respective carat/purity) that is charged by the goldsmith for designing the ornament
    - **"total_payable_wt"**: The total weight of pure 24k gold that is payable to the goldsmith
    - **"excess_wt"**: total_payable_wt - total_pure_wt; Basically the excess weight (in 24k) that the goldsmith charges for making charges
    - **"breakeven_making_perc"**: The making charges that the shopkeeper needs to charge to break even, that is recover the 'excess_wt'
    - **"cp_total"**: The total cost price of the gold ornament, including the extra charges (if any)
    """

    if is_22k:
        gold_rate_24k = gold_rate / (22.0 / 24.0)
    else:
        gold_rate_24k = gold_rate
    total_pure_wt = total_weight * (carat / 24.0)
    goldsmith_loss_wt = total_weight * (
        goldsmith_loss_perc / 100.0
    )  # ? goldsmith loss in same purity as 'total_weight'
    total_payable_wt = (
        total_weight + goldsmith_loss_wt
    ) * baseline  # ? this is the total payable to the goldsmith in 24k purity
    excess_wt = (
        total_payable_wt - total_pure_wt
    )  # ? this is the excess weight (in 24k) that the goldsmith charges for making charges
    breakeven_making_perc = ((total_payable_wt - total_pure_wt) / total_pure_wt) * 100.0

    excess_wt_24k_price = excess_wt * gold_rate_24k
    cost_price_gold = total_payable_wt * gold_rate_24k
    cp_total = cost_price_gold + extra_charges

    return (
        total_pure_wt,
        goldsmith_loss_wt,
        total_payable_wt,
        excess_wt,
        excess_wt_24k_price,
        breakeven_making_perc,
        cp_total,
    )


# print(cost_price_gold())
