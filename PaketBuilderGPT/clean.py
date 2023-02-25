import os
import platform
from tkinter import messagebox  # for Windows message box

# Get operating system
os_name = platform.system()

# Delete all .pcap files in current directory
for file in os.listdir("."):
    if file.endswith(".pcap"):
        os.remove(file)

# Show message box or output to console depending on OS
if os_name == "Windows":
    messagebox.showinfo("PCAP Files Deleted", "All PCAP files have been deleted.")
else:
    print("All PCAP files have been deleted.")
