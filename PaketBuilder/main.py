from scapy.all import *
from scapy.layers.inet6 import IPv6ExtHdrRouting, IPv6

from paket import paket
import pickle

run = True
dir = '/home/xhamra02/Desktop/'
suffix = '.cap'

print("Vitajte v programe PaketBuilder v1, ktorý používa Scapy")
while run:

    print("1. Vytvoriť paket")
    print("2. Uložiť paket ako predvolbu")
    print("Vypísať predvolby")
    print("0. Exit")

    p = None

    od = input("Zadajte adresu odosielateľa: ")
    sl = int(input("Zadajte meziľahlých uzlov: "))
    pr = input("Zadajte adaresu príjemcu: ")

    segList = []
    iterator = sl
    while iterator > 0:
        segList.append(input("Zadajte adresu ďalšieho segmentu: "))
        iterator -= 1



    typ = []
    pktAmount = int(input("Kolko takýchto paketov si prajete vytvoriť?: "))
    while pktAmount > 0:
        typ.append(4)
        pktAmount -= 1

    meno = input("Zadajte meno paketu/paketom: ")

    p = paket(meno, od, pr, typ, sl, segList)

    print("meno: " + p.get_meno())
    print("Odosielatel: " + p.get_od())
    print("Príjemca: " + p.get_pr())
    print("typ:", p.get_typ()[0])
    print("Počet zostávajucich segmentov:", p.get_segmentsLeft())
    print("Zoznam segmentov:", p.get_segmentList())

    paket = IPv6(src=p.get_od(), dst=p.get_pr()) / IPv6ExtHdrRouting(type=p.get_typ(), segleft=p.get_segmentsLeft(), addresses=p.get_segmentList())

    plist = PacketList([p for p in paket])
    plist.summary()
    [p.display() for p in plist]

    filename = input("Zadajte meno súboru: ")

    wrpcap(dir + filename + suffix, plist)

    print("Pakety boli úspešne vygenerované a uložené do pcap súboru ", filename + suffix)

    if input("Prajete si pokračovať?(Y/N): ") == "Y":
        run = True
    else:
        run = False
