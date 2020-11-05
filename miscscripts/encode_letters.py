# Made by SockNastre
# Encodes text file as bytes, based on NUC encoding method for text
#
# NOTE: UTF-8 encoding expected from text file, encoding may be changed on line 113.
#

import os, sys

def get_encoded_int_from_char(char):
    return{
        ' ' : 0x0000,
        '0' : 0x0001,
        '1' : 0x0002,
        '2' : 0x0003,
        '3' : 0x0004,
        '4' : 0x0005,
        '5' : 0x0006,
        '6' : 0x0007,
        '7' : 0x0008,
        '8' : 0x0009,
        '9' : 0x000a,
        'U' : 0x000b,
        's' : 0x000c,
        'e' : 0x000d,
        'i' : 0x000e,
        't' : 0x000f,
        'm' : 0x0010,
        'h' : 0x0011,
        'a' : 0x0012,
        'c' : 0x0013,
        'n' : 0x0014,
        'r' : 0x0015,
        'f' : 0x0016,
        'l' : 0x0017,
        'H' : 0x0018,
        'd' : 0x0019,
        'C' : 0x001a,
        'k' : 0x001b,
        '.' : 0x001c,
        'S' : 0x001d,
        'p' : 0x001e,
        'y' : 0x001f,
        'o' : 0x0020,
        'u' : 0x0021,
        'g' : 0x0022,
        'w' : 0x0023,
        'b' : 0x0024,
        'R' : 0x0025,
        'v' : 0x0026,
        ',' : 0x0027,
        'P' : 0x0028,
        'N' : 0x0029,
        '!' : 0x002a,
        'V' : 0x002b,
        'G' : 0x002c,
        'B' : 0x002d,
        'K' : 0x002e,
        '-' : 0x002f,
        'W' : 0x0030,
        'L' : 0x0031,
        'j' : 0x0032,
        'M' : 0x0033,
        'F' : 0x0034,
        'z' : 0x0035,
        'A' : 0x0036,
        '&' : 0x0037,
        'I' : 0x0038,
        'D' : 0x0039,
        'T' : 0x003a,
        'J' : 0x003b,
        'Q' : 0x003c,
        '+' : 0x003d,
        '"' : 0x003e,
        'E' : 0x003f,
        'x' : 0x0040,
        'ç' : 0x0041,
        'Y' : 0x0042,
        '(' : 0x0043,
        'q' : 0x0044,
        ')' : 0x0045,
        '=' : 0x0046,
        'O' : 0x0047,
        ':' : 0x0048,
        'X' : 0x0049,
        '%' : 0x004a,
        '?' : 0x004b,
        'Z' : 0x004c,
        '/' : 0x004d,
        ';' : 0x004e,
        '_' : 0x004f,
        '\'' : 0x0050,
        'Â' : 0x0051,
        'á' : 0x0052,
        'à' : 0x0053,
        'ã' : 0x0054,
        'â' : 0x0055,
        'é' : 0x0056,
        'ê' : 0x0057,
        'ó' : 0x0058,
        'ô' : 0x0059,
        'Ú' : 0x005a,
        'ú' : 0x005b,
        'í' : 0x005c,
        'À' : 0x005d,
        'Á' : 0x005e,
        'Ê' : 0x005f,
        'Í' : 0x0060,
        '\n' : 0x8000 # Text section terminator, AKA end of line
    }.get(char, 0x4F4E)

# Path of inputted file
path = sys.argv[1]
text = open(path, 'r', encoding='utf-8')

encodedIntArray = []

for line in text:
        indexSkipArray = []

        # Looping through characters in line
        for i in range(len(line)):
                if i in indexSkipArray:
                        continue

                c = line[i]
                encodedChar = get_encoded_int_from_char(c)

                if c == '0':
                        if line[i + 1] == 'x':
                                # Separates hex short into two separate bytes for endianness fixing
                                hexByte1 = line[i+2:i+4]
                                hexByte2 = line[i+4:i+6]
                                encodedChar = int(hexByte2 + hexByte1, 16)

                                # Adds hex short-related indexes to array to indicate them to be skipped in line 119
                                indexSkipArray.extend(range(i+1, i+6))
                encodedIntArray.append(encodedChar)

# Splits extension from path
pre, ext = os.path.splitext(path)
outputPath = pre + ".bytes"

# Outputs parsed .raw text file
with open(outputPath, 'wb') as bytesFile:
	for encodedInt in encodedIntArray:
                bytesFile.write(encodedInt.to_bytes(2, 'little'))
