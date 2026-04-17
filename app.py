from pathlib import Path
from datetime import datetime, timedelta
import uuid
from functools import wraps
from database import get_connection

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
    guardar_conversacion_chatbot,  # ✅ ARREGLADO
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


# ========================
# UTILIDADES
# ========================

def _extraer_token_autorizacion():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def _to_float(value, default=0.0):
    try:
        return float(value)
    except:
        return default


def _normalize_records(records):
    return [
        {**r, "cantidad": _to_float(r.get("cantidad"))}
        for r in records
    ]


def _normalize_preferencias(prefs):
    return {
        **prefs,
        "ingresos_mensuales": _to_float(prefs.get("ingresos_mensuales")),
        "meta_ahorro_mensual": _to_float(prefs.get("meta_ahorro_mensual")),
    }


# ========================
# AUTH
# ========================

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = _extraer_token_autorizacion()
        if not token:
            return jsonify({"error": "Token no proporcionado"}), 401

        sesion = obtener_sesion(token)
        if not sesion:
            return jsonify({"error": "Sesión inválida"}), 401

        usuario = obtener_usuario_por_id(sesion["usuario_id"])
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        g.usuario_id = usuario["id"]
        g.usuario = usuario
        g.auth_token = token

        return f(*args, **kwargs)
    return wrapper


# ========================
# REGISTER (IMPORTANTE)
# ========================

@app.post("/api/register")
def register():
    data = request.get_json() or {}

    nombre = data.get("nombre", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400

    if len(password) < 6:
        return jsonify({"error": "Mínimo 6 caracteres"}), 400

    try:
        # Validar si ya existe
        if obtener_usuario_por_email(email):
            return jsonify({"error": "Correo ya registrado"}), 400

        usuario_id = crear_usuario(nombre, email, password)

        if not usuario_id:
            return jsonify({"error": "No se pudo crear el usuario"}), 500

        return jsonify({
            "message": "Usuario creado",
            "id": usuario_id
        }), 201

    except Exception as e:
        print("🔥 ERROR EN REGISTER:", e)
        return jsonify({"error": str(e)}), 500


# ========================
# LOGIN
# ========================

@app.post("/api/login")
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    usuario = verificar_usuario(email, password)

    if not usuario:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = str(uuid.uuid4())
    crear_sesion(usuario["id"], token, datetime.now() + timedelta(days=7))

    return jsonify({"token": token, "usuario": usuario})


# ========================
# TEST
# ========================

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


# ========================
# HOME
# ========================

@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# ========================
# MAIN
# ========================

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ MYSQL CONECTADO")
        conn.close()
    except Exception as e:
        print("❌ ERROR MYSQL:", e)

    app.run(host="0.0.0.0", port=5000)


from flask import redirect, url_for

@app.route("/")
def index():
    return redirect(url_for("login"))
