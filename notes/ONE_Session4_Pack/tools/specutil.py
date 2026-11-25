"""Helpers to patch extracted spec bodies without retyping their text."""
import sys
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from people import who  # noqa


def _sec_range(body, title):
    """(start, end) index of the section whose heading text starts with title."""
    for i, b in enumerate(body):
        if b[0] in ("h1", "app", "h2") and b[1].lower().startswith(title.lower()):
            lvl = b[0]
            j = i + 1
            while j < len(body):
                k = body[j][0]
                if k in ("h1", "app") or (lvl == "h2" and k == "h2"):
                    break
                j += 1
            return i, j
    raise KeyError(title)


def add(body, title, blocks, at_start=False):
    i, j = _sec_range(body, title)
    pos = i + 1 if at_start else j
    body[pos:pos] = blocks


def rename(body, old, new, tags=None, kind=None):
    i, _ = _sec_range(body, old)
    b = list(body[i])
    b[1] = new
    if tags:
        b[2] = tags
    if kind:
        b[0] = kind
    body[i] = tuple(b)


def drop(body, title):
    i, j = _sec_range(body, title)
    del body[i:j]


def take_controls(body, title):
    """Remove a controls appendix and return its table rows (minus header)."""
    i, j = _sec_range(body, title)
    rows = []
    for b in body[i:j]:
        if b[0] == "t":
            rows = [tuple(r) for r in b[1][1:]]
    del body[i:j]
    return rows


def restyle(body, startswith, kind):
    n = 0
    for i, b in enumerate(body):
        if b[0] not in ("h1", "h2", "app", "t") and b[1].startswith(startswith):
            body[i] = (kind, b[1])
            n += 1
    if n == 0:
        raise KeyError(startswith)


def replace(body, startswith, kind, text):
    for i, b in enumerate(body):
        if b[0] not in ("h1", "h2", "app", "t") and b[1].startswith(startswith):
            body[i] = (kind, text)
            return
    raise KeyError(startswith)


def section_titles(body):
    return [b[1] for b in body if b[0] in ("h1", "app")]
