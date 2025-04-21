# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import csv
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py input_file")
    sys.exit(1)

input_file = sys.argv[1]

# Initialize data structures
vendors = []              # List of (vendor_id, vendor_name)
devices = {}             # Dict: vendor_id -> list of (device_id, device_name)
interfaces = {}          # Dict: (vendor_id, device_id) -> list of (interface_id, interface_name)
current_vendor = None
current_device = None

# Parse the input file
with open(input_file, 'r') as f:
    for line in f:
        line = line.rstrip('\n')
        # Count leading tabs to determine level
        level = 0
        while line.startswith('\t'):
            level += 1
            line = line[1:]
        line = line.lstrip()  # Remove leading spaces after tabs
        if not line:
            continue  # Skip empty lines
        # Split into id and name by the first space
        try:
            id, name = line.split(' ', 1)
            id = id.strip()
            name = name.strip()
        except ValueError:
            raise ValueError(f"Invalid line format: {line}")
        
        if level == 0:
            # Vendor line
            current_vendor = id
            vendors.append((id, name))
            current_device = None
        elif level == 1:
            # Device line
            if current_vendor is None:
                raise ValueError("Device line without preceding vendor")
            current_device = id
            if current_vendor not in devices:
                devices[current_vendor] = []
            devices[current_vendor].append((id, name))
        elif level == 2:
            # Interface line
            if current_vendor is None or current_device is None:
                raise ValueError("Interface line without preceding vendor or device")
            key = (current_vendor, current_device)
            if key not in interfaces:
                interfaces[key] = []
            interfaces[key].append((id, name))
        else:
            raise ValueError(f"Invalid indentation level: {level}")

# Write vendors.csv
with open('vendors.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for vendor_id, vendor_name in vendors:
        writer.writerow([vendor_id, vendor_name])

# Write devices CSV files for each vendor
for vendor_id, device_list in devices.items():
    with open(f"{vendor_id}_devices.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for device_id, device_name in device_list:
            writer.writerow([device_id, device_name])

# Write interfaces CSV files for each device
for (vendor_id, device_id), interface_list in interfaces.items():
    with open(f"{vendor_id}_{device_id}_interfaces.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for interface_id, interface_name in interface_list:
            writer.writerow([interface_id, interface_name])