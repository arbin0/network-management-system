import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from netmiko import ConnectHandler
import sys
import json
import os
import time
import threading

host_json_path = r'static\data\host_info.json'
host = {}
with open(host_json_path) as json_file:
    data = json.load(json_file)
    host = data
net_connect = ConnectHandler(**host)
if sys.argv[1] == 'juniper':
    output = net_connect.send_command('show configuration')
else:
    net_connect.enable()
    output = net_connect.send_command('show running-config')
filename=''
save_text_as = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
#enter data here
save_text_as.write(output)
save_text_as.close()
