from flask import Blueprint, redirect, render_template, request, url_for

from app.db import get_db_connection


main = Blueprint("main", __name__)


@main.get("/")
def inicio():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                i.id,
                i.titulo,
                c.nombre AS categoria,
                i.prioridad,
                i.estado,
                i.tecnico_id,
                solicitante.nombre AS solicitante,
                tecnico.nombre AS tecnico_asignado,
                i.creada_en
            FROM incidencias AS i
            JOIN categorias AS c
                ON i.categoria_id = c.id
            JOIN usuarios AS solicitante
                ON i.solicitante_id = solicitante.id
            LEFT JOIN usuarios AS tecnico
                ON i.tecnico_id = tecnico.id
            ORDER BY i.creada_en DESC, i.id DESC
            """
        )
        incidencias = cursor.fetchall()

        cursor.execute(
            """
            SELECT id, nombre
            FROM categorias
            WHERE activa = 1
            ORDER BY nombre
            """
        )
        categorias = cursor.fetchall()

        cursor.execute(
            """
            SELECT id, nombre
            FROM usuarios
            WHERE rol = 'solicitante' AND activo = 1
            ORDER BY nombre
            """
        )
        solicitantes = cursor.fetchall()

        cursor.execute(
            """
            SELECT id, nombre
            FROM usuarios
            WHERE rol = 'tecnico' AND activo = 1
            ORDER BY nombre
            """
        )
        tecnicos = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template(
        "inicio.html",
        incidencias=incidencias,
        categorias=categorias,
        solicitantes=solicitantes,
        tecnicos=tecnicos,
        creada=request.args.get("creada") == "1",
        error=request.args.get("error") == "datos",
    )


@main.post("/incidencias")
def crear_incidencia():
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    categoria_id = request.form.get("categoria_id", type=int)
    prioridad = request.form.get("prioridad")
    solicitante_id = request.form.get("solicitante_id", type=int)

    prioridades_validas = {"baja", "media", "alta"}

    if (
        not titulo
        or len(titulo) > 150
        or not descripcion
        or categoria_id is None
        or prioridad not in prioridades_validas
        or solicitante_id is None
    ):
        return redirect(url_for("main.inicio", error="datos"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO incidencias (
                titulo,
                descripcion,
                categoria_id,
                prioridad,
                estado,
                solicitante_id,
                tecnico_id
            )
            VALUES (%s, %s, %s, %s, 'abierta', %s, NULL)
            """,
            (titulo, descripcion, categoria_id, prioridad, solicitante_id),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.inicio", creada="1"))


@main.post("/incidencias/<int:incidencia_id>/estado")
def cambiar_estado(incidencia_id):
    nuevo_estado = request.form.get("estado")
    estados_validos = {"abierta", "en_proceso", "resuelta"}

    if nuevo_estado not in estados_validos:
        return redirect(url_for("main.inicio", error="datos"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE incidencias
            SET estado = %s, actualizada_en = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (nuevo_estado, incidencia_id),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.inicio"))


@main.post("/incidencias/<int:incidencia_id>/tecnico")
def asignar_tecnico(incidencia_id):
    tecnico_id = request.form.get("tecnico_id", type=int)

    if tecnico_id is None:
        return redirect(url_for("main.inicio", error="datos"))

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE id = %s AND rol = 'tecnico' AND activo = 1
            """,
            (tecnico_id,),
        )

        if cursor.fetchone() is None:
            return redirect(url_for("main.inicio", error="datos"))

        cursor.execute(
            """
            UPDATE incidencias
            SET tecnico_id = %s, actualizada_en = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (tecnico_id, incidencia_id),
        )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for("main.inicio"))


@main.get("/incidencias/<int:incidencia_id>")
def ver_incidencia(incidencia_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                i.id,
                i.titulo,
                i.descripcion,
                c.nombre AS categoria,
                i.prioridad,
                i.estado,
                solicitante.nombre AS solicitante,
                tecnico.nombre AS tecnico_asignado,
                i.creada_en,
                i.actualizada_en
            FROM incidencias AS i
            JOIN categorias AS c
                ON i.categoria_id = c.id
            JOIN usuarios AS solicitante
                ON i.solicitante_id = solicitante.id
            LEFT JOIN usuarios AS tecnico
                ON i.tecnico_id = tecnico.id
            WHERE i.id = %s
            """,
            (incidencia_id,),
        )
        incidencia = cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

    if incidencia is None:
        return "No se encontró esa incidencia.", 404

    return render_template("detalle.html", incidencia=incidencia)