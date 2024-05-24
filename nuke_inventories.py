import argparse
import requests

API_VERSION = 'v1'
PARSER = argparse.ArgumentParser(description='Delete All Trend Micro Software Inventories')

def main() -> None:
    PARSER.add_argument(
        '--apiKey', 
        type=str,
        help='Provide Trend Vision One API Key',
        required=True
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

    inventories = requests.get(
        url=f"{api_url}/softwareinventories",
        headers={
            "api-version": API_VERSION,
            "api-secret-key": args.apiKey
        }
    ).json().get('softwareInventories')

    for inventory in inventories:
        response = requests.delete(
            url=f"{api_url}/softwareinventories/{inventory.get('ID')}",
            headers={
                "api-version": API_VERSION,
                "api-secret-key": args.apiKey
            }
        )

if __name__ == '__main__':
    main()