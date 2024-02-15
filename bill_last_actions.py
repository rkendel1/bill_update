import os
import requests
import json
from datetime import datetime, timedelta



##this script will return a list of bills sorted by date of last action from the congress API and save them to a json file

def get_bill_data(api_key, start_date, start_index=0):
    url = f"https://api.congress.gov/v3/bill?api_key={api_key}&offset={start_index}&introduced_on={start_date}"

    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve data from the API.")
        return None

    data = response.json()
    return data

def save_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

def get_last_action_date(bills):
    last_action_date = None
    for bill in bills:
        action_date = datetime.strptime(bill['latestAction']['actionDate'], "%Y-%m-%d").date()
        if not last_action_date or action_date > last_action_date:
            last_action_date = action_date
    return last_action_date

def main():
    api_key = "jgLP3byCGhhRaBjxtpA8VnBHkU53LZNWCXnNAsoi"
    start_index = 0
    base_filename = "newleg_"
    start_date = "2024-01-01"

    skipped_days = 0
    while True:
        bill_data = get_bill_data(api_key, start_date, start_index)
        if not bill_data or not bill_data.get("bills"):
            print("No more bill data available.")
            break

        last_action_date = get_last_action_date(bill_data['bills'])
        filename = f"{base_filename}{last_action_date}.json"
        
        # Check if the file already exists for the previous day
        if os.path.exists(filename):
            print(f"Data for {last_action_date} already exists. Skipping...")
            skipped_days += 1
            if skipped_days >= 3:
                print("Skipped 3 consecutive days. Stopping the program.")
                break
        else:
            save_to_json(bill_data['bills'], filename)
            print(f"Saved data to {filename}")
            skipped_days = 0  # Reset the counter if data is saved

        start_index += len(bill_data['bills'])

if __name__ == "__main__":
    main()
