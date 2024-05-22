# Software Inventories

Scripts to help manage Trend Micro Vision One software inventories.

## Overview

This repository contains three Python scripts to manage software inventories:

1. **build_inventories.py**: <br>This script builds software inventories by attempting to create an inventory for each computer. <br>
   It will write any errors to software_build_errors.csv in the directory it is ran in.<br>
2. **build_inventory_report.py**: <br>This script generates a detailed report based on the inventories created by `build_inventories.py`.<br>
   This while write to software_build_report.csv in the same directory it is ran it.<br>
3. **nuke_inventories.py**: 
<br>This script deletes all existing inventories to allow for a fresh start or cleanup.

## Usage

Each script requires an `apiKey` parameter to authenticate API requests. 

The build_inventories.py script requires either the `--all` or `--computers_csv` parameter to build software inventories..

Computers CSV:
<br>
This parameter accepts a filepath to a CSV file. Each row should have a "Hostname" column. This maps to the output from a computers export from the Workload Security Console.

```sh
python3 build_inventories.py --apiKey YOUR_API_KEY --computers_csv /tmp/test_batch.csv
```
<br>
All:
<br>
This paramater option will build inventories for all computers in Workload Security.

```sh
python3 build_inventories.py --apiKey YOUR_API_KEY --all
```


