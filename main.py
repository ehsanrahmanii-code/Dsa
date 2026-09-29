"""
TITAN Android Entry Point
Starts the Flask dashboard server in a background thread and loads it in a WebView.
"""
import os
import sys
import threading
import time

# Ensure the script directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Android: use shared storage path (already handled by titan_engine.py)
# Prevent desktop browser opening on Android
os.environ.setdefault("TITAN_PORT", "8080")

# Import the TITAN engine module
import titan_engine


def _wait_for_server(host="127.0.0.1", port=8080, timeout=30):
    """Wait until the Flask server responds on /health."""
    import urllib.request
    url = f"http://{host}:{port}/health"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            req = urllib.request.Request(url)
            urllib.request.urlopen(req, timeout=2)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    # Start TITAN Flask server in a background thread (no desktop browser)
    server_thread = threading.Thread(
        target=titan_engine.run_titan,
        kwargs={"open_browser": False},
        daemon=True,
        name="titan-flask-server",
    )
    server_thread.start()

    # Give the server a moment to initialize
    time.sleep(2)

    # Wait for the server to be ready
    port = getattr(titan_engine, "PORT", 8080)
    _wait_for_server(port=port, timeout=30)

    # Load the dashboard in the Android WebView
    dashboard_url = f"http://127.0.0.1:{port}"
    try:
        import android
        android.load_url(dashboard_url)
    except ImportError:
        # Not on Android / no webview bootstrap - just keep the server running
        print(f"TITAN dashboard running at {dashboard_url}")
        # Keep the main thread alive
        while True:
            time.sleep(1)


if __name__ == "__main__":
    main()
