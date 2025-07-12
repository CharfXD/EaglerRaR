
import webview
import sys
from pathlib import Path

file_path = r"modded\Solar.3.5.html"
abs_path = Path(file_path).absolute()
file_url = f"file:///{abs_path}"

# Create window with fullscreen support
window = webview.create_window(
    title="Modded Eaglercraft - Solar.3.5",
    url=file_url,
    width=1200,
    height=800,
    resizable=True,
    min_size=(800, 600),
    fullscreen=False
)

# Start webview with fullscreen capability
webview.start(debug=False)
