import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
from pathlib import Path
import glob
import webbrowser
import subprocess

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False

class EaglercraftLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Eaglercraft Launcher")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
        # Set window icon and style
        self.root.configure(bg='#2b2b2b')
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.style.configure('Title.TLabel', 
                           font=('Arial', 24, 'bold'), 
                           foreground='#ffffff',
                           background='#2b2b2b')
        
        self.style.configure('Section.TLabel', 
                           font=('Arial', 16, 'bold'), 
                           foreground='#ffffff',
                           background='#2b2b2b')
        
        self.style.configure('Custom.TButton',
                           font=('Arial', 12, 'bold'),
                           padding=10)
        
        # Create main frame
        main_frame = tk.Frame(root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')
        
        # Title
        title_label = ttk.Label(main_frame, 
                               text="Eaglercraft Launcher", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 30))
        
        # Create sections frame
        sections_frame = tk.Frame(main_frame, bg='#2b2b2b')
        sections_frame.pack(expand=True, fill='both')
        
        # Vanilla Section
        vanilla_frame = tk.Frame(sections_frame, bg='#3b3b3b', relief='raised', bd=2)
        vanilla_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        vanilla_label = ttk.Label(vanilla_frame, 
                                 text="Eaglercraft: Vanilla", 
                                 style='Section.TLabel')
        vanilla_label.pack(pady=10)
        
        vanilla_desc = tk.Label(vanilla_frame, 
                               text="Launch the vanilla version of Eaglercraft",
                               font=('Arial', 10),
                               fg='#cccccc',
                               bg='#3b3b3b')
        vanilla_desc.pack(pady=(0, 10))
        
        vanilla_button = ttk.Button(vanilla_frame, 
                                   text="Launch Vanilla", 
                                   style='Custom.TButton',
                                   command=self.launch_vanilla)
        vanilla_button.pack(pady=(0, 15))
        
        # Modded Section
        modded_frame = tk.Frame(sections_frame, bg='#3b3b3b', relief='raised', bd=2)
        modded_frame.pack(fill='x', pady=(0, 20), padx=10)
        
        modded_label = ttk.Label(modded_frame, 
                                text="Eaglercraft: Modded", 
                                style='Section.TLabel')
        modded_label.pack(pady=10)
        
        modded_desc = tk.Label(modded_frame, 
                              text="Select and launch a modded version of Eaglercraft",
                              font=('Arial', 10),
                              fg='#cccccc',
                              bg='#3b3b3b')
        modded_desc.pack(pady=(0, 10))
        
        # Modded version selection
        modded_select_frame = tk.Frame(modded_frame, bg='#3b3b3b')
        modded_select_frame.pack(pady=(0, 10))
        
        ttk.Label(modded_select_frame, 
                 text="Select Version:", 
                 font=('Arial', 10),
                 foreground='#ffffff',
                 background='#3b3b3b').pack(side='left', padx=(0, 10))
        
        self.modded_var = tk.StringVar()
        self.modded_combo = ttk.Combobox(modded_select_frame, 
                                        textvariable=self.modded_var,
                                        state='readonly',
                                        width=30)
        self.modded_combo.pack(side='left', padx=(0, 10))
        
        modded_button = ttk.Button(modded_frame, 
                                  text="Launch Modded", 
                                  style='Custom.TButton',
                                  command=self.launch_modded)
        modded_button.pack(pady=(0, 15))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to launch Eaglercraft")
        status_bar = tk.Label(root, 
                             textvariable=self.status_var,
                             font=('Arial', 9),
                             fg='#888888',
                             bg='#1b1b1b',
                             relief='sunken',
                             bd=1)
        status_bar.pack(side='bottom', fill='x')
        
        # Check for Eaglercraft files and populate dropdown
        self.check_files()
        self.populate_modded_dropdown()
    
    def find_html_file(self, folder_path):
        """Find any HTML file in the specified folder"""
        html_files = glob.glob(os.path.join(folder_path, "*.html"))
        if html_files:
            return html_files[0]  # Return the first HTML file found
        return None
    
    def find_all_html_files(self, folder_path):
        """Find all HTML files in the specified folder"""
        html_files = glob.glob(os.path.join(folder_path, "*.html"))
        return html_files
    
    def populate_modded_dropdown(self):
        """Populate the modded version dropdown"""
        modded_files = self.find_all_html_files("modded")
        if modded_files:
            # Create display names for the dropdown
            display_names = []
            for file_path in modded_files:
                filename = os.path.basename(file_path)
                # Remove .html extension for display
                display_name = filename.replace('.html', '')
                display_names.append(display_name)
            
            self.modded_combo['values'] = display_names
            if display_names:
                self.modded_combo.set(display_names[0])  # Set first item as default
        else:
            self.modded_combo['values'] = ['No modded versions found']
            self.modded_combo.set('No modded versions found')
    
    def check_files(self):
        """Check if Eaglercraft files exist and update status"""
        vanilla_file = self.find_html_file("vanilla")
        modded_files = self.find_all_html_files("modded")
        
        if not vanilla_file and not modded_files:
            self.status_var.set("Warning: No Eaglercraft HTML files found. Please place .html files in 'vanilla/' and 'modded/' folders.")
        elif not vanilla_file:
            self.status_var.set(f"Warning: No HTML files found in 'vanilla/' folder. Found {len(modded_files)} modded versions.")
        elif not modded_files:
            vanilla_name = os.path.basename(vanilla_file)
            self.status_var.set(f"Found: {vanilla_name} (vanilla), No modded versions found.")
        else:
            vanilla_name = os.path.basename(vanilla_file)
            modded_names = [os.path.basename(f) for f in modded_files]
            self.status_var.set(f"Found: {vanilla_name} (vanilla), {len(modded_files)} modded versions: {', '.join(modded_names)}")
    
    def launch_vanilla(self):
        """Launch vanilla Eaglercraft"""
        vanilla_file = self.find_html_file("vanilla")
        if vanilla_file:
            try:
                if WEBVIEW_AVAILABLE:
                    # Launch in separate process to avoid threading issues
                    self.launch_webview_process(vanilla_file, "Vanilla Eaglercraft")
                    self.status_var.set(f"Launched Vanilla Eaglercraft: {os.path.basename(vanilla_file)}")
                else:
                    # Fallback to external browser
                    abs_path = Path(vanilla_file).absolute()
                    file_url = f"file:///{abs_path}"
                    webbrowser.open(file_url, new=2)
                    self.status_var.set(f"Launched Vanilla Eaglercraft in browser: {os.path.basename(vanilla_file)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch vanilla Eaglercraft: {str(e)}")
                self.status_var.set("Error launching vanilla version")
        else:
            messagebox.showwarning("File Not Found", 
                                 "No HTML files found in the 'vanilla/' folder.\n"
                                 "Please place your vanilla Eaglercraft HTML file in the 'vanilla/' folder.")
            self.status_var.set("Vanilla files not found")
    
    def launch_modded(self):
        """Launch selected modded Eaglercraft"""
        selected_version = self.modded_var.get()
        
        if selected_version == 'No modded versions found':
            messagebox.showwarning("No Modded Versions", 
                                 "No modded versions found in the 'modded/' folder.\n"
                                 "Please place your modded Eaglercraft HTML files in the 'modded/' folder.")
            return
        
        # Find the file corresponding to the selected version
        modded_files = self.find_all_html_files("modded")
        selected_file = None
        
        for file_path in modded_files:
            filename = os.path.basename(file_path)
            display_name = filename.replace('.html', '')
            if display_name == selected_version:
                selected_file = file_path
                break
        
        if selected_file:
            try:
                if WEBVIEW_AVAILABLE:
                    # Launch in separate process to avoid threading issues
                    self.launch_webview_process(selected_file, f"Modded Eaglercraft - {selected_version}")
                    self.status_var.set(f"Launched Modded Eaglercraft: {selected_version}")
                else:
                    # Fallback to external browser
                    abs_path = Path(selected_file).absolute()
                    file_url = f"file:///{abs_path}"
                    webbrowser.open(file_url, new=2)
                    self.status_var.set(f"Launched Modded Eaglercraft in browser: {selected_version}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to launch modded Eaglercraft: {str(e)}")
                self.status_var.set("Error launching modded version")
        else:
            messagebox.showerror("Error", f"Could not find file for selected version: {selected_version}")
            self.status_var.set("Error: File not found")
    
    def launch_webview_process(self, file_path, title):
        """Launch webview in a separate process"""
        try:
            # Create a temporary Python script to run webview
            script_content = f'''
import webview
import sys
from pathlib import Path

file_path = r"{file_path}"
abs_path = Path(file_path).absolute()
file_url = f"file:///{{abs_path}}"

# Create window with fullscreen support
window = webview.create_window(
    title="{title}",
    url=file_url,
    width=1200,
    height=800,
    resizable=True,
    min_size=(800, 600),
    fullscreen=False
)

# Start webview with fullscreen capability
webview.start(debug=False)
'''
            
            # Write the script to a temporary file
            script_path = f"temp_webview_{title.lower().replace(' ', '_').replace('-', '_')}.py"
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            # Launch the script in a separate process
            subprocess.Popen([sys.executable, script_path], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
        except Exception as e:
            print(f"Error launching webview process: {e}")
            # Fallback to external browser
            abs_path = Path(file_path).absolute()
            file_url = f"file:///{abs_path}"
            webbrowser.open(file_url, new=2)

def main():
    root = tk.Tk()
    app = EaglercraftLauncher(root)
    
    # Show webview availability status
    if not WEBVIEW_AVAILABLE:
        messagebox.showinfo("WebView Not Available", 
                          "pywebview is not installed. The launcher will use your default browser instead.\n\n"
                          "To install webview support, run:\n"
                          "pip install pywebview")
    
    root.mainloop()

if __name__ == "__main__":
    main() 