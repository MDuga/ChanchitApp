ChanchitApp es una aplicación web para el control de finanzas personales. 
Está pensado para adolescentes que recién comienzan a gestionar su dinero.

VIDEO EXPLICATIVO: https://drive.google.com/drive/folders/1J9J8RxTstap-e-1TNKBzOKKh7GlNnZ4K?usp=sharing

INSTALACIÓN Y EJECUCIÓN

1) Posicionarse en carpeta raiz
2) Crear un entorno virtual e ingresar al mismo
3) Instalar el archivo requirements.txt
4) Aplicar migraciones
5) Ejecutar el servidor
6) En el navegador ingresar al sitio: http://localhost:8000/

EXPLICATIVA DE LA APLICACIÓN

Página principal: página para presentación de la aplicación. 
Se incluyen las siguientes acciones en la misma:

Registro de usuario: el registro se realiza mediante dirección de correo electrónico, nombre de usuario y contraseña. 
En caso de registro de usuario exitoso se redirecciona a página de inicio.

Login de usuario: el ingreso de usuario se realiza usando dirección de correo registrada y contraseña. 
En caso de login de usuario exitoso se redirecciona a página de inicio.


Página de inicio: a esta página se accede con el usuario logueado.
El usuario se puede visualizar en la esquina superior derecha de la página.
Haciendo click en el usuario se puede acceder a la edición de los datos de usuario, donde se puede cambiar el avatar. 
Al lado del mismo se incluye un botón para cerrar sesión.

En la página de inicio Se muestran 4 tarjetas superiores desde donde se puede acceder a las diferentes acciones: 
- ingresos 
- egresos 
- consultas 
- eventos.
A estas acciones también se puede acceder mediante un menú fijo a la izquierda de la pantalla en donde se agrega al listado el acceso al About me.

En la parte inferior se muestran 2 tarjetas:
- saldo
- próximos eventos

En la tarjeta izquierda se muestra el saldo a la fecha, mostrándose diferentes imágenes según el saldo (saldo positivo, negativo o cero).
En la tarjeta derecha se muestran los eventos agendados para el mes corriente, indicando el monto deseado de ahorro para los mismos y el estado. También se agerga un mensaje / imagen relacionada al cumplimiento o no de la meta de ahorro establecida para ese mes.

Las acciones se describen a continuación: 
Ingresos: 
Formulario para el registro de ingresos, requiriendo ingresar el monto, la descripción y la fecha de ingreso. Esta fecha será utilizada posteriormente para “Consultas”.
En esta etapa se estableció el uso de una única moneda (pesos uruguayos - UYU) para simplificar el proceso.

EGRESOS:
Formulario para el registro de egresos (salidas), requiriendo ingresar el monto, la descripción y la f echa de egreso. Esta fecha será utilizada posteriormente para “Consultas”.
En esta etapa se estableció el uso de una única moneda (pesos uruguayos - UYU) para simplificar el proceso.

CONSULTAS:
Formulario para hacer consultas de movimientos en un mes/año específico o en un período establecido. 
Se muestra el saldo al inicio del período consultado, los movimientos (ingresos / egresos) ordenados por fecha y el saldo al finalizar ese período.
En cada una de las líneas de los movimientos se encuentran botones que permiten editar o eliminar movimientos (previa confirmación).
En esta página se muestra a la derecha un mini- análisis de los datos del período, donde se muestran los siguientes gráficos:
- ingresos vs egresos
- % Ahorro
- Distribución de gastos

EVENTOS:
Formulario para registrar eventos  y establecer un monto estimado de ahorro para el mismo.
Del lado derecho de la página se muestran los eventos para el mes actual y siguiente en los calendarios.
Para el mes actual se muestra el monto total deseado de ahorro (meta), el saldo actual y el faltante (en caso de haber). También se muestra un mensaje motivador / imagen para el usuario. Etsa información se muestra también en la pçagina de inicio.


