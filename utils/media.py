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