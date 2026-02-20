"""
Unit tests for the pure-Python parts of displayio.py.

These tests exercise Palette, Bitmap, TileGrid, and Group entirely in
standard CPython – no Pyodide or JS required.  Display.refresh() is not
tested here because it relies on the Pyodide js bridge.
"""

import os
import sys
import unittest

# Locate the module one directory above this file.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import displayio


# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

class TestPalette(unittest.TestCase):

    def test_len(self):
        p = displayio.Palette(4)
        self.assertEqual(len(p), 4)

    def test_default_color_is_black(self):
        p = displayio.Palette(3)
        self.assertEqual(p[0], 0x000000)

    def test_set_and_get(self):
        p = displayio.Palette(2)
        p[0] = 0xFF0000
        p[1] = 0x0000FF
        self.assertEqual(p[0], 0xFF0000)
        self.assertEqual(p[1], 0x0000FF)

    def test_set_tuple_rgb(self):
        p = displayio.Palette(2)
        p[0] = (255, 0, 0)
        self.assertEqual(p[0], 0xFF0000)
        p[1] = (0, 128, 64)
        self.assertEqual(p[1], 0x008040)

    def test_set_tuple_black(self):
        p = displayio.Palette(1)
        p[0] = (0, 0, 0)
        self.assertEqual(p[0], 0x000000)

    def test_set_tuple_wrong_length(self):
        p = displayio.Palette(1)
        with self.assertRaises(ValueError):
            p[0] = (255,)
        with self.assertRaises(ValueError):
            p[0] = (255, 0, 0, 0)

    def test_set_tuple_out_of_range(self):
        p = displayio.Palette(1)
        with self.assertRaises(ValueError):
            p[0] = (300, 0, 0)
        with self.assertRaises(ValueError):
            p[0] = (0, -1, 0)

    def test_transparent_defaults_opaque(self):
        p = displayio.Palette(2)
        self.assertFalse(p.is_transparent(0))
        self.assertFalse(p.is_transparent(1))

    def test_make_transparent_and_opaque(self):
        p = displayio.Palette(2)
        p.make_transparent(0)
        self.assertTrue(p.is_transparent(0))
        p.make_opaque(0)
        self.assertFalse(p.is_transparent(0))


# ---------------------------------------------------------------------------
# Bitmap
# ---------------------------------------------------------------------------

class TestBitmap(unittest.TestCase):

    def test_dimensions(self):
        b = displayio.Bitmap(10, 20, 4)
        self.assertEqual(b.width, 10)
        self.assertEqual(b.height, 20)
        self.assertEqual(b.value_count, 4)

    def test_default_zero(self):
        b = displayio.Bitmap(3, 3, 2)
        self.assertEqual(b[1, 1], 0)

    def test_set_and_get_tuple(self):
        b = displayio.Bitmap(5, 5, 2)
        b[2, 3] = 1
        self.assertEqual(b[2, 3], 1)

    def test_set_and_get_linear(self):
        b = displayio.Bitmap(5, 5, 2)
        b[7] = 1
        self.assertEqual(b[7], 1)

    def test_fill(self):
        b = displayio.Bitmap(4, 4, 4)
        b.fill(3)
        for y in range(4):
            for x in range(4):
                self.assertEqual(b[x, y], 3)

    def test_fill_then_overwrite(self):
        b = displayio.Bitmap(3, 3, 2)
        b.fill(1)
        b[1, 1] = 0
        self.assertEqual(b[1, 1], 0)
        self.assertEqual(b[0, 0], 1)


# ---------------------------------------------------------------------------
# TileGrid._render_to_buffer  (pure Python)
# ---------------------------------------------------------------------------

def _make_solid_tilegrid(color, w=4, h=4, x=0, y=0):
    """Helper: a TileGrid filled with a single opaque colour."""
    palette = displayio.Palette(1)
    palette[0] = color
    bitmap = displayio.Bitmap(w, h, 1)
    bitmap.fill(0)
    return displayio.TileGrid(bitmap, pixel_shader=palette, x=x, y=y)


class TestTileGrid(unittest.TestCase):

    def _buf(self, w=10, h=10):
        return bytearray(w * h * 4)

    def test_renders_red_pixel(self):
        tg = _make_solid_tilegrid(0xFF0000, w=1, h=1)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0xFF)  # R
        self.assertEqual(pixels[1], 0x00)  # G
        self.assertEqual(pixels[2], 0x00)  # B
        self.assertEqual(pixels[3], 0xFF)  # A

    def test_renders_green_pixel(self):
        tg = _make_solid_tilegrid(0x00FF00, w=1, h=1)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0x00)
        self.assertEqual(pixels[1], 0xFF)
        self.assertEqual(pixels[2], 0x00)
        self.assertEqual(pixels[3], 0xFF)

    def test_respects_x_y(self):
        tg = _make_solid_tilegrid(0x0000FF, w=1, h=1, x=3, y=2)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        off = (2 * 10 + 3) * 4
        self.assertEqual(pixels[off + 2], 0xFF)  # B at (3,2)
        self.assertEqual(pixels[0], 0)            # (0,0) untouched

    def test_respects_parent_offset(self):
        tg = _make_solid_tilegrid(0xFF0000, w=1, h=1)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 5, 5)
        off = (5 * 10 + 5) * 4
        self.assertEqual(pixels[off], 0xFF)
        self.assertEqual(pixels[0], 0)

    def test_transparent_index_not_drawn(self):
        palette = displayio.Palette(1)
        palette[0] = 0xFF0000
        palette.make_transparent(0)
        bitmap = displayio.Bitmap(2, 2, 1)
        bitmap.fill(0)
        tg = displayio.TileGrid(bitmap, pixel_shader=palette)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(sum(pixels), 0)

    def test_hidden_not_drawn(self):
        tg = _make_solid_tilegrid(0xFF0000, w=2, h=2)
        tg.hidden = True
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(sum(pixels), 0)

    def test_clipping_left(self):
        # x=-1: only the rightmost column of a 2-wide bitmap is visible.
        tg = _make_solid_tilegrid(0xFF0000, w=2, h=1, x=-1, y=0)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        # pixel at x=0 (bm col 1) should be red
        self.assertEqual(pixels[0], 0xFF)
        # no out-of-bounds writes occurred (bytearray is not resized)
        self.assertEqual(len(pixels), 10 * 10 * 4)

    def test_clipping_right(self):
        tg = _make_solid_tilegrid(0xFF0000, w=3, h=1, x=9, y=0)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        # Only x=9 is inside a 10-wide buffer
        self.assertEqual(pixels[9 * 4], 0xFF)
        # x=10 and x=11 must not have been written
        self.assertEqual(len(pixels), 10 * 10 * 4)

    def test_clipping_top(self):
        tg = _make_solid_tilegrid(0xFF0000, w=1, h=2, x=0, y=-1)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0xFF)  # y=0 (bm row 1) is visible

    def test_clipping_bottom(self):
        tg = _make_solid_tilegrid(0xFF0000, w=1, h=2, x=0, y=9)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[9 * 10 * 4], 0xFF)  # y=9 visible
        self.assertEqual(len(pixels), 10 * 10 * 4)

    def test_two_colours(self):
        palette = displayio.Palette(2)
        palette[0] = 0xFF0000  # red
        palette[1] = 0x0000FF  # blue
        bitmap = displayio.Bitmap(2, 1, 2)
        bitmap[0, 0] = 0   # red
        bitmap[1, 0] = 1   # blue
        tg = displayio.TileGrid(bitmap, pixel_shader=palette)
        pixels = self._buf()
        tg._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0xFF)  # R of pixel (0,0)
        self.assertEqual(pixels[2], 0x00)  # B of pixel (0,0)
        self.assertEqual(pixels[4], 0x00)  # R of pixel (1,0)
        self.assertEqual(pixels[6], 0xFF)  # B of pixel (1,0)


# ---------------------------------------------------------------------------
# Group._render_to_buffer  (pure Python)
# ---------------------------------------------------------------------------

class TestGroup(unittest.TestCase):

    def test_append_and_len(self):
        g = displayio.Group()
        self.assertEqual(len(g), 0)
        g.append("a")
        self.assertEqual(len(g), 1)

    def test_getitem_and_setitem(self):
        g = displayio.Group()
        g.append("a")
        g.append("b")
        self.assertEqual(g[0], "a")
        g[0] = "x"
        self.assertEqual(g[0], "x")

    def test_remove(self):
        g = displayio.Group()
        g.append("a")
        g.remove("a")
        self.assertEqual(len(g), 0)

    def test_insert(self):
        g = displayio.Group()
        g.append("b")
        g.insert(0, "a")
        self.assertEqual(g[0], "a")
        self.assertEqual(g[1], "b")

    def test_pop_default(self):
        g = displayio.Group()
        g.append("a")
        g.append("b")
        self.assertEqual(g.pop(), "b")
        self.assertEqual(len(g), 1)

    def test_pop_index(self):
        g = displayio.Group()
        g.append("a")
        g.append("b")
        self.assertEqual(g.pop(0), "a")

    def test_iter(self):
        g = displayio.Group()
        g.append("a")
        g.append("b")
        self.assertEqual(list(g), ["a", "b"])

    def test_hidden_skips_render(self):
        tg = _make_solid_tilegrid(0xFF0000, w=2, h=2)
        g = displayio.Group()
        g.append(tg)
        g.hidden = True
        pixels = bytearray(10 * 10 * 4)
        g._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(sum(pixels), 0)

    def test_x_y_offset_applied(self):
        tg = _make_solid_tilegrid(0xFF0000, w=1, h=1)
        g = displayio.Group(x=5, y=5)
        g.append(tg)
        pixels = bytearray(10 * 10 * 4)
        g._render_to_buffer(pixels, 10, 10, 0, 0)
        off = (5 * 10 + 5) * 4
        self.assertEqual(pixels[off], 0xFF)
        self.assertEqual(pixels[0], 0)

    def test_nested_group_offsets_accumulate(self):
        tg = _make_solid_tilegrid(0x0000FF, w=1, h=1)
        inner = displayio.Group(x=2, y=2)
        inner.append(tg)
        outer = displayio.Group(x=3, y=3)
        outer.append(inner)
        pixels = bytearray(10 * 10 * 4)
        outer._render_to_buffer(pixels, 10, 10, 0, 0)
        off = (5 * 10 + 5) * 4  # (3+2, 3+2) = (5, 5)
        self.assertEqual(pixels[off + 2], 0xFF)   # blue

    def test_multiple_children_rendered(self):
        red = _make_solid_tilegrid(0xFF0000, w=1, h=1, x=0, y=0)
        blue = _make_solid_tilegrid(0x0000FF, w=1, h=1, x=1, y=0)
        g = displayio.Group()
        g.append(red)
        g.append(blue)
        pixels = bytearray(10 * 10 * 4)
        g._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0xFF)        # red at (0,0)
        self.assertEqual(pixels[4 + 2], 0xFF)    # blue at (1,0)

    def test_later_child_overwrites_earlier(self):
        first = _make_solid_tilegrid(0xFF0000, w=2, h=2)  # red
        second = _make_solid_tilegrid(0x0000FF, w=2, h=2)  # blue, same pos
        g = displayio.Group()
        g.append(first)
        g.append(second)
        pixels = bytearray(10 * 10 * 4)
        g._render_to_buffer(pixels, 10, 10, 0, 0)
        self.assertEqual(pixels[0], 0x00)    # R overwritten by blue
        self.assertEqual(pixels[2], 0xFF)    # B


if __name__ == "__main__":
    unittest.main()
