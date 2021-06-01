import csv

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


with open('TEST123devices') as f:
    fields = ['hostname', 'devtype']
    hosts = csv.DictReader(f,fieldnames=fields,delimiter=',')
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


print(cisco_ios_list)
print(unknown_os_list)

