import argparse
import csv
import sys

import requests

API_VERSION = 'v1'
PARSER = argparse.ArgumentParser(description='Delete Trend Micro Software Inventories')

def get_hostname(url: str, computer_id: int, api_key: str) -> str:
    hostname = requests.get(
        url=f"{url}/computers/{computer_id}",
        headers={
            "api-version": API_VERSION,
            "api-secret-key": api_key
        },
        params={"expand": "none"}
    ).json().get('hostName')

    return hostname

def main() -> None:
    PARSER.add_argument(
        '--computers_csv', 
        type=str,
        help='Path to exported computer list. With hostname included in columns.'
    )

    PARSER.add_argument(
        '--apiKey', 
        type=str,
        help='Provide Trend Vision One API Key',
        required=True
    )
    
    PARSER.add_argument(
        '--region',
        choices=['us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'],
        default='us-1',
        help="Regions: 'us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'."
    )

    args = PARSER.parse_args()
    api_url = f"https://workload.{args.region}.cloudone.trendmicro.com/api"

    if args.computers_csv:
        try:
            with open(args.computers_csv, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                computers = [row.get('Hostname') for row in reader]
        except FileNotFoundError:
            print(f'{args.computers_csv} file not found')
            sys.exit()

    inventories = requests.get(
        url=f"{api_url}/softwareinventories",
        headers={
            "api-version": API_VERSION,
            "api-secret-key": args.apiKey
        }
    ).json().get('softwareInventories')

    for inventory in inventories:
        hostname = get_hostname(api_url, inventory.get('computerID'), args.apiKey)
        if args.computers_csv:
            if hostname not in computers:
                continue
        requests.delete(
            url=f"{api_url}/softwareinventories/{inventory.get('ID')}",
            headers={
                "api-version": API_VERSION,
                "api-secret-key": args.apiKey
            }
        )

if __name__ == '__main__':
    main()