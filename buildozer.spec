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
# These are the Python packages that need recipes in python-for-android
requirements = python3,flask,numpy,pandas,requests,sqlite3,websocket-client

# Use the webview bootstrap (native Android WebView, no Kivy/SDL2 needed)
bootstrap = webview

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

# Presplash and icon (use defaults if not provided)
# presplash.filename = presplash.png
# icon.filename = icon.png

# Build settings
log_level = 2
warn_on_root = 1

# Don't copy unnecessary files
source.exclude_dirs = tests,docs,examples,build,dist,.git,__pycache__
source.exclude_patterns = *.pyc,*.pyo,*.so,*.o

# p4a settings
p4a.branch = develop

# Build options
android.accept_sdk_license = True
android.gradle_build = True
