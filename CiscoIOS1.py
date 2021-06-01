from netmiko import ConnectHandler
import getpass
import sys
import time

#Date
day = time.strftime('%d')
month = time.strftime('%m')
year = time.strftime('%Y')
today = day + "-" + month + "-" + year

#Iinitialize "device" using predefined dictionary
device = {
    'device_type': 'cisco_ios',
    'ip': '1.1.1.1',
    'username': 'username',
    'password': 'password',
    'secret': 'password'
}

#Open a new .txt file
ipfile1 = open("ciscoios.txt") #ciscoIOS

#Enter credentials
print("Script to create device backup configuration, please enter your credentials:")
device['username'] = input("User name: ")
device['password'] = getpass.getpass()
print("Enter enable password: ")
device['secret'] = getpass.getpass()

#Taking CiscoIOS backup
for line in ipfile1:
    try:
        print("\n\nTrying SSH...")
        device['ip'] = line.strip("\n")
        device['device_type'] = "cisco_ios"
        print("Connecting Device ", line)
        net_connect = ConnectHandler(**device)
        net_connect.enable()
        devicename = net_connect.find_prompt()
        time.sleep(1)
        print("Reading the running config ")
        output = net_connect.send_command('show run')
        time.sleep(3)
        filename = devicename + device['ip'] + '-' + today + ".txt"
        saveconfig = open(filename, 'w+')
        print("Writing Configuration to file")
        saveconfig.write(output)
        saveconfig.close()
        time.sleep(2)
        net_connect.disconnect()
        print("Configuration saved to file", filename)
    except:
        try:
            print("SSH access failed, trying Telnet...")
            device['device_type'] = "cisco_ios_telnet"
            net_connect = ConnectHandler(**device)
            net_connect.enable()
            devicename = net_connect.find_prompt()
            time.sleep(1)
            print("Reading the running config ")
            output = net_connect.send_command('show run')
            time.sleep(3)
            filename = devicename + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            print("Writing Configuration to file")
            saveconfig.write(output)
            saveconfig.close()
            time.sleep(2)
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed, configuration backup did not finish")
            continue
ipfile1.close()

print("\nDevice configuration backup script completed")
