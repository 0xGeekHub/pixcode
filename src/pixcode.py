from os import path
from io import BytesIO
from PIL import Image, ImageDraw
from binascii import unhexlify
from math import sqrt
from libs.core import *


class Pixcode:
    def __init__(self) -> None:
        pass

    def image_obj_to_bytes(self, image: Image.Image) -> bytes:
        image_byte_array = BytesIO()
        image.save(image_byte_array, format="png")
        return image_byte_array.getvalue()


    def hex_to_rgb(self, hex_segment: list):
        global HEX_DIGITS_PER_CHAR
        hex_char_array = [hex_segment[i : i + HEX_DIGITS_PER_CHAR] for i in range(0, len(hex_segment), HEX_DIGITS_PER_CHAR)]
        r = int(hex_char_array[0], 16) if len(hex_char_array) >= 1 else 0
        g = int(hex_char_array[1], 16) if len(hex_char_array) >= 2 else 160 # 0xA0 >> 160
        b = int(hex_char_array[2], 16) if len(hex_char_array) == 3 else 177 # 0xB1 >> 177
        return (r, g, b)


    def rgb_to_hex(self, r: str, g: str, b: str) -> str:
        return "{:02x}{:02x}{:02x}".format(r, g, b)


    def add_prefix_hex(self, hex_array: list):
        last_segment_pos = len(hex_array) - 1
        if (len(hex_array[last_segment_pos]) % 2 != 0):
            hex_array[last_segment_pos] = '0' + hex_array[last_segment_pos]
        return hex_array


    def decode_hex_codes(self, hex_decode_canvas: str) -> str:
        hex_decode_canvas = hex_decode_canvas[::-1]
        new_hex_decode_canvas = []
        done = False
        for i in hex_decode_canvas:
            if (i == "000000" and done == False):
                continue
            else:
                done = True
                new_hex_decode_canvas.append(i)
        new_hex_decode_canvas = new_hex_decode_canvas[::-1]
        new_hex_decode_canvas.pop()
        segment = new_hex_decode_canvas[len(new_hex_decode_canvas) - 1]
        if (str(segment[len(segment) - 4::]) == "a0b1"):
            new_hex_decode_canvas[len(new_hex_decode_canvas) - 1] = segment[0:len(segment) - 4]
        elif (str(segment[len(segment) - 2::]) == "b1"):
            new_hex_decode_canvas[len(new_hex_decode_canvas) - 1] = segment[0:len(segment) - 2]
        return "".join(new_hex_decode_canvas)
    

    def has_disk_capacity(self, hex_data_size: int, disk_dimension: int):
        return disk_dimension ** 2 >= hex_data_size


    def _encode(self, input_bytes: bytes, output_file_name: str, disk: DiskSize|int|None) -> None|bytes:
        global HEX_DIGITS, LAST_SEGMENT_PADDDING, NULL_COLOR
        hex_data = input_bytes.hex()
        hex_encode_canvas = [hex_data[i : i + HEX_DIGITS] for i in range(0, len(hex_data), HEX_DIGITS)]
        
        disk_dimension: int = 0
        if (type(disk) == int):
            disk_dimension = int(disk)
        else:
            if (disk == None or (type(disk) == DiskSize and disk == DiskSize.AUTO)):
                disk_dimension = int(sqrt(len(hex_encode_canvas))) + 1
            else:
                disk_dimension = int(disk.value)

        if (self.has_disk_capacity(len(hex_encode_canvas), disk_dimension)):
            vertical = disk_dimension
            horizontal = disk_dimension
            hex_encode_canvas = self.add_prefix_hex(hex_encode_canvas)
            hex_encode_canvas.append(LAST_SEGMENT_PADDDING)

            image = Image.new('RGB', (horizontal, vertical), NULL_COLOR)
            draw = ImageDraw.Draw(image)
            i = 0
            for v in range(vertical):
                if (i == len(hex_encode_canvas)):
                    break
                for h in range(horizontal):
                    if (i == len(hex_encode_canvas)):
                        break
                    draw.rectangle((v, h, v, h), fill=(self.hex_to_rgb(hex_encode_canvas[i])))
                    i += 1
            
            if (not (output_file_name == None or len(output_file_name) == 0)):
                image.save(f"{output_file_name}.png")
            return (hex_encode_canvas, self.image_obj_to_bytes(image))
        return None


    def encode(self, input_file: str, output_file_name: str, disk: DiskSize|int|None) -> None|bytes:
        if (input_file == None or len(input_file) == 0 or not path.exists(input_file)):
            return None
        file = open(input_file, "rb")
        input_bytes = file.read()
        file.close()
        return self._encode(input_bytes, output_file_name, disk)


    def encode_bytes(self, input_bytes: bytes, output_file_name: str, disk: DiskSize|int|None) -> None|bytes:
        if (input_bytes == None or len(input_bytes) == 0):
            return None
        return self._encode(input_bytes, output_file_name, disk)


    def _decode(self, image: Image.Image, output_file_name: str) -> bytes:
        global HEX_DIGITS
        pixel_map = image.load()
        hex_decode_canvas = ""
        for h in range(int(image.size[0])):
            for v in range(int(image.size[1])):
                colors = pixel_map[h, v]
                hex_decode_canvas += self.rgb_to_hex(colors[0], colors[1], colors[2])
        
        hex_decode_canvas = [hex_decode_canvas[i : i + HEX_DIGITS] for i in range(0, len(hex_decode_canvas), HEX_DIGITS)]
        hex_decode_canvas = unhexlify(self.decode_hex_codes(hex_decode_canvas))
        
        if (not (output_file_name == None or len(output_file_name) == 0)):
            newFile = open(output_file_name, "wb")
            newFile.write(hex_decode_canvas)
            newFile.close()
        return hex_decode_canvas


    def decode(self, input_file: str, output_file_name: str) -> None|bytes:
        if (input_file == None or len(input_file) == 0 or not path.exists(input_file)):
            return None
        image = Image.open(input_file)
        return self._decode(image, output_file_name)
        

    def decode_bytes(self, input_bytes: bytes, output_file_name: str) -> None|bytes:
        if (input_bytes == None or len(input_bytes) == 0):
            return None
        image = Image.open(BytesIO(input_bytes))
        return self._decode(image, output_file_name)