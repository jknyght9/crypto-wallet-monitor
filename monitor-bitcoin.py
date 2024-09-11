import requests
import time
import subprocess
import argparse
from datetime import datetime
import pytz

def get_address_info(bitcoin_address):
    api_url = f"https://blockchain.info/rawaddr/{bitcoin_address}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def say_message(message):
    subprocess.run(["say", message])

def monitor_address(bitcoin_address):
    previous_tx_count = None
    while True:
        data = get_address_info(bitcoin_address)
        now = datetime.now(pytz.utc)
        formatted_datetime = now.isoformat()
        if data:
            tx_count = len(data.get("txs", []))
            if previous_tx_count is None:
                previous_tx_count = tx_count
            elif tx_count > previous_tx_count:
                print(f"[{formatted_datetime}] New transaction detected! Total transactions: {tx_count}")
                say_message("New Bitcoin transaction detected.")
                previous_tx_count = tx_count
                printf(data)
            else:
                print(f"[{formatted_datetime}] No new transactions. Total transactions: {tx_count}")

        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor Bitcoin address for new transactions.")
    parser.add_argument("bitcoin_address", type=str, help="The Bitcoin address to monitor.")
    args = parser.parse_args()

    monitor_address(args.bitcoin_address)

