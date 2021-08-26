import Aemet
import time

#Madrid - 28079
#Lleida - 25120

tiempo = Aemet.Localidad('28079', time.strftime("%d/%m/%Y"))

print('Localidad: ', tiempo.get_localidad())
print('Temp. max:', tiempo.get_temperatura_maxima())
print('Temp. min:', tiempo.get_temperatura_minima())
