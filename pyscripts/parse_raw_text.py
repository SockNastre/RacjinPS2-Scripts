# Made by SockNastre
# Parses .raw text files into utf-8 .txt , only works with some .raw text files

import os, sys

def get_letter_from_encoding(encodedCharBytes):
    return{
        0x0000 : ' ',
        0x0001 : '0',
        0x0002 : '1',
        0x0003 : '2',
        0x0004 : '3',
        0x0005 : '4',
        0x0006 : '5',
        0x0007 : '6',
        0x0008 : '7',
        0x0009 : '8',
        0x000A : '9',
        0x000B : 'U',
        0x000C : 's',
        0x000D : 'e',
        0x000E : 'i',
        0x000F : 't',
        0x0010 : 'm',
        0x0011 : 'h',
        0x0012 : 'a',
        0x0013 : 'c',
        0x0014 : 'n',
        0x0015 : 'r',
        0x0016 : 'f',
        0x0017 : 'l',
        0x0018 : 'H',
        0x0019 : 'd',
        0x001A : 'C',
        0x001B : 'k',
        0x001C : '.',
        0x001D : 'S',
        0x001E : 'p',
        0x001F : 'y',
        0x0020 : 'o',
        0x0021 : 'u',
        0x0022 : 'g',
        0x0023 : 'w',
        0x0024 : 'b',
        0x0025 : 'R',
        0x0026 : 'v',
        0x0027 : ',',
        0x0028 : 'P',
        0x0029 : 'N',
        0x002A : '!',
        0x002B : 'V',
        0x002C : 'G',
        0x002D : 'B',
        0x002E : 'K',
        0x002F : '-',
        0x0030 : 'W',
        0x0031 : 'L',
        0x0032 : 'j',
        0x0033 : 'M',
        0x0034 : 'F',
        0x0035 : 'z',
        0x0036 : 'A',
        0x0037 : '&',
        0x0038 : 'I',
        0x0039 : 'D',
        0x003A : 'T',
        0x003B : 'J',
        0x003C : 'Q',
        0x003D : '+',
        0x003E : '\'',
        0x003F : 'E',
        0x0040 : 'x',
        0x0041 : 'ç',
        0x0042 : 'Y',
        0x0043 : '(',
        0x0044 : 'q',
        0x0045 : ')',
        0x0046 : '=',
        0x0047 : 'O',
        0x0048 : ':',
        0x0049 : 'X',
        0x004A : '%',
        0x004B : '?',
        0x004C : 'Z',
        0x004D : '/',
        0x004E : ';',
        0x004F : '_',
        0x0050 : '"',
        0x0051 : 'Â',
        0x0052 : 'á',
        0x0053 : 'à',
        0x0054 : 'ã',
        0x0055 : 'â',
        0x0056 : 'é',
        0x0057 : 'ê',
        0x0058 : 'ó',
        0x0059 : 'ô',
        0x005A : 'Ú',
        0x005B : 'ú',
        0x005C : 'í',
        0x005D : 'À',
        0x005E : 'Á',
        0x005F : 'Ê',
        0x0060 : 'Í'
	}.get(encodedCharBytes, "0x" + encodedCharBytes.to_bytes(2, 'little').hex())

# Path of inputted file
path = sys.argv[1]
rawText = open(path , 'rb')

# If text is extracted from .raw
isExtracted = True

# Checks if inputted text is still contained in .raw
if int.from_bytes(rawText.read(4), 'little') == 0:
    isExtracted = False
    rawText.seek(4, 1) # Goes to, potentially, section offset

    if int.from_bytes(rawText.read(4), 'little') != 16:
        isExtracted = True

# How many bytes to skip at the beginning of the file
initialSkipCount = 0

if isExtracted == False:
    # Where text data would begin
    initialSkipCount = 16

# Header reading
rawText.seek(initialSkipCount)
sectionCount = int.from_bytes(rawText.read(4), 'little')
sectionOffsetArray = []

for i in range(sectionCount):
	sectionOffsetArray.append(int.from_bytes(rawText.read(4), 'little'))

sectionTerminator = 0x8000 # Designates end of section
parsedData = "" # Decoded text that will be output from this tool

for sectionOffset in sectionOffsetArray:
	rawText.seek(initialSkipCount + sectionOffset)
	encodedCharBytes = int.from_bytes(rawText.read(2), 'little')

	while encodedCharBytes != sectionTerminator:
		parsedData += get_letter_from_encoding(encodedCharBytes)
		encodedCharBytes = int.from_bytes(rawText.read(2), 'little')
	parsedData += '\n'

# Splits extension from path
pre, ext = os.path.splitext(path)
outputPath = pre + ".txt"

# Outputs parsed .raw text file
with open(outputPath, 'w', encoding='utf-8') as txt:
    txt.write(parsedData)
