import csv
import requests
import json
import time

#oldResId = "67c316b58d19793f7e6492df" # Id of restaurant from which menu is to be fetched
#newResId = "68335552b1cfc2b91788a6b3"
newResId = "67eafb6bf427ecd71f64884b"  # Id of restaurant in for which menu is to be added

#SourceEndpoint = "https://core.baksish.in/api/restaurant-menu/menu/"+oldResId
#TargetEndpoint = "https://core-v1.xoup.co.in/api/v1/menu/"+newResId  # Production
TargetEndpoint = "https://core-v1-ocbi.onrender.com/api/v1/menu/"+newResId  # Staging
Authtoken = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNjdlYWZiNzBmNDI3ZWNkNzFmNjQ4ODlkIiwibmFtZSI6IkJpYnUiLCJlbWFpbCI6IjIxMDU1OTZAa2lpdC5hYy5pbiIsInBob25lIjoiOTg3NjU0MzIxMCIsInJvbGUiOlsiU1VQRVJBRE1JTiJdLCJhY2Nlc3Nfcm91dGVzIjpbIi9kYXNoYm9hcmQiLCIvZGFzaGJvYXJkL21lbnUvYWRkLWl0ZW0iLCIvZGFzaGJvYXJkL21lbnUvdmlldy1tZW51IiwiL2Rhc2hib2FyZC9tZW51L3ZpZXctYWRkb24tY3VzdG9taXplcnMiLCIvZGFzaGJvYXJkL2JpbGxpbmcvY3VycmVudC1vcmRlciIsIi9kYXNoYm9hcmQvYmlsbGluZy9jcmVhdGUtb3JkZXIiLCIvZGFzaGJvYXJkL2NvbmZpZy9tZW51LXZpZXciLCIvZGFzaGJvYXJkL3NldHRpbmdzL2Jhc2ljLWRldGFpbHMiLCIvZGFzaGJvYXJkL3NldHRpbmdzL2J1c2luZXNzLWRldGFpbHMiLCIvZGFzaGJvYXJkL3NldHRpbmdzL2FjY291bnQiXSwicmVzdGF1cmFudCI6eyJpZCI6IjY3ZWFmYjZiZjQyN2VjZDcxZjY0ODg0YiIsIm5hbWUiOiJUcmlhbEA2OSIsImVtYWlsIjoiMjEwNTU5NkBraWl0LmFjLmluIiwicGhvbmUiOiI5MzMwMjc3OTUzIiwibG9nb1VybCI6Imh0dHBzOi8vaS5wb3N0aW1nLmNjL1NLN21jR0hEL2tvamppbmxnby5wbmciLCJjZ3N0Ijo1LCJzZ3N0Ijo1LCJkaXNjb3VudCI6MTAsImFkZHJlc3MiOiI2NC8yLzgsIFJhamEgUmFtTW9oYW4gcm95IHJvYWQsIFNodWthbnRhIE5hZ2FyLCBCZWhhbGEgQ2hvd3Jhc3RhLCBLb2xrYXRhIC0wOCIsImlzVmVnT25seSI6ZmFsc2UsImlzQ2FzaE9ubHkiOnRydWUsImlzT3BlbiI6dHJ1ZSwiaXNTZWF0aW5nIjp0cnVlLCJ0eXBlIjoiQ2FzdWFsIERpbmluZyIsImRlc2NyaXB0aW9uIjoiQSBjb3p5IHBsYWNlIHNlcnZpbmcgZGVsaWNpb3VzIG1lYWxzLiIsImlzQWN0aXZlIjp0cnVlLCJpc1Rha2Vhd2F5Ijp0cnVlLCJmZWVkQmFja3VybCI6Imh0dHBzOi8vZXhhbXBsZS5jb20vZmVlZGJhY2siLCJzdGF0aWNQYXltZW50UVJDb2RlIjoiaHR0cHM6Ly9yZXMuY2xvdWRpbmFyeS5jb20vZHI5Z3drcWFwL2ltYWdlL3VwbG9hZC92MTc0NTE0NTY0My9xci1jb2RlXzRfY29nY25wLnBuZyIsInNlbmRQYXltZW50UVJDb2RlIjp0cnVlLCJ0YWJsZXMiOiIyMCIsImFsaWFzIjoiVEwzOCIsInJldmlld1VybCI6Imh0dHBzOi8vc2VhcmNoLmdvb2dsZS5jb20vbG9jYWwvd3JpdGVyZXZpZXc_cGxhY2VpZD1DaElKNDZKRm5kaW5HVG9SN2YzOVpEajl3TG8iLCJhZGRpdGlvbmFsSW5mbyI6bnVsbCwiY2F0ZWdvcmllcyI6WyJTdGFydGVycyIsIkRlc3NlcnRzIiwiUmljZSBBbmQgTm9vZGxlcyIsIlJhbWVuIiwiS29qamluIFNwZWNpYWxzIiwiU3BhcmtsaW5nIFdhdGVyIEJhc2UiLCJNaWxrIEJhc2UiLCJIb3QgQmV2ZXJhZ2VzIiwiUmVmcmVzaGVycyIsIk1pbmVyYWwgd2F0ZXIiLCJUSEFJIiwiRVhPVElDIl0sInBhcmVudENhdGVnb3JpZXMiOlsiRm9vZCIsIkRyaW5rcyJdLCJjdXN0b21pemVyQ2F0ZWdvcmllcyI6WyJOT04gVkVHIFNUQVJURVIiLCJDdXN0b20iXSwib3BlbmluZ1RpbWUiOiIxMDowMCBBTSIsImNsb3NpbmdUaW1lIjoiMTE6MDAgUE0ifSwibWVudVZpZXdzIjpbeyJfaWQiOiI2N2ViMDAwNWIzMjYwODZiMDdkODQyMGIiLCJuYW1lIjoiRGluZSBJbiIsInJlc3RhdXJhbnRfcmVmX2lkIjoiNjdlYWZiNmJmNDI3ZWNkNzFmNjQ4ODRiIiwiZGlzcGxheV9jYXRlZ29yaWVzIjpbIlN0YXJ0ZXJzIiwiUmFtZW4iLCJNaWxrIEJhc2UiLCJNaW5lcmFsIHdhdGVyIiwiRGVzc2VydHMiLCJLb2pqaW4gU3BlY2lhbHMiLCJIb3QgQmV2ZXJhZ2VzIiwiUmljZSBBbmQgTm9vZGxlcyIsIlNwYXJrbGluZyBXYXRlciBCYXNlIiwiUmVmcmVzaGVycyIsIlRIQUkiLCJFWE9USUMiXSwiaXNfYWN0aXZlIjp0cnVlLCJpc19kZWxldGVkIjpmYWxzZSwiaXNfcHJlX3BheW1lbnRfZW5hYmxlZCI6ZmFsc2UsImlzX3RhYmxlX3N5c3RlbSI6dHJ1ZSwiZW5kaW5nX3RhYmxlX251bWJlciI6MTAsInN0YXJ0aW5nX3RhYmxlX251bWJlciI6MX0seyJfaWQiOiI2N2YyNjcxNTFkYzEzZjUzNjEzZDcyZmQiLCJuYW1lIjoiUVNSIiwicmVzdGF1cmFudF9yZWZfaWQiOiI2N2VhZmI2YmY0MjdlY2Q3MWY2NDg4NGIiLCJkaXNwbGF5X2NhdGVnb3JpZXMiOlsiU3RhcnRlcnMiLCJSYW1lbiIsIk1pbGsgQmFzZSIsIk1pbmVyYWwgd2F0ZXIiLCJEZXNzZXJ0cyIsIkhvdCBCZXZlcmFnZXMiLCJSaWNlIEFuZCBOb29kbGVzIiwiUmVmcmVzaGVycyJdLCJpc19hY3RpdmUiOnRydWUsImlzX2RlbGV0ZWQiOmZhbHNlLCJpc19wcmVfcGF5bWVudF9lbmFibGVkIjp0cnVlLCJpc190YWJsZV9zeXN0ZW0iOmZhbHNlLCJlbmRpbmdfdGFibGVfbnVtYmVyIjoxMiwic3RhcnRpbmdfdGFibGVfbnVtYmVyIjoxfV19LCJpYXQiOjE3NTg3MzczMjQsImV4cCI6MTc1ODc2NjEyNH0.1_Bpx07vqe4tlHmA_68xkb-fgtkFayphcW1fPtKTqiA'


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