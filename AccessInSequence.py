#dodato ucitavanje fajla sa komandama

from netmiko import ConnectHandler
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
#from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException
#import sys
import time
import csv

##datum
day = time.strftime('%d')
month = time.strftime('%m')
year = time.strftime('%Y')
today = day + "-" + month + "-" + year

##definisanje liste ip adresa uredjaja razlicitih vendora
cisco_ios_list = []
cisco_nxos_list = []
cisco_asa_list = []
cisco_wlc_list = []
huawei_list = []
huawei_vrpv8_list = []
alcatel_sros_list = []
checkpoint_gaia_list = []
fortinet_list = []
juniper_list = []
juniper_junos_list = []
nokia_sros_list = []
zte_zxros_list = []
unknown_os_list = []

#definisanje liste komandi za uredjaje razlicitih vendora
cisco_ios_commands_list = []
cisco_nxos_commands_list = []
cisco_asa_commands_list = []
cisco_wlc_commands_list = []
huawei_commands_list = []
huawei_vrpv8_commands_list = []
alcatel_sros_commands_list = []
checkpoint_gaia_commands_list = []
fortinet_commands_list = []
juniper_commands_list = []
juniper_junos_commands_list = []
nokia_sros_commands_list = []
zte_zxros_commands_list = []
unknown_os_commands_list = []

##otvaranje spiska svih uredjaja sa adresama i sortiranje u listama po vendor OS-u
with open('AIS-devicelist') as fajl:
    fields = ['hostname', 'devtype']
    hosts = csv.DictReader(fajl,fieldnames=fields,delimiter=',')
    for host in hosts:
        hostname = host['hostname']
        devtype = host['devtype']
        if devtype == "cisco_ios":
            cisco_ios_list.append(hostname)
        elif devtype == "cisco_nxos":
            cisco_nxos_list.append(hostname)
        elif devtype == "cisco_asa":
            cisco_asa_list.append(hostname)
        elif devtype == "cisco_wlc":
            cisco_wlc_list.append(hostname)
        elif devtype == "huawei":
            huawei_list.append(hostname)
        elif devtype == "huawei_vrpv8_list":
            huawei_vrpv8_list.append(hostname)
        elif devtype == "alcatel_sros":
            alcatel_sros_list.append(hostname)
        elif devtype == "checkpoint_gaia":
            checkpoint_gaia_list.append(hostname)
        elif devtype == "fortinet":
            fortinet_list.append(hostname)
        elif devtype == "juniper":
            juniper_list.append(hostname)
        elif devtype == "juniper_junos":
            juniper_junos_list.append(hostname)
        elif devtype == "nokia_sros":
            nokia_sros_list.append(hostname)
        elif devtype == "zte_zxros":
            zte_zxros_list.append(hostname)
        else:
            unknown_os_list.append(hostname)

#otvaranje fajla sa spiskom komandi
with open('AIS-commands') as f:
    fields = ['commands', 'devtype']
    commands = csv.DictReader(f,fieldnames=fields,delimiter=',')
    for Acommand in commands:
        command = Acommand['commands']
        devtype = Acommand['devtype']
        if devtype == "cisco_ios":
            cisco_ios_commands_list.append(command)
        elif devtype == "cisco_nxos":
            cisco_nxos_commands_list.append(command)
        elif devtype == "cisco_asa":
            cisco_asa_commands_list.append(command)
        elif devtype == "cisco_wlc":
            cisco_wlc_commands_list.append(command)
        elif devtype == "huawei":
            huawei_commands_list.append(command)
        elif devtype == "huawei_vrpv8_list":
            huawei_vrpv8_commands_list.append(command)
        elif devtype == "alcatel_sros":
            alcatel_sros_commands_list.append(command)
        elif devtype == "checkpoint_gaia":
            checkpoint_gaia_commands_list.append(command)
        elif devtype == "fortinet":
            fortinet_commands_list.append(command)
        elif devtype == "juniper":
            juniper_commands_list.append(command)
        elif devtype == "juniper_junos":
            juniper_junos_commands_list.append(command)
        elif devtype == "nokia_sros":
            nokia_sros_commands_list.append(command)
        elif devtype == "zte_zxros":
            zte_zxros_commands_list.append(command)
        else:
            unknown_os_commands_list.append(command)


##unapred definisan dictionary
device = {
    'device_type': 'cisco_ios',
    'ip': '1.1.1.1',
    'username': 'username',
    'password': 'password',
    'secret': 'password',
    'global_delay_factor': 2
}

##unos kredencijala
print("Script will be used to create backup configuration of network devices, please enter your credentials:")
device['username'] = input("User name: ")
device['password'] = getpass()
print("Enter enable password: ")
device['secret'] = getpass()

#CiscoIOS backup
#iteracija kroz cisco_ios_list listu, ukoliko ConnectHandler ne prodje, baci exception.
for line1 in cisco_ios_list:
    device['ip'] = line1
    device['device_type'] = "cisco_ios"
    try:
        print("\n\nTrying SSH access...")
        print("Connecting to device IP: ", line1)
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device['ip'])
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device['ip'])
        continue
    except:
        try:
            print("SSH access failed, trying Telnet...")
            device['device_type'] = "cisco_ios_telnet"
            net_connect = ConnectHandler(**device)
            net_connect.enable()
            devicename = net_connect.find_prompt()
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in cisco_ios_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
            continue
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue
    else:
        try:
            net_connect.enable()
            devicename = net_connect.find_prompt()
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in cisco_ios_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue

#CiscoNXOS backup
for line2 in cisco_nxos_list:
    device['device_type'] = "cisco_nxos"
    device['ip'] = line2
    try:
        print("\n\nTrying SSH access...")
        print("Connecting to device IP: ", line2)
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device['ip'])
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device['ip'])
        continue
    except:
        print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
        continue
    else:
        try:
            net_connect.enable()
            devicename = net_connect.find_prompt()
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in cisco_nxos_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue

#CiscoASA backup
for line3 in cisco_asa_list:
    device['device_type'] = "cisco_asa"
    device['ip'] = line3
    try:
        print("\n\nTrying SSH access...")
        print("Connecting to device IP: ", line3)
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device['ip'])
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device['ip'])
        continue
    except:
        print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
        continue
    else:
        try:
            net_connect.enable()
            devicename = net_connect.send_command('show hostname')
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + '-' + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in cisco_asa_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue

#CiscoWLC backup
for line4 in cisco_wlc_list:
    device['device_type'] = "cisco_wlc"
    device['ip'] = line4
    try:
        print("\n\nTrying SSH access...")
        print("Connecting to device IP: ", line4)
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device['ip'])
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device['ip'])
        continue
    except:
        print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
        continue
    else:
        try:
            net_connect.enable()
            time.sleep(1)
            print("Reading the running config ")
            filename = "WLC-" + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in cisco_wlc_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue

#Huawei backup
for line5 in huawei_list:
    device['device_type'] = "huawei"
    device['ip'] = line5
    try:
        print("\n\nTrying SSH access...")
        print("Connecting to device IP: ", line5)
        net_connect = ConnectHandler(**device)
    except (AuthenticationException):
        print ('Authentication failure: ' + device['ip'])
        continue
    except (NetMikoTimeoutException):
        print ('Timeout to device: ' + device['ip'])
        continue
    except (EOFError):
        print ('End of file while attempting device ' + device['ip'])
        continue
    except:
        try:
            print("SSH access failed, trying Telnet...")
            device['device_type'] = "huawei_telnet"
            net_connect = ConnectHandler(**device)
            devicename = net_connect.find_prompt()
            devicename = devicename.translate({ord(i): None for i in '<>'})
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + '-' + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in huawei_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue
    else:
        try:
            devicename = net_connect.find_prompt()
            devicename = devicename.translate({ord(i): None for i in '<>'})
            time.sleep(1)
            print("Reading the running config ")
            filename = devicename + '-' + device['ip'] + '-' + today + ".txt"
            saveconfig = open(filename, 'w+')
            for command in huawei_commands_list:
                output = net_connect.send_command(command, delay_factor=2)
                time.sleep(2)
                FileOutput = "\n Command - " + command + "\n" + output + "\n"
                saveconfig.write(FileOutput)
            print("Writing configuration to file")
            saveconfig.close()
            net_connect.disconnect()
            print("Configuration saved to file", filename)
        except:
            print("Access to " + device['ip'] + " failed for unknown reason, configuration backup task was not finished")
            continue

#kraj skripte
print("\nDEVICE CONFIGURATION BACKUP SCRIPT COMPLETED!")
