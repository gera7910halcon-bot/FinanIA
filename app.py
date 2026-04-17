from pathlib import Path
from datetime import datetime, timedelta
import uuid
from functools import wraps

from flask import Flask, jsonify, request, send_from_directory, g
from flask_cors import CORS

from database import (
    actualizar_password_por_email,
    actualizar_preferencias,
    calcular_racha,
    crear_ahorro,
    crear_gasto,
    crear_notificacion,
    crear_sesion,
    crear_ticket,
    crear_usuario,
    eliminar_ahorro,
    eliminar_gasto,
    eliminar_sesion,
    eliminar_ticket,
    guardar_conversacion_chatbot,
    marcar_dia_ahorro,
    marcar_notificacion_leida,
    marcar_todas_notificaciones_leidas,
    obtener_ahorros,
    obtener_ahorros_por_mes,
    obtener_estadisticas_mes,
    obtener_gastos,
    obtener_gastos_por_mes,
    obtener_notificaciones,
    obtener_datos_usuario_semanal,
    obtener_estadisticas_globales,
    obtener_estadisticas_usuario_admin,
    obtener_todos_usuarios,
    obtener_usuario_por_email,
    obtener_usuario_por_id,
    obtener_preferencias,
    obtener_sesion,
    obtener_tickets,
    obtener_tickets_por_mes,
    obtener_total_ahorros,
    verificar_usuario,
)
from pdf_generator import generar_reporte_semanal_global_pdf, generar_reporte_usuario_pdf


app = Flask(__name__)
CORS(app)
BASE_DIR = Path(__file__).resolve().parent


def _extraer_token_autorizacion():
    """Extrae token del header Authorization: Bearer <token>."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def _to_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_records(records):
    normalized = []
    for r in records:
        item = dict(r)
        if "cantidad" in item:
            item["cantidad"] = _to_float(item.get("cantidad"))
        normalized.append(item)
    return normalized


def _normalize_preferencias(prefs):
    item = dict(prefs)
    item["ingresos_mensuales"] = _to_float(item.get("ingresos_mensuales"))
    item["meta_ahorro_mensual"] = _to_float(item.get("meta_ahorro_mensual"))
    return item


def _chatbot_respuesta_financiera(usuario_id, mensaje):
    texto = (mensaje or "").lower().strip()
    hoy = datetime.now()
    stats = obtener_estadisticas_mes(usuario_id, hoy.year, hoy.month)
    prefs = _normalize_preferencias(obtener_preferencias(usuario_id))
    ingresos = _to_float(prefs.get("ingresos_mensuales"))
    meta_ahorro = _to_float(prefs.get("meta_ahorro_mensual"))
    total_gastos = _to_float(stats.get("total_mes"))
    total_ahorros = sum(_to_float(a.get("cantidad")) for a in obtener_ahorros_por_mes(usuario_id, hoy.year, hoy.month))
    balance = ingresos - total_gastos + total_ahorros
    porcentaje_gasto = (total_gastos / ingresos * 100) if ingresos > 0 else 0
    avance_meta = (total_ahorros / meta_ahorro * 100) if meta_ahorro > 0 else 0

    categorias = stats.get("gastos_por_categoria", {}) or {}
    cat_top = "sin categoría dominante"
    cat_top_val = 0.0
    if categorias:
        cat_top = max(categorias, key=categorias.get)
        cat_top_val = _to_float(categorias.get(cat_top))

    # Intenciones simples por palabras clave + contexto de datos
    if any(k in texto for k in ["resumen", "estado", "situacion", "cómo voy", "como voy"]):
        return (
            f"Tu resumen del mes: ingresos ${ingresos:.2f}, gastos ${total_gastos:.2f}, "
            f"ahorros ${total_ahorros:.2f}, balance ${balance:.2f}. "
            f"Has usado el {porcentaje_gasto:.1f}% de tus ingresos."
        )

    if any(k in texto for k in ["ahorro", "meta", "ahorrar"]):
        if meta_ahorro <= 0:
            return (
                f"Este mes llevas ${total_ahorros:.2f} ahorrados. "
                "Te recomiendo definir una meta de ahorro mensual en Configuración para medir tu avance."
            )
        restante = max(meta_ahorro - total_ahorros, 0)
        return (
            f"Has ahorrado ${total_ahorros:.2f} de tu meta mensual de ${meta_ahorro:.2f} "
            f"({avance_meta:.1f}% completado). "
            f"Te faltan ${restante:.2f} para cumplirla."
        )

    if any(k in texto for k in ["gasto", "gastos", "categoria", "categoría", "categoria"]):
        return (
            f"Tu gasto acumulado del mes es ${total_gastos:.2f}. "
            f"La categoría con mayor consumo es '{cat_top}' con ${cat_top_val:.2f}. "
            "Si quieres, te doy un plan para reducirla."
        )

    if any(k in texto for k in ["presupuesto", "plan", "organizar"]):
        recomendacion = "alto" if porcentaje_gasto > 85 else "normal"
        return (
            f"Te sugiero presupuesto 50/30/20 adaptado: necesidades 50%, estilo de vida 30%, ahorro 20%. "
            f"Tu nivel actual de gasto va {recomendacion} ({porcentaje_gasto:.1f}% de ingresos)."
        )

    # Respuesta por defecto contextual
    return (
        f"Con tus datos actuales: gastos ${total_gastos:.2f}, ahorros ${total_ahorros:.2f}, balance ${balance:.2f}. "
        "Puedo ayudarte con: 1) plan de ahorro, 2) recorte de gastos por categoría, 3) metas mensuales."
    )


def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = _extraer_token_autorizacion()
        if not token:
            return jsonify({"error": "Token no proporcionado."}), 401

        sesion = obtener_sesion(token)
        if not sesion:
            return jsonify({"error": "Sesión inválida o expirada."}), 401

        usuario = obtener_usuario_por_id(sesion["usuario_id"])
        if not usuario:
            return jsonify({"error": "Usuario no encontrado."}), 404

        g.auth_token = token
        g.usuario_id = usuario["id"]
        g.usuario = usuario
        return f(*args, **kwargs)

    return wrapper


def require_admin(f):
    @wraps(f)
    @require_auth
    def wrapper(*args, **kwargs):
        if not g.usuario.get("es_administrador"):
            return jsonify({"error": "Acceso denegado. Requiere administrador."}), 403
        return f(*args, **kwargs)

    return wrapper


@app.get("/api/health")
def health():
    """Healthcheck simple para verificar servidor en producción."""
    return jsonify({"status": "ok", "service": "FinanIA API"}), 200


@app.post("/api/recuperar-password/reset")
def reset_password_directo():
    """
    Restablece contraseña directamente por email.
    No usa flujo de token ni envío por correo.
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email:
        return jsonify({"error": "El email es obligatorio."}), 400

    if not password or len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres."}), 400

    usuario = obtener_usuario_por_email(email)
    if not usuario:
        return jsonify({"error": "El correo no existe en el sistema."}), 404

    actualizado = actualizar_password_por_email(email, password)
    if not actualizado:
        return jsonify({"error": "No se pudo actualizar la contraseña por un error del servidor."}), 500

    return jsonify({"message": "Contraseña actualizada exitosamente."}), 200


@app.post("/api/recuperar-password")
def recuperar_password_deshabilitado():
    """
    Endpoint legado mantenido por compatibilidad.
    El nuevo flujo no envía código/correo, solo update directo.
    """
    return jsonify(
        {
            "message": (
                "Flujo de recuperación por correo deshabilitado. "
                "Usa /api/recuperar-password/reset con email y password."
            )
        }
    ), 200


@app.post("/api/register")
def register():
    """Registro de usuario."""
    data = request.get_json(silent=True) or {}

    nombre = (data.get("nombre") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    # Validaciones básicas
    if not nombre or not email or not password:
        return jsonify({"error": "Nombre, email y contraseña son obligatorios."}), 400

    if len(password) < 6:
        return jsonify({"error": "La contraseña debe tener al menos 6 caracteres."}), 400

    # 🔥 VALIDACIÓN CLAVE (AQUÍ ESTÁ EL ARREGLO)
    if obtener_usuario_por_email(email):
        return jsonify({"error": "Este correo ya está registrado."}), 400

    # Crear usuario
    usuario_id = crear_usuario(nombre, email, password)

    if not usuario_id:
        return jsonify({"error": "Error real en servidor (ver consola backend)."}), 500

    return jsonify({
        "message": "Usuario creado exitosamente.",
        "usuario_id": usuario_id
    }), 201


@app.post("/api/login")
def login():
    """Inicio de sesión."""
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios."}), 400

    usuario = verificar_usuario(email, password)
    if not usuario:
        return jsonify({"error": "Credenciales incorrectas."}), 401

    token = str(uuid.uuid4())
    fecha_expiracion = datetime.now() + timedelta(days=7)
    crear_sesion(usuario["id"], token, fecha_expiracion)

    return jsonify({"token": token, "usuario": usuario}), 200


@app.post("/api/logout")
@require_auth
def logout():
    """Cerrar sesión actual."""
    eliminar_sesion(g.auth_token)
    return jsonify({"message": "Sesión cerrada."}), 200


@app.get("/api/preferencias")
@require_auth
def get_preferencias():
    return jsonify(_normalize_preferencias(obtener_preferencias(g.usuario_id))), 200


@app.put("/api/preferencias")
@require_auth
def put_preferencias():
    data = request.get_json(silent=True) or {}
    actualizado = actualizar_preferencias(g.usuario_id, **data)
    if not actualizado:
        return jsonify({"error": "No se pudieron actualizar las preferencias."}), 400
    return jsonify({"message": "Preferencias actualizadas."}), 200


@app.get("/api/notificaciones")
@require_auth
def get_notificaciones():
    no_leidas = request.args.get("no_leidas", "false").lower() == "true"
    limite = int(request.args.get("limite", 20))
    return jsonify(obtener_notificaciones(g.usuario_id, no_leidas=no_leidas, limite=limite)), 200


@app.post("/api/notificaciones/<int:notificacion_id>/leida")
@require_auth
def post_notificacion_leida(notificacion_id):
    ok = marcar_notificacion_leida(notificacion_id, g.usuario_id)
    if not ok:
        return jsonify({"error": "No se pudo marcar la notificación."}), 404
    return jsonify({"message": "Notificación marcada como leída."}), 200


@app.post("/api/notificaciones/leer-todas")
@require_auth
def post_notificaciones_leer_todas():
    count = marcar_todas_notificaciones_leidas(g.usuario_id)
    return jsonify({"message": "Notificaciones actualizadas.", "cantidad": count}), 200


@app.post("/api/chatbot")
@require_auth
def post_chatbot():
    data = request.get_json(silent=True) or {}
    mensaje = (data.get("mensaje") or "").strip()
    if not mensaje:
        return jsonify({"error": "Mensaje requerido."}), 400

    respuesta = _chatbot_respuesta_financiera(g.usuario_id, mensaje)
    guardar_conversacion_chatbot(g.usuario_id, mensaje, respuesta)
    return jsonify({"respuesta": respuesta}), 200


@app.post("/api/gastos")
@require_auth
def post_gastos():
    data = request.get_json(silent=True) or {}
    gasto_id = crear_gasto(
        g.usuario_id,
        data.get("descripcion", ""),
        _to_float(data.get("cantidad")),
        data.get("categoria", "General"),
        data.get("fecha") or datetime.now().date().isoformat(),
    )
    if not gasto_id:
        return jsonify({"error": "No se pudo crear el gasto."}), 400
    return jsonify({"id": gasto_id, "message": "Gasto creado."}), 201


@app.get("/api/gastos")
@require_auth
def get_gastos():
    limite = int(request.args.get("limite", 50))
    return jsonify(_normalize_records(obtener_gastos(g.usuario_id, limite=limite))), 200


@app.delete("/api/gastos/<int:gasto_id>")
@require_auth
def delete_gasto(gasto_id):
    ok = eliminar_gasto(gasto_id, g.usuario_id)
    if not ok:
        return jsonify({"error": "Gasto no encontrado."}), 404
    return jsonify({"message": "Gasto eliminado."}), 200


@app.post("/api/tickets")
@require_auth
def post_tickets():
    imagen = request.files.get("imagen")
    imagen_path = ""
    if imagen and imagen.filename:
        uploads_dir = BASE_DIR / "uploads"
        uploads_dir.mkdir(exist_ok=True)
        filename = f"{uuid.uuid4().hex}_{imagen.filename}"
        save_path = uploads_dir / filename
        imagen.save(save_path)
        imagen_path = f"uploads/{filename}"

    ticket_id = crear_ticket(
        g.usuario_id,
        imagen_path,
        request.form.get("descripcion", ""),
        request.form.get("categoria", "General"),
        _to_float(request.form.get("cantidad")),
        request.form.get("fecha") or datetime.now().date().isoformat(),
    )
    if not ticket_id:
        return jsonify({"error": "No se pudo crear el ticket."}), 400
    return jsonify({"id": ticket_id, "message": "Ticket creado."}), 201


@app.get("/api/tickets")
@require_auth
def get_tickets():
    limite = int(request.args.get("limite", 50))
    return jsonify(_normalize_records(obtener_tickets(g.usuario_id, limite=limite))), 200


@app.delete("/api/tickets/<int:ticket_id>")
@require_auth
def delete_ticket(ticket_id):
    ok, _ = eliminar_ticket(ticket_id, g.usuario_id)
    if not ok:
        return jsonify({"error": "Ticket no encontrado."}), 404
    return jsonify({"message": "Ticket eliminado."}), 200


@app.post("/api/ahorros")
@require_auth
def post_ahorros():
    data = request.get_json(silent=True) or {}
    ahorro_id = crear_ahorro(
        g.usuario_id,
        _to_float(data.get("cantidad")),
        data.get("descripcion", ""),
        data.get("fecha") or datetime.now().date().isoformat(),
    )
    if not ahorro_id:
        return jsonify({"error": "No se pudo crear el ahorro."}), 400
    return jsonify({"id": ahorro_id, "message": "Ahorro creado."}), 201


@app.get("/api/ahorros")
@require_auth
def get_ahorros():
    limite = int(request.args.get("limite", 50))
    return jsonify(_normalize_records(obtener_ahorros(g.usuario_id, limite=limite))), 200


@app.get("/api/ahorros/total")
@require_auth
def get_ahorros_total():
    return jsonify({"total": obtener_total_ahorros(g.usuario_id)}), 200


@app.delete("/api/ahorros/<int:ahorro_id>")
@require_auth
def delete_ahorro(ahorro_id):
    ok = eliminar_ahorro(ahorro_id, g.usuario_id)
    if not ok:
        return jsonify({"error": "Ahorro no encontrado."}), 404
    return jsonify({"message": "Ahorro eliminado."}), 200


@app.get("/api/ahorro/racha")
@require_auth
def get_ahorro_racha():
    from database import obtener_dias_ahorro

    dias = obtener_dias_ahorro(g.usuario_id)
    racha = calcular_racha(g.usuario_id)
    return jsonify({"racha": racha, "dias": dias, "dias_totales": len(dias)}), 200


@app.post("/api/ahorro/marcar")
@require_auth
def post_ahorro_marcar():
    data = request.get_json(silent=True) or {}
    fecha = data.get("fecha") or datetime.now().date().isoformat()
    ok = marcar_dia_ahorro(g.usuario_id, fecha)
    if not ok:
        return jsonify({"error": "Ese día ya fue marcado."}), 400
    racha = calcular_racha(g.usuario_id)
    crear_notificacion(g.usuario_id, "Racha de ahorro", f"Has marcado un nuevo día de ahorro. Racha: {racha} días", "success")
    return jsonify({"message": "Día marcado.", "racha": racha}), 200


@app.get("/api/estadisticas")
@require_auth
def get_estadisticas():
    anio = int(request.args.get("año") or request.args.get("anio") or request.args.get("year") or datetime.now().year)
    mes = int(request.args.get("mes") or datetime.now().month)
    return jsonify(obtener_estadisticas_mes(g.usuario_id, anio, mes)), 200


@app.get("/api/analisis/gastos")
@require_auth
def get_analisis_gastos():
    anio = int(request.args.get("año") or request.args.get("anio") or datetime.now().year)
    mes = int(request.args.get("mes") or datetime.now().month)
    stats = obtener_estadisticas_mes(g.usuario_id, anio, mes)
    prefs = obtener_preferencias(g.usuario_id)
    ingresos = _to_float(prefs.get("ingresos_mensuales"))
    total_ahorros = sum(_to_float(a.get("cantidad")) for a in obtener_ahorros(g.usuario_id, limite=200))
    total_gastos = _to_float(stats.get("total_mes"))
    balance = ingresos - total_gastos + total_ahorros
    porcentaje_gastos = (total_gastos / ingresos * 100) if ingresos > 0 else 0
    porcentaje_ahorros = (total_ahorros / ingresos * 100) if ingresos > 0 else 0
    recomendaciones = [
        "Reduce gastos en categorías con mayor consumo.",
        "Mantén un ahorro mensual constante.",
    ]
    return jsonify(
        {
            "ingresos": ingresos,
            "total_gastos": total_gastos,
            "total_ahorros": total_ahorros,
            "balance": balance,
            "cambio_porcentual": 0,
            "recomendaciones": recomendaciones,
            "porcentaje_gastos": porcentaje_gastos,
            "porcentaje_ahorros": porcentaje_ahorros,
            "cantidad_transacciones": stats.get("cantidad_gastos", 0) + stats.get("cantidad_tickets", 0),
        }
    ), 200


@app.get("/api/predicciones")
@require_auth
def get_predicciones():
    hoy = datetime.now()
    stats_actual = obtener_estadisticas_mes(g.usuario_id, hoy.year, hoy.month)
    mes_anterior = hoy.month - 1 or 12
    anio_anterior = hoy.year - 1 if hoy.month == 1 else hoy.year
    stats_prev = obtener_estadisticas_mes(g.usuario_id, anio_anterior, mes_anterior)
    gasto_actual = _to_float(stats_actual.get("total_mes"))
    gasto_prev = _to_float(stats_prev.get("total_mes"))
    cambio = ((gasto_actual - gasto_prev) / gasto_prev * 100) if gasto_prev > 0 else 0
    categorias = stats_actual.get("gastos_por_categoria", {})
    cat_nombre, cat_cantidad = ("General", 0.0)
    if categorias:
        cat_nombre = max(categorias, key=categorias.get)
        cat_cantidad = _to_float(categorias[cat_nombre])
    return jsonify(
        {
            "proyeccion_mes": gasto_actual,
            "recomendacion": "Alto" if cambio > 10 else "Normal",
            "gasto_actual": gasto_actual,
            "gasto_mes_anterior": gasto_prev,
            "cambio_porcentual": cambio,
            "categoria_mayor_gasto": {"nombre": cat_nombre, "cantidad": cat_cantidad},
        }
    ), 200


@app.post("/api/reportes/generar-pdf")
@require_auth
def post_reporte_pdf():
    data = request.get_json(silent=True) or {}
    anio = int(data.get("año") or data.get("anio") or datetime.now().year)
    mes = int(data.get("mes") or datetime.now().month)

    usuario = g.usuario
    gastos = _normalize_records(obtener_gastos_por_mes(g.usuario_id, anio, mes))
    tickets = _normalize_records(obtener_tickets_por_mes(g.usuario_id, anio, mes))
    ahorros = _normalize_records(obtener_ahorros_por_mes(g.usuario_id, anio, mes))
    stats = obtener_estadisticas_mes(g.usuario_id, anio, mes)
    prefs = _normalize_preferencias(obtener_preferencias(g.usuario_id))

    total_gastos = _to_float(stats.get("total_gastos"))
    total_tickets = _to_float(stats.get("total_tickets"))
    total_ahorros = sum(_to_float(a.get("cantidad")) for a in ahorros)
    ingresos = _to_float(prefs.get("ingresos_mensuales"))
    balance = ingresos - total_gastos - total_tickets + total_ahorros

    datos_reporte = {
        "usuario": usuario,
        "fecha_inicio": f"{anio}-{mes:02d}-01",
        "fecha_fin": f"{anio}-{mes:02d}-31",
        "gastos": gastos,
        "tickets": tickets,
        "ahorros": ahorros,
        "total_gastos": total_gastos,
        "total_tickets": total_tickets,
        "total_ahorros": total_ahorros,
        "ingresos_mensuales": ingresos,
        "balance": balance,
        "estadisticas_mes_actual": stats,
    }

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    filename = f"reporte_{g.usuario_id}_{anio}{mes:02d}_{datetime.now().strftime('%H%M%S')}.pdf"
    output = reports_dir / filename

    generar_reporte_usuario_pdf(datos_reporte, str(output))

    return jsonify({"message": "Reporte generado.", "ruta": f"/reports/{filename}"}), 200


@app.get("/api/reports/<path:filename>")
def get_report_file(filename):
    return send_from_directory(BASE_DIR / "reports", filename)


@app.get("/api/admin/usuarios")
@require_admin
def admin_get_usuarios():
    return jsonify(obtener_todos_usuarios()), 200


@app.get("/api/admin/usuario/<int:usuario_id>")
@require_admin
def admin_get_usuario_detalle(usuario_id):
    data = obtener_estadisticas_usuario_admin(usuario_id)
    if not data:
        return jsonify({"error": "Usuario no encontrado."}), 404
    return jsonify(data), 200


@app.get("/api/admin/estadisticas-globales")
@require_admin
def admin_get_estadisticas_globales():
    data = obtener_estadisticas_globales()
    if not data:
        return jsonify({"error": "No se pudieron obtener estadísticas globales."}), 500
    return jsonify(data), 200


@app.post("/api/admin/reporte-semanal-global")
@require_admin
def admin_post_reporte_semanal_global():
    hoy = datetime.now().date()
    fecha_fin = hoy.isoformat()
    fecha_inicio = (hoy - timedelta(days=7)).isoformat()

    stats_global = obtener_estadisticas_globales() or {}
    usuarios = obtener_todos_usuarios()
    usuarios_datos = []
    gastos_periodo = 0.0
    ahorros_periodo = 0.0

    for u in usuarios:
        datos = obtener_datos_usuario_semanal(u["id"], fecha_inicio, fecha_fin)
        if datos:
            usuarios_datos.append(datos)
            gastos_periodo += _to_float(datos.get("total_gastos"))
            ahorros_periodo += _to_float(datos.get("total_ahorros"))

    stats_global["fecha_inicio"] = fecha_inicio
    stats_global["fecha_fin"] = fecha_fin
    stats_global["gastos_periodo"] = gastos_periodo
    stats_global["ahorros_periodo"] = ahorros_periodo

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    filename = f"reporte_semanal_global_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = reports_dir / filename
    generar_reporte_semanal_global_pdf(stats_global, usuarios_datos, str(output))

    return jsonify({"message": "Reporte generado.", "ruta": f"/reports/{filename}"}), 200


@app.post("/api/admin/reporte-usuario/<int:usuario_id>")
@require_admin
def admin_post_reporte_usuario(usuario_id):
    data = request.get_json(silent=True) or {}
    tipo = (data.get("tipo") or "semanal").lower()
    hoy = datetime.now().date()

    if tipo == "mensual":
        fecha_inicio = hoy.replace(day=1).isoformat()
    else:
        fecha_inicio = (hoy - timedelta(days=7)).isoformat()
    fecha_fin = hoy.isoformat()

    datos_usuario = obtener_datos_usuario_semanal(usuario_id, fecha_inicio, fecha_fin)
    if not datos_usuario:
        return jsonify({"error": "No se pudo generar reporte para el usuario."}), 404

    reports_dir = BASE_DIR / "reports"
    reports_dir.mkdir(exist_ok=True)
    filename = f"reporte_usuario_{usuario_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = reports_dir / filename
    generar_reporte_usuario_pdf(datos_usuario, str(output))

    return jsonify({"message": "Reporte generado.", "ruta": f"/reports/{filename}"}), 200


@app.get("/")
def home():
    """Sirve la pagina principal de FinanIA."""
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/<path:filename>")
def archivos_publicos(filename):
    """
    Sirve archivos estaticos del proyecto (html, css, js, imagenes).
    Esto permite abrir login.html, dashboard.html, etc. desde localhost:5000.
    """
    return send_from_directory(BASE_DIR, filename)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
