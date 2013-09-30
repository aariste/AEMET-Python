from xml.etree.ElementTree import parse
import urllib
import datetime

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

		self.__load_xml()

	def __load_xml(self):
		self.rss = parse(urllib.urlopen(self.__url)).getroot()

		self.__load_datos_base()		

	def __load_datos_base(self):
		self.__fecha_de_actualizacion = self.rss.find('elaborado').text
		self.__localidad = self.rss.find('nombre').text
		self.__provincia = self.rss.find('provincia').text

	def get_fecha_actualizacion(self):
		return self.__fecha_de_actualizacion

	def get_localidad(self):
		return self.__localidad

	def get_provincia(self):
		return self.__provincia

class Localidad(Base):

	def __init__(self, codigo_postal):
		url = 'http://www.aemet.es/xml/municipios/localidad_' + codigo_postal + '.xml'
		Base.__init__(self, url)

	def a(self):
		a = '2013-09-30'

		return list(self.rss.find("prediccion/dia[@fecha='" + a + "']"))


	def __obtener_primer_dia(self):
		dia = self.rss.find("prediccion/dia")
		return dia.get('fecha')

	def obtener_precipitacion(self, dias):
		primer_dia = self.__obtener_primer_dia()

		fecha = Helper.anadir_dias(self, primer_dia, dias)

		nodo = "prediccion/dia[@fecha='" + fecha + "']/prob_precipitacion"

		for element in self.rss.findall(nodo):
			self.precipitacion.append([element.get('periodo'), element.text])

		return self.precipitacion

	def obtener_cota_nieve(self, dias):
		primer_dia = self.__obtener_primer_dia()

		fecha = Helper.anadir_dias(self, primer_dia, dias)

		nodo = "prediccion/dia[@fecha='" + fecha + "']/cota_nieve_prov"

		for element in self.rss.findall(nodo):
			self.cota_nieve.append([element.get('periodo'), element.text])

		return self.cota_nieve

	def obtener_estado_cielo(self, dias):
		primer_dia = self.__obtener_primer_dia()

		fecha = Helper.anadir_dias(self, primer_dia, dias)

		nodo = "prediccion/dia[@fecha='" + fecha + "']/estado_cielo"

		for element in self.rss.findall(nodo):
			self.estado_cielo.append([element.get('periodo'), element.get('descripcion'), element.text])

		return self.estado_cielo

	def obtener_viento(self, dias):
		direccion = ''
		velocidad = ''

		primer_dia = self.__obtener_primer_dia()

		fecha = Helper.anadir_dias(self, primer_dia, dias)

		nodo = "prediccion/dia[@fecha='" + fecha + "']/viento"

		for element in self.rss.findall(nodo):
			periodo = element.get('periodo')
			
			nodo_direccion = nodo + '/direccion'
			nodo_velocidad = nodo + '/velocidad'

			for el_direccion in element.findall(nodo_direccion):
				direccion = el_direccion.text

			for el_velocidad in element.findall(nodo_velocidad):
				velocidad = el_velocidad.text

			self.viento.append([periodo, direccion, velocidad])

		return self.viento

class Helper:
	def __init__(self):
		self.__data = ''

	@staticmethod
	def anadir_dias(self, fecha, dias):
		fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d') + datetime.timedelta(days=dias)
		return fecha.strftime('%Y-%m-%d')