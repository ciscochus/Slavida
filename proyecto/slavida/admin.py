from django.contrib import admin

from slavida.models import Usuario, Notificacion, Conversacion, Mensaje, Votacion, Comentario, Perfil, Pensamiento, Diario, Box

admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Perfil)
admin.site.register(Pensamiento)
admin.site.register(Diario)
admin.site.register(Box)
admin.site.register(Votacion)
admin.site.register(Notificacion)
admin.site.register(Conversacion)
admin.site.register(Mensaje)