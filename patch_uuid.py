#!/usr/bin/env python3
"""Patch p4a python3 recipe to remove _uuid from Modules/Setup.
libuuid is not available in Android NDK, so _uuid module can't be built.
We remove it from Modules/Setup in prebuild_arch so make doesn't try to build it."""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
text = f.read_text()

# Patch prebuild_arch to remove _uuid from Modules/Setup
old_prebuild = """    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        self.ctx.python_recipe = self
"""
new_prebuild = """    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        self.ctx.python_recipe = self
        # Remove _uuid from Modules/Setup (libuuid not in Android NDK)
        setup_file = Path(self.get_build_dir(arch.arch), 'Modules', 'Setup')
        if setup_file.exists():
            lines = setup_file.read_text().splitlines(True)
            new_lines = [l for l in lines if '_uuid' not in l]
            setup_file.write_text(''.join(new_lines))
"""

if old_prebuild in text:
    text = text.replace(old_prebuild, new_prebuild)
    f.write_text(text)
    print("Patched python3 recipe: remove _uuid from Modules/Setup in prebuild_arch")
else:
    print("ERROR: Could not find prebuild_arch to patch")
    import sys
    sys.exit(1)
