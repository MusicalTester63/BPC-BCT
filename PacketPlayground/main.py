import os
import sys
import subprocess
from packet import *
import pickle
import random
from time import sleep
import datetime

def install(package):
    result = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True)
    if result.returncode == 0:
        print(f"{package} installed ✓")        
    else:
        print(f"{package} failed to install ✘")

#pyx==0.16 may not be necessary but I want to have it here just to be safe
def check_packages():
    clear_console()
    with open('requirements.txt', 'r') as f:
        packages = f.readlines()

    installed = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode().splitlines()
    installed_packages = [package.split('==')[0] for package in installed]

    for package in packages:
        package = package.strip()

        if package.split('==')[0] not in installed_packages:
            print(f"{package} is not installed, installing now...")
            install(package)
    print("All packages have been installed")
    #sleep(1)

#Export templates to a file
def export_dict_to_file(data, file_name):
    with open(file_name, "wb") as file:
        pickle.dump(data, file)
    print(f'{file_name} has been created.')

#Import tamplates from a file
def import_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, "rb") as file:
            data = pickle.load(file)
        return data
    else:
        print(f'{file_name} does not exist')

# Clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Packet creator menu
def p_creator(templates):

    p = None

    while True:
        clear_console()
        print("=" * 50)
        print("{:^50}".format("Packet creator"))
        print("=" * 50)
        print("  [1]    Create a packet")
        print("  [2]    Modify loaded packet")
        print("  [3]    Print templates")
        print("  [4]    Load packet from a template")
        print("  [5]    Save packet as a template")
        print("  [6]    Print loaded packet")
        print("  [7]    Export packet to pcap file")
        print("  [Q]    Quit the packet creator")
        print("=" * 50)

        choice = input("Enter your choice: ")

        if choice == "1":
            p = create_packet()
        elif choice == "2":
            modify_packet(p)
        elif choice == "3":
            browse_templates(False,templates)
        elif choice == "4":
            p = load_packet(templates)
        elif choice == "5":
            save_packet(p)
        elif choice == "6":
            clear_console()
            print_packet(p)
        elif choice == "7":
            export_packet(p)
        elif choice == "Q":
            break
        else:
            print("Invalid choice.")
        input("\nPress enter to continue...")

# Iterate over an array to get a chosen value
def iter(object, array):
    clear_console()
    print("Choose a "+object)
    for i, object in enumerate(array):
        print(f"{i+1}. {object}")

    while True:
        try:
            choice = int(input("Enter your choice (1-"+str(len(array))+"): "))
            if choice < 1 or choice > len(array):
                raise ValueError
            break
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and "+str(len(array))+".")

    chosen_value = array[choice-1]
    return chosen_value

# Code to create a packet object
def create_packet():

    ipv6_pool = ["fd12::", "fd13::", "fd23::", "fd24::", "fd25::", "fd34::", "fd35::", "fd45::", "fd46::", "fd56::", "fd91::", "fd92::"]
    #Slice ids: pink, green, purple, red, blue
    slice_ids = ['a000', 'b000', 'c000', 'e000', 'd000']

    
    packet_name = input("Enter packet name: ")
    packet_sender = iter("packet sender", ipv6_pool)
    packet_receiver = iter("packet receiver", ipv6_pool)
    
    packet_segmentsLeft = int(input("Enter number of segments left: "))
    packet_segmentList = []

    iterator = packet_segmentsLeft
    while iterator > 0:
        packet_segmentList.append(iter("address of the next segment", ipv6_pool))
        iterator -= 1

    packet_type = 4
    
    chosen_id = iter("slice ID", slice_ids)

    packet = pkt(packet_name, packet_sender, packet_receiver, packet_type, packet_segmentsLeft, packet_segmentList, chosen_id)

    print("Packet created!")
    print_packet(packet)
    return packet

# Browse saved templates
def browse_templates(browsing,templates):    
    """
    Allows the user to browse a dictionary of templates by key and print the selected value.
    """
    if not templates:
        print("No templates found.")
        return
    # prompt user for selection
    while True:
        clear_console()
        # print list of template keys with numbers
        print("Available templates:")
        for i, key in enumerate(templates):
            print(f"{i+1}. {key}")

        try:
            selection = input("Enter a number to select a template (or 'Q' to quit): ")
            if selection.upper() == 'Q':
                return
            else:
                selection = int(selection)
                if 1 <= selection <= len(templates):
                    key = list(templates.keys())[selection-1]
                    value = templates[key]
                    print(f"\nSelected template: {key}")
                    print_packet(value)
                    print("\n")
                    if browsing:
                        return value
                else:
                    print("Invalid selection. Please enter a number between 1 and", len(templates))
            input("\nPress enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a number or 'Q'.")
            sleep(0.5)

# code to load a packet from a template
def load_packet(templates):
    while True:
        packet = browse_templates(True, templates)        
        if packet:
            choice = input("Load this packet? (Y/N)")
            if choice == "Y":
                print("Packet loaded")
                return packet
            else:
                continue
        else:
            break

# code to save a packet as a template
def save_packet(packet):
    if packet:
        name = packet.get_name()
        templates[name] = packet
        print(f"Packet saved as template: {name}")
    else:
            print("No packet is loaded")

# code to print the loaded packet
def print_packet(packet):
    if packet:
        print("=" * 50)
        print("{:^50}".format(packet.get_name()))
        print("=" * 50)
        print("Sender: " + packet.get_sender())
        print("Receiver: " + packet.get_receiver())
        print("Routing header type: ", packet.get_type())
        print("Segments left: ", packet.get_segmentsLeft())
        print("Segment list: ", packet.get_segmentList())
        print("Slice ID: ", packet.get_identifier())
    else:
        print("No packet is loaded")

# code to export packet to a pcap file --NOT FINISHED
def export_packet(packet):
    if packet:
        name = packet.get_name()
        dir = ''
    
        pktTypeArray = []
        pktAmount = int(input("How many of these packets would you like to create?: "))
        while pktAmount > 0:
            pktTypeArray.append(packet.get_type())
            pktAmount -= 1

        count = len(pktTypeArray)

        ipv6 = IPv6(src=packet.get_sender(), dst=packet.get_receiver())

        srv6_seg_list = packet.get_segmentList()

        padN = IPv6ExtHdrSegmentRoutingTLVPadN(type=4,len=5,padding=packet.get_identifier())
        
        srv6 = IPv6ExtHdrSegmentRouting(type=pktTypeArray, segleft=None, addresses=srv6_seg_list, tlv_objects=[padN])

        data = packet.get_identifier()

        paket = ipv6 / srv6 / TCP() / data

        try:
            paket.display()

            plist = PacketList([p for p in paket])

            filename = input("Input the file name: ")

            if not filename.endswith(".pcap"):
                filename += ".pcap"

            wrpcap(dir + filename, plist)

            print(f"{count} {name} packets exported to PCAP file.")
        except:
            print("Oops something happened. Probably at line 259 :P")
    else:
        print("No packet loaded")

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

#For modifying packets -- NOT FINISHED
def modify_packet(packet):
    if packet:
        print("=" * 50)
        print("{:^50}".format("Modify Packet Attribute"))
        print("=" * 50)
        print("  [1]    Name")
        print("  [2]    Sender")
        print("  [3]    Receiver")
        print("  [4]    Identifier")
        print("  [5]    Segment List")
        print("=" * 50)

        choice = int(input("Enter your choice: "))
        if choice == 1:
            name = input("Enter new name: ")
            packet.set_name(name)
        elif choice == 2:
            sender = input("Enter new sender: ")
            packet.set_sender(sender)
        elif choice == 3:
            receiver = input("Enter new receiver: ")
            packet.set_receiver(receiver)
        elif choice == 4:
            chosen_id = iter("slice ID", slice_ids)
            packet.set_identifier(chosen_id)
        elif choice == 5:
            packet_segmentsLeft = int(input("Enter number of segments left: "))
            packet_segmentList = []
            iterator = packet_segmentsLeft
            while iterator > 0:
                packet_segmentList.append(iter("address of the next segment", ipv6_pool))
                iterator -= 1
            packet.set_segmentList(packet_segmentList)
        else:
            print("Invalid choice")
    else:
        print("No packet is loaded")

#Add a ID to the packet
def add_id():
     # Ask the user for the input pcap file name
    input_filename = input("Enter the input pcap file name: ")

    # Add ".pcap" to file name if not already present
    if not input_filename.endswith(".pcap"):
        input_filename += ".pcap"


    if os.path.exists(input_filename):        

        # Read in the pcap file using rdpcap
        packets = rdpcap(input_filename)

        # Ask the user for the output pcap file name
        output_filename = input("Enter the output pcap file name: ")

        # Add ".pcap" to file name if not already present
        if not output_filename.endswith(".pcap"):
            output_filename += ".pcap"

        #Slice ids: pink, green, purple, red, blue
        slice_ids = ['a000', 'b000', 'c000', 'e000', 'd000']

        print("Choose a slice ID:")
        for i, id in enumerate(slice_ids):
            print(f"{i+1}. {id}")

        while True:
            try:
                choice = int(input("Enter your choice (1-4): "))
                if choice < 1 or choice > 4:
                    raise ValueError
                break
            except ValueError:
                print("Invalid choice. Please enter a number between 1 and 4.")

        chosen_id = slice_ids[choice-1]

        padN = IPv6ExtHdrSegmentRoutingTLVPadN(type=4,len=5,padding=chosen_id)

        # Loop over each packet in the pcap file
        for packet in packets:
            # Check if the packet has an IPv6 header
            if IPv6 in packet:
                if IPv6ExtHdrSegmentRouting in packet:
                    # Export the modified packet to a new pcap file
                    packet.plen = None
                    packet.len = None
                    # Create the padding TLV with the user's identifier
                    packet[IPv6ExtHdrSegmentRouting].tlv_objects = [padN]
                    wrpcap(output_filename, packet, append=True)
                
            else:
                continue
    else:
        print("File does not exist")

#For generating random packets from pool of IPv6 addresses
def generate_random_ipv6_pcap(packet_count, output_filename):
    # Define a list of IPv6 address prefixes to use
    #ipv6_pool = ["fd12::/64", "fd13::/64", "fd23::/64", "fd24::/64", "fd25::/64", "fd34::/64", "fd35::/64", "fd45::/64", "fd46::/64", "fd56::/64", "fd91::/64", "fd92::/64"]
    ipv6_pool = ["fd12::", "fd13::", "fd23::", "fd24::", "fd25::", "fd34::", "fd35::", "fd45::", "fd46::", "fd56::", "fd91::", "fd92::"]

    # Create a list of random IPv6 source and destination addresses using the specified address pool
    src_addrs = [random.choice(ipv6_pool) for i in range(packet_count)]
    dst_addrs = [random.choice(ipv6_pool) for i in range(packet_count)]

    # Generate random packets with IPv6 headers
    packets = []
    for i in range(packet_count):
        # Create an Ethernet header with fixed source and destination MAC addresses
        eth = Ether(dst="00:01:00:01:00:00", src="00:01:00:00:00:00")

        # Create an IPv6 header with random source and destination addresses
        ipv6 = IPv6(src=src_addrs[i], dst=dst_addrs[i])

        # Create an SRv6 header with random addresses in the segment list
        srv6_seg_list = [random.choice(ipv6_pool) for j in range(3)] # Add 3 random segments to the SRv6 header

        #Slice ids: pink, green, purple, red, blue
        slice_ids = ['a000', 'b000', 'c000', 'e000', 'd000']

        random_slice_id = random.choice(slice_ids)

        data = random_slice_id

        # Create a payload with random data
        payload = Raw(load=(str(RandString(size=128))+data))

        padN = IPv6ExtHdrSegmentRoutingTLVPadN(type=4,len=5,padding=random_slice_id)

        srv6 = IPv6ExtHdrSegmentRouting(type=4, segleft=None, addresses=srv6_seg_list, tlv_objects=[padN])

        # Combine the Ethernet, IPv6, SRv6, and payload layers into a single packet
        packet = eth / ipv6 / srv6 / TCP() / data
        
        # Add the packet to the list of packets
        packets.append(packet)
    try:
        # Write the packets to a pcap file
        wrpcap(output_filename, packets)
    except TypeError as e:
        print("An error occured when trying to write to pcap file,",e)

#For analyzing packets
def analyze():
    clear_console()
    print("=" * 50)
    print("{:^50}".format("Packet analysis"))
    print("=" * 50)

    # Ask the user for the input pcap file name
    input_filename = input("Enter the input pcap file name: ")

    # Add ".pcap" to file name if not already present
    if not input_filename.endswith(".pcap"):
        input_filename += ".pcap"

    if os.path.exists(input_filename):
        # Read in the pcap file using rdpcap
        packets = rdpcap(input_filename)

        # Store packets in a list
        packet_list = list(packets)       

        while True:
            clear_console()
            print("=" * 50)
            print("{:^50}".format("Packet analysis"))
            print("=" * 50)

             # Print packet info and ask user which packet to view
            for i, packet in enumerate(packet_list):
                print(f"[{i}] {packet.summary()}")

            packet_index = input("Enter the index of the packet you want to view (Q to quit): ")
            if packet_index == "Q":
                break
            else:
                # Check if user input is a valid integer and within range of packet_list
                try:
                    packet_index = int(packet_index)
                    if packet_index < 0 or packet_index >= len(packet_list):
                        raise ValueError()
                except ValueError:
                    print("Invalid packet index!")
                    return

                # Display the selected packet
                selected_packet = packet_list[packet_index]
                selected_packet.display()
                input("\nPress enter to continue...")
    else:
        print("File does not exist")

#Launching Scapy console
def launch_scapy_console():
    conf.prompt = "Scapy >>> "
    while True:
        try:
            user_input = input(conf.prompt).strip()
            if user_input.lower() == "exit":
                print("Exiting Scapy console...")
                break  # Exit the while loop to return control to the main script
            else:
                # Execute the user input in Scapy's environment
                result = eval(user_input, globals(), locals())
                if result is not None:
                    print(result)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt received, returning to Scapy console...")
            continue  # Restart the while loop to return to the Scapy console
        except Exception as e:
            print("Error: ", e)


check_packages()
try:
    from scapy.all import *
except ImportError:
    print("Restart the script please :)")
    sys.exit(1)

def PacketPlayground():
    clear_console()
    print("Loading templates...")
    #sleep(2)
    templates = import_dict_from_file('templates.pickle')
    if templates:
        print("Templates loaded..")
    else:
        templates = {}
        print("Templates failed to load")
    #sleep(1)


    while True:
        clear_console()

        print("=" * 50)
        print("{:^50}".format("Packet Playground"))
        print("=" * 50)
        print("  [C]    Packet creator")
        print("  [A]    Add identifier to packet(s)")
        print("  [T]    Create a test pcap file")
        print("  [a]    Analyze packet(s)")
        print("  [S]    Launch Scapy")
        print("  [J]    Join PCAP files")
        print("  [Q]    Quit the program")
        print("=" * 50)


        choice = input("Enter your choice: ")

        if choice == "C":
            p_creator(templates)
        elif choice == "A":
            add_id()
        elif choice == "T":
            pktAmount= int(input("How many packets would you like to generate?: "))
            generate_random_ipv6_pcap(pktAmount, datetime.now().strftime("%d-%m-%Y-%H-%M-%S")+".pcap")
        elif choice == "a":
            analyze()
        elif choice == "S":
            launch_scapy_console()
        elif choice == "J":
            join_pcap_files()
        elif choice == "Q":
            export_dict_to_file(templates, 'templates.pickle')
            break
        else:
            print("Invalid choice.")

        input("\nPress enter to continue...")


PacketPlayground()