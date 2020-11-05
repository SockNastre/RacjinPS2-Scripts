# Made by SockNastre
# Unpacks decompressed .raw, requires Python 3

import os, sys

class Section:
    def __init__(self, index, size, offset):
        self.index = index
        self.size = size
        self.offset = offset

# Path of inputted file
path = sys.argv[1]
raw = open(path , 'rb')

sectionMetaSize = 16
textureMagicNumber = 2
sections = [];

# Checks if file is decompressed, 0 is magic number (not really, but first 4 bytes must always be 0)
if int.from_bytes(raw.read(4), byteorder='little') != 0:
    raise ValueError("Invalid file input, not a decompressed .raw file.")

# Getting number of sections
raw.seek(8)
sectionCount = int(int.from_bytes(raw.read(4), byteorder='little') / sectionMetaSize)

for i in range(sectionCount):
    raw.seek(i * 16)
    s = Section(int.from_bytes(raw.read(4), byteorder='little'), int.from_bytes(raw.read(4), byteorder='little'), int.from_bytes(raw.read(8), byteorder='little'))
    sections.append(s)

for s in sections:
    raw.seek(s.offset)
    
    # Checks if section is texture data
    extension = ".unk"
    if int.from_bytes(raw.read(4), byteorder='little') == textureMagicNumber:
        extension = ".texture"
    
    raw.seek(s.offset)
    data = bytes(raw.read(s.size))
    
    # Splits extension from path
    pre, ext = os.path.splitext(path)
    outputPath = pre + '_' + str(s.index) + extension
    
    # Outputs section
    with open(outputPath, 'wb') as sec:
        sec.write(data)
