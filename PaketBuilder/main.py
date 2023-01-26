from scapy.all import *
from scapy.layers.inet6 import IPv6, IPv6ExtHdrRouting
from scapy.plist import PacketList
from scapy.utils import wrpcap

from paket import paket
import pickle

run = True
#dir = '/home/xhamra02/Desktop/'
dir = ''
suffix = '.cap'

print("Vitajte v programe PaketBuilder v1, ktorý používa Scapy")
while run:

    print("-------------------------------------")
    print("1. Vytvoriť paket")
    print("2. Uložiť paket ako predvolbu")
    print("3. Vypísať predvolby")
    print("4. Vypísať nastavený paket")
    print("5. Exportovať paket do PCAP súboru")
    print("0. Exit")
    print("-------------------------------------")

    control = input("Volba: ")
    print(control)

    if(control == "1"):

        od = input("Zadajte adresu odosielateľa: ")
        sl = int(input("Zadajte meziľahlých uzlov: "))
        pr = input("Zadajte adaresu príjemcu: ")

        segList = []
        iterator = sl
        while iterator > 0:
            segList.append(input("Zadajte adresu ďalšieho segmentu: "))
            iterator -= 1

        meno = input("Zadajte meno paketu/paketom: ")

        typ = []
        pktAmount = int(input("Kolko takýchto paketov si prajete vytvoriť?: "))
        while pktAmount > 0:
            typ.append(4)
            pktAmount -= 1

        p = paket(meno, od, pr, typ, sl, segList)

        print("meno: " + p.get_meno())
        print("Odosielatel: " + p.get_od())
        print("Príjemca: " + p.get_pr())
        print("typ:", p.get_typ()[0])
        print("Počet zostávajucich segmentov:", p.get_segmentsLeft())
        print("Zoznam segmentov:", p.get_segmentList())

        paket = IPv6(src=p.get_od(), dst=p.get_pr()) / IPv6ExtHdrRouting(type=p.get_typ(), segleft=p.get_segmentsLeft(), addresses=p.get_segmentList())



    elif(control == "2"):
        print("cic")

    elif(control == "3"):
        print("cic")

    elif(control == "4"):
        paket.display()

    elif(control == "5"):

        plist = PacketList([p for p in paket])
        filename = input("Zadajte meno súboru: ")
        wrpcap(dir + filename + suffix, plist)

        print("Pakety boli úspešne vygenerované a uložené do pcap súboru ", filename + suffix)

    elif(control == "0"):
        run = False
