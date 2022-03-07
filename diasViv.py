import datetime

fechaNacimiento = datetime.datetime(1997, 11, 7)
fechaLim = datetime.datetime(2022, 2, 23)

diferencia = fechaLim - fechaNacimiento

diasVividos = diferencia.days

bloque = (diasVividos % 3) + 1
print('Eres del bloque ' + str(bloque))
