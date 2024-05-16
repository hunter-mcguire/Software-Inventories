# Software Inventories

Scripts to help manage Trend Micro Vision One software inventories.

## Overview

This repository contains three Python scripts to manage software inventories:

1. **build_inventories.py**: This script builds software inventories by gathering relevant data from specified sources.
2. **build_inventory_report.py**: This script generates a detailed report based on the inventories created by `build_inventories.py`.
3. **nuke_inventories.py**: This script deletes all existing inventories to allow for a fresh start or cleanup.

## Usage

Each script requires an `apiKey` parameter to authenticate API requests. Below are examples of how to run each script with the `apiKey` parameter.

### build_inventories.py

```sh
python3 build_inventories.py --apiKey YOUR_API_KEY
