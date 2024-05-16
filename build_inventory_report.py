import argparse
import csv
import requests


SOFTWARE_STATES  = ("unknown", "building", "complete", "failed", "requested")
API_URL = "https://workload.us-1.cloudone.trendmicro.com/api"
API_VERSION = 'v1'
REPORT_FILE = "software_build_report.csv"
CSV_FIELDS = ('hostname', 'start_time', 'status', 'filename', 'path', 'sha256')
PARSER = argparse.ArgumentParser(description='Build Trend Micro Software Inventories')


def process_inventory(inventory_id: dict, hostname: str, api_key: str,
                      writer: csv.DictWriter) -> None:
    items = requests.get(
        url=f"{API_URL}/softwareinventories/{inventory_id}/items",
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

def get_hostname(computer_id: int, api_key: str) -> str:
    hostname = requests.get(
        url=f"{API_URL}/computers/{computer_id}",
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

    args = PARSER.parse_args()

    inventories = requests.get(
        url=f"{API_URL}/softwareinventories",
        headers={
            "api-version": API_VERSION,
            "api-secret-key": args.apiKey
        }
    ).json().get('softwareInventories')

    with open(REPORT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for inventory in inventories:
            hostname = get_hostname(inventory.get('computerID'), args.apiKey)
            if inventory.get('state') == 'complete':
                process_inventory(
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
