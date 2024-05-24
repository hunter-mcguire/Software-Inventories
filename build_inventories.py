import argparse
import csv
import sys

import requests

ERROR_FILE = "software_build_errors.csv"
CSV_FIELDS = ('hostname','error')
PARSER = argparse.ArgumentParser(description='Build Trend Micro Software Inventories')
API_VERSION = 'v1'

def get_computers(csv_path: str, headers: dict) -> list:
    computers = []
    try:
        with open(csv_path, mode='r') as csv_path:
            csv_reader = csv.DictReader(csv_path)

            for row in csv_reader:
                try:
                    response = requests.post(
                        url=f'{API_URL}/computers/search',
                        headers=headers,
                        params={"expand": "computerStatus"},
                        json={
                            'searchCriteria': [
                                {
                                    'fieldName': 'hostName',
                                    'stringTest': 'equal',
                                    'stringValue': row.get('Hostname')
                                }
                            ]
                        }
                    ).json().get('computers')[0]
                    computers.append(response)
                except Exception as error:
                    print(error)
        return computers
    except Exception as error:
        print(f"Failed to load computers from: {csv_path}\n")
        print(f"Error: {error}")
        sys.exit()

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
        '--region',
        choices=['us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'],
        required=True,
        default='us-1',
        help="Regions: 'us-1', 'in-1', 'gb-1', 'jp-1', 'de-1', 'au-1', 'ca-1', 'sg-1'."
    )

    PARSER.add_argument(
        '--all', 
        action='store_true',
        help='Create an inventory for all agents.'
    )

    args = PARSER.parse_args()
    api_url = f"https://workload.{args.region}.cloudone.trendmicro.com/api"
    
    headers={
        "api-version": "v1",
        "api-secret-key": args.apiKey
    }

    if args.all:
        computers = requests.get(
            url=f"{api_url}/computers",
            headers=headers,
            params={"expand": "computerStatus"}
        ).json().get('computers')
    else:
        if args.computers_csv:
            computers = get_computers(args.computers_csv, headers)
        else:
            print('Must specific --all or --computers_csv parameter. Not Both')
            sys.exit()

    
    with open(ERROR_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for computer in computers:
            hostname = computer.get('hostName')
            build_response = requests.post(
                url=f"{api_url}/softwareinventories",
                json={
                    "computerID": computer.get('ID'),
                    "description": computer.get('displayName'),
                    "name": computer.get('hostName')
                },
                headers={
                    "api-version": API_VERSION,
                    "api-secret-key": args.apiKey
                }
            )

            if build_response.status_code >= 400:
                writer.writerow({'hostname': hostname, 'error': build_response.json().get('message')})
                continue


if __name__ == '__main__':
    main()