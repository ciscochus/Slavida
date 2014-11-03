#encoding:utf-8
from django.forms import ModelForm
from django import forms
from slavida.models import Usuario, Perfil, Pensamiento, Diario, Box, Comentario, Calendario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.extras.widgets import SelectDateWidget


class RegistroInicioForm(UserCreationForm):
	first_name=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Escriba su nombre', 'class':'span3'}))
	last_name=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Escriba sus apellidos', 'class':'span3'}))
	email=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Escriba su correo electrónico', 'class':'span3'}))
	password1=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Escribe la contraseña', 'class':'span3'}))
	password2=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña', 'class':'span3'}))
	nacimiento=forms.DateField(required=True, widget=SelectDateWidget(years=range(1930, 2014), attrs={'class': 'span1'}))
	class Meta:
		model=Usuario
		fields=('email','username','first_name','last_name', 'password1','password2','genero','nacimiento')

class CrearPerfil(ModelForm):
	class Meta:
		model=Perfil
		fields=('propietario','username','first_name','last_name','orientacion_sex','veracidad','religion','intereses','otros','imagen','cabecera','act_votacion')

class Login(AuthenticationForm):
	username=forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Escriba su correo electrónico', 'class':'form-control input-lg'}))
	password=forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Escribe la contraseña','class':'form-control input-lg'}))
	class Meta:
		model=Usuario

class EditPerfil(ModelForm):
  	imagen=forms.ImageField(required=False,widget=forms.FileInput(attrs={'title':'Cambiar Imagen'}))
	intereses=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe algunos de tus intereses'}))
	otros=forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Escribe algunos de tus intereses'}))
	class Meta:
		model=Perfil
		fields=('propietario','username','first_name','last_name','orientacion_sex','veracidad','religion','intereses','otros','imagen','cabecera','act_votacion')


class EnviarComentario(ModelForm):
	texto=forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Deja un comentario a esta persona', 'rows':'2','class':'span7'}))
	anonimo=forms.BooleanField(widget=forms.CheckboxInput(attrs={'value':'False'}))
	privado=forms.BooleanField(widget=forms.CheckboxInput(attrs={'value':'False'}))
	class Meta:
		model=Comentario

class FormPensamiento(ModelForm):
	texto=forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': '¿Qué estás pensando?', 'rows':'2','cols':'20'}))
	class Meta:
		model=Pensamiento

class FormDiario(ModelForm):
	contenido=forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Querido diario...', 'class':'span6'}))
	class Meta:
		model=Diario
		fields=('autor','fecha','titulo','contenido')

class FormEvento(ModelForm):
	descripcion=forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Descripcion del evento', 'class':'span4'}))
	fecha=forms.DateInput.input_type="date"
	class Meta:
		model=Calendario

class FormBox(ModelForm):
	nombre_archivo = forms.CharField(label='Nombre del archivo',required=True, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Nombre de archivo'})) #, 'class':'span5'}))
	archivo = forms.FileField(label='Seleccione un archivo', required=True, widget=forms.FileInput(attrs={}))
	class Meta:
		model=Box
		exclude=('autor','fecha')
