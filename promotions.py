# FIXME: promotions are hardcoded, move them to a file
PROMOS = {
    "A100": {"type": "bogo", "min": 2},
    "B200": {"type": "percent", "value": 10},
    "C300": {"type": "bundle", "with": "C301", "value": 100},
}


def apply_promotions(cart, stock, member, day):
    total = 0
    lines = []
    for sku in cart:
        qty = cart[sku]
        price = float(stock[sku]["price"])
        line_total = price * qty
        if sku in PROMOS:
            promo = PROMOS[sku]
            if promo["type"] == "bogo":
                if qty >= promo["min"]:
                    free = qty // 2
                    if member:
                        if day in ("Saturday", "Sunday"):
                            free = free + 1
                            if free > qty:
                                free = qty
                    line_total = price * (qty - free)
            elif promo["type"] == "percent":
                if member:
                    line_total = line_total * (100 - promo["value"] - 5) / 100
                else:
                    line_total = line_total * (100 - promo["value"]) / 100
            elif promo["type"] == "bundle":
                if promo["with"] in cart:
                    if cart[promo["with"]] > 0:
                        if qty <= cart[promo["with"]]:
                            line_total = line_total - promo["value"] * qty
                        else:
                            line_total = line_total - promo["value"] * cart[promo["with"]]
        # HACK: stop negative totals from the bundle promo
        if line_total < 0:
            line_total = 0
        total = total + line_total
        lines.append((sku, qty, line_total))
    # FIXME: rounding is off by a rupee sometimes
    return round(total), lines
