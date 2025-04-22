# USB - GET_DESCRIPTOR

## 🔍 **What is `USB_GET_DESCRIPTOR`?**

The `USB_GET_DESCRIPTOR` is a **standard USB control request** defined in the [USB specification](https://usb.org/document-library/usb-20-specification), used to **retrieve information ("descriptors")** about a USB device, its configuration, interfaces, endpoints, and more.

---

## 🧠 TL;DR

- It’s a **standard control transfer request** (part of USB protocol).
- Sent from host (e.g., your PC) to device.
- Used to ask the device to send back one of its descriptors (like its ID card or blueprint).

---

## ⚙️ Descriptor Types You Can Request

Each descriptor has a **type code**, and `USB_GET_DESCRIPTOR` lets you request any of these:

| Descriptor Type       | Value | Description                                   |
|-----------------------|-------|-----------------------------------------------|
| Device Descriptor     | 0x01  | Info about the device (VID, PID, USB version) |
| Configuration         | 0x02  | All interfaces and endpoints for a config     |
| String                | 0x03  | Human-readable strings (manufacturer, etc.)   |
| Interface             | 0x04  | Info about a logical function within a device |
| Endpoint              | 0x05  | Info about how data is transferred            |
| HID                   | 0x21  | HID-specific info (if it's a HID device)      |
| Report                | 0x22  | HID report format                             |

---

## 🧾 Structure of the Control Transfer (Host → Device)

Here's how `GET_DESCRIPTOR` is formatted in a USB control request:

| Field           | Value (for GET_DESCRIPTOR)              |
|----------------|------------------------------------------|
| **bmRequestType** | `0x80` = Device-to-host, Standard, Device |
| **bRequest**      | `0x06` = `GET_DESCRIPTOR`              |
| **wValue**        | High byte = descriptor type, Low byte = index |
| **wIndex**        | Language ID (used for string descriptors) |
| **wLength**       | Number of bytes to read               |

### Example (get device descriptor)

```c
bmRequestType = 0x80;
bRequest      = 0x06; // GET_DESCRIPTOR
wValue        = (0x01 << 8) | 0x00; // Device descriptor (type 1, index 0)
wIndex        = 0;
wLength       = 18; // Device descriptor is 18 bytes
```

---

## 📦 What Does It Return?

It returns a **structure (descriptor)**, which is just a block of bytes. For example, a **Device Descriptor** looks like this:

```text
Offset | Field              | Value (example)
-------|--------------------|----------------
0      | bLength            | 18
1      | bDescriptorType    | 01 (Device)
2-3    | bcdUSB             | 0x0200 (USB 2.0)
4      | bDeviceClass       | 00
...
8-9    | idVendor           | 0x046D (Logitech)
10-11  | idProduct          | 0xC534
```

---

## 💡 Why Is It Important?

- The **USB host must call `GET_DESCRIPTOR`** to enumerate and understand a device before using it.
- OSes like Linux, Windows, macOS all rely on this as the **first step when detecting a USB device**.

---

## 🛠️ Related Concepts

- `libusb_get_descriptor()` or `control_transfer()` functions in user-space tools like `libusb`
- `USBDEVFS_CONTROL` ioctl in Linux for raw USB access
- USB descriptors define the device’s capabilities — they're like a self-description manual

---

If you're reverse engineering a USB device or writing a custom USB driver, `GET_DESCRIPTOR` is one of the **first and most important tools** in your toolbox

---

## Getting Descriptors in Linux

### ✅ Requirements

Install `libusb-1.0`:

```bash
sudo apt install libusb-1.0-0-dev
```

### 📄 Code: [`simple_getDescriptor.c`](simple_getDescriptor.c)

#### 🧪 Compile & Run

```bash
gcc simple_getDescriptor.c -o simple_getDescriptor -lusb-1.0
sudo ./simple_getDescriptor
```

---

#### ✅ Output Example

```plaintext
Connected USB devices:
[0] VID: 046d PID: c534
[1] VID: 0781 PID: 5581

Select a device by number: 0

🔹 Device Descriptor:
0000: 12 01 00 02 00 00 00 40 6d 04 34 c5 01 01 01 02
0010: 03 01

🔹 Configuration Descriptor (Total length: 34 bytes):
0000: 09 02 22 00 01 01 00 a0 32 09 04 00 00 01 03 01
0010: 01 00 09 21 11 01 00 01 22 32 00 07 05 81 03 08
0020: 00 0a
```

### 📄 Code: [`dumpDescriptor.c`](dumpDescriptor.c)

#### ⚙️ Build & Run

```bash
gcc dumpDescriptor.c -o dumpDescriptor -lusb-1.0
sudo ./dumpDescriptor
```

#### 📝 Output Example: `usb_descriptors_dump.txt`

```plaintext
12 01 00 02 00 00 00 40 6d 04 c5 34 01 01 01 02 03 01 
09 02 22 00 01 01 00 a0 32 09 04 00 00 01 03 01 01 00 09 21 11 01 00 01 22 32 00 07 05 81 03 08 00 0a 
```
