Sistema Web para la Comunicación y el Desarrollo de Relaciones Interpersonales
=======

Proyecto para la asignatura de IW


Para ejecutar la aplicación
    python manage.py runserver
    
Y entrar desde el navegador en: http://127.0.0.1:8000/


¿Qué podríamos hacer con esta aplicación?
=======
A veces nos gustaría hablar con personas que tenemos a nuestro alrededor,
pero no lo hacemos. Esto puedo deberse a varios motivos: bien porque no
nos fiamos de hablar con personas desconocidas, porque pensemos que el
otro no tiene interés en hablar con nosotros, o simplemente por vergüenza.
Por ello, queremos crear una red social que nos ayude a superar estas
barreras y nos permita interactuar con personas que tengamos cerca, a
nuestro alrededor. 
Cuando estemos interesados en hablar con una persona que tenemos cerca,
podemos visitar su perfil para decidir si queremos interactuar con ella o no.
Si decidimos interactuar con ella pero no queremos hacerlo en persona,
podemos enviarle un comentario e iniciar una conversación.

¿Cómo?
=======
Al abrir la aplicación, ésta detectará a las personas que se ubiquen a
nuestro alrededor. Nos aparecerán en una lista, con su fotografía y
principales datos, así como su posición en el mapa.

¿Para qué nos puede servir?
=======
• Conocer a otras personas (un rato de charla o buscar amigos, etc.)
• Hacer partícipes a los demás de nuestros pensamientos: “Estoy
cansado de las personas que no hacen cola en la parada del autobús”
• Oferta y demanda de servicios: 
– “Doy clases particulares a niños de primaria por 7 euros los
hora”
– “Necesito albañil que me arregle el lavadero”

¿Qué queremos incluir en la aplicación?
=======
En primer lugar, el usuario debe registrarse. Para ello deberá rellenar los
siguientes campos:
• Nombre y apellidos
• Correo electrónico
• Contraseña
• Fecha de nacimiento
• Hombre o mujer
• Aceptación de las condiciones de uso de la aplicación. Deben
aceptar que son mayores de 18 años.
• Dirección particular (guardar también la geolocalización)
Una vez registrado, la aplicación llevará al usuario a rellenar el perfil
obligatoriamente.


Perfil
• ¿Qué es el perfil? Es la información sobre nosotros que
queremos que las demás personas vean al hacer “click” sobre
nuestro icono.
• ¿Qué información incluye el perfil? De la información que
puede incluir el perfil, alguna deberá ser obligatoria y otra
opcional (aquella información que se considere lesiva para el
derecho a la privacidad individual):
a) Nombre o pseudónimo
b) Edad
c) Hombre o mujer
d) Orientación sexual
e) Profesión
f) Estudios
g) Relaciones: con pareja, sin pareja, abierto a conocer
nuevas personas, etc. (esto hay que concretarlo)
h) Creencias religiosas: ateo, agnóstico, cristiano,
musulmán, judío …
i) Intereses o aficiones
j) Otra información de interés a completar por el usuario
• Daremos la opción de crear dos perfiles diferentes, uno
supuestamente verdadero y otro supuestamente falso. Los
sujetos podrán activar el perfil que deseen en cada momento.
Los demás usuarios podrán ver si una persona tiene activado
su perfil verdadero o su perfil falso. Para ello, cuando se esté
usando el perfil verdadero, el icono indicativo del sujeto estará
de color verde, en cambio, cuando se esté usando el perfil
falso, el icono indicativo será de color rojo. El histórico
relacionado con las actividades almacenará en casa caso el
perfil que ha usado el usuario.
• El perfil incluirá un apartado en el que quede reflejada la media
de las puntuaciones en cada una de las características a votar.
Comentarios 
En tiempo real (deseos, intereses, necesidades) disponibles
solamente para aquellas personas que tengamos cerca.


