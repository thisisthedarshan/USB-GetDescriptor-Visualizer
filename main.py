# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

import tempfile
import os
import subprocess
from time import sleep
from graphviz import Digraph
from processing import LoadHexArray, ProcessAndGenerateFlow
import argparse

def main():
    parser = argparse.ArgumentParser(description="Visualize USB descriptors")
    parser.add_argument('--save', type=str, nargs='?', default=None, help="Save output (defaults as usb_descriptors.png)")
    parser.add_argument('--render', action='store_true', help="Render and display output")
    args = parser.parse_args()
    
    # Get descriptors
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
            print("Saved as usb_descriptors.png")
      elif choice == "2":
            viewTemp(dot)
      elif choice == "3":
            dot.render('usb_descriptors', format='png', view=True, cleanup=True)
            print("Saved as usb_descriptors.png and displayed")
      else:
            print("Invalid choice, no action taken")
        
    # Perform actions based on arguments
    if args.save is not None and args.render:
        filename = args.save if args.save != "" else "usb_descriptors"
        dot.render(filename, format='png', view=True, cleanup=True)
        print(f"Saved as {filename}.png and displayed")
    elif args.save is not None:
        filename = args.save if args.save != "" else "usb_descriptors"
        dot.render(filename, format='png', cleanup=True)
        print(f"Saved as {filename}.png")
    elif args.render:
        viewTemp(dot)

def viewTemp(dot:Digraph):
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmp_filename = tmpfile.name
        dot.render(tmp_filename, format='png', view=True, cleanup=True)
        print(f"Rendered and displayed as {tmp_filename}.png")
    # Spawn a process to delete the file after 5 minutes (300 seconds)
    if os.name == 'nt':  # Windows
        subprocess.Popen(f'ping 127.0.0.1 -n 300 && del "{tmp_filename}.png"', shell=True)
    else:  # Unix-like (Linux, macOS)
        subprocess.Popen(f'sleep 300 && rm "{tmp_filename}.png"', shell=True)

if __name__ == "__main__":
    main()