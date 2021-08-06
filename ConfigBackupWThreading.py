#include required modules===============================================================================================
#example: import modulename (which is basically a modulename.py file) or from modulename import functionname
#if we typed import getpass, we would need to use getpass.getpass()
#but we did from getpass import getpass, so we can use the function getpass() without invoking the module

from getpass import getpass                                     #for entering passwords
from pprint import pprint                                       #for "pretty" print - pprint function
from netmiko import ConnectHandler                              #for connecting to devices
import time                                                     #time used for filenames
from datetime import datetime                                   #time used for measuring script execution time
from multiprocessing.dummy import Pool as ThreadPool            #for multi-threading
from netmiko.ssh_exception import AuthenticationException       #for throwing exception due to Authentication errors
#=======================================================================================================================


#Reading all devices from a file, function used in Main==================================================================
def read_devices(devices_filename):

    devices = {}  # Creating dictionary for storing devices info

    with open(devices_filename) as devices_file:

        for device_line in devices_file:

            device_info = device_line.strip().split(',')  #Extract device info from each file line using delimiter ","

            # Create dictionary of device objects ...
            device = {'ipaddr': device_info[0],             #Device IP address
                      'type':   device_info[1],             #Device OS type
                      'name':   device_info[2],             #Device name(hostname)
                      'access_type': device_info[3]}        #Device access type (domain or local)

            devices[device['ipaddr']] = device  # store our device in the devices dictionary - A LIST OF DICTIONARIES with key:value pairs
            # Key for devices dictionary entries is ipaddr and value is everything it has (ipaddr, type, name, acces_type)
            # devices[key] = value IS THE EXACT THOUGHT

    print('\nList of all devices:')
    pprint(devices)

    return devices
#=======================================================================================================================

#Getting all credentials that may be required, depending on authorization on specific devices===========================
def read_device_creds():

    username = input("Enter domain user name: ")
    password = getpass()
    secret = password

    localuser = input("Enter local user name: ")
    localpass = getpass()
    localsecret = localpass

    return username, password, secret, localuser, localpass, localsecret
#=======================================================================================================================

#Function to connect to devices and send commands=======================================================================
def config_worker(device_and_creds):

    # For threadpool library we had to pass only one argument, so extract the two
    # pieces (device and creds) out of the one tuple passed.
    device = device_and_creds[0]        #all devices - list of dictionaries
    creds  = device_and_creds[1]        #all credentials - list of strings

    device_ip = device['ipaddr']            #Device IP address
    device_os = device['type']              #Device OS type
    device_name = device['name']            #Device name(hostname)
    localaccess = device['access_type']      #Device access type (local: YES/NO or something different)
    if localaccess == "NO":
        user = creds[0]
        passw = creds[1]
        secret = creds[2]
    elif localaccess == "YES":
        user = creds[3]
        passw = creds[4]
        secret = creds[5]
    else:
        write_log("Error: Device" + device_name + "-" + device_ip + "has unknown/undefined type of access. Will use default cisco/cisco")
        user = "cisco"
        passw = "cisco"
        secret = "cisco"

    #Set command to be sent based on device operating system and it's adequate syntax
    if   device_os == 'cisco_nxos': command = 'show running-config'
    elif device_os == 'cisco_wlc': command = 'show run-config commands'
    elif device_os == 'cisco_asa': command = 'more system:running-config'
    elif device_os == 'cisco_xe': command = 'more system:running-config'
    elif device_os == 'zte_zxros': command = 'show running-config'
    elif device_os == 'huawei': command = 'display current-configuration'
    elif device_os == 'huawei_vrpv8': command = 'display current-configuration'
    elif device_os == 'alcatel_sros': command = 'admin display-config'
    elif device_os == 'juniper_junos': command = 'show configuration'
    elif device_os == 'juniper_screenos': command = 'get config'
    elif device_os == 'fortinet': command = 'show'
    else:                               command = 'show running-config'    # attempt Cisco IOS command as default


    #Connect to the device

    print('Connecting to device: {0} - {1} using SSH'.format(device_name, device_ip))
    try:
        session = ConnectHandler(device_type=device_os, ip=device_ip, username=user, password=passw, secret=secret, global_delay_factor=2)
    except (AuthenticationException):
        write_log('Authentication failure: ' + device_name + "-" + device_ip)
    except (EOFError):
        write_log('End of file while attempting device: ' + device_name + "-" + device_ip)
    except:
        if device_os == "cisco_ios" or "huawei" or "zte_zxros" or "juniper_junos":
            try:
                print('SSH failed, connecting to device: {0} - {1} using Telnet'.format(device_name, device_ip))
                device_os = device_os + "_telnet"
                session = ConnectHandler(device_type=device_os, ip=device_ip, username=user, password=passw, secret=secret, global_delay_factor=2)
            except:
                write_log("Access to " + device_name + '-' + device_ip + " failed for unknown reason, configuration backup task was not finished")
            else:
                #Use CLI command to get configuration data from device
                print('Getting configuration from device ' + device_name)
                config_data = session.send_command(command)
                #Write out configuration information to file  - filename: device_name#device_ip-date
                config_filename = device_name + '#' + device_ip + '-' + today  # Important - create unique file name
                write_log('Saving configuration for: ' + config_filename)
                with open(config_filename, 'w') as config_out:
                    config_out.write(config_data)
                session.disconnect()
                return
        else:
            write_log("Access to " + device_name + '-' + device_ip + " failed for unknown reason, configuration backup task was not finished")

    else:
        #Use CLI command to get configuration data from device
        print('Getting configuration from device ' + device_name)
        config_data = session.send_command(command)

        #Write out configuration information to file with following filename format: device_name#device_ip-date
        config_filename = device_name + '#' + device_ip + '-' + today   # Important - create unique file name

        write_log('Saving configuration for: ' + config_filename)
        with open(config_filename, 'w') as config_out:
            config_out.write(config_data)
        session.disconnect()

        return


#========================================================================================================================
# Main: Get Configuration
#========================================================================================================================

#set today's date========================================================================================================
day = time.strftime('%d')
month = time.strftime('%m')
year = time.strftime('%Y')
today = day + "-" + month + "-" + year
#========================================================================================================================

#Function for logging and output print===================================================================================
log_file = open((today + "-" + "message.log"), "w+")
def write_log(*args):
    line = ' '.join([str(a) for a in args])
    log_file.write(line+'\n')
    print(line)
#========================================================================================================================

devices_dict_list = read_devices('DevicesList')   #Reading file "DevicesList" using read_devices() function
credentials   = read_device_creds()                 #Getting credentials using read_device_creds() function

num_threads_str = input('\nNumber of threads (default is 7): ') or '7'  #Number of threads to use
num_threads     = int(num_threads_str)                                  #Convert input to integer type

#Create lists to pass to config worker - aDevice from device_dict_list.items() and credentials list from credentials
config_params_list = []
for ipaddr, aDevice in devices_dict_list.items():
    config_params_list.append((aDevice, credentials))
#========================================================================================================================

starting_time = datetime.now()    #start timer

#Starting thread pool=====================================================================================================
write_log('\nCreating chosen thread pool of ' + num_threads_str + ',launching get configuration threads\n')
threads = ThreadPool(num_threads)
results = threads.map(config_worker, config_params_list)

threads.close()                                     #close current thread if it's finished and remove it from thread pool
threads.join()                                      #join new thread to the thread pool
#========================================================================================================================

write_log('\nSCRIPT COMPLETED! Done in: ', datetime.now()-starting_time)  #FINISHED
log_file.close()                                    #close the logging file


#========================================================================================================================
