import AemetAPI

#Madrid - 28079
#Lleida - 25120

tiempo = AemetAPI.Localidad('28079', '01/10/2013')

print 'Localidad: ', tiempo.get_localidad()
print 'Temp. max:', tiempo.get_temperatura_maxima()
print 'Temp. min:', tiempo.get_temperatura_minima()
