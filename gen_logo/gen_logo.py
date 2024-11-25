import itertools
import sys

import png

W = 72
H = 28


def png_to_logo(path):
    reader = png.Reader(filename=path)
    w, h, rows, _ = reader.asRGBA()
    if w != W or h != H:
        raise Exception(f"image is not {W}x{H}")
    rows = list(rows)
    assert len(rows) == H
    assert all(x == W * 4 for x in map(len, rows))
    lines = []
    lines.append("#org 0xf00")
    lines.append(f"; {W}x{H} pixel Minimal logo ({int(W * H / 8)} bytes)")
    lines.append("MinimalLogo:")
    for row in rows:
        row_bits = []
        for pixel in itertools.batched(row, 4):
            if pixel[0] > 32 or pixel[1] > 32 or pixel[2] > 32:
                row_bits.append(1)
            else:
                row_bits.append(0)
        bs = []
        for bits in itertools.batched(row_bits, 8):
            s = "".join(map(str, bits))[::-1]
            i = int(s, 2)
            b = f"0x{i:02x}"
            bs.append(b)
        line = "  " + ",".join(map(str, bs))
        lines.append(line)
    code = "\n".join(lines)
    return code


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("<png>")
        sys.exit(1)
    filename = sys.argv[1]
    code = png_to_logo(filename)
    print(code)
