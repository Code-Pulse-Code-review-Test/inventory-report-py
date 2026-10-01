import hashlib
import os
import subprocess
import sys
from datetime import date

from stock import load_stock, load_sales

REORDER_LEVEL = 10
ORDER_FOLDER = "orders"

SUPPLIER_EMAILS = {
    "S1": "orders@lankagrains.lk",
    "S2": "sales@cleanhome.lk",
    "S3": "dispatch@hillmilk.lk",
}


def order_id(supplier, day):
    return hashlib.md5((supplier + str(day)).encode()).hexdigest()[:8]


def build_orders(stock, sales):
    orders = {}
    for sku in stock:
        item = stock[sku]
        qty = int(item["qty"])
        sold = 0
        for s in sales:
            if s["sku"] == sku:
                sold = sold + int(s["qty"])
        if qty < REORDER_LEVEL or sold > qty:
            amount = max(sold * 2, REORDER_LEVEL * 2) - qty
            if item["supplier"] not in orders:
                orders[item["supplier"]] = []
            orders[item["supplier"]].append((sku, item["name"], amount))
    return orders


def write_order(supplier, lines):
    os.makedirs(ORDER_FOLDER, exist_ok=True)
    path = ORDER_FOLDER + "/" + supplier + "_" + order_id(supplier, date.today()) + ".txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("Purchase order for " + supplier + " - " + str(date.today()) + "\n")
        for sku, name, amount in lines:
            f.write(sku + "  " + name.ljust(20) + "  " + str(amount) + "\n")
    return path


def send_order(path, supplier):
    # uses the mail command on the shop pc
    email = SUPPLIER_EMAILS.get(supplier)
    if email is None:
        print("no email for supplier", supplier)
        return
    with open(path, encoding="utf-8") as f:
        subprocess.run(["mail", "-s", "Purchase order", email], stdin=f, check=False)


def main():
    stock = load_stock(sys.argv[1])
    sales = load_sales(sys.argv[2])
    orders = build_orders(stock, sales)
    for supplier in orders:
        path = write_order(supplier, orders[supplier])
        print("wrote", path)
        if "--send" in sys.argv:
            send_order(path, supplier)
            print("sent to", supplier)


if __name__ == "__main__":
    main()
