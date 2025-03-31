import csv
import requests
import json
import time

SourceEndpoint = "https://baksish-backend-ms-1.onrender.com/api/restaurant-menu/menu/67603178fd5ffa67f1042b84"
TargetEndpoint = "http://localhost:5012/api/v1/menu/67d54499c27a0e8283d0720d"


session = requests.Session()
session.headers.update({
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.Z291cm1ldGh1YkBleGFtcGxlMS5jb20.aNlgWkETZaSSdoF7rjuYjYpD5vyYwz1pthVJ4m-UtBs'
})


def post_menu_item(data):
    endpoint = TargetEndpoint
 
    try:
        response = session.post(endpoint, json=data)
     
        if response.status_code == 201:
            print(f"Successfully added: {data.get("food_item_name")}")
            return True
        else:
            print(f"Error posting menu item: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return False

def process_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Helper function to handle null values
            def get_value(key):
                return row.get(key) if row.get(key) not in ["", None] else None
            
            # Prepare Menu Item Data with multiple sizes
            item_price_options = []
            
            for size in ["s", "m", "l"]:
                old_price = get_value(f"old_price_{size}")
                actual_price = get_value(f"actual_price_{size}") 
                if old_price is not None:  
                    item_price_options.append({
                        "size": size.upper(),
                        "old_price": int(old_price),
                        "current_price": int(actual_price)
                    })

            if len(item_price_options) == 1:
                item_price_options[0]['size'] = 'R'


            menu_item_data = {
                "item_name": get_value("food_item_name"),
                "item_price_options": item_price_options,
                "item_description": get_value("restaurant_food_item_description"),
                "item_image_url": get_value("food_item_image_url"),
                "item_tags": {
                    "category": get_value("food_item_category"),
                    "parent_category": get_value("food_item_parent_category"),
                    "is_veg": get_value("food_item_type") == "Vegetarian",  
                    "availability": get_value("restaurant_food_item_availability") == True
                }
            }
            
            post_menu_item(menu_item_data)
            time.sleep(5) 

def fetch_menu_items(output_file):
    endpoint = SourceEndpoint
    try:
        response = session.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            menu_items = data.get("menu", [])
            with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    "food_item_uid",
                    "food_item_name",
                    "restaurant_food_item_description",
                    "food_item_image_url",
                    "food_item_type",
                    "food_item_category",
                    "food_item_parent_category",
                    "old_price_s",
                    "old_price_m",
                    "old_price_l",
                    "actual_price_s",
                    "actual_price_m",
                    "actual_price_l",
                    "restaurant_food_item_speciality",
                    "restaurant_food_item_availability",
                    "isAddOns"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in menu_items:
                    # Initialize prices
                    old_price_s = old_price_m = old_price_l = actual_price_s = actual_price_m = actual_price_l = None
                    
                    # Extract prices from item_price
                    for price in item.get("item_price", []):
                        if price.get("size") == "S":
                            old_price_s = price.get("old_price")
                            actual_price_s = price.get("actual_price")
                        elif price.get("size") == "M":
                            old_price_m = price.get("old_price")
                            actual_price_m = price.get("actual_price")
                        elif price.get("size") == "L":
                            old_price_l = price.get("old_price")
                            actual_price_l = price.get("actual_price")
                    
                    writer.writerow({
                        "food_item_uid": item.get("restaurant_food_item_id"),
                        "food_item_name": item.get("food_item_name"),
                        "restaurant_food_item_description": item.get("food_item_description"),
                        "food_item_image_url": item.get("food_item_image_url"),
                        "food_item_type": item.get("food_item_type"),
                        "food_item_category": item.get("food_item_category"),
                        "food_item_parent_category": item.get("food_item_parent_category"),
                        "old_price_s": old_price_s,
                        "old_price_m": old_price_m,
                        "old_price_l": old_price_l,
                        "actual_price_s": actual_price_s,
                        "actual_price_m": actual_price_m,
                        "actual_price_l": actual_price_l,
                        "restaurant_food_item_speciality": item.get("restaurant_food_item_speciality"),
                        "restaurant_food_item_availability": item.get("restaurant_food_item_availability"),
                        "isAddOns": item.get("isAddOns")
                    })
            print(f"Data successfully exported to {output_file}")
        else:
            print(f"Error fetching menu items: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")

if __name__ == "__main__":
    fetch_menu_items("MenuItem.csv")
    time.sleep(5)
    process_csv("MenuItem.csv")