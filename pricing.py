def price_for(item, qty, customer_type, day, coupon, season, loyalty_points):
    price = float(item["price"])
    cost = float(item["cost"])
    total = price * qty
    if customer_type == "member":
        if loyalty_points > 1000:
            total = total * 0.85
        elif loyalty_points > 500:
            total = total * 0.9
        elif loyalty_points > 100:
            total = total * 0.95
        else:
            total = total * 0.98
    elif customer_type == "staff":
        total = total * 0.8
    elif customer_type == "wholesale":
        if qty > 100:
            total = total * 0.75
        elif qty > 50:
            total = total * 0.8
        elif qty > 20:
            total = total * 0.88
        else:
            total = total * 0.95
    if day == "Sunday":
        if item["category"] == "grocery":
            total = total - 50
        elif item["category"] == "dairy":
            total = total - 30
    elif day == "Poya":
        if item["category"] == "household":
            total = total * 0.9
    if coupon:
        if coupon == "NEW10":
            total = total * 0.9
        elif coupon == "FEST20":
            if season == "festival":
                total = total * 0.8
            else:
                total = total * 0.95
        elif coupon == "FREESHIP":
            total = total
        elif coupon.startswith("STAFF"):
            if customer_type != "staff":
                total = total * 0.97
    if season == "festival":
        if item["category"] == "grocery":
            total = total * 1.05
    if total < cost * qty:
        if customer_type == "staff":
            total = cost * qty
        elif qty > 50:
            total = cost * qty * 1.01
        else:
            total = cost * qty * 1.05
    return round(total, 2)


def delivery_charge(distance, weight, express, member, area, weekend, fragile):
    charge = 0
    if area == "Colombo":
        if distance < 5:
            charge = 150
        elif distance < 10:
            charge = 250
        else:
            charge = 350
    elif area == "Gampaha":
        if distance < 10:
            charge = 300
        elif distance < 20:
            charge = 450
        else:
            charge = 600
    elif area == "Kandy":
        charge = 900
    else:
        if distance < 50:
            charge = 1200
        elif distance < 100:
            charge = 1800
        else:
            charge = 2500
    if weight > 10:
        if weight > 25:
            charge = charge + 500
        else:
            charge = charge + 200
    if express:
        if weekend:
            charge = charge * 2
        else:
            charge = charge * 1.5
    if fragile:
        charge = charge + 150
    if member:
        if charge > 1000:
            charge = charge - 200
        else:
            charge = charge * 0.9
    return charge
