# Software Inventories

Scripts to help manage Trend Micro Vision One software inventories.

## Overview

This repository contains three Python scripts to manage software inventories:

1. **build_inventories.py**: <br>This script builds software inventories by attempting to create an inventory for each computer. <br>
   It will write any errors to software_build_errors.csv in the directory it is ran in.<br>
2. **build_inventory_report.py**: <br>This script generates a detailed report based on the inventories created by `build_inventories.py`.<br>
   This will write to software_build_report.csv in the same directory it is ran it.<br>
3. **nuke_inventories.py**: <>brThis script deletes all existing inventories to allow for a fresh start or cleanup.

## Usage

Each script requires an `apiKey` parameter to authenticate API requests. Below are examples of how to run each script with the `apiKey` parameter.

### build_inventories.py

```sh
python3 build_inventories.py --apiKey YOUR_API_KEY
