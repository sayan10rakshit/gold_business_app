def gold_sell(
    gold_rate=6500,
    qty=1,
    weight=1,
    making_charge_perc=14,
    hm_charges_per_pc=53,
    extra_charges=0,
    carat=22,
    is_22k=True,
):
    if is_22k:
        hm_rate = gold_rate
        carat = 22
    else:
        hm_rate = gold_rate * (carat / 24)
    gold_charges = hm_rate * weight
    making_charges = gold_charges * (making_charge_perc / 100) + extra_charges
    hm_charges = hm_charges_per_pc * qty

    tax = (total_before_tax := gold_charges + making_charges + hm_charges) * 0.03
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


def cost_price_gold(
    gold_rate=6500,
    making_perc=3,
    baseline=0.92,
    carat=22,
    extra_charges=0,
    total_weight=1,
    is_22k=True,
):
    """
    The cost price of gold is the following
            cost_of_24k_metal * (making_charge_wt + pure_wt)

    making perc is levied on a per gram basis

    For 22k gold, the total cp is calculated as (0.92 + making_perc/100) * 24k_rate * total_wt
    Instead of 0.9166... the goldsmiths levy making perc on 0.92
    WE NEED TO FIND A FIX FOR THIS BASELINE (0.92) TO MAKE THIS GENERIC
    Thus for 1g of ornament, a goldsmith requires (0.92 + making_perc/100)g of pure gold
    """

    if is_22k:
        gold_rate_24k = gold_rate * (24 / 22.0)
    else:
        gold_rate_24k = gold_rate
    pure_wt = total_weight * (carat / 24.0)
    actual_making_perc = baseline - (carat / 24.0) + making_perc / 100.0
    making_charge_wt = total_weight * actual_making_perc
    making_charges = making_charge_wt * gold_rate_24k
    cp = (pure_wt + making_charge_wt) * gold_rate_24k + extra_charges

    return (
        pure_wt,
        making_charge_wt,
        actual_making_perc,
        making_charges,
        cp,
    )


# print(cost_price_gold())


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
