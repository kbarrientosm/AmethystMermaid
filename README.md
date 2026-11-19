# 💜 AmethystMermaid

<p align="center">
  <strong>Sistema de gestión integral para una tienda de productos espirituales, artesanales y de bienestar.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-6D4A91?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.1.3-9675B7?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Oracle-Database%2019c-B58DAF?style=for-the-badge&logo=oracle&logoColor=white" alt="Oracle">
  <img src="https://img.shields.io/badge/HTML5-CSS3-65C9D0?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5 y CSS3">
</p>

---

## ✧ Descripción del proyecto

AmethystMermaid es una aplicación web desarrollada para gestionar las operaciones administrativas y comerciales de una tienda especializada en productos relacionados con el bienestar, el crecimiento personal y la espiritualidad.

El sistema permite centralizar la información de productos, categorías, clientes, empleados, roles, ventas, facturación y movimientos de inventario mediante una aplicación web conectada a una base de datos Oracle.

El proyecto integra tecnologías de desarrollo web, programación en Python y administración de bases de datos relacionales, utilizando una arquitectura organizada por módulos para facilitar el mantenimiento y la evolución del sistema.

## ✧ Objetivos

- Centralizar la información y las operaciones de la tienda.
- Facilitar la administración de productos y categorías.
- Gestionar clientes, empleados y roles.
- Registrar y administrar ventas y sus respectivos detalles.
- Gestionar la emisión y consulta de facturas.
- Controlar las entradas, salidas y ajustes del inventario.
- Mantener la integridad y consistencia de la información mediante Oracle Database.
- Proporcionar una interfaz web organizada y sencilla de utilizar.

## ✧ Funcionalidades principales

| Módulo | Funcionalidades |
|:---|:---|
| **Productos** | Registro, consulta, actualización y eliminación de productos. |
| **Categorías** | Administración y clasificación de productos. |
| **Clientes** | Registro y administración de información de clientes. |
| **Empleados** | Administración de empleados. |
| **Roles** | Gestión de roles y asociación con empleados. |
| **Ventas** | Registro y administración de operaciones comerciales. |
| **Detalles de ventas** | Gestión de los productos asociados a cada venta. |
| **Facturas** | Registro, consulta y visualización de facturas. |
| **Inventario** | Registro de entradas, salidas y ajustes de existencias. |

## ✧ Tecnologías utilizadas

| Tecnología | Aplicación |
|:---|:---|
| Python | Lenguaje de programación principal. |
| Flask | Framework para el desarrollo web. |
| Oracle Database 19c | Sistema de gestión de bases de datos. |
| PL/SQL | Desarrollo de lógica y objetos de base de datos. |
| HTML5 | Estructura de las páginas web. |
| CSS3 | Diseño y presentación de la interfaz. |
| python-oracledb | Conectividad entre Python y Oracle. |
| Git | Control de versiones. |
| GitHub | Alojamiento y gestión del código fuente. |

## ✧ Arquitectura del sistema

La aplicación utiliza una estructura modular basada en controladores y módulos de acceso a datos.

- **Controllers:** gestionan las rutas y las operaciones solicitadas desde la interfaz web.
- **Database:** contiene los módulos encargados de comunicarse con Oracle Database y ejecutar los procedimientos almacenados.
- **Models:** directorio reservado para la organización de modelos de datos.
- **Templates:** contiene las páginas HTML que conforman la interfaz.
- **Static:** almacena los recursos estáticos, incluyendo las hojas de estilos CSS.

La lógica de las operaciones de base de datos se implementa mediante procedimientos almacenados, invocados desde Python a través de `python-oracledb`.

## ✧ Estructura del proyecto

```text
AmethystMermaid/
│
├── app/
│   ├── controllers/
│   │   ├── productos_controller.py
│   │   ├── categorias_controller.py
│   │   ├── clientes_controller.py
│   │   ├── roles_controller.py
│   │   ├── empleados_controller.py
│   │   ├── ventas_controller.py
│   │   ├── detalle_ventas_controller.py
│   │   ├── facturas_controller.py
│   │   └── movimientos_controller.py
│   │
│   ├── database/
│   │   ├── conexion.py
│   │   ├── productos_db.py
│   │   ├── categorias_db.py
│   │   ├── clientes_db.py
│   │   ├── roles_db.py
│   │   ├── empleados_db.py
│   │   ├── ventas_db.py
│   │   ├── detalle_ventas_db.py
│   │   ├── facturas_db.py
│   │   └── movimientos_db.py
│   │
│   ├── models/
│   │
│   ├── static/
│   │   └── css/
│   │       └── estilos.css
│   │
│   ├── templates/
│   │   ├── categorias/
│   │   ├── clientes/
│   │   ├── detalle_ventas/
│   │   ├── empleados/
│   │   ├── facturas/
│   │   ├── movimientos/
│   │   ├── productos/
│   │   ├── roles/
│   │   ├── ventas/
│   │   └── index.html
│   │
│   └── __init__.py
│
├── config.example.py
├── generar_hashes.py
├── probar_conexion.py
├── probar_crud_productos.py
├── requirements.txt
├── run.py
├── .gitignore
└── README.md
```

## ✧ Componentes de base de datos

La solución utiliza Oracle Database y objetos PL/SQL para implementar la lógica de las operaciones.

Entre los componentes desarrollados se encuentran:

| Objeto PL/SQL | Cantidad |
|:---|:---:|
| Procedimientos almacenados | **45** |
| Vistas | **10** |
| Funciones | **15** |
| Paquetes | **10** |
| Disparadores (Triggers) | **5** |
| Cursores | **15** |

Estos objetos permiten organizar las operaciones de consulta, registro, actualización, eliminación y procesamiento de información dentro de la base de datos.

## ✧ Requisitos del sistema

- Python 3.13.
- Oracle Database 19c.
- Esquema de Oracle configurado con las tablas y los objetos PL/SQL necesarios.
- Acceso al servicio de base de datos Oracle.
- Git (opcional, para control de versiones).

## ✧ Instalación y configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/kbarrientosm/AmethystMermaid.git
```

### 2. Ingresar al directorio

```bash
cd AmethystMermaid
```

### 3. Crear un entorno virtual

```bash
python -m venv .venv
```

### 4. Activar el entorno virtual

En Windows:

```cmd
.venv\Scripts\activate
```

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Configurar las credenciales

Crear una copia del archivo de ejemplo:

```cmd
copy config.example.py config.py
```

Editar `config.py` y establecer los datos correspondientes a la instalación local de Oracle y la clave de seguridad de Flask.

Los parámetros de configuración son:

- `DB_USER`: usuario de Oracle.
- `DB_PASSWORD`: contraseña de Oracle.
- `DB_HOST`: servidor de base de datos.
- `DB_PORT`: puerto de conexión.
- `DB_SERVICE`: nombre del servicio Oracle.
- `SECRET_KEY`: clave de seguridad de Flask.

> **Importante:** el archivo `config.py` contiene información privada y no debe publicarse en GitHub.

### 7. Verificar la conexión con Oracle

Con el entorno virtual activado y la configuración establecida:

```bash
python probar_conexion.py
```

### 8. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible localmente en:

**http://127.0.0.1:5000**

## ✧ Seguridad y configuración

El proyecto mantiene las credenciales de conexión y la clave de seguridad fuera del repositorio mediante el archivo `.gitignore`.

Se proporciona `config.example.py` como plantilla para facilitar la configuración de nuevas instalaciones.

La aplicación utiliza una clave de seguridad de Flask configurada localmente y una conexión centralizada a Oracle Database.

## ✧ Autoría

**Keyla Barrientos**

Proyecto académico de Ingeniería en Sistemas, desarrollado como una solución web para la gestión integral de AmethystMermaid.

---

<p align="center">
  <strong>AmethystMermaid</strong>
  <br>
  <em>Un espacio donde la tecnología y la creatividad se encuentran.</em>
  <br>
  💜 🩵
</p>

<p align="center">
  <a href="https://github.com/kbarrientosm/AmethystMermaid">Ver repositorio en GitHub</a>
</p>
