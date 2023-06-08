from django.shortcuts import render, HttpResponse
from pysnmp.hlapi import *
import _thread
import time
import ipaddress
import threading
from subprocess import run,PIPE
import sys
import subprocess

def scanner(request):
    inp=request.POST.get('param')
    #Throws exception when the ip address in the request is wrong
    try:
        ip = ipaddress.IPv4Network(inp)
        out= subprocess.Popen([sys.executable,'scan_script.py',inp],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        msg = "The network is being Scanned, Please Wait"
        return render(request, 'audit/audit.html',{'ip':out.stdout, 'message': msg})
    except ValueError:
        return render(request, 'audit/audit.html',{'message': "Invalid IP Network Or Mask. Please Type In Correct Format E.G: 192.168.1.1/24"})
