import random
import os
import random
import string


os.system('cls' if os.name == 'nt' else 'clear')

try:
    from scapy.all import *
except ImportError:
    print("scapy not found")
    sys.exit(1)
print("IPv6:")
ls(IPv6)
print("\n")
print("IPv6ExtHdrRouting:")
ls(IPv6ExtHdrRouting)
print("\n")
print("IPv6ExtHdrSegmentRoutingTLVPadN:")
ls(IPv6ExtHdrSegmentRoutingTLVPadN)
print("\n")



answer = input("Do you want to generate trash? (yes/no): ")

if answer == "yes":

    # Generate a 6-bit random number
    rand_num = random.randint(0, 63)

    # Print the random number
    print("6-bit random number: ", bin(rand_num)[2:].zfill(6))
    id = bin(rand_num)[2:].zfill(6)
    print(id)

    # Generate 5 random filenames with .pcap extension
    pcap_files = [''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.pcap' for _ in range(5)]

    # Create empty pcap files with the generated filenames
    for file in pcap_files:
        open(file, 'w').close()
        print(f"Created file: {file}")
else:
    print("Done")
