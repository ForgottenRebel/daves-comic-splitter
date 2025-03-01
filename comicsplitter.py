"""
Dave's Comic Splitter - A GUI tool to split CBZ/CBR comic book files into smaller parts.
Created 1 March 2025

Libraries required:
- tkinter (usually installed with Python)
- rarfile (for handling CBR files)
- zipfile (for handling CBZ files)
- ttk (for the progress bar, included in tkinter)

Install the required libraries using:
pip install rarfile

Make sure that unrar.exe is downloaded and in your system PATH! For Windows, see https://www.rarlab.com/rar/unrarw64.exe (or https://www.rarlab.com/rar_add.htm for the website itself)

Output is always CBZ.
"""

import os
import zipfile
import rarfile
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

def split_file(input_file, output_dir, num_parts, naming_format):
    """Splits the CBZ or CBR file into smaller parts."""
    # Check file extension
    extension = input_file.split('.')[-1].lower()
    
    if extension == 'cbz':
        file_list = extract_cbz(input_file)
    elif extension == 'cbr':
        file_list = extract_cbr(input_file)
    else:
        raise ValueError("Unsupported file type. Only CBZ and CBR are supported.")
    
    # Calculate number of files per part
    files_per_part = len(file_list) // num_parts
    remaining_files = len(file_list) % num_parts
    
    part_number = 1
    file_index = 0

    for i in range(num_parts):
        # Determine the number of files for this part
        part_file_list = file_list[file_index: file_index + files_per_part + (1 if i < remaining_files else 0)]
        file_index += len(part_file_list)

        # Create a new CBZ file for each part
        part_file_name = f"{naming_format}-part{part_number}.cbz"
        part_file_path = os.path.join(output_dir, part_file_name)
        
        with zipfile.ZipFile(part_file_path, 'w') as zipf:
            for file in part_file_list:
                zipf.write(file, os.path.basename(file))
        
        part_number += 1

    # Clean up the temporary directory
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(temp_dir)

def extract_cbz(cbz_file):
    """Extract files from a CBZ file."""
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    with zipfile.ZipFile(cbz_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    extracted_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
    return extracted_files

def extract_cbr(cbr_file):
    """Extract files from a CBR file."""
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    with rarfile.RarFile(cbr_file, 'r') as rar_ref:
        rar_ref.extractall(temp_dir)
    
    extracted_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
    return extracted_files

def browse_input_file():
    """Browse for the CBZ or CBR file."""
    input_file = filedialog.askopenfilename(filetypes=[("Comic Files", "*.cbz;*.cbr")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_file)

    # Set the default naming format to the input file's name without extension
    filename = os.path.basename(input_file)
    default_name = os.path.splitext(filename)[0]
    naming_entry.delete(0, tk.END)
    naming_entry.insert(0, default_name)

def browse_output_dir():
    """Browse for the output directory."""
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def start_splitting():
    """Start the splitting process."""
    input_file = input_entry.get()
    output_dir = output_entry.get()
    naming_format = naming_entry.get()
    num_parts = int(parts_entry.get())
    
    if not input_file or not output_dir:
        messagebox.showerror("Input Error", "Please select both input file and output directory.")
        return
    
    if not num_parts or num_parts <= 0:
        messagebox.showerror("Input Error", "Please enter a valid number of parts.")
        return
    
    status_label.config(text="Processing...")
    progress_bar.start()
    
    try:
        split_file(input_file, output_dir, num_parts, naming_format)
        progress_bar.stop()
        status_label.config(text="Operation completed successfully!")
        messagebox.showinfo("Success", f"Files successfully split into {num_parts} parts.")
    except Exception as e:
        progress_bar.stop()
        status_label.config(text="Error")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Dave's Comic Splitter")

# Add a nice title effect
title_label = tk.Label(root, text="Dave's Comic Splitter", font=("Helvetica", 24, "bold"), fg="blue")
title_label.pack(pady=20)

# Set up input file selection
input_label = tk.Label(root, text="Select your CBZ/CBR file:")
input_label.pack(padx=10, pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(padx=10, pady=5)
input_button = tk.Button(root, text="Browse", command=browse_input_file)
input_button.pack(padx=10, pady=5)

# Set up output directory selection
output_label = tk.Label(root, text="Select output directory:")
output_label.pack(padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(padx=10, pady=5)
output_button = tk.Button(root, text="Browse", command=browse_output_dir)
output_button.pack(padx=10, pady=5)

# Set up naming format field
naming_label = tk.Label(root, text="Enter naming format (default: full filename):")
naming_label.pack(padx=10, pady=5)
naming_entry = tk.Entry(root, width=50)
naming_entry.pack(padx=10, pady=5)

# Set up number of parts
parts_label = tk.Label(root, text="Number of parts to split into:")
parts_label.pack(padx=10, pady=5)
parts_entry = tk.Entry(root, width=50)
parts_entry.insert(0, "2")  # Default to 2 parts
parts_entry.pack(padx=10, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode='indeterminate')
progress_bar.pack(padx=10, pady=20)

# Status label
status_label = tk.Label(root, text="Ready", font=("Helvetica", 12))
status_label.pack()

# Start button
start_button = tk.Button(root, text="Start", command=start_splitting, bg="green", fg="white")
start_button.pack(padx=10, pady=10)

# Run the GUI
root.mainloop()
