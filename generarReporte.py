import pdfkit
import getSNMPcopy as getSNMP
from generarXML import getComunidad
import subprocess

def crearReporte(host):
	comunidad = getComunidad(host)
	SO = getSNMP.consultaStringSNMP(comunidad, host,'1.3.6.1.2.1.1.1.0')
	logo = ''
	ubicacion = getSNMP.consultaStringSNMP(comunidad, host,'1.3.6.1.2.1.1.6.0')
	interfaces = getSNMP.consultaSNMP(comunidad, host, '1.3.6.1.2.1.2.1.0')
	systime = getSNMP.consultaSNMP(comunidad, host, '1.3.6.1.2.1.1.3.0')
	if SO.find('Windows') != -1:
		logo = 'windows.PNG'
	else:
		logo = 'linux.png'
	text = '''
	<html>
		<head>
			<title>Reporte</title>
			<style type="text/css">
				.contenedor{
					display:flex;
					flex-direction:column;
					align-items:center;
				}
				.logo {
					width: 200px;
					padding: 1rem;
				}
				.encabezado{
					display:flex;
					justify-content: space-evenly;
					width:50%
				}
				.graficas{
					display:flex;
					flex-direction:column;
					align-items:center;
				}
				.graph{
					width:50%;
				}
			</style>
		</head>
		<body>	<div class = "contenedor">
			<div class = "encabezado">
				<img class="logo" src = \"'''+ logo + '''\">
				<div>
					<h3>'''+SO+'''</h3>
					<p>Ubicacion: '''+ ubicacion+'''</p>
					<p>Numero de interfaces de red: '''+interfaces+'''</p>
					<p>Tiempo desde el ultimo reinicio: '''+systime+'''</p>
					<p>Comunidad: '''+comunidad+'''</p>
					<p>Host:'''+host+'''</p>
				</div>
			</div>
			</div>
			<div class = "graficas">
				<img class = "graph" src = \"/home/aldair/Documents/proyecto1Redes3/'''+host+'''_ucast.PNG\">
				<img class = "graph" src = \"'''+host+'''_pktsIP.PNG\">
				<img class = "graph" src = \"'''+host+'''_ICMPecho.png\">
				<img class = "graph" src = \"'''+host+'''_TCPSeg.png\">
				<img class = "graph" src = \"'''+host+'''_datagrams.png\">
			</div>
		</body>
	</html>'''

	f = open('reporte' + host + '.html', 'w')
	f.write(text)
	options = {
		"enable-local-file-access": ""
	}
	pdfkit.from_file(f,'reporte' + host + '.pdf', options = options)
	subprocess.Popen(['reporte' + host + '.pdf'], shell=True)
	f.close()
