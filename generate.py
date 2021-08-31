#!/usr/bin/env python3

from numpy import packbits
from png import Reader

from glob import glob
import zlib
import struct

IDAT_X_X = b"000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000700e0000700e00381c0000381c00181800001818000c3000000c30000e7000000e700007e0000007e00003c0000003c00003c0000003c00007e0000007e0000e7000000e70000c3000000c300018180000181800381c0000381c00700e0000700e000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000ffff0000000000ffff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"


SAMPLE = [
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000011110000,
    0b00000000000000000000000111111000,
    0b00000000000000000000001100001100,
    0b00000000000000000000001100001100,
    0b00000000000000000000001100001100,
    0b00000000000000000000011000000110,
    0b00000000000000000000011000000110,
    0b00000000000000000000011000000110,
    0b00000000000000000000011000000110,
    0b00000000000000000000001100001100,
    0b00000000000000000000001100001100,
    0b00000000000000000000001100001100,
    0b00000000000000000000000111111000,
    0b00000000000000000000000011110000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
    0b00000000000000000000000000000000,
]

SAMPLE_PALETTE = [
    0x00, 0x00, 0x00,  # Black
    0x00, 0xFF, 0xFF,  # Cyan
]


def chunk(name, data):
    chunk_data = bytearray()
    chunk_data.extend(struct.pack(">I", len(data)))
    chunk_data.extend(name)
    chunk_data.extend(data)

    checksum = zlib.crc32(chunk_data[4:])

    chunk_data.extend(struct.pack(">I", checksum))
    return chunk_data


def render(palette, scanlines):
    # PNG Signature
    output = bytearray(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a")

    # IHDR
    WIDTH = 48
    HEIGHT = 48
    BIT_DEPTH = 1
    COLOR_TYPE = 3
    COMPRESSION = 0
    FILTER = 0
    INTERLACE = 0

    IHDR = (
        struct.pack(">I", WIDTH) +
        struct.pack(">I", HEIGHT) +
        struct.pack(">B", BIT_DEPTH) +
        struct.pack(">B", COLOR_TYPE) +
        struct.pack(">B", COMPRESSION) +
        struct.pack(">B", FILTER) +
        struct.pack(">B", INTERLACE)
    )

    output.extend(chunk(b"IHDR", IHDR))

    # Palette (PLTE)
    output.extend(chunk(b"PLTE", palette))

    # IDAT
    filter_lines = [b"\x00" + line.to_bytes(6, "big") for line in scanlines]

    image_data = b"".join(filter_lines)

    zlib_data = bytearray(b"\x78\x01\x01")
    zlib_data.extend(struct.pack("<H", len(image_data)))
    zlib_data.extend(struct.pack("<H", 0x10000+~len(image_data)))
    zlib_data.extend(image_data)
    zlib_data.extend(struct.pack(">I", zlib.adler32(image_data)))

    output.extend(chunk(b"IDAT", zlib_data))

    output.extend(chunk(b"IEND", b""))
    return output


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def png(path):
    reader = Reader(filename=path)
    width, height, values, _ = reader.read_flat()
    return [bytes(packbits(line)) for line in chunks(values, width)]


BACKGROUNDS = bytearray.fromhex(
    "000000"
    "FFFFFF"
    # "888888"
    # "cc4444"
    # "ff9266"
    # "4e9a06"
    # "73c48f"
    # "c4a000"
    # "ffce51"
    # "3465a4"
    # "48b9c7"
    # "75507b"
    # "ad7fa8"
    # "06989a"
    # "34e2e2"
    # "d3d7cf"
    # "eeeeec"
)

FOREGROUNDS = bytearray.fromhex(
    # "000000"
    # "888888"
    "cc0000"
    "f15d22"
    "64cf00"
    # "73c48f"
    # "c4a000"
    # "ffce51"
    "006fff"
    "2222cc"
    # "75507b"
    "ad7fa8"
    # "06989a"
    "34e2e2"
    # "d3d7cf"
    # "eeeeec"
)

EYES = glob("eyes/*.png")
NOSES = glob("noses/*.png")

if __name__ == "__main__":
    import sys
    import os
    import shutil

    if sys.argv[1] == "sample":
        output = render(SAMPLE_PALETTE, SAMPLE)

        with open("output.png", "wb") as f:
            f.write(output)
    elif sys.argv[1] == "palette":
        shutil.rmtree("palette", ignore_errors=True)
        os.mkdir("palette")

        left = png(EYES[0])
        nose = png(NOSES[0])
        right = png(EYES[1])

        scanlines = [int.from_bytes(b"".join(x), "big") for x in zip(left, nose, right)]

        for bg in chunks(BACKGROUNDS, 3):
            bg = bytes(bg)
            for base_fg in chunks(FOREGROUNDS, 3):
                pairs = (
                    (bg, base_fg),
                    (bg, (0x1000000 + ~int.from_bytes(base_fg, "big")).to_bytes(3, "big")),
                )

                if bg == b"\x00\x00\x00":
                    pairs = (pairs[0],)

                for (idx, (bg, fg)) in enumerate(pairs):
                    fg = bytes(fg)
                    path = f"palette/{idx}_{bg.hex()}_{fg.hex()}.png"
                    output = render(bg + fg, scanlines)
                    with open(path, "wb") as f:
                        f.write(output)
    elif sys.argv[1] == "faces":
        shutil.rmtree("faces", ignore_errors=True)
        os.mkdir("faces")

        for l_eye_name in EYES:
            l_eye = png(l_eye_name)
            for r_eye_name in EYES:
                r_eye = png(r_eye_name)
                for nose_name in NOSES:
                    nose = png(nose_name)
                    scanlines = [int.from_bytes(b"".join(x), "big") for x in zip(l_eye, nose, r_eye)]
                    name = "_".join([
                        l_eye_name.rsplit("/")[1][:-4],
                        nose_name.rsplit("/")[1][:-4],
                        r_eye_name.rsplit("/")[1][:-4],
                    ])
                    path = f"faces/{name}.png"
                    output = render(SAMPLE_PALETTE, scanlines)
                    with open(path, "wb") as f:
                        f.write(output)
    else:
        raise Exception("bad arg")
