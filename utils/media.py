import struct

def get_image_size(file_path):
    width: int = 0
    height: int = 0
    with open(file_path, 'rb') as img_file:
        # Read the header data, which typically contains image size information
        header_data = img_file.read(24)
        if header_data.startswith(b'\x89PNG\r\n\x1a\n'):
            # If it's a PNG file, parse the width and height information
            width, height = struct.unpack('>II', header_data[16:24])
        elif header_data.startswith(b'GIF87a') or header_data.startswith(b'GIF89a'):
            # If it's a GIF file, parse the width and height information
            width, height = struct.unpack('<HH', header_data[6:10])
        elif header_data.startswith(b'\xFF\xD8'):
            # If it's a JPEG file, find the SOI marker (Start of Image) and then parse the APP1 marker
            # The APP1 marker typically contains EXIF information, including width and height
            app1_offset = header_data.find(b'\xFF\xE1')
            if app1_offset != -1:
                app1_length = struct.unpack('>H', header_data[app1_offset + 4:app1_offset + 6])[0]
                app1_data = img_file.read(app1_length - 2)
                if app1_data.startswith(b'Exif\0\0'):
                    width, height = struct.unpack('<HH', app1_data[6:10])
                else:
                    raise ValueError("No EXIF data found")
            else:
                raise ValueError("No APP1 marker found")
        elif header_data.startswith(b'RIFF') and header_data[8:12] == b'WEBP':
            # If it's a WebP file, parse the width and height information from the VP8 portion
            vp8_offset = header_data.find(b'VP8 ')
            if vp8_offset != -1:
                width = struct.unpack('<H', header_data[vp8_offset + 19:vp8_offset + 21])[0]
                height = struct.unpack('<H', header_data[vp8_offset + 21:vp8_offset + 23])[0]
            else:
                raise ValueError("No VP8 data found")
        else:
            # For other file formats, you can parse based on the specific format
            raise ValueError("Unsupported image format")
    return width, height

def get_image_channels(file_path):
    with open(file_path, 'rb') as img_file:
        header_data = img_file.read(24)

        if header_data.startswith(b'\x89PNG\r\n\x1a\n'):
            # If it's a PNG file, parse the color type information
            color_type = struct.unpack('B', header_data[25:26])[0]
            if color_type == 2:
                return "RGB"
            elif color_type == 6:
                return "RGBA"
        elif header_data.startswith(b'\xFF\xD8'):
            # If it's a JPEG file, it's typically RGB
            return "RGB"
        elif header_data.startswith(b'GIF87a') or header_data.startswith(b'GIF89a'):
            # If it's a GIF file, it's typically RGB
            return "RGB"
        elif header_data.startswith(b'RIFF') and header_data[8:12] == b'WEBP':
            # If it's a WebP file, parse the channel information in the VP8 portion
            vp8_offset = header_data.find(b'VP8 ')
            if vp8_offset != -1:
                vp8_header = header_data[vp8_offset:vp8_offset + 10]
                if vp8_header == b'VP8X\x0a\x00\x00\x00':
                    return "RGBA"
                else:
                    return "RGB"
    
    # raise ValueError("Unable to determine the number of channels")
    return "RGB"

def determine_file_type(file_path):
    with open(file_path, 'rb') as file:
        header_data = file.read(12)

        if header_data.startswith(b'\x89PNG\r\n\x1a\n'):
            return ('image', 'PNG')
        elif header_data.startswith(b'GIF87a') or header_data.startswith(b'GIF89a'):
            return ('image', 'GIF')
        elif header_data.startswith(b'\xFF\xD8'):
            return ('image', 'JPEG')
        elif header_data.startswith(b'RIFF') and header_data[8:12] == b'WEBP':
            return ('image', 'WebP')
        elif header_data.startswith(b'BM'):
            return ('image', 'BMP')
        elif header_data.startswith(b'WAVE') or header_data.startswith(b'WAVEfmt '):
            return ('audio', 'Wave')
        elif header_data.startswith(b'FORM') and header_data[8:12] == b'AIFF':
            return ('audio', 'AIFF')
        elif header_data.startswith(b'ID3'):
            return ('audio', 'MP3')
        elif header_data.startswith(b'OggS'):
            return ('audio', 'OGG')
        elif header_data.startswith(b'\x00\x00\x00\x20ftypisom'):
            return ('audio', 'M4A')
        elif header_data.startswith(b'fLaC'):
            return ('audio', 'FLAC')
        elif header_data.startswith(b'RIFF') and header_data[8:12] == b'X-X-A':
            return ('audio', 'WMA')
        elif header_data.startswith(b'RIFF') and header_data[8:12] == b'3g2a':
            return ('audio', 'AAC')
        else:
            return ('Unknown', 'Unknown')