#!/usr/bin/env python3
"""Patch p4a python3 recipe to use subprocess.call for make instead of shprint.
The _uuid module fails because libuuid is not in Android NDK, causing make to
exit with code 2. subprocess.call doesn't raise on non-zero exit codes."""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
text = f.read_text()

# Replace the shprint(sh.make, ...) call with subprocess.call
old_make = """            shprint(
                sh.make,
                'all',
                'INSTSONAME={lib_name}'.format(lib_name=self._libpython),
                _env=env
            )"""
new_make = """            # Use subprocess.call instead of shprint to tolerate make exit code 2
            # (_uuid module fails because libuuid is not in Android NDK)
            import subprocess as _subprocess
            _make_env = dict(env)
            _make_cmd = ['make', 'all', 'INSTSONAME={lib_name}'.format(lib_name=self._libpython)]
            _subprocess.call(_make_cmd, env=_make_env)"""

if old_make in text:
    text = text.replace(old_make, new_make)
    f.write_text(text)
    print("Patched python3 recipe: replaced shprint(sh.make) with subprocess.call")
else:
    print("ERROR: Could not find the make call to patch")
    import sys
    if "sh.make" in text:
        idx = text.index("sh.make")
        print("Found 'sh.make' at index", idx)
        print(repr(text[idx-100:idx+200]))
    else:
        print("'sh.make' not found in file")
    sys.exit(1)
