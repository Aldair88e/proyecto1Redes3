import time
import rrdtool
from getSNMPcopy import consultaSNMP

def update(host, comunidad):
    input_ucast_traffic = 0
    input_pkts_traffic = 0
    output_echo_traffic = 0
    input_segm_traffic = 0
    input_datagrams_traffic = 0
    interfaz = '10'
    if host == 'localhost':
        interfaz = '2'


    while 1:
	#ifUncastPkts
        input_ucast_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.2.2.1.11.' + interfaz))
	#ipInReceives
        input_pkts_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.4.3.0'))
	#icmpOutEchos
        output_echo_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.5.21.0'))
	#tcpInSegs
        input_segm_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.6.10.0'))
	#udpInDatagrams
        input_datagrams_traffic = int(
            consultaSNMP(comunidad,host,
                         '1.3.6.1.2.1.7.1.0'))

        valor = "N:" + str(input_ucast_traffic) + ':' + str(input_pkts_traffic) + ':'
        valor = valor + str(output_echo_traffic) + ':' + str(input_segm_traffic) + ':'
        valor = valor + str(input_datagrams_traffic)
        rrdtool.update(host + '.rrd', valor)
        time.sleep(1)

    if ret:
        print (rrdtool.error())
        time.sleep(300)

def dump(host):
    rrdtool.dump(host + '.rrd', host + '.xml')

