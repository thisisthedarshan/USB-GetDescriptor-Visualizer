# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from babel import Locale
from extras.db import db
from extras.classes import CountryCodes, DeviceCapabilityTypeCode

def bcd_to_string(bcd_value: int) -> str:
    """
    Convert a 2-byte BCD (e.g., 0x0210) to string like "2.10"
    """
    if not (0 <= bcd_value <= 0xFFFF):
        raise ValueError("BCD value must be a 2-byte integer (0–65535)")
    # Extract nibbles
    major = (bcd_value & 0xFF00) >> 8
    minor = bcd_value & 0x00FF
    return f"{(major >> 4)}{(major & 0xF)}.{(minor >> 4)}{(minor & 0xF)}"


def get_vendor_name(idVendor: int) -> str:
    """
    Returns vendor name from the database for given vendor ID.
    """
    key = f"0x{idVendor:04x}"
    return db.get(key, {}).get("name", f"Unknown Vendor (0x{idVendor:04x})")


def get_product_name(idVendor: int, idProduct: int) -> str:
    """
    Returns product name from the database for given vendor and product ID.
    """
    vendor_key = f"0x{idVendor:04x}"
    product_key = f"0x{idProduct:04x}"
    return db.get(vendor_key, {}).get("devices", {}).get(product_key, {}).get("name", f"Unknown Product (0x{idProduct:04x})")


def get_device_bcd_string(bcdDevice: int) -> str:
    """
    Alias to convert device BCD into string format.
    """
    return bcd_to_string(bcdDevice)

def get_bos_device_capability(hexNum:int) -> str:
  if hexNum in DeviceCapabilityTypeCode:
    return DeviceCapabilityTypeCode[hexNum]
  else:
    return "Reserved"


def decode_country_code(code):
    if isinstance(code, str):
        code = int(code, 0)
    name = CountryCodes.get(code)
    if name is not None:
        return name
    else:
        return f"Unknown (0x{code:02X})"
    
def get_language_name(tag:str):
    """Convert a language tag to its English name."""
    try:
        locale = Locale.parse(tag.replace('-', '_').split(",")[0].strip())
        return locale.english_name
    except Exception:
        return tag