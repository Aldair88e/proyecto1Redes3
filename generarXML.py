import xml.etree.ElementTree as ET

def agregarAgente(nombre, versionSNMP, comunidad, puerto):
	archivo = ET.parse('agentes.xml')
	agentes = archivo.getroot()
	agente = ET.SubElement(agentes, 'agente')
	n = ET. SubElement(agente, 'nombre')
	v = ET.SubElement(agente, 'version')
	c = ET.SubElement(agente, 'comunidad')
	p = ET.SubElement(agente, 'puerto')
	n.text = nombre
	v.text = versionSNMP
	c.text = comunidad
	p.text = puerto
	elementos = agentes.findall('agente')
	agente.set('id', str(len(elementos)))
	archivo.write('agentes.xml')

def eliminarAgente(id):
	archivo = ET.parse('agentes.xml')
	agentes = archivo.getroot()
	elementos = agentes.findall('agente')
	for i in range(0, len(elementos)):
		if elementos[i].get('id') == str(id):
			agentes.remove(elementos[i])
			elementos.pop(i)
			for i in range(0, len(elementos)):
				elementos[i].set('id', str(i+1))
			archivo.write('agentes.xml')
			return 0
	return -1

def get_Nombres():
	archivo = ET.parse('agentes.xml')
	agentes = archivo.getroot()
	elementos = agentes.findall('agente')
	nombres = []
	for e in elementos:
		nombres.append(e.find('nombre').text)
	return nombres

def getInformacion(indice):
	archivo = ET.parse('agentes.xml')
	agentes = archivo.getroot()
	elementos = agentes.findall('agente')
	for i in range(0, len(elementos)):
		if elementos[i].get('id') == str(indice):
			host = elementos[i].find('nombre').text
			comunidad = elementos[i].find('comunidad').text
			version = elementos[i].find('version').text
			return (host, comunidad, version)
	return ('', '', '')

def getComunidad(nombre):
	archivo = ET.parse('agentes.xml')
	agentes = archivo.getroot()
	elementos = agentes.findall('agente')
	for e in elementos:
		if e.find('nombre').text == nombre:
			return e.find('comunidad').text
	return ''
#agregarAgente('localhost', 'v1', 'comunidadASR', '8080')
#agregarAgente('localhost1', 'v1', 'comunidadASR', '8080')
#agregarAgente('localhost2', 'v1', 'comunidadASR', '8080')
#get_Nombres()
