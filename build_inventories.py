import argparse
import csv
import requests


API_URL = "https://workload.us-1.cloudone.trendmicro.com/api"
ERROR_FILE = "software_build_errors.csv"
CSV_FIELDS = ('hostname','error')
PARSER = argparse.ArgumentParser(description='Build Trend Micro Software Inventories')
API_VERSION = 'v1'

def main() -> None:
    PARSER.add_argument(
        '--apiKey', 
        type=str,
        help='Provide Trend Vision One API Key',
        required=True
    )

    args = PARSER.parse_args()

    computers = requests.get(
        url=f"{API_URL}/computers",
        headers={
            "api-version": "v1",
            "api-secret-key": args.apiKey
        },
        params={"expand": "computerStatus"}
    ).json().get('computers')

    with open(ERROR_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for computer in computers:
            hostname = computer.get('hostName')
            build_response = requests.post(
                url=f"{API_URL}/softwareinventories",
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