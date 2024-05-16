import argparse
import requests


API_URL = "https://workload.us-1.cloudone.trendmicro.com/api"
API_VERSION = 'v1'
PARSER = argparse.ArgumentParser(description='Delete All Trend Micro Software Inventories')

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

    for inventory in inventories:
        response = requests.delete(
            url=f"{API_URL}/softwareinventories/{inventory.get('ID')}",
            headers={
                "api-version": API_VERSION,
                "api-secret-key": args.apiKey
            }
        )

if __name__ == '__main__':
    main()