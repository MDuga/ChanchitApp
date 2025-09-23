ChanchitApp es una aplicación web para el control de finanzas personales. 
Está pensado para adolescentes que recién comienzan a gestionar su dinero.

En esta etapa no se incluyen las funcionalidades completas de gestión de usuarios incluidas en Django.

INSTALACIÓN Y EJECUCIÓN

1) Posicionarse en carpeta raiz
2) Crear un entorno virtual e ingresar al mismo
3) Instalar el archivo requirements.txt
4) Aplicar migraciones
5) Ejecutar el servidor
6) En el navegador ingresar al sitio: http://localhost:8000/

DATOS: Tiene cargado el usuario mariana@1234.com

EXPLICATIVA DE LA APLICACIÓN

Página principal: página para presentación de la aplicación. 
Se incluyen las siguientes acciones en la misma:

Registro de usuario: el registro se realiza mediante dirección de correo electrónico. En esta etapa se define un nombre de usuario en la aplicación y contraseña.
Se incluye verificación de unicidad de email y nombre de usuario así como la confirmación de contraseña al establecerla.
En caso de registro de usuario exitoso se redirecciona a página de inicio.

Login de usuario: el ingreso de usuario se realiza únicamente mediante el ingreso de dirección de correo registrada. En esta etapa no se incluyó la verificación de la contraseña.
En caso de login de usuario exitoso se redirecciona a página de inicio.


Página de inicio: a esta página se accede con el usuario logueado.
El usuario se puede visualizar en la esquina superior derecha de la página. Al lado del mismo se incluye un botón para cerrar sesión (cuya acción es redirigir a la página principal).
La misma muestran tarjetas desde dónde se pueden elegir diferentes acciones: ingresos, egresos y consultas.
A estas acciones también se puede acceder mediante un menú fijo a la izquierda de la pantalla.

En una tarjeta en la parte inferior de la pantalla se muestra el saldo a la fecha, mostrándose diferentes imágenes según el saldo (saldo positivo, negativo o cero).

Las acciones se describen a continuación: 
Ingresos: formulario para el registro de ingresos, requiriendo ingresar el monto, la descripción y la fecha de ingreso. Esta fecha será utilizada posteriormente para “Consultas”.
En esta etapa se estableció el uso de una única moneda (pesos uruguayos - UYU) para simplificar el proceso.

Egresos: formulario para el registro de egresos (salidas), requiriendo ingresar el monto, la descripción y la fecha de egreso. Esta fecha será utilizada posteriormente para “Consultas”.
En esta etapa se estableció el uso de una única moneda (pesos uruguayos - UYU) para simplificar el proceso.

Consultas: formulario para hacer consultas de movimientos en un mes/año específico. Se muestra el saldo al inicio del mes a consultar, los movimientos (ingresos / egresos) ordenados por fecha y el saldo al finalizar ese período.
