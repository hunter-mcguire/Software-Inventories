import argparse
import csv
import requests


SOFTWARE_STATES  = ("unknown", "building", "complete", "failed", "requested")
API_VERSION = 'v1'
REPORT_FILE = "software_build_report.csv"
CSV_FIELDS = ('hostname', 'start_time', 'status', 'filename', 'path', 'sha256')
PARSER = argparse.ArgumentParser(description='Build Trend Micro Software Inventories')


def process_inventory(url: str, inventory_id: dict, hostname: str, api_key: str,
                      writer: csv.DictWriter) -> None:
    items = requests.get(
        url=f"{url}/softwareinventories/{inventory_id}/items",
        headers={
            "api-version": API_VERSION,
            "api-secret-key": api_key
        }
    ).json().get('inventoryItems')

    for item in items:
        writer.writerow(
            {
                'hostname': hostname,
                'filename': item.get('fileName'),
                'path': item.get('path'),
                'sha256': item.get('sha256')
            }
        )

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
        '--apiKey', 
        type=str,
        help='Provide Trend Vision One API Key',
        required=True
    )
    
    PARSER.add_argument(
        '--computers_csv', 
        type=str,
        help='Path to exported computer list. With hostname included in columns.'
    )

    PARSER.add_argument(
        '--all', 
        action='store_true',
        help='Create an inventory for all agents.'
    )

    PARSER.add_argument(
        '--region',
        choices=['us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'],
        required=True,
        default='us-1',
        help="Regions: 'us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'."
    )

    args = PARSER.parse_args()
    api_url = f"https://workload.{args.region}.cloudone.trendmicro.com/api"

    with open(REPORT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()

        if args.computers_csv:
            with open(args.computers_csv, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                computers = [row.get('Hostname') for row in reader]

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
            if inventory.get('state') == 'complete':
                process_inventory(
                    url=api_url,
                    inventory_id=inventory.get('ID'),
                    hostname=hostname,
                    api_key=args.apiKey,
                    writer=writer
                )
            else:
                writer.writerow(
                    {
                        'hostname': hostname,
                        'start_time': inventory.get('startDate'),
                        'status': inventory.get('state')
                    }
                )

if __name__ == '__main__':
    main()
