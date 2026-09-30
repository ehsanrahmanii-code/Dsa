#!/usr/bin/env python3
"""Patch p4a python3 recipe to disable _uuid module (libuuid not in Android NDK)."""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
lines = f.read_text().splitlines(True)
for i, line in enumerate(lines):
    if 'self.ctx.python_recipe = self' in line:
        indent = '        '
        lines.insert(i + 1, indent + 'setup_local = Path(self.get_build_dir(arch.arch), "Modules", "Setup.local")\n')
        lines.insert(i + 2, indent + 'with open(setup_local, "a") as fh:\n')
        lines.insert(i + 3, indent + '    fh.write("\\n*disabled*\\n_uuid\\n")\n')
        break
f.write_text(''.join(lines))
print("Patched python3 recipe to disable _uuid module")
