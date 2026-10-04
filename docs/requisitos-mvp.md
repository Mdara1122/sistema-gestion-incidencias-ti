# Requisitos y alcance del MVP

**Proyecto:** Sistema de Gestión de Incidencias TI  
**Versión:** 1.0  
**Estado:** requisitos y modelo de datos inicial aprobados; esquema y tablas creados en MySQL Workbench; primera estructura Flask creada

## 1. Propósito

Una aplicación web para que un equipo pequeño registre problemas de TI, pueda priorizarlos y dé seguimiento hasta su resolución. Se plantea como proyecto de portafolio: debe ser fácil de ejecutar y demostrar, y permitir explicar sus decisiones técnicas.

## 2. Actores propuestos

- **Solicitante:** reporta una incidencia y revisa el avance.
- **Técnico:** consulta las incidencias, toma responsabilidad y actualiza su estado.

Para el MVP se usarán usuarios de demostración, seleccionables en los formularios, sin implementar inicio de sesión real. Esta decisión fue acordada.

## 3. Requisitos funcionales propuestos

| ID | Requisito | Criterio de aceptación inicial |
|---|---|---|
| RF-01 | Registrar una incidencia con título, descripción y categoría. | Al guardar datos válidos se crea una incidencia y se muestra su número o identificador. |
| RF-02 | Asignar prioridad a una incidencia. | La incidencia muestra una prioridad entre Baja, Media y Alta. |
| RF-03 | Consultar la lista de incidencias. | La lista muestra identificador, título, prioridad, estado y fecha de creación. |
| RF-04 | Ver el detalle de una incidencia. | El detalle muestra todos los datos registrados y los cambios de estado disponibles. |
| RF-05 | Cambiar el estado de una incidencia. | Un técnico puede moverla entre Abierta, En proceso y Resuelta. |
| RF-06 | Filtrar incidencias por estado. | La lista puede mostrar todas las incidencias o solo las de un estado elegido. |
| RF-07 | Registrar fechas de creación y última actualización. | Las fechas se guardan y aparecen en el detalle. |

Los requisitos describen el comportamiento esperado; los campos y las opciones iniciales de estado y prioridad quedaron definidos en el modelo de datos de la sección 7.

## 4. Requisitos no funcionales propuestos

- **Facilidad de uso:** formularios y mensajes claros; interfaz adaptable a pantallas comunes.
- **Validación:** rechazar campos obligatorios vacíos y mostrar errores comprensibles.
- **Integridad:** guardar incidencias de forma persistente y evitar estados o prioridades fuera de las opciones permitidas.
- **Mantenibilidad:** separar rutas/lógica del servidor, plantillas, archivos estáticos y acceso a datos.
- **Reproducibilidad:** documentar cómo instalar dependencias y ejecutar localmente la aplicación.
- **Seguridad básica:** no insertar datos del usuario sin escapar en las páginas; guardar configuración sensible fuera del código.
- **Alcance de rendimiento:** responder con fluidez para una demostración local y un volumen pequeño de registros; no se fija todavía una meta de carga.

## 5. Alcance del MVP

### Incluye

- Crear incidencias.
- Listar y consultar el detalle.
- Prioridad, categoría, estado y fechas.
- Actualizar estado.
- Filtrar por estado.
- Persistencia en MySQL.
- Interfaz web simple y documentación de ejecución.

### Fuera del MVP

- Inicio de sesión, recuperación de contraseña y permisos robustos.
- Correo y notificaciones en tiempo real.
- Adjuntos, comentarios o historial detallado de auditoría.
- SLA, escalamiento, reportes avanzados y paneles analíticos.
- Despliegue en nube o uso multiempresa.
- API pública separada de la aplicación web.

Se pueden reevaluar después de tener el flujo principal funcionando.

## 6. Estructura inicial prevista

Esta es la estructura inicial acordada para la aplicación. La ruta principal, la plantilla y los estilos básicos ya están creados; se agregarán otras piezas cuando el proyecto las necesite.

```text
incidencias-ti/
├── app/
│   ├── __init__.py       # creación/configuración de Flask
│   ├── routes.py         # páginas y acciones
│   ├── models.py         # acceso y reglas de datos
│   ├── templates/        # HTML
│   └── static/           # CSS y JavaScript
├── tests/                # pruebas del comportamiento
├── instance/             # base de datos local (no se sube a Git)
├── docs/
│   └── requisitos-mvp.md
├── .gitignore
├── requirements.txt
└── README.md
```

## 7. Diseño de datos propuesto

El modelo inicial usa tres tablas. La incidencia guarda quién la reportó y, opcionalmente, qué técnico la atiende. Las referencias entre tablas permiten evitar repetir nombres y conservar datos consistentes.

```text
usuarios (1) ─── (N) incidencias como solicitante
usuarios (1) ─── (N) incidencias como técnico asignado (opcional)
categorias (1) ─── (N) incidencias
```

| Tabla | Campos propuestos | Propósito |
|---|---|---|
| `usuarios` | `id`, `nombre`, `rol`, `activo` | Lista pequeña de solicitantes y técnicos de demostración. No almacena contraseñas porque no habrá inicio de sesión. |
| `categorias` | `id`, `nombre`, `activa` | Opciones de categoría reutilizables, por ejemplo Hardware, Software y Red. |
| `incidencias` | `id`, `titulo`, `descripcion`, `categoria_id`, `prioridad`, `estado`, `solicitante_id`, `tecnico_id` (opcional), `creada_en`, `actualizada_en` | Datos del reporte y su seguimiento. Prioridad y estado tendrán opciones controladas. |

Prioridades iniciales: Baja, Media y Alta. Estados iniciales: Abierta, En proceso y Resuelta. Al asignar un usuario como solicitante, será de rol solicitante; el técnico asignado deberá tener rol técnico.

Las tres tablas (`usuarios`, `categorias`, `incidencias`) ya se crearon correctamente en MySQL Workbench. Se cargaron tres categorías de demostración (Hardware, Software y Red) y cuatro usuarios (dos solicitantes y dos técnicos). Hay una incidencia de demostración: “La impresora no responde”, reportada por Ana Pérez y asignada a Diego Solís. Se eliminaron cuatro filas duplicadas generadas al ejecutar varias veces el mismo `INSERT`.

## 8. Decisiones confirmadas

1. **Base de datos:** acordado usar MySQL y MySQL Workbench. MySQL Server está instalado y el esquema `incidencias_ti` ya existe. La conexión local de este servidor usa el puerto `3307` porque el `3306` ya estaba ocupado. Flask se conectará al servicio MySQL por ese puerto.
2. **Autenticación:** acordado dejar el inicio de sesión fuera del MVP y seleccionar usuarios de demostración.
3. **Interfaz:** acordado usar plantillas HTML de Flask y CSS/JavaScript sencillos. Flask recibirá las solicitudes, consultará o actualizará MySQL y devolverá páginas HTML preparadas; no hace falta una API separada para este MVP.
4. **Modelo de datos:** aprobada la propuesta de tres tablas; `usuarios`, `categorias` e `incidencias` ya están creadas y contienen datos de demostración.
5. **GitHub:** repositorio público `Mdara1122/sistema-gestion-incidencias-ti` creado y conectado.

## 9. Próximo paso

Clonar el repositorio, instalar Flask dentro de un entorno virtual y ejecutar la página localmente. Después conectaremos la aplicación a MySQL.

