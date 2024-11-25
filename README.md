# Smart Car Project

Este proyecto es una simulación de un vehículo autónomo en una ciudad inteligente, donde el vehículo debe encontrar a un pasajero y llevarlo a su destino a través de una cuadrícula 10x10. Los diferentes tipos de tráfico en las calles afectan el costo del movimiento y se utilizan algoritmos de búsqueda para resolver este problema.

## Requisitos

### Frontend (Angular)
- Node.js (v14 o superior)
- Angular CLI (`@angular/cli`)

### Backend (Flask)
- Python (3.x)
- Flask
- Flask-CORS

## Estructura del Proyecto

El proyecto está dividido en dos partes principales:
1. **Frontend (Angular)**: Gestiona la interfaz de usuario, mostrando la cuadrícula de la ciudad y los movimientos del vehículo.
2. **Backend (Flask)**: Proporciona la API que ejecuta los algoritmos de búsqueda para encontrar el pasajero y llevarlo a su destino.

## Instalación

### 1. Clonar el Repositorio

Clona el repositorio en tu máquina local:

```bash
git clone https://github.com/NathaMoraHSB/AI_Project
cd tu_repositorio
```

###  2. Configuración del Frontend (Angular)
Instalación de Dependencias
En la carpeta raíz del proyecto, accede al directorio frontend y ejecuta el siguiente comando para instalar las dependencias necesarias:

```bash
cd frontend
npm install
```

Ejecución del Frontend
Una vez que las dependencias están instaladas, puedes iniciar el servidor de desarrollo de Angular:

```bash
ng serve
```
Esto iniciará la aplicación Angular en http://localhost:4200/. Puedes acceder a la interfaz de usuario del proyecto desde un navegador web.

### 3. Configuración del Backend (Flask)

```bash
pip install -r requirements.txt
```

### 4. Iniciar el Backend

```bash
cd src
python app.py
``` 


El servidor se iniciará en http://127.0.0.1:5000/.

### Autores

Nathalia Carolina Mora Arciniegas

**Codigo:** 2413217

Juan Camilo Valencia

**Codigo:** 2259459