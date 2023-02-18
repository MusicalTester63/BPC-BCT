import os
import glob
import tkinter as tk
from tkinter import messagebox

# Find all .pcap files in the current directory
pcap_files = glob.glob("*.pcap")

# Delete all .pcap files and record their names
deleted_files = []
for file in pcap_files:
    os.remove(file)
    deleted_files.append(file)

# Show a message box with the message "PCAP files deleted!"
if deleted_files:
    messagebox.showinfo("Files Deleted", "PCAP files deleted!")
