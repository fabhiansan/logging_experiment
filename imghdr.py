# imghdr.py source code from Python 3.12
# A stand-in for the removed imghdr module for Python 3.13+
# This is a simplified version for compatibility purposes.

__all__ = ['what']

def what(file, h=None):
    """Guesses the image file type from a file or byte stream."""
    f = None
    try:
        if h is None:
            if isinstance(file, str):
                f = open(file, 'rb')
                h = f.read(32)
            else:
                location = file.tell()
                h = file.read(32)
                file.seek(location)
        for tf in tests:
            res = tf(h, f)
            if res:
                return res
    finally:
        if f:
            f.close()
    return None

# All test functions
tests = []

def test_jpeg(h, f):
    """JPEG data"""
    if h[6:10] in (b'JFIF', b'Exif'):
        return 'jpeg'
    return None
tests.append(test_jpeg)

def test_png(h, f):
    """PNG"""
    if h.startswith(b'\211PNG\r\n\032\n'):
        return 'png'
    return None
tests.append(test_png)

def test_gif(h, f):
    """GIF ('87 and '89 variants)"""
    if h[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'
    return None
tests.append(test_gif)

def test_tiff(h, f):
    """TIFF (can be in Motorola or Intel byte order)"""
    if h[:2] in (b'MM', b'II'):
        return 'tiff'
    return None
tests.append(test_tiff)

def test_rgb(h, f):
    """SGI image library"""
    if h.startswith(b'\001\332'):
        return 'rgb'
    return None
tests.append(test_rgb)

def test_pbm(h, f):
    """PBM (portable bitmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'14' and h[2] in b' \t\n\r':
        return 'pbm'
    return None
tests.append(test_pbm)

def test_pgm(h, f):
    """PGM (portable graymap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'25' and h[2] in b' \t\n\r':
        return 'pgm'
    return None
tests.append(test_pgm)

def test_ppm(h, f):
    """PPM (portable pixmap)"""
    if len(h) >= 3 and \
        h[0] == ord(b'P') and h[1] in b'36' and h[2] in b' \t\n\r':
        return 'ppm'
    return None
tests.append(test_ppm)

def test_rast(h, f):
    """Sun raster file"""
    if h.startswith(b'\x59\xA6\x6A\x95'):
        return 'rast'
    return None
tests.append(test_rast)

def test_xbm(h, f):
    """X bitmap (X10 or X11)"""
    if h.startswith(b'#define '):
        return 'xbm'
    return None
tests.append(test_xbm)

def test_bmp(h, f):
    """BMP"""
    if h.startswith(b'BM'):
        return 'bmp'
    return None
tests.append(test_bmp)

def test_webp(h, f):
    """WebP"""
    if h.startswith(b'RIFF') and h[8:12] == b'WEBP':
        return 'webp'
    return None
tests.append(test_webp)

def test_exr(h, f):
    """OpenEXR"""
    if h.startswith(b'\x76\x2f\x31\x01'):
        return 'exr'
    return None
tests.append(test_exr)
