# clean_dictionary.py
import os

input_file = "cmudict.0.7a"
# Set the output directory and filename as desired.
output_dir = "speech_recognition/preprocessing"
output_file = os.path.join(output_dir, "output_dictionary.txt")

# Create the output directory if it doesn't exist.
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        # Skip header lines that start with ";;;"
        if not line.startswith(";;;"):
            fout.write(line)

print(f"Clean dictionary saved as {output_file}")
