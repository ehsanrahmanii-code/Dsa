[app]

# Application metadata
title = TITAN Trading Dashboard
package.name = titan
package.domain = org.titan

# Source code location (relative to buildozer.spec)
source.dir = .

# App version
version = 0.1

# Application requirements
# Pin Python to 3.11 for pandas/numpy compatibility (3.14 is too new)
requirements = python3==3.11.16,hostpython3==3.11.16,flask,numpy,pandas,requests,sqlite3,websocket-client

# Use the webview bootstrap (native Android WebView, no Kivy/SDL2 needed)
p4a.bootstrap = webview

# Android configuration
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 26
android.archs = arm64-v8a,armeabi-v7a

# App orientation (allow all for tablets and phones)
orientation = all

# Not fullscreen (show status bar)
fullscreen = 0

# Android entry point
android.entrypoint = main.py

# Build settings
log_level = 2
warn_on_root = 0

# Don't copy unnecessary files
source.exclude_dirs = tests,docs,examples,build,dist,.git,__pycache__
source.exclude_patterns = *.pyc,*.pyo,*.so,*.o

# p4a settings - master branch is stable, supports Python 3.11/3.12 + AAB
p4a.branch = master

# Build options
android.accept_sdk_license = True
android.gradle_build = True
