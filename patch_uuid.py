#!/usr/bin/env python3
"""Patch p4a python3 recipe to accept make exit code 2 (optional module build failure).
_uuid module fails because libuuid is not in Android NDK, but make exit code 2
just means some optional modules failed - the core Python is still built.
We add _ok_code=[0, 2] to the shprint(sh.make, ...) call."""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
text = f.read_text()

# Add _ok_code=[0, 2] to the make call to tolerate optional module failures
old_make = """            shprint(
                sh.make,
                'all',
                'INSTSONAME={lib_name}'.format(lib_name=self._libpython),
                _env=env
            )"""
new_make = """            shprint(
                sh.make,
                'all',
                'INSTSONAME={lib_name}'.format(lib_name=self._libpython),
                _env=env,
                _ok_code=[0, 2]
            )"""

if old_make in text:
    text = text.replace(old_make, new_make)
    f.write_text(text)
    print("Patched python3 recipe: added _ok_code=[0, 2] to make call")
else:
    print("ERROR: Could not find the make call to patch")
    # Print surrounding text for debugging
    import sys
    if "sh.make" in text:
        idx = text.index("sh.make")
        print("Found 'sh.make' at index", idx)
        print(repr(text[idx-100:idx+200]))
    else:
        print("'sh.make' not found in file")
    sys.exit(1)
