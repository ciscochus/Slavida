#encoding:utf-8
from slavida.models import Usuario, Perfil, Pensamiento, Conversacion, Mensaje, Notificacion, Diario, Box, Comentario, Calendario, Votacion
from django.shortcuts import render_to_response, render, redirect
from django.contrib.auth import login, authenticate, logout
from slavida.forms import RegistroInicioForm, Login, EditPerfil, FormPensamiento, FormDiario, FormBox, CrearPerfil, EnviarComentario, FormEvento
from django.contrib.auth.decorators import login_required
import random
from itertools import chain

#Funcion para crear notificaciones
def nueva_notificacion(tipo, usuario1, usuario2):
    notificacionnew=Notificacion()
    notificacionnew.tipo=tipo
    notificacionnew.usuario1=usuario1
    notificacionnew.usuario2=usuario2
    notificacionnew.save()
    usuario1.save()
    usuario2.save()


#Función que reconoce que perfil tiene activado el usuario y lo devuelve
def reconocer_perfil(request): 
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username)
	if usuario.perfilactivado == 'verdadero':
		perfil=Perfil.objects.get(propietario=usuario, veracidad='verdadero')
		print 'ASIGNO EL PERFIL VERDADERO', perfil, 'ea'
	if usuario.perfilactivado == 'falso':
		perfil=Perfil.objects.get(propietario=usuario, veracidad='falso')
		print 'ASIGNO EL PERFIL falso', perfil, 'ea'
	return perfil


@login_required(login_url='/')
def edit_perfil(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	if request.method=='POST':
		formulario=EditPerfil(request.POST, request.FILES,instance=perfil) #Rellena el formulario con los datos del usuario
		request.POST['propietario']=usuario.pk
		request.POST['veracidad']=perfil.veracidad
		if formulario.is_valid():
			print "formulario validooooooooooooo"
			formulario.save()
			return redirect('/principal')
	else:
		formulario=EditPerfil(instance=perfil)
	return render(request,'editperfil.html',{'editperfil':formulario, 'usuario':usuario, 'perfil':perfil})

@login_required(login_url='/')
def completarregistro(request):
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) #Busca el usuario y mete toda la información en user
	existeVerdadero=Perfil.objects.filter(propietario=usuario, veracidad='verdadero')
	existeFalso=Perfil.objects.filter(propietario=usuario, veracidad='falso')
	if existeFalso and existeVerdadero:  #Aqui hacemos el cambio del perfil activado y en el caso de que tenga los dos creados se cambia el perfil
		if usuario.perfilactivado == 'verdadero':
			usuario.perfilactivado='falso'
			usuario.save()
			print "Era el usuario", usuario," y se cambia a falso"
			return redirect('/principal')
		if usuario.perfilactivado == 'falso':
			usuario.perfilactivado='verdadero'
			usuario.save()
			print "Era el usuario", usuario," y se cambia a verdadero"
			return redirect('/principal') 

	if request.method=='POST':
		if request.POST['valor']=='verdadero':
			formulario=CrearPerfil(request.POST, request.FILES) #Rellena el formulario con los datos del usuario
			request.POST['propietario']=usuario.pk
			request.POST['veracidad']='verdadero'
			if formulario.is_valid():
				formulario.save()
				usuario.perfilactivado='verdadero' #Activo el perfil verdadero al usuario
				usuario.save()
				perfil=reconocer_perfil(request) #Aqui asignamos la localizacion al perfil cuando se loguea
				if request.POST['latitud']:
					lat1=float(request.POST['latitud'])
				else:
					lat1=float(0)

				if request.POST['longitud']:
					log1=float(request.POST['longitud'])
				else:
					log1=float(0)
				perfil.latitud=lat1
				perfil.longitud=log1
				perfil.save()
				return redirect('/principal')
		if request.POST['valor']=='falso':
			formulario=CrearPerfil(request.POST, request.FILES) #Rellena el formulario con los datos del usuario
			request.POST['propietario']=usuario.pk
			request.POST['veracidad']='falso'
			if formulario.is_valid():
				formulario.save()
				usuario.perfilactivado='falso' #Activo el perfil falso tras hacerlo
				usuario.save()
				perfil=reconocer_perfil(request) #Aqui asignamos la localizacion al perfil cuando se loguea
				lat=float(request.POST['latitud'])
				log=float(request.POST['longitud'])
				perfil.latitud=lat
				perfil.longitud=log
				perfil.save()
				return redirect('/principal')
	else:
		formulario=CrearPerfil()
	return render(request,'completarregistro.html',{'formperfil':formulario, 'usuariocompleto':usuario, 'existeVerdadero':existeVerdadero, 'existeFalso':existeFalso})

def inicio(request):
	usuario=None #No existe usuario logueado, sirve para que la plantilla base de la barra sin loguearse
	if not request.user.is_anonymous():
		return redirect('/principal')
	if request.method=='POST':
		loginuser=Login(request.POST)
		newuser=RegistroInicioForm(request.POST)
	  	if request.POST['valor']=='registro':
		  	request.POST['username']=request.POST['email']
		  	if newuser.is_valid():
			    newuser.save()
			    usuario=request.POST.get('username', True)
			    clave=request.POST.get('password1', True)
			    acceso=authenticate(username=usuario,password=clave)
			    if acceso is not None:
					if acceso.is_active:
						login(request, acceso)
						return redirect('/completarregistro/')
					else:
						return render(request,'noactivo.html')
			    else:
					return render(request,'nousuario.html')
		if request.POST['valor']=='login':
			if loginuser.is_valid:
				usuario=request.POST['username']
				clave=request.POST['password']
				acceso=authenticate(username=usuario,password=clave)
				if acceso is not None:
					if acceso.is_active:
						login(request, acceso)
						perfil=reconocer_perfil(request) #Aqui asignamos la localizacion al perfil cuando se loguea
						if request.POST['latitud']:
							lat=float(request.POST['latitud'])
						else:
							lat=float(0)

						if request.POST['longitud']:
							log=float(request.POST['longitud'])
						else:
							log=float(0)

						perfil.latitud=lat
						perfil.longitud=log
						perfil.save()
						return redirect('/principal')
					else:
						return render(request,'noactivo.html')
				else:
						return render(request,'nousuario.html')
	else:
		newuser=RegistroInicioForm()
		loginuser=Login()
	return render(request,'index.html',{'newuser':newuser, 'usuario':usuario,'loginuser':loginuser})

@login_required(login_url='/')
def cerrar_sesion(request):
  logout(request)
  return redirect('/')

@login_required(login_url='/')
def perfil(request, user):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	usuarioperfil=Perfil.objects.get(username=user) #Busca el usuario del perfil
	numVotos=usuarioperfil.votos_recibidos.count()
	pensamientos=usuarioperfil.pensamientos.all()
	listacomentarios=usuarioperfil.comentarios.all()
	listacomentarios2=listacomentarios.filter(privado=0)
	comentariosordenados=listacomentarios2.order_by('-fecha')
	#CALCULAR MEDIA DE VOTACIONES
	mediasimpatia=0
	mediaatraccion=0
	votosatraccion=0
	votossimpatia=0
	isVotadoSimpatia=Votacion.objects.filter(votante=perfil, votado=usuarioperfil, tipo='simpatia')
	isVotadoAtraccion=Votacion.objects.filter(votante=perfil, votado=usuarioperfil, tipo='atraccion')
	for x in usuarioperfil.votos_recibidos.all():
		if x.tipo == 'simpatia':
			mediasimpatia=mediasimpatia+x.puntuacion
			votossimpatia=votossimpatia+1
		if x.tipo == 'atraccion':
			mediaatraccion=mediaatraccion+x.puntuacion
			votosatraccion=votosatraccion+1
	if votosatraccion is not 0:
		mediaatraccion=mediaatraccion/votosatraccion
	if votossimpatia is not 0:
		mediasimpatia=mediasimpatia/votossimpatia

	#FIN DE CALCULAR VOTACIONES
	if request.method=='POST':             
		formulariocomentario=EnviarComentario(request.POST, request.FILES)
		request.POST['autor']=perfil.pk
		request.POST['usuario_destino']=usuarioperfil.pk
		print "ENTRAAAAAAAAAAAAAAAAA 0"
		if request.POST['valor']=='comentario':
			if formulariocomentario.is_valid():
				if request.POST['anonimo'].find("0") == 0:  #Esto lo hago xk en el formulario se envia como cadena y aqui le asigno un entero
					request.POST['anonimo']=0
				else:
					request.POST['anonimo']=1

				if request.POST['privado'].find("0") == 0:
					request.POST['privado']=0
				else:
					request.POST['privado']=1
				p=Comentario()
				p.autor=perfil
				p.usuario_destino=usuarioperfil
				p.texto=request.POST['texto']
				p.anonimo=request.POST['anonimo']
				p.privado=request.POST['privado']
				p.save()
				#Aqui creamos las notificaciones de los comentarios
				if request.POST['privado']==1:  
					nueva_notificacion('cop', usuarioperfil, perfil)
				if request.POST['privado']==0:
					nueva_notificacion('co', usuarioperfil, perfil)
				return redirect('/'+ usuarioperfil.username)
			#A partir de aqui se controla las votaciones!!!!
		if request.POST['valor']=='simpatia':
			v=Votacion()
			v.votante=perfil
			v.votado=usuarioperfil
			v.tipo='simpatia'
			v.puntuacion=request.POST['rating']
			v.save()
			nueva_notificacion('vos', usuarioperfil, perfil)
			return redirect('/'+ usuarioperfil.username)
		if request.POST['valor']=='atraccion':
			v=Votacion()
			v.votante=perfil
			v.votado=usuarioperfil
			v.tipo='atraccion'
			v.puntuacion=request.POST['rating']
			v.save()
			nueva_notificacion('voa', usuarioperfil, perfil)
			return redirect('/'+ usuarioperfil.username)
	else:  
		formulariocomentario=EnviarComentario()

	return render(request,'perfil.html',{'isVotadoAtraccion':isVotadoAtraccion,'isVotadoSimpatia':isVotadoSimpatia,'userperfil':usuarioperfil,'mediasimpatia':mediasimpatia,'mediaatraccion':mediaatraccion,'listacomentarios':comentariosordenados, 'formulariocomentario':formulariocomentario, 'usuario':usuario, 'listpensamientos':pensamientos,'numVotos':numVotos, 'perfil':perfil})

@login_required(login_url='/')
def principal(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	archivosperfil=perfil.archivos.all()
	eventos=perfil.eventos.all()
	listnotificaciones=perfil.notificacion.all()
	#COMIENZA LAS FUNCIONES PARA LOS PERFILES CERCANOS, ESTO HAY QUE BUSCAR OTRO ALGORITMO YA QUE ESTE NO LO ORDENA POR CERCANIA, HABRIA QUE HACERLO POR PORCENTJES Y ESO PERO NO TENGO GANAS DE PENSAR
	listaUsuariosCercanos=[]
	for x in Perfil.objects.all():
		if x.propietario != usuario: #Asi no mostramos los demas perfiles de nuestro usuario
			print x.propietario
			print usuario
			if (x.latitud > perfil.latitud and x.latitud < perfil.latitud+0.10) or (x.latitud < perfil.latitud and x.latitud > perfil.latitud-0.10):
				if (x.longitud > perfil.longitud and x.longitud < perfil.longitud+0.10) or (x.longitud < perfil.longitud and x.longitud > perfil.longitud-0.10):
					listaUsuariosCercanos.append(x)
	#ESTO ES LA POLLA, SON LAS 3 DE LA MAÑANA, NO ME PONGAS QUEJAS POR ESTA BASURA DE CÓDIGO
	listaPensamientosCercanos=[]
	for l in listaUsuariosCercanos:
		for i in l.pensamientos.all():
			listaPensamientosCercanos.append(i)

	if request.method=='POST':             
		formulariopensamiento=FormPensamiento(request.POST, request.FILES)
		request.POST['autor']=perfil.pk
		if formulariopensamiento.is_valid():
			p=Pensamiento()
			p.autor=perfil
			p.texto=request.POST['texto']
			p.save()
			return redirect('/principal')
	else:  
		formulariopensamiento=FormPensamiento()

	return render(request,'principal.html',{'eventos':eventos,'listaPensamientosCercanos':listaPensamientosCercanos,'listaUsuariosCercanos':listaUsuariosCercanos,'listnotificaciones':listnotificaciones,'usuario':usuario,'perfil':perfil,'formulariopensamiento':formulariopensamiento,'archivosperfil':archivosperfil})

@login_required(login_url='/')
def diario(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	diarios=perfil.diarios.all()
	if request.method=='POST':             
		formulariodiario=FormDiario(request.POST, request.FILES)
		request.POST['autor']=perfil.pk
		if formulariodiario.is_valid():
			# comprobamos si existe una entrada del diario con la misma fecha, en caso afirmativo
			# el contenido antiguo se sustituye por el actual.
			fecha = request.POST['fecha']
			fecha = str(fecha)
			for x in diarios:
				print "Comparando ",x.fecha," con ",request.POST['fecha']
				if str(x.fecha)==fecha:
					x.autor = perfil
					x.titulo = request.POST['titulo']
					x.contenido = x.contenido + "\n \n" + "======================== \n \n" + request.POST['contenido']
					x.save()
					print "Entrada modificada"
					return redirect('/midiario')

			d=Diario()
			d.autor=perfil
			d.titulo=request.POST['titulo']
			d.fecha=request.POST['fecha']
			print d.fecha
			d.contenido=request.POST['contenido']
			d.save()
			print "Nueva entrada"
			return redirect('/midiario')
	else:  
		formulariodiario=FormDiario()
	return render(request,'diario.html',{'usuario':usuario,'perfil':perfil,'formdiario':formulariodiario, 'listdiarios':diarios})

@login_required(login_url='/')
def edit_diario(request, pk):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	diarios=perfil.diarios.all()
	entrada_diario=perfil.diarios.get(pk=pk)
	print("pk: ",entrada_diario.pk,", titulo: ",entrada_diario.titulo,", fecha: ",entrada_diario.fecha,", contenido: ",entrada_diario.contenido);
	formulariodiario=FormDiario(instance=entrada_diario)
	return render(request,'diario.html',{'usuario':usuario,'formdiario':formulariodiario, 'listdiarios':diarios})

@login_required(login_url='/')
def remove_diario(request, pk):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	diarios=perfil.diarios.all()
	entrada_diario=perfil.diarios.get(pk=pk)
	print "Entrada con pk: ",entrada_diario.pk," ha sido eliminada"
	entrada_diario.delete()
	return redirect('/midiario')
	
@login_required(login_url='/')
def agenda(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) #Busca el usuario y mete toda la información en user
	eventos=perfil.eventos.all()

	if request.method=='POST':
		print "prueba 1"
		formularioevento=FormEvento(request.POST, request.FILES)
		request.POST['autor']=perfil.pk
		if formularioevento.is_valid():
			print "prueba 2"
			e=Calendario()
			e.autor=perfil
			e.titulo=request.POST['titulo']
			e.fecha=request.POST['fecha']
			print e.fecha
			e.descripcion=request.POST['descripcion']
			e.lugar=request.POST['lugar']
			e.save()
			print "Nuevo evento"
			return redirect('/miagenda')

	else:
		print "prueba 3"
		formularioevento=FormEvento()
	return render(request,'agenda.html',{'usuario':usuario, 'formevento':formularioevento, 'listeventos':eventos})

@login_required(login_url='/')
def remove_evento(request, pk):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	eventos=perfil.eventos.all()
	evento_agenda=perfil.eventos.get(pk=pk)
	print "evento con pk: ",evento_agenda.pk," ha sido eliminado"
	evento_agenda.delete()
	return redirect('/miagenda')

@login_required(login_url='/')
def edit_evento(request, pk):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	eventos=perfil.eventos.all()
	evento_agenda=perfil.eventos.get(pk=pk)
	print("pk: ",evento_agenda.pk,", titulo: ",evento_agenda.titulo,", fecha: ",evento_agenda.fecha,", lugar: ",evento_agenda.lugar,", descripcion: ",evento_agenda.descripcion);

	if request.method=='POST':
		print "prueba 1"
		formularioevento=FormEvento(request.POST, request.FILES)
		
		print "prueba 2"
		evento_agenda.autor=perfil
		evento_agenda.titulo=request.POST['titulo']
		evento_agenda.fecha=request.POST['fecha']
		print evento_agenda.fecha
		evento_agenda.descripcion=request.POST['descripcion']
		evento_agenda.lugar=request.POST['lugar']
		evento_agenda.save()
		print "Evento editado"
	
	return redirect('/miagenda')

@login_required(login_url='/')
def vota(request):
	generoelegido=request.GET['genero']
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	usuariosposiblesvotar=Perfil.objects.filter(act_votacion=True, genero=generoelegido) #Solo aparecen usuarios que pueden ser votados y que son del genero de la consulta GET
	aleatorio=random.choice(usuariosposiblesvotar)
	while aleatorio==usuario: #Recogemos al azar un usuario mientras no seamos nosotros mismos (Ojo que si no lo hacemos asi podria quedar en bucle infinito)
	  aleatorio=random.choice(usuariosposiblesvotar)
	return render(request,'vota.html',{'usuario':usuario,'usuarioazar':aleatorio})

@login_required(login_url='/')
def box(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username)
	archivosperfil=perfil.archivos.all() 
	archivos=Box.objects.all()
	if request.method=='POST':             
		formularioarchivo=FormBox(request.POST, request.FILES)
		request.POST['autor']=perfil
		if formularioarchivo.is_valid():
			b=Box()
			b.autor=perfil
			b.nombre_archivo=request.POST['nombre_archivo']
			b.archivo=request.FILES['archivo']
			b.save()
			return redirect('/misarchivos')
	else:  
		formularioarchivo=FormBox()
	return render(request,'box.html',{'usuario':usuario, 'perfil':perfil,'formarchivo':formularioarchivo, 'listarchivos':archivos,'archivosperfil':archivosperfil})

@login_required(login_url='/')
def remove_archivo(request,pk):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username) 
	archivos=Box.objects.all()
	archivo=perfil.archivos.get(pk=pk)
	print "Archivo con pk: ",archivo.pk," ha sido eliminado"
	archivo.delete()
	return redirect('/misarchivos')

@login_required(login_url='/')
def mensajes(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario=Usuario.objects.get(username=usuariologin.username)
	listconversaciones2=Conversacion.objects.all()
	if perfil.usuario1:
		listconversaciones=listconversaciones2.filter(usuario1=perfil.username)
	if perfil.usuario2:
		listconversaciones3=listconversaciones2.filter(usuario2=perfil.username)
		listconversaciones=list(chain(listconversaciones, listconversaciones3))
	return render(request,'mensajes.html',{'usuario':usuario, 'perfil':perfil, 'listconversaciones':listconversaciones})

@login_required(login_url='/')
def conversacion(request):
	perfil=reconocer_perfil(request)#Busca el perfil
	usuariologin=request.user
	usuario2=request.GET['usuario']
	usuarioconversacion=Perfil.objects.get(username=usuario2)
	usuario=Usuario.objects.get(username=usuariologin.username)
	existconversacion=Conversacion.objects.filter(usuario1=usuarioconversacion, usuario2=perfil)
	existconversacion2=Conversacion.objects.filter(usuario2=usuarioconversacion, usuario1=perfil)
	if existconversacion or existconversacion2:
			if existconversacion:
				conversacionfinal=Conversacion.objects.get(usuario1=usuarioconversacion, usuario2=perfil)
				listmensajes=conversacionfinal.mensajes.all()
			if existconversacion2:
				conversacionfinal=Conversacion.objects.get(usuario2=usuarioconversacion, usuario1=perfil)
				listmensajes=conversacionfinal.mensajes.all()
	else:
			c=Conversacion()
			c.usuario1=perfil
			c.usuario2=usuarioconversacion
			c.save()
			listmensajes=c.mensajes.all()
	if request.method=='POST':  
		if request.POST['valor']=='mensaje':
			m=Mensaje()
			m.conversacion=conversacionfinal
			m.usuario=perfil
			m.texto=request.POST['texto']
			m.save()
			return redirect('/conversacion?usuario='+ usuario2)
	return render(request,'conversacion.html',{'usuario':usuario, 'perfil':perfil, 'listmensajes':listmensajes,'conversacion':conversacion})
