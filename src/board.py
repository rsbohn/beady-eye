"""
board - Minimal shim giving Pyodide sketches access to board.DISPLAY.

Usage::

    import board
    display = board.DISPLAY

``DISPLAY`` is a lazy property: the first time it is accessed it looks for
a ``<canvas>`` element whose ``id`` is ``"display"`` and wraps it in a
:class:`displayio.Display`.  Subsequent accesses return the same instance.
"""

_display = None


def _get_display():
    global _display
    if _display is None:
        import js
        import displayio
        _display = displayio.Display(js.document.getElementById("display"))
    return _display


class _Board:
    @property
    def DISPLAY(self):
        return _get_display()


import sys as _sys
_sys.modules[__name__] = _Board()
