from PIL import Image, ImageDraw
import sys, os
import math
from binascii import unhexlify

def resetColor():
    return (0, 0, 0)

def hexToRgb(_hex):
    singleColorDigits = 2
    hexArray = [_hex[i:i+singleColorDigits] for i in range(0, len(_hex), singleColorDigits)]
    r = int(hexArray[0], 16) if len(hexArray) >= 1 else 0
    g = int(hexArray[1], 16) if len(hexArray) >= 2 else 160 # 0xA0 >> 160
    b = int(hexArray[2], 16) if len(hexArray) == 3 else 177 # 0xB1 >> 177
    return (r, g, b)

def RgbToHex(r, g, b):
    return "{:02x}{:02x}{:02x}".format(r, g, b)


def addPrefixHexCodes(hexEncodeArray):
    if (len(hexEncodeArray[len(hexEncodeArray) - 1]) % 2 != 0):
        hexEncodeArray[len(hexEncodeArray) - 1] = "0" + hexEncodeArray[len(hexEncodeArray) - 1]
    return hexEncodeArray

def removePrefixHexCodes(hexEncodeArray):
    hexEncodeArray[len(hexEncodeArray) - 1] = hexEncodeArray[len(hexEncodeArray) - 1].lstrip('0')
    return hexEncodeArray

def decodeHexCodes(hexArray):
    hexArray = hexArray[::-1]
    newHexArray = []
    done = False
    for i in hexArray:
        if (i == "000000" and done == False):
            continue
        else:
            done = True
            newHexArray.append(i)
    newHexArray = newHexArray[::-1]
    newHexArray.pop()
    segment = newHexArray[len(newHexArray) - 1]
    if (str(segment[len(segment) - 4::]) == "a0b1"):
        newHexArray[len(newHexArray) - 1] = segment[0:len(segment) - 4]
    elif (str(segment[len(segment) - 2::]) == "b1"):
        newHexArray[len(newHexArray) - 1] = segment[0:len(segment) - 2]
    return arrayToString(newHexArray)
        

def arrayToString(a): 
    _str = ""
    for i in a:
        _str += i
    return _str


def main():
    if os.path.exists(sys.argv[1]):
        if (sys.argv[2] == "e"):
            if (sys.argv[3] != None):
                _content = open(sys.argv[1], "rb").read()
                _contentHex = _content.hex()
                hexColorDigits = 6
                hexEncodeArray = [_contentHex[i:i+hexColorDigits] for i in range(0, len(_contentHex), hexColorDigits)]
                _scale = int(math.sqrt(len(hexEncodeArray))) + 1
                HORIZONTAL = _scale
                VERTICAL = _scale
                hexEncodeArray = addPrefixHexCodes(hexEncodeArray)
                hexEncodeArray.append("0000AA")
                
                im = Image.new('RGB', (HORIZONTAL, VERTICAL), resetColor())
                draw = ImageDraw.Draw(im)
                _i = 0
                for v in range(VERTICAL):
                    if (_i == len(hexEncodeArray)):
                        break
                    for h in range(HORIZONTAL):
                        if (_i == len(hexEncodeArray)):
                            break
                        draw.rectangle((v, h, v, h), fill=(hexToRgb(hexEncodeArray[_i])))
                        _i += 1
                im.save(f"{sys.argv[3]}.png")
            else:
                print("please specify output name.")
        elif (sys.argv[2] == "d"):
            if (sys.argv[3] != None):
                im = Image.open(sys.argv[1])
                pix = im.load()
                hexCode = ""
                for i in range(int(im.size[0])):
                    for j in range(int(im.size[1])):
                        _colors = pix[i, j]
                        hexCode += RgbToHex(_colors[0], _colors[1], _colors[2])
                hexColorDigits = 6
                hexEncodeArray = [hexCode[i:i+hexColorDigits] for i in range(0, len(hexCode), hexColorDigits)]
                hexCode = decodeHexCodes(hexEncodeArray)
                newFile = open(sys.argv[3], "wb")
                newFile.write(unhexlify(hexCode))
                newFile.close()
            else:
                print("please specify output name.")
        else:
            print(f"'{sys.argv[2]} is not a valid switch (should be e/d)'")
    else:
        print(f"file {sys.argv[1]} not exist")

if __name__ == "__main__":
    main()