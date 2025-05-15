# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import tempfile
import os
import subprocess
from graphviz import Digraph
from processing import LoadHexArray, ProcessAndGenerateFlow, addWatermark
import argparse

def USBGetDescriptorVisualizer():
    '''
        ## `main`
        
        ### Description
        Entry point for USBGetDescriptorVisualizer. Parses command-line arguments, processes USB GET_DESCRIPTOR byte sequence (little-endian), decodes descriptors, and visualizes them using GraphViz.

        ### Parameters
        - None (uses `argparse` to parse command-line inputs):
          - `data` (str, optional): Space-separated hex bytes from GET_DESCRIPTOR command.
          - `--save` (str, optional): Output filename (e.g., `output` saves as `output.png`). Defaults to `usb_descriptors.png`.
          - `--render` (flag): If set, opens visualization for viewing.

        ### Behavior
        1. **Parse Arguments**: Uses `argparse` to handle `data`, `--save`, and `--render`.
        2. **Collect Input**:
           - From `data` (positional args), `stdin` (e.g., piped file), or user prompt if no input.
           - Converts space-separated hex bytes to int list (e.g., `12 34` → `[0x12, 0x34]`).
           - Assumes little-endian format.
        3. **Decode Descriptors**: Processes bytes into Standard, Audio Class, or HID Class USB descriptors.
        4. **Visualize**: Generates GraphViz graph showing descriptor hierarchy.
        5. **Save Output**: Saves PNG to `--save` filename or `usb_descriptors.png`.
        6. **Render**: If `--render` is set, opens PNG for viewing.

        ### Returns
        - None (saves visualization and optionally displays it).

        ### Example
        ```bash
        python3 main.py --save output --render  12 01 00 03 00 00 00 09 69 00 20 04 89 00 01 02 03 01  # Saves as output.png, displays
        cat usb_descriptors_dump.txt | python3 main.py  # Reads stdin, saves as usb_descriptors.png
        ```
    '''
    parser = argparse.ArgumentParser(description="""
                                     Visualize USB descriptors!
                                     
                                     This handy tool is designed with the idea that analysing USB descriptors shouldn't be tough!
                                     It uses GraphViz to properly lay-down and visualize data from raw bytes!
                                     
                                     This tool is shared under the MIT License with the hope that it will be useful, but without any warranty.
                                     To see the license, visit <https://github.com/thisisthedarshan/USB-GetDescriptor-Visualizer/blob/main/LICENSE>
                                   
                                     The source code of this project is available on <https://github.com/thisisthedarshan/USB-GetDescriptor-Visualizer/>""")
    parser.add_argument('--save', type=str, nargs='?', default=None, help="Save output (defaults as usb_descriptors.png)")
    parser.add_argument('--render', action='store_true', help="Render and display output")
    parser.add_argument("data", nargs="*", help="Data to be processed")
    args = parser.parse_args()
    # Get descriptors from args
    input_data = " ".join(args.data)
    if len(input_data) <= 9:
        # Get descriptors from command line
        input_data = input("Enter HEX Descriptor Bytes separated by spaces: ")
        print("\n")
    descriptors = LoadHexArray(input_data)

    dot = Digraph()  # Prepare an instance

    dot.clear()  # Clear previous nodes
    # Print debug descriptors
    dot = ProcessAndGenerateFlow(descriptors)
    
    # Check if passed through command line :)
    if not (args.save or args.render):
      # Prompt user for action
      print("Choose an action:")
      print("1. Save to file")
      print("2. Render and view")
      print("3. Save and render")
      choice = input("Enter 1, 2, or 3: ")
      if choice == "1":
            dot.render('usb_descriptors', format='png', cleanup=True)
            addWatermark("usb_descriptors.png")
            print("Saved as usb_descriptors.png")
      elif choice == "2":
            viewTemp(dot)
      elif choice == "3":
            dot.render('usb_descriptors', format='png', view=True, cleanup=True)
            addWatermark("usb_descriptors.png")
            print("Saved as usb_descriptors.png and displayed")
      else:
            print("Invalid choice, no action taken")
        
    # Perform actions based on arguments
    if args.save is not None and args.render:
        filename = args.save if args.save != "" else "usb_descriptors"
        dot.render(filename, format='png', view=True, cleanup=True)
        addWatermark(filename+".png")
        print(f"Saved as {filename}.png and displayed")
    elif args.save is not None:
        filename = args.save if args.save != "" else "usb_descriptors"
        dot.render(filename, format='png', cleanup=True)
        addWatermark(filename+".png")
        print(f"Saved as {filename}.png")
    elif args.render:
        viewTemp(dot)

def viewTemp(dot:Digraph):
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmp_filename = tmpfile.name
        dot.render(tmp_filename, format='png', view=True, cleanup=True)
        addWatermark(tmp_filename+".png")
        print(f"Rendered and displayed as {tmp_filename}.png")
    # Spawn a process to delete the file after 5 minutes (300 seconds)
    if os.name == 'nt':  # Windows
        subprocess.Popen(f'ping 127.0.0.1 -n 300 && del "{tmp_filename}.png"', shell=True)
    else:  # Unix-like (Linux, macOS)
        subprocess.Popen(f'sleep 300 && rm "{tmp_filename}.png"', shell=True)

if __name__ == "__main__":
    USBGetDescriptorVisualizer()