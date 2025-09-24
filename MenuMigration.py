import csv
import requests
import json
import time

#oldResId = "67c316b58d19793f7e6492df"
#newResId = "68335552b1cfc2b91788a6b3"
newResId = "68d21251ab9c83fc3c45551b"

#SourceEndpoint = "https://core.baksish.in/api/restaurant-menu/menu/"+oldResId
TargetEndpoint = "https://core-v1.xoup.co.in/api/v1/menu/"+newResId
# TargetEndpoint = "https://core-v1-ocbi.onrender.com/api/v1/menu/"+newResId
Authtoken = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNjhkMjEyNTFhYjljODNmYzNjNDU1NTJkIiwibmFtZSI6IkVrYW1yYSBSYW5qYW4gU2Fob28gIiwiZW1haWwiOiJ3cml0b2dyYXBoZXJla2FtcmFAZ21haWwuY29tIiwicGhvbmUiOiI2MzcxNTkwOTg5Iiwicm9sZSI6WyJTVVBFUkFETUlOIl0sImFjY2Vzc19yb3V0ZXMiOlsiL2Rhc2hib2FyZCIsIi9kYXNoYm9hcmQvbWVudS9hZGQtaXRlbSIsIi9kYXNoYm9hcmQvbWVudS92aWV3LW1lbnUiLCIvZGFzaGJvYXJkL21lbnUvdmlldy1hZGRvbi1jdXN0b21pemVycyIsIi9kYXNoYm9hcmQvYmlsbGluZy9jdXJyZW50LW9yZGVyIiwiL2Rhc2hib2FyZC9iaWxsaW5nL2NyZWF0ZS1vcmRlciIsIi9kYXNoYm9hcmQvY29uZmlnL21lbnUtdmlldyIsIi9kYXNoYm9hcmQvc2V0dGluZ3MvYmFzaWMtZGV0YWlscyIsIi9kYXNoYm9hcmQvc2V0dGluZ3MvYnVzaW5lc3MtZGV0YWlscyIsIi9kYXNoYm9hcmQvc2V0dGluZ3MvYWNjb3VudCJdLCJyZXN0YXVyYW50Ijp7ImlkIjoiNjhkMjEyNTFhYjljODNmYzNjNDU1NTFiIiwibmFtZSI6IlRoZSBDb21ibyIsImVtYWlsIjoid3JpdG9ncmFwaGVyZWthbXJhQGdtYWlsLmNvbSIsInBob25lIjoiNjM3MTU5MDk4OSIsImxvZ29VcmwiOiJodHRwczovL3Jlcy5jbG91ZGluYXJ5LmNvbS9kcjlnd2txYXAvaW1hZ2UvdXBsb2FkL3YxNzU4NTk3NTQwL0lNRy0yMDI1MDMwMi1XQTAwMTBfd29hemhyLmpwZyIsImNnc3QiOjAsInNnc3QiOjAsImRpc2NvdW50IjpudWxsLCJhZGRyZXNzIjoiU2hvcCBuby0gQTMsIFNhbG9taSBDb21wbGV4LCBHaGF0aWtpYSwgQmh1YmFuZXN3YXIgIiwiaXNWZWdPbmx5IjpmYWxzZSwiaXNDYXNoT25seSI6ZmFsc2UsImlzT3BlbiI6dHJ1ZSwiaXNTZWF0aW5nIjp0cnVlLCJ0eXBlIjoiUVNSIiwiZGVzY3JpcHRpb24iOiIiLCJpc0FjdGl2ZSI6dHJ1ZSwiaXNUYWtlYXdheSI6dHJ1ZSwiZmVlZEJhY2t1cmwiOiIiLCJzdGF0aWNQYXltZW50UVJDb2RlIjpudWxsLCJzZW5kUGF5bWVudFFSQ29kZSI6ZmFsc2UsInRhYmxlcyI6IjQiLCJhbGlhcyI6IlRPOTAiLCJyZXZpZXdVcmwiOiIiLCJhZGRpdGlvbmFsSW5mbyI6bnVsbCwiY2F0ZWdvcmllcyI6WyJJbmRpYW4iLCJDaGluZXNlIl0sInBhcmVudENhdGVnb3JpZXMiOltdLCJjdXN0b21pemVyQ2F0ZWdvcmllcyI6W10sIm9wZW5pbmdUaW1lIjoiMTI6MDAiLCJjbG9zaW5nVGltZSI6IjIzOjU5In0sIm1lbnVWaWV3cyI6W119LCJpYXQiOjE3NTg2ODMwNDksImV4cCI6MTc1ODcxMTg0OX0.56UE5-tPG5XhJQQqyVKOpDiZZ3MhYUUsKTSO0yPB1zs'


session = requests.Session()
session.headers.update({
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': Authtoken
})


def post_menu_item(data):
    endpoint = TargetEndpoint
 
    try:
        print(f"Posting menu item: {data}")
        response = session.post(endpoint, json=data)
     
        if response.status_code == 201 or response.status_code == 200:
            print(f"Successfully added: {data.get("item_name")}")
            return True
        else:
            print(f"Error posting menu item: {response.status_code} - {response.text}")
            print(f"\n {response} \n")
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
            
            for size in ["r","s","l"]:
                old_price = get_value(f"old_price_{size}")
                actual_price = get_value(f"actual_price_{size}") 
                print(f"Processing {size.upper()} size: Old Price: {old_price}, Actual Price: {actual_price}")
                if old_price is not None or actual_price is not None:  
                    item_price_options.append({
                        "size": size.upper(),
                        "old_price": int(old_price) if old_price is not None else int(actual_price),
                        "current_price": int(actual_price) if actual_price is not None else int(old_price)
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
                    "availability": True
                }
            }
            time.sleep(1)
            post_menu_item(menu_item_data) 

# def fetch_menu_items(output_file):
#     endpoint = SourceEndpoint
#     try:
#         response = session.get(endpoint)
#         if response.status_code == 200:
#             data = response.json()
#             menu_items = data.get("menu", [])
#             with open(output_file, mode='w', newline='', encoding='utf-8') as csvfile:
#                 fieldnames = [
#                     "food_item_uid",
#                     "food_item_name",
#                     "restaurant_food_item_description",
#                     "food_item_image_url",
#                     "food_item_type",
#                     "food_item_category",
#                     "food_item_parent_category",
#                     "old_price_s",
#                     "old_price_m",
#                     "old_price_l",
#                     "actual_price_s",
#                     "actual_price_m",
#                     "actual_price_l",
#                     "restaurant_food_item_speciality",
#                     "restaurant_food_item_availability",
#                     "isAddOns"
#                 ]
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                 writer.writeheader()
#                 for item in menu_items:
#                     # Initialize prices
#                     old_price_s = old_price_m = old_price_l = actual_price_s = actual_price_m = actual_price_l = None
                    
#                     # Extract prices from item_price
#                     for price in item.get("item_price", []):
#                         if price.get("size") == "S":
#                             old_price_s = price.get("old_price")
#                             actual_price_s = price.get("actual_price")
#                         elif price.get("size") == "M":
#                             old_price_m = price.get("old_price")
#                             actual_price_m = price.get("actual_price")
#                         elif price.get("size") == "L":
#                             old_price_l = price.get("old_price")
#                             actual_price_l = price.get("actual_price")
                    
#                     if item.get("food_item_category")!= "Add Ons":
#                         writer.writerow({
#                             "food_item_uid": item.get("restaurant_food_item_id"),
#                             "food_item_name": item.get("food_item_name"),
#                             "restaurant_food_item_description": item.get("food_item_description"),
#                             "food_item_image_url": item.get("food_item_image_url"),
#                             "food_item_type": item.get("food_item_type"),
#                             "food_item_category": item.get("food_item_category"),
#                             "food_item_parent_category": item.get("food_item_parent_category"),
#                             "old_price_s": old_price_s,
#                             "old_price_m": old_price_m,
#                             "old_price_l": old_price_l,
#                             "actual_price_s": actual_price_s,
#                             "actual_price_m": actual_price_m,
#                             "actual_price_l": actual_price_l,
#                             "restaurant_food_item_speciality": item.get("restaurant_food_item_speciality"),
#                             "restaurant_food_item_availability": item.get("restaurant_food_item_availability"),
#                             "isAddOns": item.get("isAddOns")
#                         })
#             print(f"Data successfully exported to {output_file}")
#         else:
#             print(f"Error fetching menu items: {response.status_code} - {response.text}")
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {str(e)}")

if __name__ == "__main__":
    #fetch_menu_items("menu.csv")
    #time.sleep(5)
    process_csv("TheCombosMenu.csv")