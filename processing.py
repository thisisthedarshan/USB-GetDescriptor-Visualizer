from graphviz import Digraph

from helpers import bcd_to_string, get_vendor_name, get_product_name

dot = Digraph() # Prepare an instance
  
# Internal Functions
def CreateDeviceDescriptorNode(descriptor:list):
  '''**9.6.1 Device**: A device descriptor describes general information about a device. It includes information
that applies globally to the device and all of the device’s configurations. A device has only
one device descriptor.
  '''
  bLength = descriptor[0]
  bDescriptorType = descriptor[1]
  bcdUSB = bcd_to_string((descriptor[3] << 8) + descriptor[2])
  bDeviceClass = descriptor[4]
  bDeviceSubClass = descriptor[5]
  bDeviceProtocol = descriptor[6]
  bMaxPacketSize0 = descriptor[7]
  idVendor = descriptor[8]
  idProduct = (descriptor[9] << 8) + descriptor[10]
  bcdDevice = bcd_to_string((descriptor[11] << 8) + descriptor[12])
  iManufacturer = (descriptor[13] << 8) + descriptor[14]
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
<TR><TD>idVendor:  {idVendor} (${get_vendor_name(idVendor=idVendor)})</TD></TR>
<TR><TD>idProduct:  {idProduct} (${get_product_name(idVendor=idVendor, idProduct=idProduct)})</TD></TR>
<TR><TD>bcdDevice:  {bcdDevice}</TD></TR>
<TR><TD>iManufacturer:  {iManufacturer}</TD></TR>
<TR><TD>iProduct:  {iProduct}</TD></TR>
<TR><TD>iSerialNumber:  {iSerialNumber}</TD></TR>
<TR><TD>bNumConfigurations:  {bNumConfigurations}</TD></TR>
</TABLE>>'''
  
  
def CreateConfigurationDescriptorNode(descriptor:list):
  print("hello")
  
def CreateStringDescriptorNode(descriptor:list):
  print("hello")
  
def CreateInterfaceDescriptorNode(descriptor:list):
  print("hello")
  
def CreateEndpointDescriptorNode(descriptor:list):
  print("hello")
  
def CreateInterfaceAssociationDescriptorNode(descriptor:list):
  print("hello")
  
def CreateDeviceCapabilityDescriptorNode(descriptor:list):
  print("hello")
  
def CreateSSEndpointCompanionDescriptorNode(descriptor:list):
  print("hello")
  
def CreateSSPIsochEndpointCompanionDescriptorNode(descriptor:list):
  print("hello")
  
def CreateBOSDescriptorNode(descriptor:list):
  bLength
  bDescriptorType
  wTotalLength
  bNumDeviceCaps
  bLength
  bDescriptorType
  bDevCapabilityType
  CapabilityDependent

# Exposed APIs

def LoadHexArray(input_string):
    return [int(word, 16) for word in input_string.split() if word.startswith('0x')]

def ProcessAndGenerateFlow(descriptors:list):
  pass

# Block 1: Rectangle with title and content
dot.node('A', f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey"><B>Title 1</B></TD></TR>
<TR><TD>Content 1{1}</TD></TR>
<TR><TD>Content 2{1}</TD></TR>
</TABLE>>''', shape='none')

# Block 2: Same style, different data, title on top right
dot.node('B', '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
<TR><TD BGCOLOR="lightgrey" ALIGN="RIGHT"><B>Title 2</B></TD></TR>
<TR><TD>Content 2</TD></TR>
</TABLE>>''', shape='none')

# Connect blocks
dot.edge('A', 'B')

# Render flowchart
dot.render('flowchart', format='png', view=True)