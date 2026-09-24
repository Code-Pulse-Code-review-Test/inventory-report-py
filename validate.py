def validate_row(row, known_suppliers, strict):
    errors = []
    if not row.get("sku"):
        errors.append("missing sku")
    elif len(row["sku"]) != 4:
        errors.append("bad sku length")
    elif not row["sku"][0].isalpha():
        errors.append("sku must start with a letter")
    if not row.get("name"):
        errors.append("missing name")
    elif len(row["name"]) > 40:
        errors.append("name too long")
    if not row.get("category"):
        errors.append("missing category")
    elif row["category"] not in ("grocery", "household", "dairy", "bakery", "frozen"):
        if strict:
            errors.append("unknown category")
    if not row.get("qty"):
        errors.append("missing qty")
    elif not row["qty"].isdigit():
        errors.append("qty not a number")
    elif int(row["qty"]) > 10000:
        errors.append("qty too big")
    if not row.get("cost"):
        errors.append("missing cost")
    else:
        try:
            cost = float(row["cost"])
            if cost < 0:
                errors.append("negative cost")
            elif cost == 0 and strict:
                errors.append("zero cost")
        except ValueError:
            errors.append("cost not a number")
    if not row.get("price"):
        errors.append("missing price")
    else:
        try:
            price = float(row["price"])
            if price < 0:
                errors.append("negative price")
            elif row.get("cost") and price < float(row["cost"]):
                errors.append("price below cost")
            elif price > 100000:
                errors.append("price too high")
        except ValueError:
            errors.append("price not a number")
    if not row.get("supplier"):
        if strict:
            errors.append("missing supplier")
    elif row["supplier"] not in known_suppliers:
        errors.append("unknown supplier")
    if row.get("expiry"):
        parts = row["expiry"].split("-")
        if len(parts) != 3:
            errors.append("bad expiry format")
        elif not parts[0].isdigit() or len(parts[0]) != 4:
            errors.append("bad expiry year")
        elif not parts[1].isdigit() or int(parts[1]) > 12 or int(parts[1]) < 1:
            errors.append("bad expiry month")
        elif not parts[2].isdigit() or int(parts[2]) > 31 or int(parts[2]) < 1:
            errors.append("bad expiry day")
    elif row.get("category") == "dairy" and strict:
        errors.append("dairy needs expiry")
    if row.get("discount"):
        if not row["discount"].isdigit():
            errors.append("discount not a number")
        elif int(row["discount"]) > 50:
            errors.append("discount too big")
        elif int(row["discount"]) > 20 and row.get("category") == "dairy":
            errors.append("dairy discount too big")
    if row.get("barcode"):
        if len(row["barcode"]) not in (8, 12, 13):
            errors.append("bad barcode length")
        elif not row["barcode"].isdigit():
            errors.append("barcode not a number")
    if row.get("shelf"):
        if row["shelf"][0] not in "ABCDEF":
            errors.append("unknown aisle")
        elif len(row["shelf"]) > 3:
            errors.append("bad shelf code")
    return errors


def weekly_summary(stock, sales, returns, damaged, week, show_all):
    summary = {"sold": 0, "returned": 0, "damaged": 0, "revenue": 0, "notes": []}
    for sku in stock:
        item = stock[sku]
        price = float(item["price"])
        sold = 0
        for s in sales:
            if s["sku"] == sku:
                if week is None or int(s["day"]) // 7 == week:
                    sold = sold + int(s["qty"])
        returned = 0
        for r in returns:
            if r["sku"] == sku:
                if week is None or int(r["day"]) // 7 == week:
                    returned = returned + int(r["qty"])
        bad = 0
        for d in damaged:
            if d["sku"] == sku:
                if d.get("reason") == "expired":
                    bad = bad + int(d["qty"])
                elif d.get("reason") == "broken":
                    bad = bad + int(d["qty"])
                elif show_all:
                    bad = bad + int(d["qty"])
        summary["sold"] += sold
        summary["returned"] += returned
        summary["damaged"] += bad
        summary["revenue"] += (sold - returned) * price
        if sold == 0 and returned == 0:
            if show_all:
                summary["notes"].append(sku + " no movement")
        elif returned > sold:
            summary["notes"].append(sku + " more returns than sales")
        elif returned > 0 and returned * 2 > sold:
            summary["notes"].append(sku + " high return rate")
        if bad > 0:
            if item["category"] == "dairy":
                summary["notes"].append(sku + " dairy damaged " + str(bad))
            elif bad > 10:
                summary["notes"].append(sku + " lots damaged")
            elif show_all:
                summary["notes"].append(sku + " some damaged")
        if int(item["qty"]) < sold:
            if item["category"] in ("grocery", "dairy"):
                summary["notes"].append(sku + " reorder now")
            else:
                summary["notes"].append(sku + " reorder soon")
    if summary["returned"] > summary["sold"] / 2:
        summary["notes"].append("returns are very high this week")
    if summary["damaged"] > 20:
        summary["notes"].append("check storage, lots of damage")
    if summary["revenue"] < 10000:
        summary["notes"].append("slow week")
    elif summary["revenue"] > 100000:
        summary["notes"].append("great week")
    return summary
