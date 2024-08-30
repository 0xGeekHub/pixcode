from enum import Enum

HEX_DIGITS = 6
HEX_DIGITS_PER_CHAR = 2
LAST_SEGMENT_PADDDING = '0000AA'
NULL_COLOR = (0, 0, 0)

class DiskSize(Enum):
    AUTO = 0
    D256B = 256
    D512B = 512
    D1KB = 1024
    D2KB = 2048
    D4KB = 4096
    D8KB = 8192
    D16KB = 16384
    D32KB = 32768
    D64KB = 65536
    D1MB = D1KB ** 2
    D1GB = D1KB ** 3 # Stopping here, because all the digital data
                     # world-wide is considered around 64zb in 2020
                     # and with a 1tb pixcode disk, we need 21845
                     # disks in order to store all the world's data
                     # it's logical (or at least, theorically logical) 
                     # Here's the calculation:
                     # ((1024**3) ** 2 * 3) / (1024 ** 6) = 3eb
                     # so (64 * 1024 * 1eb) / 3eb ~= 21845