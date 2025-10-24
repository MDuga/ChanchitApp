# 🐷 ChanchitApp  

**English summary:**  
ChanchitApp is a personal finance web app built with **Django**.  
It allows users to register, log in, and manage their incomes and expenses through a clean and simple interface.  
The project also includes balance queries and visual summaries made with **Bootstrap** and **Chart.js**, tools I explored while developing the app.  

💡 I created ChanchitApp as a learning project to keep improving my skills in Python, Django, and web development — step by step, and with curiosity.

---

## 🇪🇸 Descripción general  

**ChanchitApp** es una aplicación web para el control de finanzas personales, pensada para adolescentes que recién comienzan a gestionar su dinero.  

🎥 **Video explicativo:**  
[Ver en Google Drive](https://drive.google.com/drive/folders/1J9J8RxTstap-e-1TNKBzOKKh7GlNnZ4K?usp=sharing)

---

## ⚙️ Instalación y ejecución  

1. Posicionarse en la carpeta raíz del proyecto.  
2. Crear un entorno virtual e ingresar al mismo.  
3. Instalar dependencias desde `requirements.txt`.  
4. Aplicar migraciones (`python manage.py migrate`).  
5. Ejecutar el servidor (`python manage.py runserver`).  
6. Ingresar en el navegador: [http://localhost:8000/](http://localhost:8000/)

---

## 💻 Funcionalidades principales  

### 🏠 Página principal  
Muestra una vista general con acceso a todas las secciones del sistema mediante:  
- 4 tarjetas superiores: **Ingresos**, **Egresos**, **Consultas**, **Eventos**  
- Menú lateral con las mismas opciones + **About me**

Además, incluye dos tarjetas inferiores:
- **Saldo actual:** muestra distintas imágenes según sea positivo, negativo o cero.  
- **Próximos eventos:** lista del mes con metas de ahorro y mensajes motivacionales.

---

### 👤 Gestión de usuarios  
- Registro mediante correo electrónico, usuario y contraseña.  
- Login y logout con redirección a la página de inicio.  
- Edición de datos y cambio de avatar desde el perfil del usuario.

---

### 💰 Ingresos y egresos  
Formularios para registrar movimientos de dinero, indicando:
- Monto, descripción, fecha y categoría.  
- Moneda única: **pesos uruguayos (UYU)** para simplificar el proceso.  
- CRUD completo (crear, editar, eliminar).  

---

### 📊 Consultas  
Permite consultar movimientos por mes/año o por rango de fechas.  
Muestra:
- Saldo inicial, movimientos ordenados y saldo final.  
- Botones para editar o eliminar cada movimiento.  
- Panel lateral con mini análisis y gráficos:  
  - Ingresos vs egresos  
  - Porcentaje de ahorro  
  - Distribución de gastos  

---

### 📆 Eventos  
Formulario para registrar eventos y metas de ahorro.  
En la vista lateral se muestran calendarios con:
- Eventos del mes actual y siguiente.  
- Meta de ahorro, saldo y faltante.  
- Mensajes motivadores e imágenes dinámicas.  
(Esta información también se muestra en la página de inicio).

---

## 🧩 Tecnologías  
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, Bootstrap  
- **Base de datos:** SQLite  
- **Visualización:** Chart.js  
- **Control de versiones:** Git y GitHub  

---

## 🐷 Autor  
Proyecto educativo desarrollado como parte del aprendizaje en Python y desarrollo web.  
Su objetivo es aplicar buenas prácticas de Django y explorar herramientas visuales y motivacionales para usuarios jóvenes.  



