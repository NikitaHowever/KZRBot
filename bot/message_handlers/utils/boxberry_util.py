import requests

def get_cities_list():
    token = "e058144e84382b082d6a13a6124c4584"
    url = f"https://api.boxberry.ru/json.php?token={token}&method=ListCitiesFull&CountryCode=643"

    responce = requests.get(url=url)
    json_responce = responce.json()
    print(responce)
    cities = []

    for city in json_responce:
        cities.append({"Code": city["Code"], "Name": city["Name"], "Region": city["Region"]})
    
    return cities

def get_regions(city_list):
    regions = []

    for city in city_list:
        regions.append(city["Region"])
    
    regions_set = set(regions)
    regions = list(regions_set)
    return regions

def get_points(city_code):
    token = "e058144e84382b082d6a13a6124c4584"
    url = f"https://api.boxberry.ru/json.php?token={token}&method=ListPoints&prepaid=1&CityCode={city_code}&CountryCode=643"

    responce = requests.get(url=url)

    json_responce = responce.json()

    points = []
    for point in json_responce:
        gps_arr = point["GPS"].split(",")
        points.append({"Code": point["Code"], "Name": point["Name"], "Address": point["Address"], 
        "Phone": point["Phone"], "WorkShedule": point["WorkShedule"], "Lat": gps_arr[0], "Lang": gps_arr[1]})
    
    return points



def create_parsel(order_id,price, pick2, customer_fio, customer_phone,customer_email,items):
    items_list = []
    for item in items:
        items_list.append({
            "id": item.get_id(), "name": item.get_name(), "UnitName": "шт", "nds": "10", "price": item.get_price(), 
            "quantity": item.get_quantity()})


    sdata = { "updateByTrack": "", "order_id": order_id, "PalletNumber": "", "barcode": "", "price": price, 
            "payment_sum": "", "delivery_sum": "", "issue": "", "vid": 1, "kurdost": 
            { "index": "", "citi": "", "addressp": "", "timesfrom1": "", "timesto1": "", 
            "timesfrom2": "", "timesto2": "", "timep": "", "comentk": "" }, 
            "shop": { "name": "1003", "name1": pick2 }, 
            "customer": 
            { "fio": customer_fio, "phone": customer_phone, "phone2": "", "email": customer_email, 
            "name": "", "address": "", "inn": "", "kpp": "", "r_s": "", "bank": "", "kor_s": "", "bik": "" }, 
            "items": items_list, 
            "notice": "Примечание к заказу", 
            "weights": { "weight": "1000", "x": "10", "y": "10", "z": "10", "barcode": "", "weight2": "200", 
            "barcode2": "", "x2": "10", "y2": "10", "z2": "10" } }

    url = "https://api.boxberry.ru/json.php"

    url_encode_data = {"method": "ParselCreate", "token": "e058144e84382b082d6a13a6124c4584", sdata: sdata}
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
    responce = requests.post(url, data=url_encode_data, headers=headers)

    json_responce = responce.json()
    return json_responce["track"]
