# Reto de Ingeniería de Datos - PRAGMA SAS


Este reto tiene como objetivo evaluar tu capacidad para construir un pipeline de datos que procese y analice información en tiempo real o casi real mediante la ingesta por microbatches.

## Especificaciones del Reto

## Datos:

Seis archivos .CSV con nombres "2012-1.csv", "2012-2.csv", ..., "2012-5.csv" y "validation.csv".
Cada archivo contiene tres campos: timestamp, price, user_id.
Los archivos .CSV están ordenados por hora.

## Requerimientos
1. Descargar la carpeta comprimida con los datos.

2. Construye un Pipeline de Datos:

* Carga todos los archivos .CSV excepto "validation.csv".
* Almacena los datos en una base de datos (PostgreSQL, MySQL, etc.).
* Realiza un seguimiento de:
    * Recuento de filas cargadas.
    *Valor medio, mínimo y máximo del campo "price".
    * Actualiza las estadísticas a medida que se cargan los datos.

3. Comprobación de Resultados:
* Impresión de Estadísticas: Imprime el valor actual de las estadísticas durante la ejecución del pipeline para monitorear el progreso.

* Consultas a la Base de Datos: Ejecuta consultas a la base de datos para obtener:

    * Recuento total de filas cargadas.
    * Valor promedio, mínimo y máximo del campo "price".

* Validación: Ejecuta el archivo "validation.csv" a través del pipeline y muestra el valor actualizado de las estadísticas.

* Consultas Adicionales: Realiza consultas a la base de datos nuevamente después de cargar "validation.csv" para verificar cómo cambian las estadísticas.

## Algunas reglas y consideraciones del reto:
* Puedes utilizar cualquier Framework o librería que desees.
* Puedes utilizar cualquier base de datos que desees, lo importante es  que muestres cómo te conectas a ella, cómo poblas la(s)
* tabla(s) y cómo realizas las consultas.
* Puedes hacer uso de alguna interfaz gráfica para
* administrar/manipular tu base de datos (ejemplo PgAdmin), o
* puedes hacer uso de línea de comandos.
* Puedes usar cualquier código existente que tengas a disposición.
* No hay una forma definida de resolver esta tarea. Queremos ver la forma en la que piensas para resolver un problema así.
* Las estadísticas se pueden almacenar de la forma que desees: en base de datos, en memoria, en un archivo.
* No te preocupes por el rendimiento, el objetivo es una solución funcional.
* Si no logras terminar, no te preocupes, queremos saber hasta dónde puedes llegar

## Entregables
Para este reto, te solicitamos por favor que nos hagas llegar en una carpeta .ZIP, o un enlace a algún repositorio en nube (ejemplo Drive), los siguientes
elementos:
- Notebook o script en donde tengas el pipeline escrito y documentado el  paso a paso.


# Solución propuesta

## Estructura del Proyecto GitHub

├── Dockerfile\
├── LICENSE\
├── LICENSE copy\
├── Makefile\
├── README copy.md\
├── README.md\
├── docs\
│   ├── index.md\
│   └── tutorial.md\
├── pyproject.toml\
├── requirements.txt\
├── scripts\
│   ├── postgres.sql\
│   └── publish.sh\
├── setup.py\
├── src\
│   ├── main.py\
│   ├── modules\
│   │   ├── apis\
│   │   │   ├── __init__.py\
│   │   │   ├── amazon_api\
│   │   │   ├── clockify\
│   │   │   └── google_drive\
│   │   │       ├── __init__.py\
│   │   │       └── googledrive.py\
│   │   └── clouds\
│   │       ├── aws\
│   │       │   └── __init__.py\
│   │       ├── azure\
│   │       │   └── __init__.py\
│   │       └── gcp\
│   │           └── __init__.py\
│   └── support_gcp.py\
└── tests\
    ├── dataset_testing\
    │   ├── 2012-1.csv\
    │   ├── 2012-2.csv\
    │   ├── 2012-3.csv\
    │   ├── 2012-4.csv\
    │   ├── 2012-5.csv\
    │   └── validation.csv\
    ├── integration\
    │   ├── docker-compose.yaml\
    │   ├── model\
    │   ├── run.sh\
    │   └── test_docker.py\
    └── unit\
        └── test_main.py

La estructura de archivos proporcionada para este proyecto cumple con estándares de seguridad y buenas prácticas de desarrollo. Aquí hay una breve descripción destacando algunos aspectos importantes:

- src/main.py: Este archivo contiene el punto de entrada principal de la aplicación. Aquí es donde se inicializan y se ejecutan los diferentes componentes del pipeline de datos.

-  src/modules/: Esta carpeta contiene los diferentes módulos de la aplicación, organizados por funcionalidad. Por ejemplo, en "apis" podrías encontrar los módulos para interactuar con distintas APIs (Amazon, Clockify, Google Drive), mientras que en "clouds" se encuentran los módulos relacionados con los servicios en la nube (AWS, Azure, GCP). Estos módulos están diseñados para ser modularizados y reutilizables, lo que promueve un diseño limpio y mantenible.

-  requirements.txt: Este archivo lista todas las dependencias de Python necesarias para ejecutar la aplicación. Al mantener este archivo actualizado, facilita la replicación del entorno de desarrollo en diferentes máquinas y contribuye a la reproducibilidad del proyecto.

- env: Esta carpeta podría contener configuraciones específicas del entorno, como variables de entorno o archivos de configuración sensibles. Es importante mantener esta información fuera del repositorio para evitar exponer datos sensibles, siguiendo buenas prácticas de seguridad.

-  pre-commit hooks: Se han incluido ganchos pre-commit para evitar la inclusión de datos sensibles en GitHub utilizando ggshield, una herramienta que escanea los cambios antes de realizar un commit para buscar información confidencial. Esto ayuda a proteger la seguridad y privacidad de los datos del proyecto.

- Cumplimiento con PEP8: Se garantiza el cumplimiento de las convenciones de estilo de código de Python (PEP8) utilizando herramientas como pylint, black y isort. Esto asegura que el código sea legible y consistente, facilitando su mantenimiento y colaboración entre desarrolladores. El código se formatea automáticamente utilizando pre-commit hooks para garantizar que cumpla con las convenciones de estilo PEP8 de manera consistente. Esto significa que antes de cada commit, el código se ajusta automáticamente para mantener una estructura limpia y legible.

* Pruebas unitarias: Se incluyen algunas unitarias para garantizar que todas las funciones y componentes del pipeline de datos funcionen correctamente. Estas pruebas ayudan a identificar posibles errores o regresiones durante el desarrollo y a mantener la integridad del código a medida que se realizan modificaciones. Las pruebas unitarias también ayudan a controlar los cambios en el código y a garantizar que nuevas funcionalidades no introduzcan problemas inesperados.

-  En resumen, la estructura del proyecto y las prácticas implementadas contribuyen a la seguridad, el mantenimiento y la colaboración efectiva entre los miembros del equipo.
