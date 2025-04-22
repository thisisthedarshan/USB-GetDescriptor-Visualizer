from graphviz import Digraph
from extras.classes import Classes, More
from helpers import bcd_to_string, get_vendor_name, get_product_name, get_bos_device_capability

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

    # Get class and subclass names from Classes dictionary
    class_info = Classes.get(bInterfaceClass, {})
    class_name = class_info.get("name", "Unknown")
    subclass_info = class_info.get("subclass", {}).get(bInterfaceSubClass, {})
    subclass_name = subclass_info.get("name", "Unknown")

    return f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Interface Descriptor</B></TD></TR>
<TR><TD>bLength: {bLength}</TD></TR>
<TR><TD>bDescriptorType: {bDescriptorType}</TD></TR>
<TR><TD>bInterfaceNumber: {bInterfaceNumber}</TD></TR>
<TR><TD>bAlternateSetting: {bAlternateSetting}</TD></TR>
<TR><TD>bNumEndpoints: {bNumEndpoints}</TD></TR>
<TR><TD>bInterfaceClass: {bInterfaceClass} ({class_name})</TD></TR>
<TR><TD>bInterfaceSubClass: {bInterfaceSubClass} ({subclass_name})</TD></TR>
<TR><TD>bInterfaceProtocol: {bInterfaceProtocol}</TD></TR>
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
    return [int(word, 16) for word in input_string.split() if word.startswith('0x')]

def ProcessAndGenerateFlow(descriptors: list) -> Digraph:
    dot = Digraph()  # Prepare an instance
    dot.clear()  # Clear previous nodes
    index = 0
    prev_id = None
    while index < len(descriptors):
        bLength = descriptors[index]
        if bLength == 0 or index + 1 >= len(descriptors):
            break  # Safety check for invalid length or end of list
        bDescriptorType = descriptors[index + 1]
        if index + bLength > len(descriptors):
            break  # Prevent slicing beyond list length
        descriptor = descriptors[index:index + bLength]
        if bDescriptorType == 1:  # Device Descriptor
            table_str = CreateDeviceDescriptorNode(descriptor)
        elif bDescriptorType == 2:  # Configuration Descriptor
            table_str = CreateConfigurationDescriptorNode(descriptor)
        elif bDescriptorType == 3:  # String Descriptor
            table_str = CreateStringDescriptorNode(descriptor)
        elif bDescriptorType == 4:  # Interface Descriptor
            current_interface_subclass = descriptor[6]
            table_str = CreateInterfaceDescriptorNode(descriptor)
        elif bDescriptorType == 5:  # Endpoint Descriptor
            table_str = CreateEndpointDescriptorNode(descriptor)
        elif bDescriptorType == 11:  # Interface Association Descriptor
            table_str = CreateInterfaceAssociationDescriptorNode(descriptor)
        elif bDescriptorType == 15:  # BOS Descriptor
            table_str = CreateBOSDescriptorNode(descriptor)
        elif bDescriptorType == 16:  # Device Capability Descriptor
            table_str = CreateDeviceCapabilityDescriptorNode(descriptor)
        elif bDescriptorType == 0x24:  # Class-Specific Interface Descriptor
            table_str = CreateAudioInterfaceDescriptorNode(descriptor, current_interface_subclass)
        elif bDescriptorType == 0x25:  # Class-Specific Endpoint Descriptor
            table_str = CreateAudioEndpointDescriptorNode(descriptor)
        elif bDescriptorType == 48:  # SuperSpeed Endpoint Companion
            table_str = CreateSSEndpointCompanionDescriptorNode(descriptor)
        elif bDescriptorType == 49:  # SuperSpeedPlus Isochronous Endpoint Companion
            table_str = CreateSSPIsochEndpointCompanionDescriptorNode(descriptor)
        else:
            table_str = f"Unknown Descriptor Type: {hex(bDescriptorType)}"
        node_id = f"desc_{index}"
        dot.node(node_id, table_str, shape='none')
        if prev_id is not None:
            dot.edge(prev_id, node_id)
        prev_id = node_id
        index += bLength
    dot.render('usb_descriptors', format='png', view=True)
