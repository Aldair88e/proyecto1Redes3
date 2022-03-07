import generarXML as XML
from getSNMPcopy import consultaSNMP, consultaStringSNMP
import subprocess
from os import remove
from CreateRRD import crearBD
from updateRRDcp import update, dump
import multiprocessing
from graphRRDcp import graficar

OIDMIB = '1.3.6.1.2.1.'

def comprobarConectividad(host):
	comando = ['ping', '-c', '1', host]
	response = subprocess.run(comando, capture_output=True)
	if response.returncode == 0:
		return 'UP'
	else:
		return 'DOWN'


def agregarAgente():
	print('Ingrese el host o direccion IP del agente:')
	host = input()
	print('Ingrese la comunidad del agente:')
	comunidad = input()
	print('Ingrese el puerto del agente')
	puerto = input()
	print('Ingrese la version de SNMP del agente')
	version = input()
	crearBD(host)
	XML.agregarAgente(host, version, comunidad, puerto)

def eliminarAgente(nombres, hilos):
	print('Elija uno de los agentes para eliminar:')
	for i in range(0, len(nombres)):
		print(str(i+1) + ' - ' + nombres[i])
	indice = input()
	host, comunidad, version = XML.getInformacion(indice)
	i = 0
	while i < len(hilos) :
		if hilos[i].name == host:
			hilos[i].terminate()
			hilos.pop(i)
			i = len(hilos) + 1
		i = i + 1
	remove(host + '.rrd')
	XML.eliminarAgente(indice)


def imprimirResumen(indice):
	host, comunidad, version = XML.getInformacion(indice)
	conectividad = comprobarConectividad(host)
	print('\n\nAgente ' + str(indice))
	print('Conectividad: ' + conectividad)
	if conectividad == 'UP':
		interfaces = consultaSNMP(comunidad, host, OIDMIB + '2.1.0')
		print( 'Numero de interfaces de red: ' + interfaces + '\n')
		for i in range(0, int(interfaces)):
			oidEstado = OIDMIB + '2.2.1.7.' + str(i+1)
			oidDescr = OIDMIB + '2.2.1.2.' + str(i+1)
			estadoInt = consultaSNMP(comunidad, host, oidEstado)
			descripcion = consultaStringSNMP(comunidad, host, oidDescr)
			estado = ''
			if int(estadoInt) == 1:
				estado = 'UP'
			elif int(estadoInt) == 2:
				estado = 'DOWN'
			elif int(estadoInt) == 3:
				estado = 'TESTING'
			if descripcion[0:2] == '0x':
				descripcion = bytes.fromhex(descripcion[2:]).decode('ASCII')
			print(descripcion)
			print('Estado = ' + estado)
			print()


def revisarHilos(hilos, hosts):
	if len(hilos) < len(hosts):
		for host in hosts:
			flag = False
			i = 0
			while i<len(hilos):
				if host == hilos[i].name:
					flag = True
					i = len(hilos)
				i = i + 1
			if flag == False:
				comunidad = XML.getComunidad(host)
				hilo = multiprocessing.Process(target = update, name = host,
							 args=(host, comunidad), daemon = True)
				hilos.append(hilo)
				hilos[len(hilos)-1].start()
b = True
hilos = []
while(b):
	hosts = XML.get_Nombres()
	print('Total de dispositivos en monitoreo = ' + str(len(hosts)))
	revisarHilos(hilos, hosts)
	for i in range(0, len(hosts)):
		imprimirResumen(i+1)
	print('\nElige una de las siguientes opciones')
	print('1 - Agregar un agente')
	print('2 - Eliminar un agente')
	print('3 - Generar reporte')
	opcion = input()
	if opcion == '1':
		agregarAgente()
	elif opcion == '2':
		eliminarAgente(hosts, hilos)
	elif opcion == '3':
		print('Elige uno de los siguientes agentes para generar su reporte:')
		for i in range(0,len(hosts)):
			print(str(i+1) + '- ' + hosts[i])
		id = int(input())
		graficar(hosts[id-1], 5)
		for host in hosts:
			dump(host)
		b = False
	else:
		b = False
	#b = False



