# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

Classes = {
    0: {"name": "(Defined at Interface level)", "subclass": {}},
    1: {
        "name": "Audio",
        "subclass": {
            1: {"name": "Control Device", "protocols": {}},
            2: {"name": "Streaming", "protocols": {}},
            3: {"name": "MIDI Streaming", "protocols": {}},
        },
    },
    2: {
        "name": "Communications",
        "subclass": {
            1: {"name": "Direct Line", "protocols": {}},
            2: {
                "name": "Abstract (modem)",
                "protocols": {
                    0: "None",
                    1: "AT-commands (v.25ter)",
                    2: "AT-commands (PCCA101)",
                    3: "AT-commands (PCCA101 + wakeup)",
                    4: "AT-commands (GSM)",
                    5: "AT-commands (3G)",
                    6: "AT-commands (CDMA)",
                    254: "Defined by command set " "descriptor",
                    255: "Vendor Specific (MSFT RNDIS?)",
                },
            },
            3: {"name": "Telephone", "protocols": {}},
            4: {"name": "Multi-Channel", "protocols": {}},
            5: {"name": "CAPI Control", "protocols": {}},
            6: {"name": "Ethernet Networking", "protocols": {}},
            7: {"name": "ATM Networking", "protocols": {}},
            8: {"name": "Wireless Handset Control", "protocols": {}},
            9: {"name": "Device Management", "protocols": {}},
            10: {"name": "Mobile Direct Line", "protocols": {}},
            11: {"name": "OBEX", "protocols": {}},
            12: {
                "name": "Ethernet Emulation",
                "protocols": {7: "Ethernet Emulation (EEM)"},
            },
        },
    },
    3: {
        "name": "Human Interface Device",
        "subclass": {
            0: {
                "name": "No Subclass",
                "protocols": {0: "None", 1: "Keyboard", 2: "Mouse"},
            },
            1: {
                "name": "Boot Interface Subclass",
                "protocols": {0: "None", 1: "Keyboard", 2: "Mouse"},
            },
        },
    },
    5: {"name": "Physical Interface Device", "subclass": {}},
    6: {
        "name": "Imaging",
        "subclass": {
            1: {
                "name": "Still Image Capture",
                "protocols": {1: "Picture Transfer Protocol (PIMA " "15470)"},
            }
        },
    },
    7: {
        "name": "Printer",
        "subclass": {
            1: {
                "name": "Printer",
                "protocols": {
                    0: "Reserved/Undefined",
                    1: "Unidirectional",
                    2: "Bidirectional",
                    3: "IEEE 1284.4 compatible " "bidirectional",
                    255: "Vendor Specific",
                },
            }
        },
    },
    8: {
        "name": "Mass Storage",
        "subclass": {
            1: {
                "name": "RBC (typically Flash)",
                "protocols": {
                    0: "Control/Bulk/Interrupt",
                    1: "Control/Bulk",
                    80: "Bulk-Only",
                },
            },
            2: {"name": "SFF-8020i, MMC-2 (ATAPI)", "protocols": {}},
            3: {"name": "QIC-157", "protocols": {}},
            4: {
                "name": "Floppy (UFI)",
                "protocols": {
                    0: "Control/Bulk/Interrupt",
                    1: "Control/Bulk",
                    80: "Bulk-Only",
                },
            },
            5: {"name": "SFF-8070i", "protocols": {}},
            6: {
                "name": "SCSI",
                "protocols": {
                    0: "Control/Bulk/Interrupt",
                    1: "Control/Bulk",
                    80: "Bulk-Only",
                },
            },
        },
    },
    9: {
        "name": "Hub",
        "subclass": {
            0: {
                "name": "Unused",
                "protocols": {
                    0: "Full speed (or root) hub",
                    1: "Single TT",
                    2: "TT per port",
                },
            }
        },
    },
    10: {
        "name": "CDC Data",
        "subclass": {
            0: {
                "name": "Unused",
                "protocols": {
                    48: "I.430 ISDN BRI",
                    49: "HDLC",
                    50: "Transparent",
                    80: "Q.921M",
                    81: "Q.921",
                    82: "Q.921TM",
                    144: "V.42bis",
                    145: "Q.932 EuroISDN",
                    146: "V.120 V.24 rate ISDN",
                    147: "CAPI 2.0",
                    253: "Host Based Driver",
                    254: "CDC PUF",
                    255: "Vendor specific",
                },
            }
        },
    },
    11: {"name": "Chip/SmartCard", "subclass": {}},
    13: {"name": "Content Security", "subclass": {}},
    14: {
        "name": "Video",
        "subclass": {
            0: {"name": "Undefined", "protocols": {}},
            1: {"name": "Video Control", "protocols": {}},
            2: {"name": "Video Streaming", "protocols": {}},
            3: {"name": "Video Interface Collection", "protocols": {}},
        },
    },
    15: {"name": "Personal Healthcare", "subclass": {}},
    16: {
        "name": "Audio/Video",
        "subclass": {
            1: {"name": "AVData Control", "protocols": {}},
            2: {"name": "AVData Video Stream", "protocols": {}},
            3: {"name": "AVData Audio Stream", "protocols": {}},
        },
    },
    17: {"name": "Billboard", "subclass": {}},
    18: {"name": "Type-C Bridge", "subclass": {}},
    19: {"name": "Bulk Display", "subclass": {}},
    20: {
        "name": "MCTCP over USB",
        "subclass": {
            0: {
                "name": "MCTCP Management",
                "protocols": {1: "MCTCP 1.x", 2: "MCTCP 2.x"},
            },
            1: {"name": "MCTCP Host", "protocols": {1: "MCTCP 1.x", 2: "MCTCP 2.x"}},
        },
    },
    60: {"name": "I3C", "subclass": {}},
    88: {"name": "Xbox", "subclass": {66: {"name": "Controller", "protocols": {}}}},
    220: {
        "name": "Diagnostic",
        "subclass": {
            1: {
                "name": "Reprogrammable Diagnostics",
                "protocols": {1: "USB2 Compliance"},
            }
        },
    },
    224: {
        "name": "Wireless",
        "subclass": {
            1: {
                "name": "Radio Frequency",
                "protocols": {
                    1: "Bluetooth",
                    2: "Ultra WideBand Radio Control",
                    3: "RNDIS",
                },
            },
            2: {
                "name": "Wireless USB Wire Adapter",
                "protocols": {
                    1: "Host Wire Adapter Control/Data " "Streaming",
                    2: "Device Wire Adapter " "Control/Data Streaming",
                    3: "Device Wire Adapter Isochronous " "Streaming",
                },
            },
        },
    },
    239: {
        "name": "Miscellaneous Device",
        "subclass": {
            1: {"name": "?", "protocols": {1: "Microsoft ActiveSync", 2: "Palm Sync"}},
            2: {
                "name": "?",
                "protocols": {
                    1: "Interface Association",
                    2: "Wire Adapter Multifunction " "Peripheral",
                },
            },
            3: {"name": "?", "protocols": {1: "Cable Based Association"}},
            5: {"name": "USB3 Vision", "protocols": {}},
        },
        254: {
            "name": "Application Specific Interface",
            "subclass": {
                1: {"name": "Device Firmware Update", "protocols": {}},
                2: {"name": "IRDA Bridge", "protocols": {}},
                3: {
                    "name": "Test and Measurement",
                    "protocols": {1: "TMC", 2: "USB488"},
                },
            },
        },
        255: {
            "name": "Vendor Specific Class",
            "subclass": {
                255: {
                    "name": "Vendor Specific Subclass",
                    "protocols": {255: "Vendor Specific Protocol"},
                }
            },
        },
    },
}

More = {
  "Audio" : {
    0x0100 :  "USB Undefined",
    0x0101 :  "USB Streaming",
    0x01ff :  "USB Vendor Specific",
    0x0200 :  "Input Undefined",
    0x0201 :  "Microphone",
    0x0202 :  "Desktop Microphone",
    0x0203 :  "Personal Microphone",
    0x0204 :  "Omni-directional Microphone",
    0x0205 :  "Microphone Array",
    0x0206 :  "Processing Microphone Array",
    0x0300 :  "Output Undefined",
    0x0301 :  "Speaker",
    0x0302 :  "Headphones",
    0x0303 :  "Head Mounted Display Audio",
    0x0304 :  "Desktop Speaker",
    0x0305 :  "Room Speaker",
    0x0306 :  "Communication Speaker",
    0x0307 :  "Low Frequency Effects Speaker",
    0x0400 :  "Bidirectional Undefined",
    0x0401 :  "Handset",
    0x0402 :  "Headset",
    0x0403 :  "Speakerphone, no echo reduction",
    0x0404 :  "Echo-suppressing speakerphone",
    0x0405 :  "Echo-canceling speakerphone",
    0x0500 :  "Telephony Undefined",
    0x0501 :  "Phone line",
    0x0502 :  "Telephone",
    0x0503 :  "Down Line Phone",
    0x0600 :  "External Undefined",
    0x0601 :  "Analog Connector",
    0x0602 :  "Digital Audio Interface",
    0x0603 :  "Line Connector",
    0x0604 :  "Legacy Audio Connector",
    0x0605 :  "SPDIF interface",
    0x0606 :  "1394 DA stream",
    0x0607 :  "1394 DV stream soundtrack",
    0x0700 :  "Embedded Undefined",
    0x0701 :  "Level Calibration Noise Source",
    0x0702 :  "Equalization Noise",
    0x0703 :  "CD Player",
    0x0704 :  "DAT",
    0x0705 :  "DCC",
    0x0706 :  "MiniDisc",
    0x0707 :  "Analog Tape",
    0x0708 :  "Phonograph",
    0x0709 :  "VCR Audio",
    0x070a :  "Video Disc Audio",
    0x070b :  "DVD Audio",
    0x070c :  "TV Tuner Audio",
    0x070d :  "Satellite Receiver Audio",
    0x070e :  "Cable Tuner Audio",
    0x070f :  "DSS Audio",
    0x0710 :  "Radio Receiver",
    0x0711 :  "Radio Transmitter",
    0x0712 :  "Multitrack Recorder",
    0x0713 :  "Synthesizer"
  },
  "hid" : {
    0x21 :  "HID",
    0x22 :  "Report",
    0x23 :  "Physical"
  },
  "hid-item" : {
    0x04 : "Usage Page",
    0x08 : "Usage",
    0x14 : "Logical Minimum",
    0x18 : "Usage Minimum",
    0x24 : "Logical Maximum",
    0x28 : "Usage Maximum",
    0x34 : "Physical Minimum",
    0x38 : "Designator Index",
    0x44 : "Physical Maximum",
    0x48 : "Designator Minimum",
    0x54 : "Unit Exponent",
    0x58 : "Designator Maximum",
    0x64 : "Unit",
    0x74 : "Report Size",
    0x78 : "String Index",
    0x80 : "Input",
    0x84 : "Report ID",
    0x88 : "String Minimum",
    0x90 : "Output",
    0x94 : "Report Count",
    0x98 : "String Maximum",
    0xa0 : "Collection",
    0xa4 : "Push",
    0xa8 : "Delimiter",
    0xb0 : "Feature",
    0xb4 : "Pop",
    0xc0 : "End Collection"
  }
}

DeviceCapabilityTypeCode = {
  0x01 : "Wireless_USB",
  0x02  : "USB 2.0 EXTENSION",
  0x03 : "SUPERSPEED_USB",
  0x04 : "CONTAINER_ID",
  0x05 : "PLATFORM",
  0x06  : "POWER_DELIVERY_CAPABILITY ",
  0x07 : "BATTERY_INFO_CAPABILITY",
  0x08  : "PD_CONSUMER_PORT_CAPABILITY ",
  0x09  : "PD_PROVIDER_PORT_CAPABILITY ",
  0x0A : "SUPERSPEED_PLUS",
  0x0B  : "PRECISION_TIME_MEASUREMENT ",
  0x0C : "Wireless_USB_Ext",
  0x0D  : "BILLBOARD ",
  0x0E  : "AUTHENTICATION ",
  0x0F  : "BILLBOARD_EX ",
  0x10 : "CONFIGURATION_SUMMARY",
  0x11 : "FWStatus Capability",
}

CountryCodes = {
    0x00: "Not Supported",
    0x01: "Arabic",
    0x02: "Belgian",
    0x03: "Canadian‑Bilingual",
    0x04: "Canadian‑French",
    0x05: "Czechia",
    0x06: "Danish",
    0x07: "Finnish",
    0x08: "French",
    0x09: "German",
    0x0A: "Greek",
    0x0B: "Hebrew",
    0x0C: "Hungary",
    0x0D: "International (ISO)",
    0x0E: "Italian",
    0x0F: "Japan (Katakana)",
    0x10: "Korean",
    0x11: "Latin American",
    0x12: "Netherlands",
    0x13: "Norwegian",
    0x14: "Persian",
    0x15: "Poland",
    0x16: "Portuguese",
    0x17: "Russia",
    0x18: "Slovakia",
    0x19: "Spanish",
    0x1A: "Swedish",
    0x1B: "Swiss/French",
    0x1C: "Swiss/German",
    0x1D: "Switzerland",
    0x1E: "Taiwan",
    0x1F: "Turkish‑Q",
    0x20: "UK",
    0x21: "US",
    0x22: "Yugoslavia",
    0x23: "Turkish‑F",
}



