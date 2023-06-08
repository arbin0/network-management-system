from pysnmp.carrier.asyncore.dispatch import AsyncoreDispatcher
from pysnmp.carrier.asyncore.dgram import udp, udp6, unix
from pyasn1.codec.ber import decoder
from pysnmp.proto import api
import os
import json
import sys

#This Code is taken from SNMPLabs' website which is cited well in the documentation.
#Creating the notification.json file to store notifications received from
alert_path = r'static\data\notification.json'

if not os.path.exists(alert_path):
    with open(alert_path, 'w'): pass


def listenAlert(transportDispatcher, transportDomain, transportAddress, wholeMsg):
    while wholeMsg:
        msgVer = int(api.decodeMessageVersion(wholeMsg))
        if msgVer in api.protoModules:
            pMod = api.protoModules[msgVer]
        else:
            print('Unsupported SNMP version %s' % msgVer)
            return
        reqMsg, wholeMsg = decoder.decode(
            wholeMsg, asn1Spec=pMod.Message(),
        )
        print('Notification message from %s:%s: ' % (
            transportDomain, transportAddress
        )
              )
        reqPDU = pMod.apiMessage.getPDU(reqMsg)
        if reqPDU.isSameTypeWith(pMod.TrapPDU()):
            agent = ''
            trapType=''
            if msgVer == api.protoVersion1:
                print('############################################')
                print('Enterprise: %s' % (pMod.apiTrapPDU.getEnterprise(reqPDU).prettyPrint()))
                print('Agent Address: %s' % (pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()))
                agent = pMod.apiTrapPDU.getAgentAddr(reqPDU).prettyPrint()
                print('Generic Trap: %s' % (pMod.apiTrapPDU.getGenericTrap(reqPDU).prettyPrint()))
                print('Specific Trap: %s' % (pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()))
                trapType = pMod.apiTrapPDU.getSpecificTrap(reqPDU).prettyPrint()
                print('Uptime: %s' % (pMod.apiTrapPDU.getTimeStamp(reqPDU).prettyPrint()))
                varBinds = pMod.apiTrapPDU.getVarBinds(reqPDU)
            else:
                varBinds = pMod.apiPDU.getVarBinds(reqPDU)
            print('Var-binds:')
            c = 1
            message1 =''
            message2 =''
            for oid, val in varBinds:
                if trapType == '0':
                    print('%s = %s' % (oid.prettyPrint(), val.prettyPrint()))
                    if c == 2:
                        message1 = val.prettyPrint()
                        if message1 ='1':
                            message1 ='Link up'
                        elif message1='0':
                            message1 ='Link down'

                    if c == 4:
                        message2 = val.prettyPrint()
                c= c + 1
            if trapType == '0':
                alert ={'agent': agent, 'message': '%s %s' %(message1, message2)}
                json_data ={'alerts' : [alert,],}
                if os.path.getsize(alert_path) > 0:
                    with open(alert_path) as json_file:
                        data = json.load(json_file)

                    temp = data['alerts']
                    temp.append(alert)
                    temp_data ={'alerts' : temp,}
                    with open(alert_path, "w") as outfile:
                        json.dump(temp_data, outfile, indent =2 )
                else:
                    data = json.dumps(json_data, indent=2)

                    with open(alert_path, "w") as outfile:
                        outfile.write(data)


    return wholeMsg


transportDispatcher = AsyncoreDispatcher()

transportDispatcher.registerRecvCbFun(listenAlert)

# UDP/IPv4
transportDispatcher.registerTransport(
    udp.domainName, udp.UdpSocketTransport().openServerMode(('10.1.1.2', 162))
)

# UDP/IPv6
transportDispatcher.registerTransport(
    udp6.domainName, udp6.Udp6SocketTransport().openServerMode(('::1', 162))
)



transportDispatcher.jobStarted(1)

try:
    transportDispatcher.runDispatcher()
except:
    transportDispatcher.closeDispatcher()
    raise
