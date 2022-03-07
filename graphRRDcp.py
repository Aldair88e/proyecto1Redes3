import sys
import rrdtool
import time

def graficar(nombre, tiempo):
	ventanaT = tiempo * 60
	tiempo_actual = int(time.time())
	tiempo_inicial = tiempo_actual - ventanaT


	ret = rrdtool.graph( nombre + "_ucast.png",
			"--start",str(tiempo_inicial),
			"--end","N",
			"--title=Paquetes Unicast recibidos",
			"DEF:inUcastPkts="+nombre+".rrd:inUcastPkts:AVERAGE",
			"LINE2:inUcastPkts#FF0000:Paquetes Unicast de entrada")

	ret2 = rrdtool.graph( nombre + "_pktsIP.png",
			"--start",str(tiempo_inicial),
			"--end","N",
			"--title=Paquetes IPv4 de entrada",
			"DEF:inPktsIp="+nombre+".rrd:inPktsIp:AVERAGE",
			"LINE2:inPktsIp#FF0000:Paquetes IPv4 de entrada")

	ret3 = rrdtool.graph( nombre + "_ICMPecho.png",
			"--start",str(tiempo_inicial),
			"--end","N",
			"--title=Mensajes Echo ICMP enviados",
			"DEF:outEchoesICMP="+nombre+".rrd:outEchoesICMP:AVERAGE",
			"LINE2:outEchoesICMP#FF0000:Echoes de salida")

	ret4 = rrdtool.graph( nombre + "_TCPSeg.png",
			"--start",str(tiempo_inicial),
			"--end","N",
			"--title=Segmentos TCP recibidos",
			"DEF:inSegsTCP="+nombre+".rrd:inSegsTCP:AVERAGE",
			"LINE2:inSegsTCP#FF0000:Segmentos TCP de entrada")

	ret5 = rrdtool.graph( nombre + "_datagrams.png",
			"--start",str(tiempo_inicial),
			"--end","N",
			"--title=Datagramas recibidos",
			"DEF:inDatagrams="+nombre+".rrd:inDatagrams:AVERAGE",
			"LINE2:inDatagrams#FF0000:Datagramas de entrada")




