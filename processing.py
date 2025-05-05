# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from graphviz import Digraph
from extras.classes import Classes, More
from helpers import bcd_to_string, decode_country_code, get_vendor_name, get_product_name, get_bos_device_capability

# Internal Functions
def CreateDeviceDescriptorNode(descriptor: list):
    '''**9.6.1 Device**: A device descriptor describes general information about a device. It includes information
    that applies globally to the device and all of the device’s configurations. A device has only
    one device descriptor.
    '''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bcdUSB = bcd_to_string((descriptor[3] << 8) + descriptor[2])  # Little-endian
    bDeviceClass = descriptor[4]
    bDeviceSubClass = descriptor[5]
    bDeviceProtocol = descriptor[6]
    bMaxPacketSize0 = descriptor[7]
    idVendor = (descriptor[9] << 8) + descriptor[8]  # Little-endian
    idProduct = (descriptor[11] << 8) + descriptor[10]  # Little-endian
    bcdDevice = bcd_to_string((descriptor[13] << 8) + descriptor[12])  # Little-endian
    iManufacturer = descriptor[14]
    iProduct = descriptor[15]
    iSerialNumber = descriptor[16]
    bNumConfigurations = descriptor[17]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Device Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>bcdUSB:  {bcdUSB}</TD></TR>
<TR><TD>bDeviceClass:  {bDeviceClass}</TD></TR>
<TR><TD>bDeviceSubClass:  {bDeviceSubClass}</TD></TR>
<TR><TD>bDeviceProtocol:  {bDeviceProtocol}</TD></TR>
<TR><TD>bMaxPacketSize0:  {bMaxPacketSize0}</TD></TR>
<TR><TD>idVendor:  {idVendor} ({get_vendor_name(idVendor)})</TD></TR>
<TR><TD>idProduct:  {idProduct} ({get_product_name(idVendor, idProduct)})</TD></TR>
<TR><TD>bcdDevice:  {bcdDevice}</TD></TR>
<TR><TD>iManufacturer:  {iManufacturer}</TD></TR>
<TR><TD>iProduct:  {iProduct}</TD></TR>
<TR><TD>iSerialNumber:  {iSerialNumber}</TD></TR>
<TR><TD>bNumConfigurations:  {bNumConfigurations}</TD></TR>
</TABLE>>'''

def CreateConfigurationDescriptorNode(descriptor: list):
    '''**9.6.3 Configuration**: Describes a specific device configuration.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    wTotalLength = (descriptor[3] << 8) + descriptor[2]  # Little-endian
    bNumInterfaces = descriptor[4]
    bConfigurationValue = descriptor[5]
    iConfiguration = descriptor[6]
    bmAttributes = descriptor[7]
    bMaxPower = descriptor[8]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Configuration Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>wTotalLength:  {wTotalLength}</TD></TR>
<TR><TD>bNumInterfaces:  {bNumInterfaces}</TD></TR>
<TR><TD>bConfigurationValue:  {bConfigurationValue}</TD></TR>
<TR><TD>iConfiguration:  {iConfiguration}</TD></TR>
<TR><TD>bmAttributes:  {bmAttributes}</TD></TR>
<TR><TD>bMaxPower:  {bMaxPower}</TD></TR>
</TABLE>>'''

def CreateStringDescriptorNode(descriptor: list):
    '''**9.6.7 String**: Contains a Unicode string or language ID array (if index 0).'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    string_data = bytes(descriptor[2:bLength]).decode('utf-16-le')
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>String Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>String:  {string_data}</TD></TR>
</TABLE>>'''

def CreateInterfaceDescriptorNode(descriptor: list):
    '''**9.6.5 Interface**: Describes a specific interface within a configuration.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bInterfaceNumber = descriptor[2]
    bAlternateSetting = descriptor[3]
    bNumEndpoints = descriptor[4]
    bInterfaceClass = descriptor[5]
    bInterfaceSubClass = descriptor[6]
    bInterfaceProtocol = descriptor[7]
    iInterface = descriptor[8]

    # Get class, subclass, and protocol names from Classes dictionary
    class_info = Classes.get(bInterfaceClass, {})
    class_name = class_info.get("name", "Unknown")
    subclass_info = class_info.get("subclass", {}).get(bInterfaceSubClass, {})
    subclass_name = subclass_info.get("name", "Unknown")
    protocol_name = subclass_info.get("protocols", {}).get(bInterfaceProtocol, "Unknown")

    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Interface Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bInterfaceNumber: {bInterfaceNumber}</TD></TR>
<TR><TD>bAlternateSetting: {bAlternateSetting}</TD></TR>
<TR><TD>bNumEndpoints: {bNumEndpoints}</TD></TR>
<TR><TD>bInterfaceClass: {bInterfaceClass} ({class_name})</TD></TR>
<TR><TD>bInterfaceSubClass: {bInterfaceSubClass} ({subclass_name})</TD></TR>
<TR><TD>bInterfaceProtocol: {bInterfaceProtocol} ({protocol_name})</TD></TR>
<TR><TD>iInterface: {iInterface}</TD></TR>
</TABLE>>'''

def CreateEndpointDescriptorNode(descriptor: list):
    '''**9.6.6 Endpoint**: Describes an endpoint within an interface.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bEndpointAddress = descriptor[2]
    bmAttributes = descriptor[3]
    wMaxPacketSize = (descriptor[5] << 8) + descriptor[4]  # Little-endian
    bInterval = descriptor[6]

    # Decode endpoint address
    direction = "IN" if (bEndpointAddress & 0x80) else "OUT"
    endpoint_number = bEndpointAddress & 0x0F

    # Decode bmAttributes
    transfer_type = bmAttributes & 0x03
    transfer_type_str = {
        0: "Control",
        1: "Isochronous",
        2: "Bulk",
        3: "Interrupt"
    }.get(transfer_type, "Unknown")

    if transfer_type == 1:  # Isochronous
        sync_type = (bmAttributes >> 2) & 0x03
        sync_type_str = {
            0: "No Synchronization",
            1: "Asynchronous",
            2: "Adaptive",
            3: "Synchronous"
        }.get(sync_type, "Unknown")
        usage_type = (bmAttributes >> 4) & 0x03
        usage_type_str = {
            0: "Data endpoint",
            1: "Feedback endpoint",
            2: "Implicit feedback Data endpoint",
            3: "Reserved"
        }.get(usage_type, "Unknown")
        attributes_str = f"{transfer_type_str} ({sync_type_str}, {usage_type_str})"
    else:
        attributes_str = transfer_type_str

    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Endpoint Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bEndpointAddress: {hex(bEndpointAddress)} ({direction} Endpoint {endpoint_number})</TD></TR>
<TR><TD>bmAttributes: {hex(bmAttributes)} ({attributes_str})</TD></TR>
<TR><TD>wMaxPacketSize: {wMaxPacketSize}</TD></TR>
<TR><TD>bInterval: {bInterval}</TD></TR>
</TABLE>>'''

def CreateInterfaceAssociationDescriptorNode(descriptor: list):
    '''**9.6.4 Interface Association**: Groups interfaces that form a single function.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bFirstInterface = descriptor[2]
    bInterfaceCount = descriptor[3]
    bFunctionClass = descriptor[4]
    bFunctionSubClass = descriptor[5]
    bFunctionProtocol = descriptor[6]
    iFunction = descriptor[7]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Interface Association Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>bFirstInterface:  {bFirstInterface}</TD></TR>
<TR><TD>bInterfaceCount:  {bInterfaceCount}</TD></TR>
<TR><TD>bFunctionClass:  {bFunctionClass}</TD></TR>
<TR><TD>bFunctionSubClass:  {bFunctionSubClass}</TD></TR>
<TR><TD>bFunctionProtocol:  {bFunctionProtocol}</TD></TR>
<TR><TD>iFunction:  {iFunction}</TD></TR>
</TABLE>>'''

def CreateDeviceQualifierDescriptorNode(descriptor: list):
    '''**9.6.2 Device Qualifier**: Describes information about a device that would apply at a different speed.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bcdUSB = bcd_to_string((descriptor[3] << 8) + descriptor[2])  # Little-endian
    bDeviceClass = descriptor[4]
    bDeviceSubClass = descriptor[5]
    bDeviceProtocol = descriptor[6]
    bMaxPacketSize0 = descriptor[7]
    bNumConfigurations = descriptor[8]
    bReserved = descriptor[9]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Device Qualifier Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bcdUSB: {bcdUSB}</TD></TR>
<TR><TD>bDeviceClass: {bDeviceClass}</TD></TR>
<TR><TD>bDeviceSubClass: {bDeviceSubClass}</TD></TR>
<TR><TD>bDeviceProtocol: {bDeviceProtocol}</TD></TR>
<TR><TD>bMaxPacketSize0: {bMaxPacketSize0}</TD></TR>
<TR><TD>bNumConfigurations: {bNumConfigurations}</TD></TR>
<TR><TD>bReserved: {bReserved}</TD></TR>
</TABLE>>'''

def CreateOtherSpeedConfigurationDescriptorNode(descriptor: list):
    '''**9.6.4 Other Speed Configuration**: Describes a configuration at a different speed.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    wTotalLength = (descriptor[3] << 8) + descriptor[2]  # Little-endian
    bNumInterfaces = descriptor[4]
    bConfigurationValue = descriptor[5]
    iConfiguration = descriptor[6]
    bmAttributes = descriptor[7]
    bMaxPower = descriptor[8]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Other Speed Configuration Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>wTotalLength: {wTotalLength}</TD></TR>
<TR><TD>bNumInterfaces: {bNumInterfaces}</TD></TR>
<TR><TD>bConfigurationValue: {bConfigurationValue}</TD></TR>
<TR><TD>iConfiguration: {iConfiguration}</TD></TR>
<TR><TD>bmAttributes: {bmAttributes}</TD></TR>
<TR><TD>bMaxPower: {bMaxPower}</TD></TR>
</TABLE>>'''

def CreateDeviceCapabilityDescriptorNode(descriptor: list):
    '''**9.6.2 Device Capability**: Describes capabilities within a BOS descriptor.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bDevCapabilityType = descriptor[2]
    capability_name = get_bos_device_capability(bDevCapabilityType)
    data_bytes = [hex(byte) for byte in descriptor[3:bLength]]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Device Capability Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>bDevCapabilityType:  {bDevCapabilityType} ({capability_name})</TD></TR>
<TR><TD>Capability Data:  {data_bytes}</TD></TR>
</TABLE>>'''

def CreateSSEndpointCompanionDescriptorNode(descriptor: list):
    '''**SuperSpeed Endpoint Companion**: Additional descriptor for SuperSpeed endpoints.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bMaxBurst = descriptor[2]
    bmAttributes = descriptor[3]
    wBytesPerInterval = (descriptor[5] << 8) + descriptor[4]  # Little-endian
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>SuperSpeed Endpoint Companion Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>bMaxBurst:  {bMaxBurst}</TD></TR>
<TR><TD>bmAttributes:  {bmAttributes}</TD></TR>
<TR><TD>wBytesPerInterval:  {wBytesPerInterval}</TD></TR>
</TABLE>>'''

def CreateSSPIsochEndpointCompanionDescriptorNode(descriptor: list):
    '''**SuperSpeedPlus Isochronous Endpoint Companion**: For USB 3.1+ isochronous endpoints.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    wReserved = (descriptor[3] << 8) + descriptor[2]  # Little-endian
    dwBytesPerInterval = (descriptor[7] << 24) + (descriptor[6] << 16) + (descriptor[5] << 8) + descriptor[4]  # Little-endian
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>SuperSpeedPlus Isochronous Endpoint Companion Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>wReserved:  {wReserved}</TD></TR>
<TR><TD>dwBytesPerInterval:  {dwBytesPerInterval}</TD></TR>
</TABLE>>'''

def CreateBOSDescriptorNode(descriptor: list):
    '''**9.6.2 BOS**: Binary Object Store descriptor, followed by capability descriptors.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    wTotalLength = (descriptor[3] << 8) + descriptor[2]  # Little-endian
    bNumDeviceCaps = descriptor[4]
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>BOS Descriptor</B></TD></TR>
<TR><TD>bLength:  {bLength}</TD></TR>
<TR><TD>bDescriptorType:  {bDescriptorType}</TD></TR>
<TR><TD>wTotalLength:  {wTotalLength}</TD></TR>
<TR><TD>bNumDeviceCaps:  {bNumDeviceCaps}</TD></TR>
</TABLE>>'''

# Class-Specific functions:
def CreateHIDDescriptorNode(descriptor: list) -> str:
    '''**HID Descriptor**: Describes a Human Interface Device, including HID version and additional descriptor info.'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bcdHID = bcd_to_string((descriptor[3] << 8) + descriptor[2])  # Little-endian
    bCountryCode = descriptor[4]
    bNumDescriptors = descriptor[5]
    class_descriptors = []
    offset = 6
    for i in range(bNumDescriptors):
        if offset + 3 > bLength:
            break
        desc_type = descriptor[offset]
        desc_length = (descriptor[offset + 2] << 8) + descriptor[offset + 1]  # Little-endian
        class_descriptors.append((desc_type, desc_length))
        offset += 3
    table_str = f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>HID Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType} (HID)</TD></TR>
<TR><TD>bcdHID: {bcdHID}</TD></TR>
<TR><TD>bCountryCode: {bCountryCode} (${decode_country_code(bCountryCode)})</TD></TR>
<TR><TD>bNumDescriptors: {bNumDescriptors}</TD></TR>'''
    for i, (desc_type, desc_length) in enumerate(class_descriptors):
        desc_type_str = More["hid"].get(desc_type, "Unknown")
        table_str += f'<TR><TD>Class Descriptor {i+1}: Type {desc_type} ({desc_type_str}), Length {desc_length}</TD></TR>'
    table_str += '</TABLE>>'
    return table_str

def CreateReportDescriptorNode(descriptor: list) -> str:
    '''**Report Descriptor (0x22)**: Describes the format of data exchanged with a HID device.'''
    def decode_item(data: list, index: int) -> (str, int):
        if index >= len(data):
            return "", index
        b = data[index]
        item_size = (b & 0x03) if (b & 0x03) < 3 else 4  # 0:0 bytes, 1:1 byte, 2:2 bytes, 3:4 bytes
        item_type = (b & 0x0C) >> 2  # 0:Main, 1:Global, 2:Local, 3:Reserved
        item_tag = (b & 0xF0) >> 4
        item_data = 0
        for i in range(item_size):
            if index + 1 + i >= len(data):
                break
            item_data |= data[index + 1 + i] << (8 * i)
        item_name = More["hid-item"].get(b, f"Unknown Tag 0x{b:02x}")
        if item_type == 0:  # Main Items
            if b == 0x80:  # Input
                flags = [ "Constant" if item_data & 0x01 else "Data",
                          "Variable" if item_data & 0x02 else "Array",
                          "Relative" if item_data & 0x04 else "Absolute",
                          "Wrap" if item_data & 0x08 else "No Wrap",
                          "Non Linear" if item_data & 0x10 else "Linear",
                          "No Preferred" if item_data & 0x20 else "Preferred State",
                          "Null State" if item_data & 0x40 else "No Null",
                          "Volatile" if item_data & 0x80 else "Non Volatile",
                          "Buffered Bytes" if item_data & 0x100 else "Bit Field"]
                item_str = f"Input ({', '.join(f for f in flags if 'No ' not in f)})"
            elif b == 0x90:  # Output
                flags = [ "Constant" if item_data & 0x01 else "Data",
                          "Variable" if item_data & 0x02 else "Array",
                          "Relative" if item_data & 0x04 else "Absolute",
                          "Wrap" if item_data & 0x08 else "No Wrap",
                          "Non Linear" if item_data & 0x10 else "Linear",
                          "No Preferred" if item_data & 0x20 else "Preferred State",
                          "Null State" if item_data & 0x40 else "No Null",
                          "Volatile" if item_data & 0x80 else "Non Volatile",
                          "Buffered Bytes" if item_data & 0x100 else "Bit Field"]
                item_str = f"Output ({', '.join(f for f in flags if 'No ' not in f)})"
            elif b == 0xb0:  # Feature
                flags = [ "Constant" if item_data & 0x01 else "Data",
                          "Variable" if item_data & 0x02 else "Array",
                          "Relative" if item_data & 0x04 else "Absolute",
                          "Wrap" if item_data & 0x08 else "No Wrap",
                          "Non Linear" if item_data & 0x10 else "Linear",
                          "No Preferred" if item_data & 0x20 else "Preferred State",
                          "Null State" if item_data & 0x40 else "No Null",
                          "Volatile" if item_data & 0x80 else "Non Volatile",
                          "Buffered Bytes" if item_data & 0x100 else "Bit Field"]
                item_str = f"Feature ({', '.join(f for f in flags if 'No ' not in f)})"
            elif b == 0xa0:  # Collection
                collection_types = {0: "Physical", 1: "Application", 2: "Logical", 3: "Report",
                                  4: "Named Array", 5: "Usage Switch", 6: "Usage Modifier"}
                item_str = f"Collection ({collection_types.get(item_data, 'Vendor Defined')})"
            elif b == 0xc0:  # End Collection
                item_str = "End Collection"
            else:
                item_str = f"{item_name}: 0x{item_data:x}"
        else:
            item_str = f"{item_name}: 0x{item_data:x}"
        return item_str, index + 1 + item_size

    items = []
    index = 0
    while index < len(descriptor):
        item_str, new_index = decode_item(descriptor, index)
        if not item_str:
            break
        items.append(item_str)
        index = new_index

    table_str = f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Report Descriptor</B></TD></TR>
<TR><TD>Length: {len(descriptor)}</TD></TR>'''
    for i, item in enumerate(items):
        table_str += f'<TR><TD>Item {i}: {item}</TD></TR>'
    table_str += '</TABLE>>'
    return table_str

def CreatePhysicalDescriptorNode(descriptor: list) -> str:
    '''**Physical Descriptor (0x23)**: Describes physical characteristics of a HID device (e.g., for force feedback).'''
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bData = [hex(b) for b in descriptor[2:bLength]]  # Raw data as hex
    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Physical Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType} (Physical)</TD></TR>
<TR><TD>Data: {bData}</TD></TR>
</TABLE>>'''

def CreateAudioInterfaceDescriptorNode(descriptor: list, interface_subclass: int) -> str:
    """Create a graph node for audio class-specific interface descriptors (bDescriptorType=0x24)."""
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bDescriptorSubtype = descriptor[2]

    if interface_subclass == 0x01:  # AudioControl
        if bDescriptorSubtype == 0x01:  # HEADER
            bcdADC = bcd_to_string((descriptor[4] << 8) + descriptor[3])
            wTotalLength = (descriptor[6] << 8) + descriptor[5]
            bInCollection = descriptor[7]
            baInterfaceNr = descriptor[8:8 + bInCollection]
            return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>AudioControl Header Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (HEADER)</TD></TR>
<TR><TD>bcdADC: {bcdADC}</TD></TR>
<TR><TD>wTotalLength: {wTotalLength}</TD></TR>
<TR><TD>bInCollection: {bInCollection}</TD></TR>
<TR><TD>baInterfaceNr: {baInterfaceNr}</TD></TR>
</TABLE>>'''
        elif bDescriptorSubtype == 0x02:  # INPUT_TERMINAL
            bTerminalID = descriptor[3]
            wTerminalType = (descriptor[5] << 8) + descriptor[4]
            terminal_type_name = More["Audio"].get(wTerminalType, "Unknown")
            bAssocTerminal = descriptor[6]
            bNrChannels = descriptor[7]
            wChannelConfig = (descriptor[9] << 8) + descriptor[8]
            iChannelNames = descriptor[10]
            iTerminal = descriptor[11]
            return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Input Terminal Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (INPUT_TERMINAL)</TD></TR>
<TR><TD>bTerminalID: {bTerminalID}</TD></TR>
<TR><TD>wTerminalType: {wTerminalType} ({terminal_type_name})</TD></TR>
<TR><TD>bAssocTerminal: {bAssocTerminal}</TD></TR>
<TR><TD>bNrChannels: {bNrChannels}</TD></TR>
<TR><TD>wChannelConfig: {wChannelConfig}</TD></TR>
<TR><TD>iChannelNames: {iChannelNames}</TD></TR>
<TR><TD>iTerminal: {iTerminal}</TD></TR>
</TABLE>>'''
        elif bDescriptorSubtype == 0x03:  # OUTPUT_TERMINAL
            bTerminalID = descriptor[3]
            wTerminalType = (descriptor[5] << 8) + descriptor[4]
            terminal_type_name = More["Audio"].get(wTerminalType, "Unknown")
            bAssocTerminal = descriptor[6]
            bSourceID = descriptor[7]
            iTerminal = descriptor[8]
            return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Output Terminal Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (OUTPUT_TERMINAL)</TD></TR>
<TR><TD>bTerminalID: {bTerminalID}</TD></TR>
<TR><TD>wTerminalType: {wTerminalType} ({terminal_type_name})</TD></TR>
<TR><TD>bAssocTerminal: {bAssocTerminal}</TD></TR>
<TR><TD>bSourceID: {bSourceID}</TD></TR>
<TR><TD>iTerminal: {iTerminal}</TD></TR>
</TABLE>>'''
        elif bDescriptorSubtype == 0x06:  # FEATURE_UNIT
            bUnitID = descriptor[3]
            bSourceID = descriptor[4]
            bControlSize = descriptor[5]
            n = (bLength - 7) // bControlSize  # Number of bmaControls entries
            bmaControls = []
            offset = 6
            for i in range(n):
                control = 0
                for j in range(bControlSize):
                    control += descriptor[offset + j] << (8 * j)
                bmaControls.append(control)
                offset += bControlSize
            iFeature = descriptor[offset]
            bmaControls_str = ", ".join(hex(ctrl) for ctrl in bmaControls)
            return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Feature Unit Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (FEATURE_UNIT)</TD></TR>
<TR><TD>bUnitID: {bUnitID}</TD></TR>
<TR><TD>bSourceID: {bSourceID}</TD></TR>
<TR><TD>bControlSize: {bControlSize}</TD></TR>
<TR><TD>bmaControls: [{bmaControls_str}]</TD></TR>
<TR><TD>iFeature: {iFeature}</TD></TR>
</TABLE>>'''
        else:
            return f"Unknown AudioControl Subtype: {hex(bDescriptorSubtype)}"
    elif interface_subclass == 0x02:  # AudioStreaming
        if bDescriptorSubtype == 0x01:  # AS_GENERAL
            bTerminalLink = descriptor[3]
            bDelay = descriptor[4]
            wFormatTag = (descriptor[6] << 8) + descriptor[5]
            return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>AudioStreaming General Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (AS_GENERAL)</TD></TR>
<TR><TD>bTerminalLink: {bTerminalLink}</TD></TR>
<TR><TD>bDelay: {bDelay}</TD></TR>
<TR><TD>wFormatTag: {wFormatTag}</TD></TR>
</TABLE>>'''
        elif bDescriptorSubtype == 0x02:  # FORMAT_TYPE (Type I example)
            bFormatType = descriptor[3]
            if bFormatType == 1:  # TYPE_I
                bNrChannels = descriptor[4]
                bSubframeSize = descriptor[5]
                bBitResolution = descriptor[6]
                bSamFreqType = descriptor[7]
                if bSamFreqType == 0:  # Continuous
                    tLowerSamFreq = (descriptor[9] << 16) + (descriptor[8] << 8) + descriptor[7]
                    tUpperSamFreq = (descriptor[12] << 16) + (descriptor[11] << 8) + descriptor[10]
                    sam_freq_str = f"Continuous from {tLowerSamFreq} to {tUpperSamFreq} Hz"
                else:  # Discrete
                    sam_freq = [(descriptor[8 + i*3] << 16) + (descriptor[7 + i*3] << 8) + descriptor[6 + i*3] for i in range(bSamFreqType)]
                    sam_freq_str = ", ".join(str(freq) for freq in sam_freq)
                return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Format Type I Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (FORMAT_TYPE)</TD></TR>
<TR><TD>bFormatType: {bFormatType} (TYPE_I)</TD></TR>
<TR><TD>bNrChannels: {bNrChannels}</TD></TR>
<TR><TD>bSubframeSize: {bSubframeSize}</TD></TR>
<TR><TD>bBitResolution: {bBitResolution}</TD></TR>
<TR><TD>bSamFreqType: {bSamFreqType}</TD></TR>
<TR><TD>Sampling Frequencies: {sam_freq_str}</TD></TR>
</TABLE>>'''
            else:
                return f"Unknown Format Type: {bFormatType}"
        else:
            return f"Unknown AudioStreaming Subtype: {hex(bDescriptorSubtype)}"
    else:
        return f"Unknown Interface Subclass: {hex(interface_subclass)}"

def CreateAudioEndpointDescriptorNode(descriptor: list) -> str:
    """Create a graph node for audio class-specific endpoint descriptors (bDescriptorType=0x25)."""
    bLength = descriptor[0]
    bDescriptorType = descriptor[1]
    bDescriptorSubtype = descriptor[2]
    bmAttributes = descriptor[3]
    bLockDelayUnits = descriptor[4]
    wLockDelay = (descriptor[6] << 8) + descriptor[5]  # Little-endian

    # Decode bmAttributes
    sampling_freq_control = "Yes" if bmAttributes & 0x01 else "No"
    pitch_control = "Yes" if bmAttributes & 0x02 else "No"

    # Decode bLockDelayUnits
    lock_delay_units_str = {
        0: "Undefined",
        1: "Milliseconds",
        2: "Decoded PCM samples"
    }.get(bLockDelayUnits, "Unknown")

    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Audio Streaming Endpoint Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bDescriptorSubtype: {bDescriptorSubtype} (EP_GENERAL)</TD></TR>
<TR><TD>bmAttributes: {hex(bmAttributes)} (Sampling Frequency Control: {sampling_freq_control}, Pitch Control: {pitch_control})</TD></TR>
<TR><TD>bLockDelayUnits: {bLockDelayUnits} ({lock_delay_units_str})</TD></TR>
<TR><TD>wLockDelay: {wLockDelay}</TD></TR>
</TABLE>>'''

# Exposed APIs
def LoadHexArray(input_string):
    return [int(word, 16) for word in input_string.split()]

def ProcessAndGenerateFlow(descriptors: list) -> Digraph:
    dot = Digraph()
    dot.clear()
    index = 0
    device_node = None
    root_node = None
    current_config = None
    current_interface = None
    current_endpoint = None
    string_nodes = []
    class_specific_nodes = []
    unknown_nodes = []
    node_counter = 0
    current_interface_subclass = 0

    # Process all descriptors
    while index < len(descriptors):
        bLength = descriptors[index]
        if bLength == 0 or index + 1 >= len(descriptors):
            break
        bDescriptorType = descriptors[index + 1]
        if index + bLength > len(descriptors):
            break
        descriptor = descriptors[index:index + bLength]
        node_id = f"desc_{node_counter}"
        node_counter += 1

        if bDescriptorType == 1:  # Device Descriptor
            table_str = CreateDeviceDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            device_node = node_id
            root_node = node_id  # Temporarily set as root, may update later

        elif bDescriptorType == 2:  # Configuration Descriptor
            table_str = CreateConfigurationDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if device_node:
                dot.edge(device_node, node_id)
            current_config = node_id
            root_node = node_id  # Update root to last in chain

        elif bDescriptorType == 15:  # BOS Descriptor
            table_str = CreateBOSDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if device_node:
                dot.edge(device_node if root_node == device_node else root_node, node_id)
            root_node = node_id  # Update root to last in chain

        elif bDescriptorType == 16:  # Device Capability Descriptor
            table_str = CreateDeviceCapabilityDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if device_node:
                dot.edge(device_node if root_node == device_node else root_node, node_id)
            root_node = node_id  # Update root to last in chain

        elif bDescriptorType == 4:  # Interface Descriptor
            current_interface_subclass = descriptor[6]
            table_str = CreateInterfaceDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if root_node:
                dot.edge(root_node, node_id)
            current_interface = node_id

        elif bDescriptorType == 5:  # Endpoint Descriptor
            table_str = CreateEndpointDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if current_interface:
                dot.edge(current_interface, node_id)
            current_endpoint = node_id

        elif bDescriptorType in [48, 49]:  # Superspeed companions
            if bDescriptorType == 48:
                table_str = CreateSSEndpointCompanionDescriptorNode(descriptor)
            elif bDescriptorType == 49:
                table_str = CreateSSPIsochEndpointCompanionDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if current_endpoint:
                dot.edge(current_endpoint, node_id)

        elif bDescriptorType == 3:  # String Descriptor
            table_str = CreateStringDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            string_nodes.append(node_id)

        elif bDescriptorType in [0x21, 0x22, 0x23, 0x24, 0x25]:  # Class-specific
            if bDescriptorType == 0x21:
                table_str = CreateHIDDescriptorNode(descriptor)
            elif bDescriptorType == 0x22:
                table_str = CreateReportDescriptorNode(descriptor)
            elif bDescriptorType == 0x23:
                table_str = CreatePhysicalDescriptorNode(descriptor)
            elif bDescriptorType == 0x24:
                table_str = CreateAudioInterfaceDescriptorNode(descriptor, current_interface_subclass)
            elif bDescriptorType == 0x25:
                table_str = CreateAudioEndpointDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            class_specific_nodes.append(node_id)

        elif bDescriptorType in [6, 7, 11]:  # Other standard (excluding BOS and Device Capability)
            if bDescriptorType == 6:
                table_str = CreateDeviceQualifierDescriptorNode(descriptor)
            elif bDescriptorType == 7:
                table_str = CreateOtherSpeedConfigurationDescriptorNode(descriptor)
            elif bDescriptorType == 11:
                table_str = CreateInterfaceAssociationDescriptorNode(descriptor)
            dot.node(node_id, table_str, shape='none')
            if device_node:
                dot.edge(device_node, node_id)

        else:
            table_str = f"Unknown Descriptor Type: {hex(bDescriptorType)}"
            dot.node(node_id, table_str, shape='none')
            unknown_nodes.append(node_id)

        index += bLength

    # Chain string descriptors and position on the right
    if string_nodes:
        for i in range(len(string_nodes) - 1):
            dot.edge(string_nodes[i], string_nodes[i + 1])
        if root_node:
            dot.edge(root_node, string_nodes[0], style='invis')

    # Chain class-specific descriptors and position on the left
    if class_specific_nodes:
        for i in range(len(class_specific_nodes) - 1):
            dot.edge(class_specific_nodes[i], class_specific_nodes[i + 1])
        if root_node:
            dot.edge(class_specific_nodes[0], root_node, style='invis')

    # Chain unknown descriptors and position at the bottom
    if unknown_nodes:
        for i in range(len(unknown_nodes) - 1):
            dot.edge(unknown_nodes[i], unknown_nodes[i + 1])
        with dot.subgraph() as s:
            s.attr(rank='sink')
            for node in unknown_nodes:
                s.node(node)

    # Ensure horizontal positioning for class-specific and string chains
    if root_node:
        with dot.subgraph() as s:
            s.attr(rank='same')
            if class_specific_nodes:
                s.node(class_specific_nodes[0])
            s.node(root_node)
            if string_nodes:
                s.node(string_nodes[0])

    return dot