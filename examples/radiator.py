"""
Bloons TD6 themed information radiator for web-displayio (Pyodide).
No MQTT and no busy loop; demo values update on a JS interval.
"""

import js
from pyodide.ffi import create_proxy

import displayio

# Display colors
PALETTE = displayio.Palette(8)
PALETTE[0] = 0x0B1F12  # Deep jungle background
PALETTE[1] = 0x1E7D37  # Header green
PALETTE[2] = 0x163926  # Panel background
PALETTE[3] = 0x2BB24C  # Panel border
PALETTE[4] = 0xF7F1E1  # Primary text
PALETTE[5] = 0xFFD24A  # Accent yellow
PALETTE[6] = 0xFF6B3D  # Orange accent
PALETTE[7] = 0x5BC0EB  # Bloon blue

FONT_WIDTH = 5
FONT_HEIGHT = 7
FONT_SPACING = 1

FONT_5X7 = {
    " ": [
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
        "00000",
    ],
    "$": [
        "00100",
        "01111",
        "10100",
        "01110",
        "00101",
        "11110",
        "00100",
    ],
    "0": [
        "01110",
        "10001",
        "10011",
        "10101",
        "11001",
        "10001",
        "01110",
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "2": [
        "01110",
        "10001",
        "00001",
        "00010",
        "00100",
        "01000",
        "11111",
    ],
    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110",
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],
    "5": [
        "11111",
        "10000",
        "10000",
        "11110",
        "00001",
        "00001",
        "11110",
    ],
    "6": [
        "00110",
        "01000",
        "10000",
        "11110",
        "10001",
        "10001",
        "01110",
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ],
    "8": [
        "01110",
        "10001",
        "10001",
        "01110",
        "10001",
        "10001",
        "01110",
    ],
    "9": [
        "01110",
        "10001",
        "10001",
        "01111",
        "00001",
        "00010",
        "11100",
    ],
    "A": [
        "01110",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
    "B": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10001",
        "10001",
        "11110",
    ],
    "C": [
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110",
    ],
    "D": [
        "11100",
        "10010",
        "10001",
        "10001",
        "10001",
        "10010",
        "11100",
    ],
    "E": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "11111",
    ],
    "F": [
        "11111",
        "10000",
        "10000",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
    "G": [
        "01110",
        "10001",
        "10000",
        "10111",
        "10001",
        "10001",
        "01110",
    ],
    "H": [
        "10001",
        "10001",
        "10001",
        "11111",
        "10001",
        "10001",
        "10001",
    ],
    "I": [
        "01110",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "J": [
        "00001",
        "00001",
        "00001",
        "00001",
        "10001",
        "10001",
        "01110",
    ],
    "K": [
        "10001",
        "10010",
        "10100",
        "11000",
        "10100",
        "10010",
        "10001",
    ],
    "L": [
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "10000",
        "11111",
    ],
    "M": [
        "10001",
        "11011",
        "10101",
        "10101",
        "10001",
        "10001",
        "10001",
    ],
    "N": [
        "10001",
        "11001",
        "10101",
        "10011",
        "10001",
        "10001",
        "10001",
    ],
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "P": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10000",
        "10000",
        "10000",
    ],
    "Q": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10101",
        "10010",
        "01101",
    ],
    "R": [
        "11110",
        "10001",
        "10001",
        "11110",
        "10100",
        "10010",
        "10001",
    ],
    "S": [
        "01111",
        "10000",
        "10000",
        "01110",
        "00001",
        "00001",
        "11110",
    ],
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "U": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
    "V": [
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01010",
        "00100",
    ],
    "W": [
        "10001",
        "10001",
        "10001",
        "10101",
        "10101",
        "10101",
        "01010",
    ],
    "X": [
        "10001",
        "10001",
        "01010",
        "00100",
        "01010",
        "10001",
        "10001",
    ],
    "Y": [
        "10001",
        "10001",
        "01010",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
    "Z": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "10000",
        "11111",
    ],
}


def solid_tilegrid(width, height, color_index, x=0, y=0):
    bitmap = displayio.Bitmap(width, height, len(PALETTE))
    bitmap.fill(color_index)
    return displayio.TileGrid(bitmap, pixel_shader=PALETTE, x=x, y=y)


def circle_tilegrid(radius, color, x=0, y=0):
    size = radius * 2 + 1
    bitmap = displayio.Bitmap(size, size, 2)
    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = color
    palette.make_transparent(0)
    for py in range(size):
        for px in range(size):
            dx = px - radius
            dy = py - radius
            if dx * dx + dy * dy <= radius * radius:
                bitmap[px, py] = 1
    return displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)


class TextLabel:
    def __init__(self, text, x, y, color, scale=1, max_chars=None):
        self.scale = max(1, int(scale))
        self.max_chars = max_chars or len(text)
        self.char_width = FONT_WIDTH + FONT_SPACING
        width = (self.char_width * self.max_chars - FONT_SPACING) * self.scale
        height = FONT_HEIGHT * self.scale

        self.bitmap = displayio.Bitmap(width, height, 2)
        self.palette = displayio.Palette(2)
        self.palette[0] = 0x000000
        self.palette[1] = color
        self.palette.make_transparent(0)
        self.tilegrid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette, x=x, y=y)
        self.set_text(text)

    def set_text(self, text):
        text = (text or "").upper()[: self.max_chars]
        padded = text.ljust(self.max_chars)
        self.bitmap.fill(0)
        x = 0
        for ch in padded:
            self._draw_char(ch, x, 0, 1)
            x += self.char_width * self.scale

    def _draw_char(self, ch, x, y, color_index):
        pattern = FONT_5X7.get(ch, FONT_5X7[" "])
        for row, line in enumerate(pattern):
            for col, bit in enumerate(line):
                if bit == "1":
                    for dy in range(self.scale):
                        for dx in range(self.scale):
                            self.bitmap[
                                x + col * self.scale + dx,
                                y + row * self.scale + dy,
                            ] = color_index


class StatPanel:
    def __init__(self, title, value, x, y, width, height, value_scale=2):
        self.group = displayio.Group(x=x, y=y)

        self.group.append(solid_tilegrid(width, height, 3))
        self.group.append(solid_tilegrid(width - 4, height - 4, 2, x=2, y=2))

        title_label = TextLabel(title, 10, 8, PALETTE[5], max_chars=10)
        self.group.append(title_label.tilegrid)

        self.value_label = TextLabel(
            value,
            10,
            30,
            PALETTE[4],
            scale=value_scale,
            max_chars=8,
        )
        self.group.append(self.value_label.tilegrid)

    def set_value(self, value):
        self.value_label.set_text(value)


class StatusBadge:
    def __init__(self, x, y):
        self.group = displayio.Group(x=x, y=y)
        self.group.append(solid_tilegrid(140, 26, 6))
        self.label = TextLabel("WEB DEMO", 10, 8, PALETTE[4], max_chars=10)
        self.group.append(self.label.tilegrid)

    def set_text(self, text):
        self.label.set_text(text)


class BloonTrack:
    def __init__(self, x, y, width, height):
        self.group = displayio.Group(x=x, y=y)
        self.group.append(solid_tilegrid(width, height, 3))
        self.group.append(solid_tilegrid(width - 4, height - 4, 2, x=2, y=2))

        title_label = TextLabel("BLOON TRACK", 10, 8, PALETTE[5], max_chars=12)
        self.group.append(title_label.tilegrid)

        track = solid_tilegrid(width - 40, 6, 1, x=20, y=height // 2)
        self.group.append(track)

        bloon_count = 6
        start_x = 40
        end_x = max(start_x + 1, width - 40)
        spacing = (end_x - start_x) // (bloon_count - 1)
        offsets = [-12, 6, -8, 10, -6, 4]
        colors = [PALETTE[7], PALETTE[6], PALETTE[5], PALETTE[7], PALETTE[6], PALETTE[5]]
        for index in range(bloon_count):
            bx = start_x + spacing * index
            by = height // 2 + offsets[index]
            self.group.append(circle_tilegrid(14, colors[index], x=bx, y=by))


def build_display(display):
    root = displayio.Group()
    width = display.width
    height = display.height

    root.append(solid_tilegrid(width, height, 0))

    header_height = 40
    root.append(solid_tilegrid(width, header_height, 1))

    title = TextLabel("BLOONS TD6 COMMAND", 16, 10, PALETTE[4], max_chars=20)
    root.append(title.tilegrid)

    status_badge = StatusBadge(width - 160, 7)
    root.append(status_badge.group)

    margin = 10
    panel_width = (width - margin * 5) // 4
    panel_height = 110
    panel_y = header_height + margin

    panels = {
        "round": StatPanel("ROUND", "01", margin, panel_y, panel_width, panel_height),
        "cash": StatPanel(
            "CASH",
            "$650",
            margin * 2 + panel_width,
            panel_y,
            panel_width,
            panel_height,
        ),
        "lives": StatPanel(
            "LIVES",
            "100",
            margin * 3 + panel_width * 2,
            panel_y,
            panel_width,
            panel_height,
        ),
        "pops": StatPanel(
            "POPS",
            "0",
            margin * 4 + panel_width * 3,
            panel_y,
            panel_width,
            panel_height,
        ),
    }

    for panel in panels.values():
        root.append(panel.group)

    track = BloonTrack(
        margin,
        panel_y + panel_height + margin,
        width - margin * 2,
        height - panel_y - panel_height - margin * 2,
    )
    root.append(track.group)

    return root, panels, status_badge


def run():
    canvas = js.document.getElementById("display")
    display = displayio.Display(canvas, auto_refresh=False)

    root, panels, status_badge = build_display(display)
    display.show(root)
    display.refresh()

    status_badge.set_text("WEB DEMO")
    display.refresh()

    demo_round = 1
    demo_cash = 650
    demo_lives = 100
    demo_pops = 0

    def tick():
        nonlocal demo_round, demo_cash, demo_lives, demo_pops
        demo_round = min(99, demo_round + 1)
        demo_cash += 125
        demo_lives = max(1, demo_lives - 1)
        demo_pops += 350

        panels["round"].set_value(f"{demo_round:02d}")
        panels["cash"].set_value(f"${demo_cash}")
        panels["lives"].set_value(str(demo_lives))
        panels["pops"].set_value(str(demo_pops))
        display.refresh()

    tick_proxy = create_proxy(tick)
    js.setInterval(tick_proxy, 1500)


run()
