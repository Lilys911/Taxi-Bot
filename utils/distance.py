from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return round(R * c, 2)

def calculate_price(tariff):
    prices = {
        "standart": "15,000 - 25,000 so'm",
        "comfort": "25,000 - 40,000 so'm",
        "business": "40,000 - 60,000 so'm",
    }
    return prices[tariff]