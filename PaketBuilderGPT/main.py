import os
import sys
import subprocess
from packet import *
import pickle
import random
from time import sleep


def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])


print("Installing packages...")

with open('requirements.txt') as f:
    required = f.read().splitlines()

installed = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().splitlines()
installed_packages = [package.split('==')[0] for package in installed]

for package in required:
    if package.split('==')[0] not in installed_packages:
        install(package)


try:
    from scapy.all import *
except ImportError:
    print("Restart the script please :)")
    sys.exit(1)


def export_dict_to_file(data, file_name):
    with open(file_name, "wb") as file:
        pickle.dump(data, file)
    print(f'{file_name} has been created.')

def import_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            data = pickle.load(file)
        return data
    else:
        print(f'{file_name} does not exist')





# code to create a packet
def create_packet():
    packet_name = input("Enter packet name: ")
    packet_sender = input("Enter packet sender: ")
    packet_receiver = input("Enter packet receiver: ")
    packet_segmentsLeft = int(input("Enter number of segments left: "))

    packet_segmentList = []
    iterator = packet_segmentsLeft
    while iterator > 0:
        packet_segmentList.append(input("Input the address of the next segment: "))
        iterator -= 1

    packet_type = 4
    
    packet_identifier = input("Enter packet identifier: ")

    packet = pkt(packet_name, packet_sender, packet_receiver, packet_type, packet_segmentsLeft, packet_segmentList, packet_identifier)

    print("\nName: " + packet.get_name())
    print("Sender: " + packet.get_sender())
    print("Receiver: " + packet.get_receiver())
    print("Type:", packet.get_type())
    print("Segments left:", packet.get_segmentsLeft())
    print("Segment list:", packet.get_segmentList())

    print("Packet created!")
    return packet




# code to print templates
def print_templates():
    if not templates:
        print("No templates found.")
    else:
        print("\n")
        for name, packet in templates.items():
            print(f"Template name: {name}")
            print(f"Sender: {packet.get_sender()}")
            print(f"Receiver: {packet.get_receiver()}")
            print("Type:", packet.get_type())
            print(f"Segments left: {packet.get_segmentsLeft()}")
            print(f"Segment list: {packet.get_segmentList()}")
            print("\n")




# code to load a packet from a template
def load_packet():
    
    name = input("Enter template name: ")
    if name in templates:
        packet = templates[name]
        print_loaded_packet(packet)
        print("Packet loaded")
        return packet
    else:
        print("Template not found.")
        return None




# code to save a packet as a template
def save_packet(packet):
    
    name = packet.get_name()
    templates[name] = packet
    print(f"Packet saved as template: {name}")




# code to print the loaded packet
def print_loaded_packet(packet):
    
    if packet:
        print("\nName: " + packet.get_name())
        print("Sender: " + packet.get_sender())
        print("Receiver: " + packet.get_receiver())
        print("Type:", packet.get_type())
        print("Segments left:", packet.get_segmentsLeft())
        print("Segment list:", packet.get_segmentList())
    else:
        print("No packet is loaded")


# code to export packet to a pcap file
def export_packet(packet):
    
    name = packet.get_name()
    dir = ''
    suffix = '.pcap'
   
    pktTypeArray = []
    pktAmount = int(input("How many of these packets would you like to create?: "))
    while pktAmount > 0:
        pktTypeArray.append(packet.get_type())
        pktAmount -= 1

    count = len(pktTypeArray)

    paket = IPv6(src=packet.get_sender(), dst=packet.get_receiver()) / IPv6ExtHdrRouting(type=pktTypeArray, segleft=packet.get_segmentsLeft(),addresses=packet.get_segmentList()) / IPv6ExtHdrSegmentRoutingTLVPadN(type=129,len=5,padding=packet.get_identifier())

    plist = PacketList([p for p in paket])
    filename = input("Input the file name: ")
    wrpcap(dir + filename + suffix, plist)

    print(f"{count} {name} packets exported to PCAP file.")





# Define function to join pcap files
def join_pcap_files():
    # Prompt user for input files
    input_files = []
    while True:
        file = input("Enter file name to join (or 'done' to finish): ")
        if file.lower() == "done":
            break
        # Add ".pcap" to file name if not already present
        if not file.endswith(".pcap"):
            file += ".pcap"
        # Check if file exists in current directory
        if not os.path.isfile(file):
            print(f"{file} does not exist in the current directory. Please try again.")
            continue        
        input_files.append(file)
    
    # Prompt user for output file
    output_file = input("Enter output file name: ")
    # Add ".pcap" to output file name if not already present
    if not output_file.endswith(".pcap"):
        output_file += ".pcap"

    # Read packets from all input files
    packets = []
    for file in input_files:
        packets += rdpcap(file)

    # Write combined packets to output file
    wrpcap(output_file, packets)




p = None
os.system('cls' if os.name == 'nt' else 'clear')

print("Loading templates...")

templates = import_dict_from_file('templates.pickle')
if templates:
    print("Templates loaded..")
else:
    templates = {}
    print("Templates failed to load")

sleep(2)

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("----------------------------------------------------------------")
    print("Menu:")
    print("1. Create a packet")
    print("2. Modify loaded packet")
    print("3. Print templates")
    print("4. Load packet from a template")
    print("5. Save packet as a template")
    print("6. Print loaded packet")
    print("7. Export packet to pcap file")
    print("8. Join pcap files")
    print("0. Exit")
    print("----------------------------------------------------------------")

    choice = input("Enter your choice: ")

    if choice == "1":
        p = create_packet()
    elif choice == "2":
        #modify_packet()
        print("To be implemented")
    elif choice == "3":
        print_templates()
    elif choice == "4":
        p = load_packet()
    elif choice == "5":
        save_packet(p)
    elif choice == "6":
        print_loaded_packet(p)
    elif choice == "7":
        export_packet(p)
    elif choice == "8":
        join_pcap_files()
    elif choice == "0":
        export_dict_to_file(templates, 'templates.pickle')
        break
    else:
        print("Invalid choice.")

    input("\nPress enter to continue...")
