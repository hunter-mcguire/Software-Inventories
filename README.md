# Software Inventories

Scripts to help manage Trend Micro Vision One software inventories.

## Overview

This repository contains three Python scripts to manage software inventories:

These scripts only have a single dependacy, which is the Requests library.

If using pip:
```sh
pip3 install requests
```
OR
```sh
python3 -m pip install requests
```

1. **build_inventories.py**: <br>This script builds software inventories by attempting to create an inventory for each computer. <br>
   It will write any errors to software_build_errors.csv in the directory it is ran in.<br>
2. **build_inventory_report.py**: <br>This script generates a detailed report based on the inventories created by `build_inventories.py`.<br>
   This while write to software_build_report.csv in the same directory it is ran it.<br>
3. **delete_inventories.py**: 
<br>This script deletes software inventories.

## Usage

Each script requires an `--apiKey` parameter to authenticate API requests. 

There is also a region `--region` paramater which defaults to 'us-1'.
Regions:
* us-1
* in-1
* gb-1
* jp-1 
* de-1
* au-1
* ca-1 
* sg-1

All 3 scripts require either the `--all` or `--computers_csv` parameter to build software inventories, reports, and handle deletions.

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
<br>
Build the report for all inventories or ones specificed in a csv file.

<br>

```sh
python3 build_inventory_report.py --apiKey YOUR_API_KEY --computers_csv /tmp/test_batch.csv
```

<br>

```sh
python3 build_inventory_report.py --apiKey YOUR_API_KEY --all
```