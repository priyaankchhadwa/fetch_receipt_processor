import math
import re

def calculate_points(receipt):
    points = 0

    # 1. One point for every alphanumeric character in retailer name
    points += len(re.findall(r'[a-zA-Z0-9]', receipt.retailer))

    # 2. 50 points if total is a round dollar amount
    if receipt.total.is_integer():
        points += 50

    # 3. 25 points if total is a multiple of 0.25
    if receipt.total % 0.25 == 0:
        points += 25

    # 4. 5 points for every two items
    points += (len(receipt.items) // 2) * 5

    # 5. Points for item descriptions
    for item in receipt.items:
        trimmed_desc = item.short_description.strip()
        if len(trimmed_desc) % 3 == 0:
            # Multiply price by 0.2 and round up
            desc_points = math.ceil(item.price * 0.2)
            points += desc_points

    # 6. 6 points if purchase day is odd
    if receipt.purchase_date.day % 2:
        points += 6

    # 7. 10 points if purchase time is between 2pm and 4pm
    if 14 <= receipt.purchase_time.hour < 16:
        points += 10

    return points