# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import json

def process_file(input_file):
    # Open and read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize the main dictionary
    usb_data = {}
    current_vendor = None
    current_device = None

    # Parse the file line by line
    for line in lines:
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        if not line.startswith('\t'):  # Vendor line
            parts = line.split(None, 1)
            if len(parts) == 2:
                vendor_id, vendor_name = parts
                current_vendor = f'0x{vendor_id}'
                usb_data[f'0x{vendor_id}'] = {'name': vendor_name, 'devices': {}}
                current_device = None
        elif line.startswith('\t') and not line.startswith('\t\t'):  # Device line
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and current_vendor:
                device_id, device_name = parts
                current_device = f'0x{device_id}'
                usb_data[current_vendor]['devices'][f'0x{device_id}'] = {'name': device_name, 'interfaces': {}}
        elif line.startswith('\t\t'):  # Interface line
            parts = line.strip().split(None, 1)
            if len(parts) == 2 and current_vendor and current_device:
                interface_id, interface_name = parts
                usb_data[current_vendor]['devices'][current_device]['interfaces'][f'0x{interface_id}'] = interface_name

    return usb_data

# Example usage
usb_data = process_file('usbIDs')

# Write the usb_data dictionary to a JSON file
with open('usb_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(usb_data, json_file, indent=4)