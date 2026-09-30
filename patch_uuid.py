#!/usr/bin/env python3
"""Patch p4a python3 recipe to disable _uuid module by telling configure
that libuuid is not available (ac_cv_lib_uuid_uuid_generate=no)."""
import pathlib

f = pathlib.Path('pythonforandroid/recipes/python3/__init__.py')
text = f.read_text()

# Patch get_recipe_env to add ac_cv_lib_uuid_uuid_generate=no
# This tells configure that libuuid is not available, so _uuid won't be built
old_env = "        env = super().get_recipe_env(arch)\n        env['HOSTARCH'] = arch.command_prefix\n"
new_env = "        env = super().get_recipe_env(arch)\n        env['HOSTARCH'] = arch.command_prefix\n        # Disable _uuid module - libuuid not available in Android NDK\n        env['ac_cv_lib_uuid_uuid_generate'] = 'no'\n"
text = text.replace(old_env, new_env)

f.write_text(text)
print("Patched python3 recipe: set ac_cv_lib_uuid_uuid_generate=no in get_recipe_env")
