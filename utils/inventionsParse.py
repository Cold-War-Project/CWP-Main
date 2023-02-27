import re
import yaml

# Regular expression to match "some_text_here" = {
pattern = re.compile(r'^(\w+)\s*=\s*{')

# Input file path and output file path
# Change this file name to the tech file you want to parse
input_file = '../common/technology/technologies/30_society.txt'
#optional output file name, can be sent to any folder, but defaults to the same folder this script is in.
output_file = 'output.yml'

# Dictionary to store the key-value pairs
data = {}

# Read the input file line by line
with open(input_file, 'r') as f:
    for line in f:
        # Match the pattern
        match = pattern.match(line.strip())
        if match:
            key = match.group(1)
            # Add the key to the dictionary with a dummy value
            data[key] = ''

# Write the output YAML file
with open(output_file, 'w') as f:
    for key in data:
        # Capitalize every word in the key
        title_case_key = ' '.join(word.capitalize() for word in key.split('_'))
        # Write the key-value pair to the output file
        f.write(f'{key}: "{title_case_key}"\n')

# Print the contents of the output YAML file
with open(output_file, 'r') as f:
    print(f.read())