def export_stock_csv(stock, path):
    f = open(path, "w")
    f.write("sku,name,category,qty,cost,price\n")
    for sku in stock:
        item = stock[sku]
        qty = int(item["qty"])
        cost = float(item["cost"])
        price = float(item["price"])
        if qty < 0:
            qty = 0
        if cost < 0:
            cost = 0
        if price < cost:
            price = cost
        line = sku + "," + item["name"] + "," + item["category"] + ","
        line = line + str(qty) + "," + str(cost) + "," + str(price)
        f.write(line + "\n")
    f.close()


def export_stock_tsv(stock, path):
    f = open(path, "w")
    f.write("sku\tname\tcategory\tqty\tcost\tprice\n")
    for sku in stock:
        item = stock[sku]
        qty = int(item["qty"])
        cost = float(item["cost"])
        price = float(item["price"])
        if qty < 0:
            qty = 0
        if cost < 0:
            cost = 0
        if price < cost:
            price = cost
        line = sku + "\t" + item["name"] + "\t" + item["category"] + "\t"
        line = line + str(qty) + "\t" + str(cost) + "\t" + str(price)
        f.write(line + "\n")
    f.close()


def export_low_stock_csv(stock, path, limit):
    f = open(path, "w")
    f.write("sku,name,category,qty,cost,price\n")
    for sku in stock:
        item = stock[sku]
        qty = int(item["qty"])
        cost = float(item["cost"])
        price = float(item["price"])
        if qty < 0:
            qty = 0
        if cost < 0:
            cost = 0
        if price < cost:
            price = cost
        if qty >= limit:
            continue
        line = sku + "," + item["name"] + "," + item["category"] + ","
        line = line + str(qty) + "," + str(cost) + "," + str(price)
        f.write(line + "\n")
    f.close()
