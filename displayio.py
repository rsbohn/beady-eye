"""
displayio - Pure Python shim for CircuitPython's displayio module.

Runnable under Pyodide; rendering is delegated to the HTML Canvas
(beady-eye JavaScript canvas layer) via a single ``putImageData`` call
inside :meth:`Display.refresh`.

All other code is pure Python with no JS dependencies and can be
exercised with standard CPython.

Version: 0.1 (MVP)

Supported classes (core subset of CircuitPython displayio):
    Palette    – indexed colour table
    Bitmap     – 2-D array of palette indices
    TileGrid   – renders a Bitmap via a Palette into a pixel buffer
    Group      – ordered container of TileGrid / Group objects
    Display    – wraps an HTML <canvas>; drives show / refresh

Usage (inside Pyodide)::

    import js, displayio

    display = displayio.Display(js.document.getElementById("display"))

    palette = displayio.Palette(2)
    palette[0] = 0x000000
    palette[1] = 0xFF0000
    palette.make_transparent(0)

    bitmap = displayio.Bitmap(64, 32, 2)
    bitmap.fill(1)

    tg = displayio.TileGrid(bitmap, pixel_shader=palette, x=10, y=10)

    group = displayio.Group()
    group.append(tg)
    display.show(group)
"""


class Palette:
    """A mutable, indexed sequence of RGB colours.

    Compatible with CircuitPython's ``displayio.Palette``.

    Args:
        num_colors (int): Number of colour slots.
    """

    def __init__(self, num_colors):
        self._colors = [0x000000] * num_colors
        self._transparent = [False] * num_colors

    def __len__(self):
        return len(self._colors)

    def __setitem__(self, index, color):
        if isinstance(color, tuple):
            if len(color) != 3:
                raise ValueError("color tuple must have exactly 3 elements (r, g, b)")
            r, g, b = color
            for name, val in (("r", r), ("g", g), ("b", b)):
                if not (0 <= val <= 255):
                    raise ValueError(
                        f"{name} value {val} is out of range 0-255"
                    )
            color = (r << 16) | (g << 8) | b
        self._colors[index] = int(color)

    def __getitem__(self, index):
        return self._colors[index]

    def make_transparent(self, palette_index):
        """Mark palette entry *palette_index* as fully transparent."""
        self._transparent[palette_index] = True

    def make_opaque(self, palette_index):
        """Mark palette entry *palette_index* as fully opaque."""
        self._transparent[palette_index] = False

    def is_transparent(self, palette_index):
        """Return ``True`` if palette entry *palette_index* is transparent."""
        return self._transparent[palette_index]


class Bitmap:
    """A mutable 2-D grid of palette colour indices.

    Compatible with CircuitPython's ``displayio.Bitmap``.
    Pixels are accessed with ``bitmap[x, y]`` notation.

    Args:
        width (int): Bitmap width in pixels.
        height (int): Bitmap height in pixels.
        value_count (int): Number of distinct palette indices (kept for
            API compatibility; not enforced at runtime).
    """

    def __init__(self, width, height, value_count):
        self.width = width
        self.height = height
        self.value_count = value_count
        self._data = bytearray(width * height)

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            return self._data[y * self.width + x]
        return self._data[index]

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            x, y = index
            self._data[y * self.width + x] = int(value)
        else:
            self._data[index] = int(value)

    def fill(self, value):
        """Set every pixel to palette index *value*."""
        v = int(value)
        for i in range(len(self._data)):
            self._data[i] = v


class TileGrid:
    """Renders a :class:`Bitmap` into an RGBA pixel buffer using a
    :class:`Palette`.

    Compatible with the core subset of CircuitPython's
    ``displayio.TileGrid``.  No JS imports; rendering targets a plain
    Python :class:`bytearray`.

    Args:
        bitmap: A :class:`Bitmap` instance.
        pixel_shader: A :class:`Palette` instance.
        x (int): Horizontal position on the display.
        y (int): Vertical position on the display.
    """

    def __init__(self, bitmap, *, pixel_shader, x=0, y=0, **kwargs):
        self.bitmap = bitmap
        self.pixel_shader = pixel_shader
        self.x = x
        self.y = y
        self._hidden = False

    @property
    def hidden(self):
        """Whether this TileGrid is hidden (not rendered)."""
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = bool(value)

    def _render_to_buffer(self, pixels, buf_width, buf_height, offset_x, offset_y):
        """Pure Python: write RGBA pixel data into the flat bytearray *pixels*.

        Args:
            pixels (bytearray): RGBA buffer of size
                ``buf_width * buf_height * 4``.
            buf_width (int): Width of the destination buffer.
            buf_height (int): Height of the destination buffer.
            offset_x (int): Accumulated horizontal offset from parent Groups.
            offset_y (int): Accumulated vertical offset from parent Groups.
        """
        if self._hidden:
            return
        bm = self.bitmap
        palette = self.pixel_shader
        ox = self.x + offset_x
        oy = self.y + offset_y
        for y in range(bm.height):
            py = oy + y
            if py < 0 or py >= buf_height:
                continue
            for x in range(bm.width):
                px = ox + x
                if px < 0 or px >= buf_width:
                    continue
                idx = bm[x, y]
                if palette.is_transparent(idx):
                    continue
                color = palette[idx]
                off = (py * buf_width + px) * 4
                pixels[off] = (color >> 16) & 0xFF      # R
                pixels[off + 1] = (color >> 8) & 0xFF   # G
                pixels[off + 2] = color & 0xFF           # B
                pixels[off + 3] = 255                    # A


class Group:
    """An ordered, mutable list of :class:`TileGrid` and nested
    :class:`Group` objects.

    Compatible with the core subset of CircuitPython's
    ``displayio.Group``.  No JS imports.

    Args:
        scale (int): Scale factor (stored for API compatibility; currently
            treated as 1 – scaling is deferred to a future version).
        x (int): Horizontal translation applied to all children.
        y (int): Vertical translation applied to all children.
    """

    def __init__(self, *, scale=1, x=0, y=0):
        self.scale = scale
        self.x = x
        self.y = y
        self._contents = []
        self._hidden = False

    @property
    def hidden(self):
        """Whether this Group (and all its children) is hidden."""
        return self._hidden

    @hidden.setter
    def hidden(self, value):
        self._hidden = bool(value)

    def append(self, item):
        """Append *item* to the end of the group."""
        self._contents.append(item)

    def remove(self, item):
        """Remove the first occurrence of *item* from the group."""
        self._contents.remove(item)

    def insert(self, index, item):
        """Insert *item* before position *index*."""
        self._contents.insert(index, item)

    def pop(self, index=-1):
        """Remove and return the item at *index* (default: last)."""
        return self._contents.pop(index)

    def __len__(self):
        return len(self._contents)

    def __getitem__(self, index):
        return self._contents[index]

    def __setitem__(self, index, value):
        self._contents[index] = value

    def __iter__(self):
        return iter(self._contents)

    def _render_to_buffer(self, pixels, buf_width, buf_height, offset_x, offset_y):
        """Pure Python: recursively render all children into *pixels*."""
        if self._hidden:
            return
        ox = offset_x + self.x
        oy = offset_y + self.y
        for item in self._contents:
            item._render_to_buffer(pixels, buf_width, buf_height, ox, oy)


class Display:
    """Manages the root display group and renders it to an HTML ``<canvas>``.

    Compatible with the core subset of CircuitPython's
    ``displayio.Display``.

    The **only** JS bridge in the entire module is a single
    ``ctx.putImageData()`` call inside :meth:`refresh`.  Every other
    method is pure Python.

    Pass either an HTML canvas *element* (obtained via Pyodide's ``js``
    bridge) or a canvas element *id* string.

    Args:
        canvas: An HTML canvas element or its ``id`` string.
        width (int | None): Override canvas width in pixels.
        height (int | None): Override canvas height in pixels.
        auto_refresh (bool): When ``True`` (default), :meth:`refresh` is
            called automatically after :meth:`show` or a
            :attr:`root_group` assignment.

    Example::

        import js, displayio
        display = displayio.Display(js.document.getElementById("display"))
    """

    def __init__(self, canvas, *, width=None, height=None, auto_refresh=True):
        if isinstance(canvas, str):
            try:
                import js as _js
            except ImportError:
                raise RuntimeError(
                    "js module is not available; pass a canvas element directly"
                )
            self._canvas = _js.document.getElementById(canvas)
        else:
            self._canvas = canvas

        if width is not None:
            self._canvas.width = width
        if height is not None:
            self._canvas.height = height

        self.width = int(self._canvas.width)
        self.height = int(self._canvas.height)
        self._root_group = None
        self._auto_refresh = auto_refresh

    @property
    def root_group(self):
        """The root :class:`Group` currently shown on the display."""
        return self._root_group

    @root_group.setter
    def root_group(self, group):
        self._root_group = group
        if self._auto_refresh:
            self.refresh()

    def show(self, group):
        """Set *group* as the root group and refresh the display."""
        self.root_group = group

    def refresh(self):
        """Render the scene graph into an RGBA buffer, then upload it to
        the HTML canvas.

        Scene traversal is entirely pure Python.  The single JS bridge
        call is ``ctx.putImageData()`` at the end of this method.
        """
        pixels = bytearray(self.width * self.height * 4)
        if self._root_group is not None:
            self._root_group._render_to_buffer(
                pixels, self.width, self.height, 0, 0
            )
        # --- single JS bridge call ----------------------------------------
        # Convert the Python bytearray to a JS Uint8ClampedArray and push
        # it to the canvas in one putImageData call.
        from pyodide.ffi import to_js
        from js import Uint8ClampedArray, ImageData
        js_buf = to_js(pixels)
        img = ImageData.new(
            Uint8ClampedArray.new(js_buf.buffer), self.width, self.height
        )
        self._canvas.getContext("2d").putImageData(img, 0, 0)
        # ------------------------------------------------------------------
