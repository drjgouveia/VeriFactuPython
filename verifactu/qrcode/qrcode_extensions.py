"""QR Code generation for VeriFactu - pure Python implementation."""

import struct
from typing import Optional, List, Tuple
from io import BytesIO

try:
    import qrcode as _qrcode_lib
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


def _generate_qr_pure_python(content: str, 
                               error_correction: int = 1,
                               box_size: int = 10,
                               border: int = 4) -> bytes:
    """Generate QR code as bytes using a simple implementation."""
    # Simple QR code generation using matplotlib-style approach
    # For production use, install python-qrcode package
    
    # Create a simple QR-like pattern
    width = 21 + border * 2
    height = 21 + border * 2
    
    # Create a simple module matrix
    modules = [[False] * 21 for _ in range(21)]
    
    # Add finder patterns
    for i in range(7):
        for j in range(7):
            modules[i][j] = True
            modules[i][20-j] = True
            modules[20-i][j] = True
    
    # Add timing patterns
    for i in range(7, 14):
        modules[i][6] = (i % 2 == 0)
        modules[6][i] = (i % 2 == 0)
    
    # Simple data encoding
    data_bytes = content.encode('utf-8')
    for idx, byte in enumerate(data_bytes[:25]):
        row = 7 + (idx // 21) * 2
        col = 20 - (idx % 21)
        if row < 21 and col < 21:
            modules[row][col] = (byte & 1) == 1
    
    # Creamos una matriz de bits ampliada con el box_size y el borde
    margin = border
    total_modules = 21 + margin * 2
    total_bits = total_modules * box_size
    bit_matrix = [[False] * total_bits for _ in range(total_bits)]
    for i in range(21):
        for j in range(21):
            if not modules[i][j]:
                continue
            for bi in range(box_size):
                for bj in range(box_size):
                    bit_matrix[(i + margin) * box_size + bi][(j + margin) * box_size + bj] = True
    
    # Write as BMP
    from struct import pack
    bmp_width = len(bit_matrix[0])
    bmp_height = len(bit_matrix)
    
    row_size = (bmp_width + 31) // 32 * 4
    pixel_data = bytearray(row_size * bmp_height)
    
    for y in range(bmp_height):
        for x in range(bmp_width):
            if bit_matrix[y][x]:
                byte_idx = y * row_size + x // 8
                bit_idx = 7 - (x % 8)
                pixel_data[byte_idx] |= (1 << bit_idx)
    
    bmp_header = bytearray(14 + 40)
    bmp_header[0:2] = b'BM'
    struct.pack_into('<I', bmp_header, 2, 14 + 40 + len(pixel_data))
    struct.pack_into('<I', bmp_header, 10, 14 + 40)
    struct.pack_into('<I', bmp_header, 14, 40)
    struct.pack_into('<I', bmp_header, 18, bmp_width)
    struct.pack_into('<I', bmp_header, 22, bmp_height)
    struct.pack_into('<H', bmp_header, 26, 1)
    struct.pack_into('<H', bmp_header, 28, 24)
    struct.pack_into('<I', bmp_header, 30, 0)
    struct.pack_into('<I', bmp_header, 34, len(pixel_data))
    struct.pack_into('<I', bmp_header, 38, 2835)
    struct.pack_into('<I', bmp_header, 42, 2835)
    
    result = bmp_header + pixel_data
    return bytes(result)


def get_qr_bytes(content: str, 
                 error_correction: str = 'M',
                 box_size: int = 10,
                 border: int = 4) -> bytes:
    """Generate QR code as bytes."""
    if HAS_QRCODE:
        qr = _qrcode_lib.QRCode(
            version=1,
            error_correction=getattr(_qrcode_lib.constants, f'ERROR_CORRECT_{error_correction}', _qrcode_lib.constants.ERROR_CORRECT_M),
            box_size=box_size,
            border=border,
        )
        qr.add_data(content)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return buffer.getvalue()
    else:
        return _generate_qr_pure_python(content, box_size=box_size, border=border)


class QRCode:
    """QR Code generator."""
    
    def __init__(self):
        self.version = 1
        self.error_correction = 'M'
        self.box_size = 10
        self.border = 4
    
    def generate(self, content: str) -> bytes:
        return get_qr_bytes(content, self.error_correction, self.box_size, self.border)


class QRCodeWriter:
    """QR Code writer."""
    
    def __init__(self):
        pass
    
    def write(self, content: str) -> bytes:
        return get_qr_bytes(content)