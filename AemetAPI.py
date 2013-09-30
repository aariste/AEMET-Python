from xml.etree.ElementTree import parse
from xml.etree.ElementTree import XMLParser
import urllib
import datetime
import codecs

class Base:

	def __init__(self, url):
		self.rss = ''
		self.__url = url		
		self.__fecha_de_actualizacion = ''
		self.__localidad = ''
		self.__provincia = ''

		self.precipitacion = []
		self.cota_nieve = []
		self.estado_cielo = []
		self.viento = []
		self.racha = []
		self.temperatura_maxima = 0
		self.temperatura_minima = 0
		self.temperatura_horas = []
		self.sensacion_termica_maxima = 0
		self.sensacion_termica_minima = 0
		self.sensacion_termica = []
		self.humedad_maxima = 0
		self.humedad_minima = 0
		self.humedad = []
		self.uv_max = 0

		self.__load_xml()

	def __load_xml(self):
		self.rss = parse(urllib.urlopen(self.__url)).getroot()

		self.__load_datos_base()

	def __load_datos_base(self):
		self.__fecha_de_actualizacion = self.rss.find('elaborado').text
		self.__localidad = self.rss.find('nombre').text.encode('latin_1')
		self.__provincia = self.rss.find('provincia').text

	'''Parte publica'''
	def get_fecha_actualizacion(self):
		return self.__fecha_de_actualizacion

	def get_localidad(self):
		return self.__localidad

	def get_provincia(self):
		return self.__provincia

	def get_precipitacion(self):
		return self.precipitacion

	def get_cota_nieve(self):
		return self.cota_nieve

	def get_estado_cielo(self):
		return self.estado_cielo

	def get_viento(self):
		return self.viento

	def get_racha(self):
		return self.racha

	def get_temperatura_maxima(self):
		return self.temperatura_maxima

	def get_temperatura_minima(self):
		return self.temperatura_minima
		
	def get_temperatura_horas(self):
		return self.temperatura_horas

	def get_sensacion_termica_maxima(self):
		return self.sensacion_termica_maxima

	def get_sensacion_termica_minima(self):
		return self.sensacion_termica_minima

	def get_sensacion_termica(self):
		return self.sensacion_termica

	def get_humedad_maxima(self):
		return self.humedad_maxima

	def get_humedad_minima(self):
		return self.humedad_minima

	def get_humedad(self):
		return self.humedad

	def get_uv_max(self):
		return self.uv_max

class Localidad(Base):

	def __init__(self, codigo_postal, fecha):
		url = 'http://www.aemet.es/xml/municipios/localidad_' + codigo_postal + '.xml'
		Base.__init__(self, url)		
		self.__load_datos(fecha)

	def __load_datos(self, fecha):
		nodo = self.rss.find("prediccion/dia[@fecha='" + fecha + "']")

		'''Probabilidad de precipitacion'''
		for elem in nodo.findall('prob_precipitacion'):
			self.precipitacion.append([elem.get('periodo'), elem.text])

		'''Cota de nieve'''
		for elem in nodo.findall('cota_nieve_prov'):
			self.cota_nieve.append([elem.get('periodo'), elem.text])
		
		'''Estado'''
		for elem in nodo.findall('estado_cielo'):
			self.estado_cielo.append([elem.get('periodo'), elem.get('descripcion')])

		'''Viento'''
		for elem in nodo.findall('viento'):					
			self.viento.append([elem.get('periodo'), elem.find('direccion').text, elem.find('velocidad').text])

		'''Racha maxima'''
		for elem in nodo.findall('racha_max'):
			self.racha.append([elem.get('periodo'), elem.text])

		'''Temperatura'''
		temperatura_maxima = nodo.find('temperatura/maxima')
		temperatura_minima = nodo.find('temperatura/minima')

		for elem in nodo.findall('temperatura/dato'):
			self.temperatura_horas.append([elem.get('hora'), elem.text])

		'''Sensacion termica'''
		sensacion_termica_maxima = nodo.find('sens_termica/maxima')
		sensacion_termica_minima = nodo.find('sens_termica/minima')

		for elem in nodo.findall('sens_termica/dato'):
			self.sensacion_termica.append([elem.get('hora'), elem.text])

		'''Humedad'''
		humedad_maxima = nodo.find('humedad_relativa/maxima')
		humedad_minima = nodo.find('humedad_relativa/minima')

		for elem in nodo.findall('humedad_relativa/dato'):
			self.humedad.append([elem.get('hora'), elem.text])

		self.uv_max = nodo.find('uv_max').text		
	
	def __obtener_primer_dia(self):
		dia = self.rss.find("prediccion/dia")
		return dia.get('fecha')	

class Helper:
	def __init__(self):
		self.__data = ''

	@staticmethod
	def anadir_dias(self, fecha, dias):
		fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d') + datetime.timedelta(days=dias)
		return fecha.strftime('%Y-%m-%d')