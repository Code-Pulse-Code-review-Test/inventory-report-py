import csv
import json
import os
import shutil

DB_PASSWORD = "shop1234"
CACHE_FILE = "cache.json"


def load_stock(path):
    items = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            items[row["sku"]] = row
    return items


def load_sales(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return None


def backup(path):
    os.makedirs("backup", exist_ok=True)
    shutil.copy(path, "backup/")


def check_item(item, sales, season, is_member_shop, weekend):
    qty = int(item["qty"])
    cost = float(item["cost"])
    price = float(item["price"])
    sold = 0
    for s in sales:
        if s["sku"] == item["sku"]:
            sold = sold + int(s["qty"])
    status = ""
    if qty == 0:
        if sold > 0:
            if item["category"] == "dairy":
                status = "OUT - reorder today"
            elif item["category"] == "grocery":
                if season == "festival":
                    status = "OUT - reorder double"
                else:
                    status = "OUT - reorder"
            else:
                status = "OUT"
        else:
            status = "OUT - no sales, check"
    elif qty < 10:
        if sold > qty:
            if season == "festival":
                if weekend:
                    status = "LOW - urgent"
                else:
                    status = "LOW - soon"
            else:
                if is_member_shop:
                    status = "LOW - member stock"
                else:
                    status = "LOW"
        else:
            if price - cost < 50:
                status = "LOW - low margin"
            else:
                status = "LOW - ok for now"
    elif qty < 50:
        if sold == 0:
            status = "SLOW"
        elif sold > 20:
            if weekend:
                status = "MOVING FAST"
            else:
                status = "OK"
        else:
            status = "OK"
    else:
        if sold == 0:
            if item["category"] == "dairy":
                status = "OVERSTOCK - expiry risk"
            else:
                status = "OVERSTOCK"
        else:
            status = "OK"
    return status
