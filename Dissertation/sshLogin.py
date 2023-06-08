from netmiko import ConnectHandler
import sys
import json
import os
import time
import threading
stop_threads =False

pid_file = "pip.pid"
if not os.path.exists(pid_file):
   pass
else:
    with open("pip.pid", "r") as f:
       pid = int(f.read())
       try:
           os.kill(pid,9)
       except:
           pass



def run( type, net_connect ):
    pid = os.getpid()
    with open("pip.pid", "w") as f:
       f.write(str(pid))
    while True:
        print('thread started')
        json_file_path = r'static\data\data.json'
        host_json_path = r'static\data\host_info.json'

        if type == 'router':
            output1 = net_connect.send_command('show interface', use_textfsm=True)
            output2 = net_connect.send_command('show ip route')
            output3 = net_connect.send_command('show version', use_textfsm=True)
            output4 = net_connect.send_command('show ip ospf neighbor')
            output5 = net_connect.send_command('show ip eigrp neighbors')
            output6 = net_connect.send_command('show ip bgp summary')
            output = {'interface': output1, 'route': output2, 'version': output3, 'ospf': output4, 'eigrp': output5, 'bgp': output6, 'device_type': type}
        else:
            output1 = net_connect.send_command('show interface', use_textfsm=True)
            output2 = net_connect.send_command('show interfaces switchport', use_textfsm=True)
            output3 = net_connect.send_command('show version', use_textfsm=True)
            output4 = net_connect.send_command('show spanning-tree', use_textfsm=True)
            output5 = net_connect.send_command('show vtp status', use_textfsm=True)
            output6 = net_connect.send_command('show vlan', use_textfsm=True)
            output = {'interface': output1, 'switchport': output2, 'version': output3, 'spanning': output4, 'vtp': output5, 'vlan': output6, 'device_type': type}


        json_output = json.dumps(output, indent =2)
        json_host = json.dumps(cisco, indent=2)
        with open(json_file_path, "w") as outfile:
            outfile.write(json_output)
        if not os.path.exists(host_json_path):
            with open(host_json_path, 'w'): pass

        with open(host_json_path, "w") as outfile:
            outfile.write(json_host)
        # net_connect.find_prompt()
        if stop_threads:
            break
def connect( host, username, password, device_type, secret ):
    # cisco ={
    #     'device_type': 'cisco_ios',
    #     'host': 'host',
    #     'username': username,
    #     'password':password,
    #     'secret' : secret,
    # }
    cisco ={
        'device_type': 'cisco_ios',
        'host':'10.10.10.10',
        'username': 'cisco',
        'password': 'cisco',
        'secret' : 'cisco',
    }
    type = ''

    net_connect = ConnectHandler(**cisco)
    if device_type == 'router':
        stop_threads =False
        t1 = threading.Thread(target = run, args= (device_type,net_connect,))
        t1.start()
        time.sleep(100)
        stop_threads = True
        t1.join()
        print('thread killed')
    else:
        stop_threads =False
        t1 = threading.Thread(target = run, args= (device_type,net_connect,))
        t1.start()
        time.sleep(200)
        stop_threads = True
        t1.join()
        print('thread killed')
