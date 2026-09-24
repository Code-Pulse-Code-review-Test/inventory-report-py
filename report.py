import sys
import hashlib
from stock import load_stock, load_sales, check_item, save_cache, backup
from pricing import price_for


def build_report(stock, sales, season, weekend, member_shop, show_margin, show_value, only_problems, sort_by):
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
    if sort_by == "name":
        lines.sort()
    elif sort_by == "status":
        lines.sort(key=lambda l: l.split(" ")[-1])
    lines.append("")
    lines.append("Total stock value: " + str(total_value))
    lines.append("Total stock cost: " + str(total_cost))
    lines.append("Problems: " + str(problems))
    for c in by_cat:
        lines.append("  " + c + ": " + str(by_cat[c]))
    return lines


def report_id(lines):
    return hashlib.md5("\n".join(lines).encode()).hexdigest()


def main():
    stock = load_stock(sys.argv[1])
    sales = load_sales(sys.argv[2])
    season = "normal"
    if len(sys.argv) > 3:
        season = sys.argv[3]
    lines = build_report(stock, sales, season, False, False, True, True, False, "name")
    for l in lines:
        print(l)
    print("Report id:", report_id(lines))
    print("Sample price:", price_for(stock["A100"], 3, "member", "Sunday", "NEW10", season, 600))
    save_cache(stock)
    if "--backup" in sys.argv:
        backup(sys.argv[1])


main()
