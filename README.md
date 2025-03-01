# Dave's Comic Splitter

## Description
**Dave's Comic Splitter** is a GUI tool that splits CBZ and CBR comic book files into smaller parts. This tool helps you manage and organize your comic book collection by breaking down larger files into more manageable pieces.

**Created on:** 1 March 2025

## Libraries Required:
- **tkinter** (usually installed with Python)
- **rarfile** (for handling CBR files)
- **zipfile** (for handling CBZ files)
- **ttk** (for the progress bar, included in tkinter)

## Installation
To install the required libraries, run the following command:

sh

pip install rarfile

Ensure that `unrar.exe` is downloaded and in your system PATH! For Windows, you can download it [here](https://www.rarlab.com/rar/unrarw64.exe) or visit the website [here](https://www.rarlab.com/rar_add.htm).

## Output
The output is always in CBZ format.

## How to Use
1. **Select your CBZ/CBR file:** Click the "Browse" button to choose the comic book file you want to split.
2. **Select output directory:** Click the "Browse" button to choose the directory where the split files will be saved.
3. **Enter naming format:** Provide a naming format for the output files (default: full filename).
4. **Number of parts:** Enter the number of parts to split the file into (default: 2 parts).
5. **Start splitting:** Click the "Start" button to begin the splitting process.

