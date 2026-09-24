from stock import check_item


# old version, keep until the new report is checked
def build_report_old(stock, sales, season, weekend, member_shop, show_margin, show_value, only_problems, sort_by):
    lines = []
    total_value = 0
    total_cost = 0
    problems = 0
    by_cat = {}
    for sku in stock:
        item = stock[sku]
        status = check_item(item, sales, season, member_shop, weekend)
        qty = int(item["qty"])
        cost = float(item["cost"])
        price = float(item["price"])
        value = qty * price
        total_value = total_value + value
        total_cost = total_cost + qty * cost
        if item["category"] not in by_cat:
            by_cat[item["category"]] = 0
        by_cat[item["category"]] = by_cat[item["category"]] + value
        if status != "OK":
            problems = problems + 1
        if only_problems and status == "OK":
            continue
        line = item["sku"] + " " + item["name"].ljust(20) + " " + str(qty).rjust(4) + " " + status
        if show_margin:
            if price > 0:
                margin = (price - cost) / price * 100
                if margin < 10:
                    line = line + "  margin " + str(round(margin, 1)) + "% (LOW)"
                elif margin > 40:
                    line = line + "  margin " + str(round(margin, 1)) + "% (HIGH)"
                else:
                    line = line + "  margin " + str(round(margin, 1)) + "%"
            else:
                line = line + "  margin n/a"
        if show_value:
            line = line + "  value " + str(value)
        lines.append(line)
    lines.append("")
    lines.append("Total stock value: " + str(total_value))
    lines.append("Total stock cost: " + str(total_cost))
    lines.append("Problems: " + str(problems))
    for c in by_cat:
        lines.append("  " + c + ": " + str(by_cat[c]))
    return lines
