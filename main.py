from processing import LoadHexArray, ProcessAndGenerateFlow

# Get descriptors
input_data = input("Enter Descriptor Bytes separated by spaces: ")
descriptors = LoadHexArray(input_data)

# Print debug descriptors
flowDiagram = ProcessAndGenerateFlow(descriptors)


