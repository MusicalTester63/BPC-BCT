from scapy.all import *
import os
from paket import paket
import pickle
from time import sleep


run = True
dir = ''
suffix = '.pcap'
templates = {}


print("Vitajte v programe PaketBuilder v1, ktorý používa Scapy")
while run:

    os.system('clear')
    print("-------------------------------------")
    print("1. Vytvoriť paket")
    print("2. Uložiť paket ako predvolbu")
    print("3. Načítať paket z predvolby")
    print("4. Vypísať predvolby")
    print("5. Vypísať nastavený paket")
    print("6. Exportovať paket do PCAP súboru")
    print("0. Exit")
    print("-------------------------------------")

    control = input("Volba: ")

    if(control == "1"):

        od = input("\nZadajte adresu odosielateľa: ")
        sl = int(input("Zadajte meziľahlých uzlov: "))
        pr = input("Zadajte adaresu príjemcu: ")

        segList = []
        iterator = sl
        while iterator > 0:
            segList.append(input("Zadajte adresu ďalšieho segmentu: "))
            iterator -= 1

        meno = input("Zadajte meno paketu: ")

        #Typ je ukladaný ako array kvôli tvorbe viacerých paketov, konečná vyexportovaná hodnota bude rovná typ[0], čiže 4
        typ = []
        pktAmount = int(input("Kolko takýchto paketov si prajete vytvoriť?: "))
        while pktAmount > 0:
            typ.append(4)
            pktAmount -= 1

        p = paket(meno, od, pr, typ, sl, segList)

        print("\nmeno: " + p.get_meno())
        print("Odosielatel: " + p.get_od())
        print("Príjemca: " + p.get_pr())
        print("typ:", p.get_typ()[0])
        print("Počet zostávajucich segmentov:", p.get_segmentsLeft())
        print("Zoznam segmentov:", p.get_segmentList())
        input("\nPress enter to continue...")


    elif(control == "2"):
        templates[p.get_meno()] = p
        print("Paket bol úspešne uložný do predvolieb.")        
        input("\nPress enter to continue...")

    elif(control == "3"):
        #input("Zadajte meno paketu: ")
        p = templates[input("Zadajte meno paketu: ")]
        print("Paket bol úspešne načítaný.")
        input("\nPress enter to continue...")


    elif(control == "4"):

        if(len(templates) == 0):
            print("Momentálne nemáte uložené žiadne predvolby")
            input("\nPress enter to continue...")
        else:
            for x in templates:
                print("meno: " + templates[x].get_meno())
                print("Odosielatel: " + templates[x].get_od())
                print("Príjemca: " + templates[x].get_pr())
                print("typ:", templates[x].get_typ()[0])
                print("Počet zostávajucich segmentov:", templates[x].get_segmentsLeft())
                print("Zoznam segmentov:", templates[x].get_segmentList())
            input("\nPress enter to continue...")

    elif(control == "5"):
        print("meno: " + p.get_meno())
        print("Odosielatel: " + p.get_od())
        print("Príjemca: " + p.get_pr())
        print("typ:", p.get_typ()[0])
        print("Počet zostávajucich segmentov:", p.get_segmentsLeft())
        print("Zoznam segmentov:", p.get_segmentList())
        input("\nPress enter to continue...")

    elif(control == "6"):

        paket = IPv6(src=p.get_od(), dst=p.get_pr()) / IPv6ExtHdrRouting(type=p.get_typ(), segleft=p.get_segmentsLeft(),addresses=p.get_segmentList())
        plist = PacketList([p for p in paket])
        filename = input("Zadajte meno súboru: ")
        wrpcap(dir + filename + suffix, plist)

        print("Pakety boli úspešne vygenerované a uložené do pcap súboru ", filename + suffix)
        input("\nPress enter to continue...")

    elif(control == "0"):
        run = False
