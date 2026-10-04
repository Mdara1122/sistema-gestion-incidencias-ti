# Sistema de Gestión de Incidencias TI

Proyecto personal de portafolio para registrar, asignar y dar seguimiento a incidencias de soporte de TI.

## Estado

Primera estructura de Flask creada: la aplicación sirve una página HTML con estilos básicos. Todavía falta conectarla a MySQL. El alcance y las decisiones acordadas están en [Requisitos y alcance](docs/requisitos-mvp.md).

## Objetivo

Construir una aplicación web pequeña, pero presentable y explicable en una entrevista de pasantía. El proyecto servirá para practicar análisis de requisitos, modelado de datos, desarrollo web, control de versiones y documentación.

## Alcance inicial propuesto

Una persona usuaria puede reportar incidencias y consultar su estado. Una persona técnica puede revisar las incidencias, asignarlas y actualizar su estado. Flask generará las páginas HTML usando plantillas y MySQL almacenará los datos. El primer incremento se mantendrá pequeño; autenticación y otras funciones avanzadas quedan fuera del MVP.

## Tecnologías acordadas

- Python y Flask
- Plantillas HTML de Flask, con CSS y JavaScript sencillos
- MySQL (administrado visualmente con MySQL Workbench)
- Git y GitHub

## Documentación

- [Requisitos funcionales, no funcionales y alcance del MVP](docs/requisitos-mvp.md)

## Ejecutar localmente

1. Cloná el repositorio y entrá a su carpeta:

   ```powershell
   git clone https://github.com/Mdara1122/sistema-gestion-incidencias-ti.git
   cd sistema-gestion-incidencias-ti
   ```

2. Creá un entorno virtual para mantener las dependencias de este proyecto separadas:

   ```powershell
   python -m venv .venv
   ```

3. Instalá Flask dentro de ese entorno y ejecutá la aplicación:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   .\.venv\Scripts\python.exe run.py
   ```

4. Abrí `http://127.0.0.1:5000` en el navegador.

