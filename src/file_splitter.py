import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os
import threading
import random
import time
import sys
import py7zr
import zipfile
import tarfile

class HackerTerminalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CYBERSPLIT v1.0")
        self.root.geometry("1000x700")
        
        self.root.configure(bg='#000000')
        
        # Modified icon handling
        try:
            if getattr(sys, 'frozen', False):
                # Running in a bundle
                base_path = sys._MEIPASS
            else:
                # Running in normal Python environment
                base_path = os.path.join(os.path.dirname(__file__), '..')
                
            icon_path = os.path.join(base_path, 'assets', 'file.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")
        
        # Center and maximize the window
        self.root.state('zoomed')  # This maximizes the window
        
        # Variables
        self.input_file = tk.StringVar(value="[NO_FILE_SELECTED]")
        self.output_dir = tk.StringVar(value="[NO_DIR_SELECTED]")
        self.chunk_size = tk.IntVar(value=10)
        self.is_running = False
        self.selected_chunks = []
        self.matrix_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"
        
        # Configure styles
        self.configure_styles()
        self.create_gui()
        
        # Start matrix effect
        self.matrix_labels = []
        self.create_matrix_effect()
        
        # Bind keyboard shortcuts
        self.bind_shortcuts()
        
    def bind_shortcuts(self):
        # Bind keyboard shortcuts
        self.root.bind('<Control-h>', lambda e: self.show_help())
        self.root.bind('<Control-H>', lambda e: self.show_help())  # For Caps Lock
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<Control-q>', lambda e: self.quit_app())
        self.root.bind('<Control-Q>', lambda e: self.quit_app())  # For Caps Lock
        self.root.bind('<Escape>', lambda e: self.quit_app())
        
        # Add tooltips
        self.create_tooltips()
        
    def show_help(self):
        # Switch to help tab
        self.notebook.select(2)  # Index 2 is the help tab
        
    def quit_app(self):
        if messagebox.askokcancel("Quit", "[CONFIRM]: EXIT CYBERSPLIT?"):
            self.root.quit()
            
    def create_tooltips(self):
        # Create tooltips for common actions
        tooltips = {
            "Ctrl+H or F1": "Show Help",
            "Ctrl+Q or ESC": "Quit Application",
            "Tab": "Switch Between Tabs"
        }
        
        tooltip_text = "SHORTCUTS:\n" + "\n".join(f"{k}: {v}" for k, v in tooltips.items())
        
        # Add a status label at the bottom of the window
        status_frame = tk.Frame(self.root, bg='black')
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20)
        
        status_label = tk.Label(status_frame,
                              text=tooltip_text,
                              font=self.terminal_font,
                              fg='#0f0',
                              bg='black',
                              justify=tk.LEFT)
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
    def configure_styles(self):
        self.terminal_font = font.Font(family='Courier New', size=12)
        self.title_font = font.Font(family='Courier New', size=20, weight='bold')
        
    def create_matrix_effect(self):
        for _ in range(20):  # Number of falling characters
            label = tk.Label(self.root, 
                           font=('Courier New', 10),
                           fg='#0f0',
                           bg='black')
            label.place(x=random.randint(0, 980), y=-20)
            self.matrix_labels.append(label)
        self.update_matrix()
        
    def update_matrix(self):
        for label in self.matrix_labels:
            x = label.winfo_x()
            y = label.winfo_y()
            if y > 700:
                y = -20
                x = random.randint(0, 980)
            label.place(x=x, y=y+2)
            label.configure(text=random.choice(self.matrix_chars))
        self.root.after(50, self.update_matrix)
        
    def create_gui(self):
        # Main container with terminal border
        self.main_frame = tk.Frame(self.root, bg='#0f0', padx=2, pady=2)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Inner frame with black background
        inner_frame = tk.Frame(self.main_frame, bg='black')
        inner_frame.pack(fill=tk.BOTH, expand=True)
        
        # Terminal header
        self.create_terminal_header(inner_frame)
        
        # Create notebook with custom style
        self.notebook = ttk.Notebook(inner_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        split_tab = self.create_split_tab()
        merge_tab = self.create_merge_tab()
        help_tab = self.create_help_tab()
        donation_tab = self.create_donation_tab()
        
        
        self.notebook.add(split_tab, text="[SPLIT_MODE]")
        self.notebook.add(merge_tab, text="[MERGE_MODE]")
        self.notebook.add(help_tab, text="[HELP]")
        self.notebook.add(donation_tab, text="[DONATE]")
        
        
    def create_terminal_header(self, parent):
        header_frame = tk.Frame(parent, bg='black')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # ASCII Art Title
        title = """
    ╔══════════════════════════════════════════════════════════╗
    ║  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███████╗██████╗██╗     ██╗████████╗  ║
    ║ ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██╔════╝██╔══██╗██║     ██║╚══██╔══╝ ║
    ║ ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝███████╗██████╔╝██║     ██║   ██║    ║
    ║ ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗╚════██║██╔═══╝ ██║     ██║   ██║    ║
    ║ ╚██████╗   ██║   ██████╔╝███████╗██║  ██║███████║██║     ███████╗██║   ██║    ║
    ║  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚══════╝╚═╝   ╚═╝    ║
    ╚══════════════════════════════════════════════════════════╝
        """
        tk.Label(header_frame, 
                text=title,
                font=('Courier New', 8),
                fg='#0f0',
                bg='black').pack()
                
        # Fake terminal info
        info_text = f"""
    [SYSTEM]: INITIALIZING CYBERSPLIT v1.0...
    [STATUS]: SYSTEM READY
    [TIME]: {time.strftime('%H:%M:%S')}
    [MODE]: SECURE FILE SPLITTING AND MERGING
    {'='*80}"""
        
        tk.Label(header_frame,
                text=info_text,
                font=self.terminal_font,
                fg='#0f0',
                bg='black',
                justify=tk.LEFT).pack(anchor='w')
        
    def create_terminal_button(self, parent, text, command):
        return tk.Button(parent,
                        text=text,
                        command=command,
                        font=self.terminal_font,
                        fg='#0f0',
                        bg='black',
                        activebackground='#0f0',
                        activeforeground='black',
                        relief=tk.RIDGE,
                        bd=2)
        
    def create_terminal_entry(self, parent, textvariable):
        return tk.Entry(parent,
                       textvariable=textvariable,
                       font=self.terminal_font,
                       fg='#0f0',
                       bg='black',
                       insertbackground='#0f0',
                       relief=tk.SUNKEN,
                       bd=2)

    def create_split_tab(self):
        frame = tk.Frame(self.notebook, bg='black')
        
        # Input section
        tk.Label(frame,
                text="╔═[ INPUT_FILE ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
                
        input_frame = tk.Frame(frame, bg='black')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.create_terminal_entry(input_frame, self.input_file).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(20,10))
        self.create_terminal_button(input_frame, "[ SELECT_FILE ]", self.browse_input).pack(side=tk.LEFT)
        
        # Output directory section
        tk.Label(frame,
                text="╔═[ OUTPUT_DIRECTORY ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
                
        output_frame = tk.Frame(frame, bg='black')
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.create_terminal_entry(output_frame, self.output_dir).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(20,10))
        self.create_terminal_button(output_frame, "[ SELECT_DIR ]", self.browse_output).pack(side=tk.LEFT)
        
        # Chunk size section
        tk.Label(frame,
                text="╔═[ CHUNK_SIZE_MB ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
                
        size_frame = tk.Frame(frame, bg='black')
        size_frame.pack(fill=tk.X, padx=30, pady=5)
        
        spinbox = tk.Spinbox(size_frame,
                            from_=1,
                            to=1000,
                            textvariable=self.chunk_size,
                            font=self.terminal_font,
                            fg='#0f0',
                            bg='black',
                            buttonbackground='#0f0',
                            width=10)
        spinbox.pack(side=tk.LEFT)
        
        # Action button
        self.create_terminal_button(frame, "[ EXECUTE_SPLIT ]", self.start_split).pack(pady=20)
        
        # Progress section
        tk.Label(frame,
                text="╔═[ OPERATION_STATUS ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
                
        self.split_progress_var = tk.StringVar(value="[" + "░" * 50 + "]")
        tk.Label(frame,
                textvariable=self.split_progress_var,
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(pady=5)
                
        self.split_status = tk.Label(frame,
                                   text="[STATUS]: AWAITING_COMMAND",
                                   font=self.terminal_font,
                                   fg='#0f0',
                                   bg='black')
        self.split_status.pack()
        
        return frame
        
    def create_merge_tab(self):
        frame = tk.Frame(self.notebook, bg='black')
        
        # Chunks list section
        tk.Label(frame,
                text="╔═[ SELECTED_CHUNKS ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
        
        self.chunks_listbox = tk.Listbox(frame,
                                       font=self.terminal_font,
                                       bg='black',
                                       fg='#0f0',
                                       selectmode=tk.MULTIPLE,
                                       height=10,
                                       relief=tk.SUNKEN,
                                       bd=2)
        self.chunks_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))
        
        # Buttons frame
        btn_frame = tk.Frame(frame, bg='black')
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.create_terminal_button(btn_frame, "[ ADD_CHUNKS ]", self.add_chunks).pack(side=tk.LEFT, padx=5)
        self.create_terminal_button(btn_frame, "[ CLEAR_LIST ]", self.clear_chunks).pack(side=tk.LEFT, padx=5)
        
        # Merge button
        self.create_terminal_button(frame, "[ EXECUTE_MERGE ]", self.start_merge).pack(pady=20)
        
        # Progress section
        tk.Label(frame,
                text="╔═[ OPERATION_STATUS ]",
                font=self.terminal_font,
                fg='#0f0',
                bg='black').pack(anchor='w', padx=10, pady=(10,0))
        
        self.merge_progress_var = tk.StringVar(value="[" + "░" * 50 + "]")
        self.merge_progress_label = tk.Label(frame,
                                          textvariable=self.merge_progress_var,
                                          font=self.terminal_font,
                                          fg='#0f0',
                                          bg='black')
        self.merge_progress_label.pack(pady=(0, 10))
        
        self.merge_status = tk.Label(frame,
                                   text="[STATUS]: AWAITING_COMMAND",
                                   font=self.terminal_font,
                                   fg='#0f0',
                                   bg='black')
        self.merge_status.pack()
        
        return frame
        
    def create_help_tab(self):
        frame = tk.Frame(self.notebook, bg='black')
        
        # Create a Text widget for the help content
        help_text = tk.Text(frame,
                           font=self.terminal_font,
                           fg='#0f0',
                           bg='black',
                           relief=tk.SUNKEN,
                           bd=2,
                           padx=10,
                           pady=10)
        help_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Help content
        instructions = """
╔══════════════════════════════════════════════════════════╗
║                   CYBERSPLIT MANUAL                      ║
╚══════════════════════════════════════════════════════════╝

[SPLIT MODE INSTRUCTIONS]
------------------------
1. Select input file using [ SELECT_FILE ]
2. Choose output directory using [ SELECT_DIR ]
3. Set chunk size in MB (1-1000)
4. Click [ EXECUTE_SPLIT ] to start operation
5. Monitor progress in status bar
6. Files will be created as: filename.000, filename.001, etc.

[MERGE MODE INSTRUCTIONS]
------------------------
1. Choose output directory using [ SELECT_DIR ]
2. Click [ ADD_CHUNKS ] to select chunk files
3. Selected chunks will appear in the list
4. Use [ CLEAR_LIST ] to reset selection
5. Click [ EXECUTE_MERGE ] to combine chunks
6. Original file will be reconstructed in output directory

[IMPORTANT NOTES]
----------------
• Chunks must be merged in correct order
• All chunks must be from the same original file
• Keep chunks in sequence (.000, .001, etc.)
• Do not rename chunk files
• Ensure enough disk space in output location

[KEYBOARD SHORTCUTS]
-------------------
Tab          - Switch between modes
Ctrl+Q       - Quit application
Ctrl+H       - Show this help

[ERROR CODES]
------------
[ERROR: NO_FILE]      - Input file not selected
[ERROR: NO_DIR]       - Output directory not selected
[ERROR: NO_CHUNKS]    - No chunks selected for merge
[ERROR: DISK_FULL]    - Insufficient disk space
[ERROR: BAD_CHUNK]    - Corrupted chunk file


"""
        
        help_text.insert('1.0', instructions)
        help_text.config(state='disabled')  # Make text read-only
        
        return frame
        
    def add_chunks(self):
        chunks = filedialog.askopenfilenames(
            title="Select Chunk Files",
            filetypes=[("Chunk files", "*.???")]
        )
        if chunks:
            self.chunks_listbox.delete(0, tk.END)
            for chunk in sorted(chunks):
                self.chunks_listbox.insert(tk.END, os.path.basename(chunk))
            self.selected_chunks = list(chunks)
            self.merge_status['text'] = f"[STATUS]: {len(chunks)} CHUNKS SELECTED"
            
    def clear_chunks(self):
        self.chunks_listbox.delete(0, tk.END)
        self.selected_chunks = []

    def update_progress(self, value, status=""):
        # Convert progress to retro style bar
        bar_length = 50
        filled_length = int(value * bar_length / 100)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        if self.notebook.index(self.notebook.select()) == 0:
            # Split tab
            self.split_progress_var.set(f"[{bar}]")
            if status:
                self.split_status['text'] = f"STATUS: {status}"
        else:
            # Merge tab
            self.merge_progress_var.set(f"[{bar}]")
            if status:
                self.merge_status['text'] = f"STATUS: {status}"
        
        self.root.update_idletasks()

    def browse_input(self):
        filename = filedialog.askopenfilename(title="Select File")
        if filename:
            self.input_file.set(filename)
            
    def browse_output(self):
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_dir.set(dirname)
            
    def split_file(self, input_file, chunk_size):
        try:
            # Get file size
            file_size = os.path.getsize(input_file)
            chunk_size_bytes = chunk_size * 1024 * 1024  # Convert MB to bytes
            
            # Get output directory and base filename
            output_dir = self.output_dir.get()
            if output_dir == "[NO_DIR_SELECTED]":
                messagebox.showerror("Error", "Please select an output directory")
                return
            
            base_name = os.path.basename(input_file)
            
            with open(input_file, 'rb') as f:
                chunk_number = 0
                bytes_read = 0
                
                while True:
                    chunk_data = f.read(chunk_size_bytes)
                    if not chunk_data:
                        break
                        
                    output_filename = os.path.join(output_dir, f"{base_name}.{chunk_number:03d}")
                    with open(output_filename, 'wb') as chunk_file:
                        chunk_file.write(chunk_data)
                    
                    bytes_read += len(chunk_data)
                    progress = (bytes_read / file_size) * 100
                    self.root.after(0, self.update_progress, progress, f"[STATUS]: SPLITTING {progress:.1f}%")
                    
                    chunk_number += 1
                    
            self.root.after(0, self.update_progress, 100, "[STATUS]: SPLIT COMPLETE")
            
        except Exception as e:
            self.root.after(0, self.update_progress, 0, f"[ERROR]: {str(e)}")
        finally:
            self.is_running = False
            
    def merge_files(self, chunks):
        try:
            if not chunks:
                raise Exception("No chunks selected")
            
            # Sort chunks to ensure correct order
            chunks = sorted(chunks)
            first_chunk = chunks[0]
            
            # Get output directory and base filename
            output_dir = self.output_dir.get()
            if output_dir == "[NO_DIR_SELECTED]":
                messagebox.showerror("Error", "Please select an output directory")
                return
            
            base_filename = os.path.join(output_dir, os.path.basename(first_chunk[:-4]))
            total_size = sum(os.path.getsize(chunk) for chunk in chunks)
            
            with open(base_filename, 'wb') as output_file:
                bytes_written = 0
                
                for chunk_file_path in chunks:
                    with open(chunk_file_path, 'rb') as chunk_file:
                        while True:
                            chunk_data = chunk_file.read(8192)  # Read in 8KB chunks
                            if not chunk_data:
                                break
                            output_file.write(chunk_data)
                            bytes_written += len(chunk_data)
                            progress = (bytes_written / total_size) * 100
                            self.root.after(0, self.update_progress, progress, f"[STATUS]: MERGING {progress:.1f}%")
                            
            self.root.after(0, self.update_progress, 100, "[STATUS]: MERGE COMPLETE")
            
        except Exception as e:
            self.root.after(0, self.update_progress, 0, f"[ERROR]: {str(e)}")
        finally:
            self.is_running = False
            
    def start_split(self):
        if self.is_running:
            return
            
        input_file = self.input_file.get()
        if input_file == "Select a file...":
            messagebox.showerror("Error", "Please select an input file")
            return
            
        self.is_running = True
        self.update_progress(0, "Starting split operation...")
        
        # Start splitting in a separate thread
        thread = threading.Thread(target=self.split_file, args=(input_file, self.chunk_size.get()))
        thread.daemon = True
        thread.start()
        
    def start_merge(self):
        if self.is_running:
            return
        
        if not self.selected_chunks:
            messagebox.showerror("Error", "Please add chunks first")
            return
        
        self.is_running = True
        self.update_progress(0, "[STATUS]: INITIALIZING MERGE...")
        
        # Start merging in a separate thread
        thread = threading.Thread(target=self.merge_files, args=(self.selected_chunks,))
        thread.daemon = True
        thread.start()

    def create_donation_tab(self):
        frame = tk.Frame(self.notebook, bg='black')
        
        # Bitcoin donation section
        donation_text = """
╔══════════════════════════════════════════════════════════╗
║                 SUPPORT DEVELOPMENT                       ║
╚══════════════════════════════════════════════════════════╝

[WHY DONATE?]
------------
• Support continuous development
• Help maintain the project
• Keep CyberSplit free and open source

[BITCOIN DONATION ADDRESS]
-------------------------
█████████████████████████████████████████████████████
█                                                   █
█   bc1qhwfd6zm7t7uqrk77uc5t788h4h6sadw48mqfzn    █
█                                                   █
█████████████████████████████████████████████████████


"""
        
        # Create Text widget with scroll
        text_frame = tk.Frame(frame, bg='black')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(text_frame, bg='black', troughcolor='black')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Donation text area
        donation_area = tk.Text(text_frame,
                              font=self.terminal_font,
                              fg='#0f0',
                              bg='black',
                              relief=tk.SUNKEN,
                              bd=2,
                              padx=10,
                              pady=10,
                              yscrollcommand=scrollbar.set)
        donation_area.pack(fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=donation_area.yview)
        
        # Add copy button for Bitcoin address
        def copy_address():
            btc_address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
            self.root.clipboard_clear()
            self.root.clipboard_append(btc_address)
            self.root.update()
            messagebox.showinfo("Copied!", "[SUCCESS]: Bitcoin address copied to clipboard!")
        
        button_frame = tk.Frame(frame, bg='black')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        copy_button = self.create_terminal_button(
            button_frame,
            "[ COPY_BTC_ADDRESS ]",
            copy_address
        )
        copy_button.pack(side=tk.LEFT, padx=5)
        
        # Insert the donation text
        donation_area.insert('1.0', donation_text)
        donation_area.config(state='disabled')  # Make text read-only
        
        return frame

   

def main():
    root = tk.Tk()
    
    # Set minimum size
    root.minsize(1000, 700)
    
    # Optional: Set custom cursor
    root.config(cursor="crosshair")  # or "trek" for a more tech look
    
    # Create splash screen
    splash = tk.Toplevel(root)
    splash.title("")
    splash.geometry("400x300")  # Made taller to accommodate logo
    splash.overrideredirect(True)
    
    # Center splash screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 400) // 2
    y = (screen_height - 300) // 2
    splash.geometry(f"400x300+{x}+{y}")
    
    # Configure splash screen
    splash.configure(bg='black')
    
    # Add logo to splash screen
    try:
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        if os.path.exists(logo_path):
            logo_img = tk.PhotoImage(file=logo_path)
            logo_label = tk.Label(splash, image=logo_img, bg='black')
            logo_label.image = logo_img  # Keep a reference!
            logo_label.pack(pady=20)
    except:
        pass  # If logo loading fails, continue without it
    
    # Loading text
    loading_label = tk.Label(splash,
                           text="INITIALIZING CYBERSPLIT...",
                           font=('Courier New', 14),
                           fg='#0f0',
                           bg='black')
    loading_label.pack(expand=True)
    
    # Update splash screen
    splash.update()
    
    # Create main application
    app = HackerTerminalApp(root)
    
    # Destroy splash screen after a delay
    root.after(2000, splash.destroy)
    
    # Hide main window until splash is done
    root.withdraw()
    root.after(2000, root.deiconify)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main() 