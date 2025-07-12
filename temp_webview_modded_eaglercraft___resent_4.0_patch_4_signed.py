
import webview
import sys
from pathlib import Path

file_path = r"modded\Resent-4.0-Patch-4-Signed.html"
abs_path = Path(file_path).absolute()
file_url = f"file:///{abs_path}"

# Create window with fullscreen support
window = webview.create_window(
    title="Modded Eaglercraft - Resent-4.0-Patch-4-Signed",
    url=file_url,
    width=1200,
    height=800,
    resizable=True,
    min_size=(800, 600),
    fullscreen=False
)

# Start webview with fullscreen capability
webview.start(debug=False)
