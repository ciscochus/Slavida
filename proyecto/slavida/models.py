# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

OPVERACIDAD=(
	('falso','FALSO'), 
	('verdadero','VERDADERO'), 
)

# El model Usuario hereda de la clase Usuario de Django añadiendo algunos campos más, por ejemplo username, last_name, email, password, etc
class Usuario(User):
	SEXO=(
		('hombre','HOMBRE'), #El usuario tiene el perfil falso
		('mujer','MUJER'), #El usuario tiene el perfil verdadero
	)
	genero=models.CharField(max_length=10,choices=SEXO)
	perfilactivado=models.CharField(max_length=10,choices=OPVERACIDAD) #Campo de tipo char donde solo tiene dos posiblidades a elegir
	nacimiento=models.DateField()
	def __unicode__(self):
		return unicode(self.username) #Esto sirve para devolver por defecto en admin el campo username para representar al Usuario


class Perfil(models.Model):
	RELIGION=(
		('cristiana','CRISTIANA'), 
		('budista','BUDISTA'), 
		('ateo','ATEO'),
		('musulman','MUSULMÁN'),
		('judio','JUDIO'),
		('agnostico','AGNOSTICO'),
	)
	ORIENTACION=(
		('heterosexual','HETEROSEXUAL'), 
		('homosexual','HOMOSEXUAL'), 
		('bisexual','BISEXUAL'),
		('asexual','ASEXUAL'),
	)
	latitud=models.FloatField(blank=True, null=True,max_length=50)#latitud ultima posición
	longitud=models.FloatField(blank=True, null=True,max_length=50)#longitud ultima posición
	propietario=models.ForeignKey('Usuario',related_name='perfiles')
	username=models.CharField(max_length=15, primary_key=True)
	first_name=models.CharField(max_length=15)
	last_name=models.CharField(max_length=15)
	veracidad=models.CharField(max_length=15,choices=OPVERACIDAD)
	orientacion_sex=models.CharField(max_length=15,choices=ORIENTACION, blank=True, null=True) #Orientacion sexual
	religion=models.CharField(max_length=15,choices=RELIGION, blank=True, null=True) #Creencias
	act_votacion=models.BooleanField(default=0) #Este campo sirve para dar la posibilidad si puede ser votado, tipo Booleano, lo hago de diferente manera que vericidad para probar cual es mejor para trabajar
	intereses=models.CharField(max_length=140, blank=True, null=True)
	otros=models.CharField(max_length=140, blank=True, null=True)
	imagen=models.ImageField(upload_to='photos/user', blank=True, null=True, default='photos/defecto.png')
	cabecera=models.ImageField(upload_to='photos/cabecera', blank=True, null=True, default='photos/cabecera.png')
	def __unicode__(self):
		return unicode(self.username) #Esto sirve para devolver por defecto en admin el campo username para representar al Usuario

class Pensamiento(models.Model):
  	autor=models.ForeignKey('Perfil',related_name='pensamientos') #La relación ForeignKey es 1:N El usuario puede tener muchos pensamientos, crea un atributo invisible en Perfil llamado pensamientos
	texto=models.CharField(max_length=200)
	fecha=models.DateTimeField(auto_now=True) #Rellena automaticamente la fecha en la que se crea el pensamiento
	def __unicode__(self):
		return unicode(self.pk)

class Votacion(models.Model):
	TIPO=(
		('simpatia','SIMPATIA'), 
		('atraccion','ATRACCION'), #
	)
  	votante=models.ForeignKey('Perfil',related_name='votos_realizados') #Votos_realizados es la cantidad de votos que ha realizado
	votado=models.ForeignKey('Perfil',related_name='votos_recibidos') 
	tipo=models.CharField(max_length=10,choices=TIPO, blank=True, null=True)
	puntuacion=models.FloatField(default=0,blank=True, null=True)
	def __unicode__(self):
		return unicode(self.pk)

class Notificacion(models.Model):
  	TIPOS=(
  		('re','RE'), #registro
		('co','CO'), #comentario
		('voa','VOA'), #votacion atracción
		('vos','VOS'), #votación simpatía
		('cop','COP'), #comentario privado
	)
	usuario1=models.ForeignKey('Perfil', blank=True, null=True, related_name='notificacion')
	usuario2=models.ForeignKey('Perfil',blank=True, null=True, related_name='notificacion_usuario2')
	tipo=models.CharField(max_length=3,choices=TIPOS)
	fecha=models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return unicode(self.pk)

class Comentario(models.Model):
	anonimo=models.BooleanField(default=0) #Comentario privado o publico
  	autor=models.ForeignKey('Perfil',related_name='comentarios_enviados') #La relación ForeignKey es 1:N El usuario puede tener muchos pensamientos, crea un atributo invisible en Perfil llamado pensamientos
	usuario_destino=models.ForeignKey('Perfil', related_name='comentarios')
	texto=models.CharField(max_length=200)
	fecha=models.DateTimeField(auto_now=True) #Rellena automaticamente la fecha en la que se crea el pensamiento
	privado=models.BooleanField(default=0) #Comentario privado o publico
	def __unicode__(self):
		return unicode(self.pk)

class Diario(models.Model):
  	autor=models.ForeignKey('Perfil',related_name='diarios') #La relación ForeignKey es 1:N El usuario puede tener muchos diarios, crea un atributo invisible en Perfil llamado diarios
	titulo=models.CharField(max_length=100)
	contenido=models.CharField(max_length=500)
	fecha=models.DateField(blank=True, null=True) #Rellena automaticamente la fecha en la que se crea el pensamiento
	def __unicode__(self):
		return unicode(self.pk)

class Calendario(models.Model):
  	autor=models.ForeignKey('Perfil',related_name='eventos') #La relación ForeignKey es 1:N El usuario puede tener muchos diarios, crea un atributo invisible en Perfil llamado diarios
	titulo=models.CharField(max_length=100)
	descripcion=models.CharField(max_length=500)
	fecha=models.DateField(blank=True, null=True)
	lugar=models.CharField(max_length=100)
	def __unicode__(self):
		return unicode(self.pk)

class Box(models.Model):
	autor=models.ForeignKey('Perfil',related_name='archivos')
	nombre_archivo = models.CharField(max_length=100)
	fecha=models.DateTimeField(auto_now=True)
	archivo=models.FileField(upload_to='documents/box')
	def __unicode__(self):
		return unicode(self.pk)

class Conversacion(models.Model):
	usuario1=models.ForeignKey('Perfil',related_name='usuario1')
	usuario2=models.ForeignKey('Perfil',related_name='usuario2')
	def __unicode__(self):
		return unicode(self.pk)

class Mensaje(models.Model):
	conversacion=models.ForeignKey('Conversacion',related_name='mensajes')
	usuario=models.ForeignKey('Perfil',related_name='listamensajes')
	fecha=models.DateTimeField(auto_now=True)
	texto=models.CharField(max_length=200)
	def __unicode__(self):
		return unicode(self.pk)