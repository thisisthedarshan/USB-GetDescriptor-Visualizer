# usb-getdescriptor-visualizer

This project uses given sequence of bytes (assuming little endian format) and shows a visualization of the descriptors. The input given is the result of a USB *GET_DESCRIPTOR* command

## Pre-requisites

To use this, you need to install the [GraphViz](https://graphviz.org/) library for python (use [requirements.txt](requirements.txt) for installation of all packages).

You also need to have GraphViz installed on your system. Refer [GraphViz Downloads](https://graphviz.org/download/) section to install it for your distribution.

## Running

To run the program, simply install the [pre-requisites](#pre-requisites) and then run `python3 main.py`.

Once the program starts, it asks you to enter the result of **GET_DESCRIPTOR** USB Command in bytes (hex form), separated by space. Once all bytes are entered, it will then decode the data and generate a graph.

> [!NOTE]
> The program assumes the byte order to be in Little Endian format.

You can also pass `--render`, `--save` so as to skip the menu option asking you whether you want to save file or render it.

## Supported Descriptors

1. Standard USB Descriptors.
2. Audio Class USB Descriptors.
3. HID Class USB Descriptors.

---

Simple way to check what your system's device descriptors are:
> Pre-requisites: libusb-1.0 (sudo apt install libusb-1.0-0-dev)

1. Build the [`dumpDescriptor.c`](dumpDescriptor.c) file using `gcc dumpDescriptor.c -o dumpDescriptor -lusb-1.0`
2. Run the generated `dumpDescriptor` with **sudo** permissions.
3. Simply run `cat usb_descriptors_dump.txt | python3 main.py --render` to see the output

> [!NOTE]
> Check out the info [USB-GET_DESCRIPTORS](GET_DESCRIPTOR.md) to learn more about what is `USB_GET_DESCRIPTOR` command.
