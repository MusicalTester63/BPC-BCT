import os
from packet import *
import pickle
import json


def export_dict_to_file(data, file_name):
    with open(file_name, "wb") as file:
        pickle.dump(data, file)
    print(f'{file_name} has been created.')

def export_dict_to_json(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file)
    print(f'{file_name} has been created.')

def import_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            data = pickle.load(file)
        return data
    else:
        print(f'{file_name} does not exist')

def import_dict_from_json(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
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
        packet_segmentList.append(input("Zadajte adresu ďalšieho segmentu: "))
        iterator -= 1

    packet_type = []
    pktAmount = int(input("How many of these packets would you like to create?: "))
    while pktAmount > 0:
        packet_type.append(4)
        pktAmount -= 1

    packet = Packet(packet_name, packet_sender, packet_receiver, packet_type, packet_segmentsLeft, packet_segmentList)

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
    print(f"Packet {name} exported to PCAP file.")


p = None

templates = import_dict_from_file('templates.pickle')
if templates:
    print("Templates loaded..")
else:
    templates = import_dict_from_json('templates.json')

    if templates:
        print("templates loaded..")

    else:
        templates = {}
        print("Templates failed to load")

while True:
    os.system("cls")
    print("Menu:")
    print("1. Create a packet")
    print("2. Print templates")
    print("3. Load packet from a template")
    print("4. Save packet as a template")
    print("5. Print loaded packet")
    print("6. Export packet to pcap file")
    print("0. Exit")

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
        # export_dict_to_json(templates, 'templates.json')
        break
    else:
        print("Invalid choice.")

    input("Press enter to continue...")
