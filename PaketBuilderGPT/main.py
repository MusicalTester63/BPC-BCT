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
    print("scapy not found")
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

    packet_type = []
    pktAmount = int(input("How many of these packets would you like to create?: "))
    while pktAmount > 0:
        packet_type.append(4)
        pktAmount -= 1

    packet = pkt(packet_name, packet_sender, packet_receiver, packet_type, packet_segmentsLeft, packet_segmentList)

    print("\nName: " + packet.get_name())
    print("Sender: " + packet.get_sender())
    print("Receiver: " + packet.get_receiver())
    print("Type:", packet.get_type()[0])
    print("Packet amount:", len(packet.get_type()))
    print("Segments left:", packet.get_segmentsLeft())
    print("Segment list:", packet.get_segmentList())

    print("Packet created!")
    return packet

def print_templates():
    if not templates:
        print("No templates found.")
    else:
        print("\n")
        for name, packet in templates.items():
            print(f"Template name: {name}")
            print(f"Sender: {packet.get_sender()}")
            print(f"Receiver: {packet.get_receiver()}")
            print(f"Segments left: {packet.get_segmentsLeft()}")
            print(f"Segment list: {packet.get_segmentList()}")
            print("\n")

def load_packet():
    # code to load a packet from a template
    name = input("Enter template name: ")
    if name in templates:
        packet = templates[name]
        print("Packet loaded")
        return packet
    else:
        print("Template not found.")
        return None

def save_packet(packet):
    # code to save a packet as a template
    name = packet.get_name()
    templates[name] = packet
    print(f"Packet saved as template: {name}")

def print_loaded_packet(packet):
    # code to print the loaded packet
    if packet:
        print("\nName: " + packet.get_name())
        print("Sender: " + packet.get_sender())
        print("Receiver: " + packet.get_receiver())
        print("Type:", packet.get_type()[0])
        print("Packet amount:", len(packet.get_type()))
        print("Segments left:", packet.get_segmentsLeft())
        print("Segment list:", packet.get_segmentList())
    else:
        print("No packet is loaded")

def export_packet(packet):
    # code to export packet to a pcap file

    name = packet.get_name()
    count = len(packet.get_type())

    dir = ''
    suffix = '.pcap'


    rand_num = random.randint(0, 63)
    id = bin(rand_num)[2:].zfill(6)

    paket = IPv6(src=packet.get_sender(), dst=packet.get_receiver()) / IPv6ExtHdrRouting(type=packet.get_type(), segleft=packet.get_segmentsLeft(),addresses=packet.get_segmentList()) / IPv6ExtHdrSegmentRoutingTLVPadN(type=129,len=5,padding=id)

    plist = PacketList([p for p in paket])
    filename = input("Input the file name: ")
    wrpcap(dir + filename + suffix, plist)

    print(f"{count} {name} packets exported to PCAP file.")


p = None
os.system('cls' if os.name == 'nt' else 'clear')

print("Loading templates...")

templates = import_dict_from_file('templates.pickle')
if templates:
    print("Templates loaded..")
else:
    
    if templates:
        print("templates loaded..")

    else:
        templates = {}
        print("Templates failed to load")

sleep(2)

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("----------------------------------------------------------------")
    print("Menu:")
    print("1. Create a packet")
    print("2. Print templates")
    print("3. Load packet from a template")
    print("4. Save packet as a template")
    print("5. Print loaded packet")
    print("6. Export packet to pcap file")
    print("7. JSON export")
    print("0. Exit")
    print("----------------------------------------------------------------")

    choice = input("Enter your choice: ")

    if choice == "1":
        p = create_packet()
    elif choice == "2":
        print_templates()
    elif choice == "3":
        p = load_packet()
    elif choice == "4":
        save_packet(p)
    elif choice == "5":
        print_loaded_packet(p)
    elif choice == "6":
        export_packet(p)
    elif choice == "0":
        export_dict_to_file(templates, 'templates.pickle')
        break
    else:
        print("Invalid choice.")

    input("\nPress enter to continue...")
