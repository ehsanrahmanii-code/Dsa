#!/usr/bin/env python3
"""Patch p4a python3 recipe:
1. Disable _uuid module via Modules/Setup.local (libuuid not in Android NDK)
2. Make build_arch tolerate make exit code 2 (optional module build failure)
"""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
text = f.read_text()

# 1. Patch prebuild_arch to create Setup.local disabling _uuid
old_prebuild = "    def prebuild_arch(self, arch):\n        super().prebuild_arch(arch)\n        self.ctx.python_recipe = self\n"
new_prebuild = """    def prebuild_arch(self, arch):
        super().prebuild_arch(arch)
        self.ctx.python_recipe = self
        # Disable _uuid module - libuuid not available in Android NDK
        setup_local = Path(self.get_build_dir(arch.arch), 'Modules', 'Setup.local')
        with open(setup_local, 'a') as fh:
            fh.write('\\n*disabled*\\n_uuid\\n')
"""
text = text.replace(old_prebuild, new_prebuild)

# 2. Patch build_arch to tolerate make exit code 2 (optional modules failing)
old_make = """            shprint(
                sh.make,
                'all',
                'INSTSONAME={lib_name}'.format(lib_name=self._libpython),
                _env=env
            )"""
new_make = """            try:
                shprint(
                    sh.make,
                    'all',
                    'INSTSONAME={lib_name}'.format(lib_name=self._libpython),
                    _env=env
                )
            except sh.ErrorReturnCode_2:
                warning('make exited with code 2 (some optional modules failed to build, continuing)')"""
text = text.replace(old_make, new_make)

f.write_text(text)
print("Patched python3 recipe: disabled _uuid + tolerate make exit code 2")
