# Copyright (c) 2025 Darshan P. All rights reserved.

# This work is licensed under the terms of the MIT license.  
# For a copy, see <https://opensource.org/licenses/MIT>.

from graphviz import Digraph
from processing import LoadHexArray, ProcessAndGenerateFlow
import argparse

def main():
    parser = argparse.ArgumentParser(description="Visualize USB descriptors")
    parser.add_argument('--save', action='store_true', help="Save output as usb_descriptors.png")
    parser.add_argument('--render', action='store_true', help="Render and display output")
    args = parser.parse_args()
    
    # Get descriptors
    input_data = input("Enter HEX Descriptor Bytes separated by spaces: ")
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
          dot.render('usb_descriptors', format='png', view=True, cleanup=True)
          print("Rendered and displayed")
      elif choice == "3":
          dot.render('usb_descriptors', format='png', view=True, cleanup=True)
          print("Saved as usb_descriptors.png and displayed")
      else:
          print("Invalid choice, no action taken")
        
    # Perform actions based on arguments
    if args.save and args.render:
        dot.render('usb_descriptors', format='png', view=True, cleanup=True)
        print("Saved as usb_descriptors.png and displayed")
    elif args.save:
        dot.render('usb_descriptors', format='png', cleanup=True)
        print("Saved as usb_descriptors.png")
    elif args.render:
        dot.render('usb_descriptors', format='png', view=True, cleanup=True)
        print("Rendered and displayed")
        

if __name__ == "__main__":
    main()