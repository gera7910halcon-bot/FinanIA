"""
FinanIA - Módulo de Base de Datos
Maneja todas las operaciones con la base de datos MySQL
"""

import pymysql
from datetime import datetime, timedelta
import hashlib
import json

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'finania',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    """Obtener conexión a la base de datos"""
    return pymysql.connect(**DB_CONFIG)

def hash_password(password):
    """Hashear contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ========== USUARIOS ==========

def crear_usuario(nombre, email, password):
    """Crear nuevo usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Normalizar email
        email = email.strip().lower()

        # Verificar si ya existe el usuario
        cursor.execute(
            "SELECT id FROM usuarios WHERE email = %s",
            (email,)
        )
        existente = cursor.fetchone()

        if existente:
            print("⚠️ El usuario ya existe con ese email")
            cursor.close()
            conn.close()
            return None

        # Hashear contraseña
        password_hash = hash_password(password)

        # Insertar usuario
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
            (nombre, email, password_hash)
        )

        conn.commit()
        usuario_id = cursor.lastrowid

        # Crear preferencias por defecto
        try:
            cursor.execute(
                "INSERT INTO preferencias_usuario (usuario_id) VALUES (%s)",
                (usuario_id,)
            )
            conn.commit()
        except Exception as e:
            print("⚠️ Error creando preferencias (no crítico):", e)

        cursor.close()
        conn.close()

        print(f"✅ Usuario creado correctamente ID: {usuario_id}")
        return usuario_id

    except Exception as e:
        print("🔥 ERROR REAL AL CREAR USUARIO:")
        print(e)  # 👈 AQUÍ verás el problema real
        return None

def verificar_usuario(email, password):
    """Verificar credenciales de usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT id, nombre, email, es_administrador FROM usuarios WHERE email = %s AND password_hash = %s",
            (email, password_hash)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    except Exception as e:
        print(f"Error verificando usuario: {e}")
        return None

def obtener_usuario_por_id(usuario_id):
    """Obtener usuario por ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, email, es_administrador FROM usuarios WHERE id = %s",
            (usuario_id,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None

def obtener_usuario_por_email(email):
    """Obtener usuario por email"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, email, es_administrador FROM usuarios WHERE email = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        return usuario
    except Exception as e:
        print(f"Error obteniendo usuario: {e}")
        return None

def es_administrador(usuario_id):
    """Verificar si un usuario es administrador"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT es_administrador FROM usuarios WHERE id = %s",
            (usuario_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result['es_administrador'] if result else False
    except Exception as e:
        print(f"Error verificando administrador: {e}")
        return False

def obtener_todos_usuarios():
    """Obtener todos los usuarios (solo para administradores)"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, email, es_administrador, fecha_registro FROM usuarios ORDER BY fecha_registro DESC"
        )
        usuarios = cursor.fetchall()
        cursor.close()
        conn.close()
        return usuarios
    except Exception as e:
        print(f"Error obteniendo usuarios: {e}")
        return []

def marcar_como_administrador(usuario_id):
    """Marcar un usuario como administrador"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET es_administrador = TRUE WHERE id = %s",
            (usuario_id,)
        )
        conn.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return actualizado
    except Exception as e:
        print(f"Error marcando como administrador: {e}")
        return False

# ========== SESIONES ==========

def crear_sesion(usuario_id, token, fecha_expiracion):
    """Crear nueva sesión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sesiones (usuario_id, token, fecha_expiracion) VALUES (%s, %s, %s)",
            (usuario_id, token, fecha_expiracion)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando sesión: {e}")

def obtener_sesion(token):
    """Obtener sesión por token"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT usuario_id FROM sesiones WHERE token = %s AND fecha_expiracion > NOW()",
            (token,)
        )
        sesion = cursor.fetchone()
        cursor.close()
        conn.close()
        return sesion
    except Exception as e:
        print(f"Error obteniendo sesión: {e}")
        return None

def eliminar_sesion(token):
    """Eliminar sesión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sesiones WHERE token = %s", (token,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error eliminando sesión: {e}")

# ========== GASTOS ==========

def crear_gasto(usuario_id, descripcion, cantidad, categoria, fecha):
    """Crear nuevo gasto"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO gastos (usuario_id, descripcion, cantidad, categoria, fecha) VALUES (%s, %s, %s, %s, %s)",
            (usuario_id, descripcion, cantidad, categoria, fecha)
        )
        conn.commit()
        gasto_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return gasto_id
    except Exception as e:
        print(f"Error creando gasto: {e}")
        return None

def obtener_gastos(usuario_id, limite=10):
    """Obtener gastos de un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM gastos WHERE usuario_id = %s ORDER BY fecha DESC, timestamp DESC LIMIT %s",
            (usuario_id, limite)
        )
        gastos = cursor.fetchall()
        cursor.close()
        conn.close()
        return gastos
    except Exception as e:
        print(f"Error obteniendo gastos: {e}")
        return []

def obtener_gastos_por_mes(usuario_id, año, mes):
    """Obtener gastos por mes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM gastos WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s ORDER BY fecha DESC",
            (usuario_id, año, mes)
        )
        gastos = cursor.fetchall()
        cursor.close()
        conn.close()
        return gastos
    except Exception as e:
        print(f"Error obteniendo gastos por mes: {e}")
        return []

def eliminar_gasto(gasto_id, usuario_id):
    """Eliminar gasto"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM gastos WHERE id = %s AND usuario_id = %s",
            (gasto_id, usuario_id)
        )
        conn.commit()
        eliminado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return eliminado
    except Exception as e:
        print(f"Error eliminando gasto: {e}")
        return False

# ========== TICKETS ==========

def crear_ticket(usuario_id, imagen_path, descripcion, categoria, cantidad, fecha):
    """Crear nuevo ticket"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (usuario_id, imagen_path, descripcion, categoria, cantidad, fecha) VALUES (%s, %s, %s, %s, %s, %s)",
            (usuario_id, imagen_path, descripcion, categoria, cantidad, fecha)
        )
        conn.commit()
        ticket_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return ticket_id
    except Exception as e:
        print(f"Error creando ticket: {e}")
        return None

def obtener_tickets(usuario_id, limite=10):
    """Obtener tickets de un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tickets WHERE usuario_id = %s ORDER BY fecha DESC, timestamp DESC LIMIT %s",
            (usuario_id, limite)
        )
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return tickets
    except Exception as e:
        print(f"Error obteniendo tickets: {e}")
        return []

def obtener_tickets_por_mes(usuario_id, año, mes):
    """Obtener tickets por mes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tickets WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s ORDER BY fecha DESC",
            (usuario_id, año, mes)
        )
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return tickets
    except Exception as e:
        print(f"Error obteniendo tickets por mes: {e}")
        return []

def eliminar_ticket(ticket_id, usuario_id):
    """Eliminar ticket y retornar ruta de imagen"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT imagen_path FROM tickets WHERE id = %s AND usuario_id = %s",
            (ticket_id, usuario_id)
        )
        ticket = cursor.fetchone()
        if ticket:
            imagen_path = ticket['imagen_path']
            cursor.execute(
                "DELETE FROM tickets WHERE id = %s AND usuario_id = %s",
                (ticket_id, usuario_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True, imagen_path
        cursor.close()
        conn.close()
        return False, None
    except Exception as e:
        print(f"Error eliminando ticket: {e}")
        return False, None

# ========== AHORROS ==========

def crear_ahorro(usuario_id, cantidad, descripcion, fecha):
    """Crear nuevo ahorro"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ahorros (usuario_id, cantidad, descripcion, fecha) VALUES (%s, %s, %s, %s)",
            (usuario_id, cantidad, descripcion, fecha)
        )
        conn.commit()
        ahorro_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return ahorro_id
    except Exception as e:
        print(f"Error creando ahorro: {e}")
        return None

def obtener_ahorros(usuario_id, limite=50):
    """Obtener ahorros de un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ahorros WHERE usuario_id = %s ORDER BY fecha DESC, timestamp DESC LIMIT %s",
            (usuario_id, limite)
        )
        ahorros = cursor.fetchall()
        cursor.close()
        conn.close()
        return ahorros
    except Exception as e:
        print(f"Error obteniendo ahorros: {e}")
        return []

def obtener_ahorros_por_mes(usuario_id, año, mes):
    """Obtener ahorros por mes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM ahorros WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s ORDER BY fecha DESC",
            (usuario_id, año, mes)
        )
        ahorros = cursor.fetchall()
        cursor.close()
        conn.close()
        return ahorros
    except Exception as e:
        print(f"Error obteniendo ahorros por mes: {e}")
        return []

def obtener_total_ahorros(usuario_id):
    """Obtener total de ahorros de un usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total FROM ahorros WHERE usuario_id = %s",
            (usuario_id,)
        )
        result = cursor.fetchone()
        total = float(result['total']) if result else 0.0
        cursor.close()
        conn.close()
        return total
    except Exception as e:
        print(f"Error obteniendo total ahorros: {e}")
        return 0.0

def eliminar_ahorro(ahorro_id, usuario_id):
    """Eliminar ahorro"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM ahorros WHERE id = %s AND usuario_id = %s",
            (ahorro_id, usuario_id)
        )
        conn.commit()
        eliminado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return eliminado
    except Exception as e:
        print(f"Error eliminando ahorro: {e}")
        return False

# ========== RACHA DE AHORRO ==========

def calcular_racha(usuario_id):
    """Calcular racha de días consecutivos de ahorro"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT fecha FROM dias_ahorro WHERE usuario_id = %s ORDER BY fecha DESC",
            (usuario_id,)
        )
        dias = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if not dias:
            return 0
        
        hoy = datetime.now().date()
        racha = 0
        
        # Calcular racha desde hoy hacia atrás
        fecha_esperada = hoy
        for dia in dias:
            fecha_dia = dia['fecha'] if isinstance(dia['fecha'], type(hoy)) else datetime.strptime(str(dia['fecha']), '%Y-%m-%d').date()
            
            if fecha_dia == fecha_esperada:
                racha += 1
                fecha_esperada = fecha_esperada - timedelta(days=1)
            elif fecha_dia < fecha_esperada:
                break
        
        return racha
    except Exception as e:
        print(f"Error calculando racha: {e}")
        return 0

def obtener_dias_ahorro(usuario_id):
    """Obtener lista de días de ahorro"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT fecha FROM dias_ahorro WHERE usuario_id = %s ORDER BY fecha DESC",
            (usuario_id,)
        )
        dias = cursor.fetchall()
        cursor.close()
        conn.close()
        return [str(dia['fecha']) for dia in dias]
    except Exception as e:
        print(f"Error obteniendo días ahorro: {e}")
        return []

def marcar_dia_ahorro(usuario_id, fecha):
    """Marcar día de ahorro"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Verificar si ya está marcado
        cursor.execute(
            "SELECT id FROM dias_ahorro WHERE usuario_id = %s AND fecha = %s",
            (usuario_id, fecha)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False
        
        cursor.execute(
            "INSERT INTO dias_ahorro (usuario_id, fecha) VALUES (%s, %s)",
            (usuario_id, fecha)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error marcando día ahorro: {e}")
        return False

# ========== ESTADÍSTICAS ==========

def obtener_estadisticas_mes(usuario_id, año, mes):
    """Obtener estadísticas del mes"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Gastos
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total, COUNT(*) as cantidad FROM gastos WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s",
            (usuario_id, año, mes)
        )
        gastos_data = cursor.fetchone()
        total_gastos = float(gastos_data['total']) if gastos_data else 0.0
        cantidad_gastos = gastos_data['cantidad'] if gastos_data else 0
        
        # Tickets
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total, COUNT(*) as cantidad FROM tickets WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s",
            (usuario_id, año, mes)
        )
        tickets_data = cursor.fetchone()
        total_tickets = float(tickets_data['total']) if tickets_data else 0.0
        cantidad_tickets = tickets_data['cantidad'] if tickets_data else 0
        
        # Gastos por categoría
        cursor.execute(
            "SELECT categoria, COALESCE(SUM(cantidad), 0) as total FROM gastos WHERE usuario_id = %s AND YEAR(fecha) = %s AND MONTH(fecha) = %s GROUP BY categoria",
            (usuario_id, año, mes)
        )
        categorias = cursor.fetchall()
        gastos_por_categoria = {cat['categoria']: float(cat['total']) for cat in categorias}
        
        cursor.close()
        conn.close()
        
        return {
            'total_gastos': total_gastos,
            'total_tickets': total_tickets,
            'total_mes': total_gastos + total_tickets,
            'cantidad_gastos': cantidad_gastos,
            'cantidad_tickets': cantidad_tickets,
            'gastos_por_categoria': gastos_por_categoria
        }
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return {
            'total_gastos': 0.0,
            'total_tickets': 0.0,
            'total_mes': 0.0,
            'cantidad_gastos': 0,
            'cantidad_tickets': 0,
            'gastos_por_categoria': {}
        }

# ========== NOTIFICACIONES ==========

def crear_notificacion(usuario_id, titulo, mensaje, tipo='info'):
    """Crear notificación"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO notificaciones (usuario_id, titulo, mensaje, tipo) VALUES (%s, %s, %s, %s)",
            (usuario_id, titulo, mensaje, tipo)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando notificación: {e}")

def obtener_notificaciones(usuario_id, no_leidas=False, limite=20):
    """Obtener notificaciones"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if no_leidas:
            cursor.execute(
                "SELECT * FROM notificaciones WHERE usuario_id = %s AND leida = FALSE ORDER BY fecha_creacion DESC LIMIT %s",
                (usuario_id, limite)
            )
        else:
            cursor.execute(
                "SELECT * FROM notificaciones WHERE usuario_id = %s ORDER BY fecha_creacion DESC LIMIT %s",
                (usuario_id, limite)
            )
        notificaciones = cursor.fetchall()
        cursor.close()
        conn.close()
        return notificaciones
    except Exception as e:
        print(f"Error obteniendo notificaciones: {e}")
        return []

def marcar_notificacion_leida(notificacion_id, usuario_id):
    """Marcar notificación como leída"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notificaciones SET leida = TRUE WHERE id = %s AND usuario_id = %s",
            (notificacion_id, usuario_id)
        )
        conn.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return actualizado
    except Exception as e:
        print(f"Error marcando notificación: {e}")
        return False

def marcar_todas_notificaciones_leidas(usuario_id):
    """Marcar todas las notificaciones como leídas"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE notificaciones SET leida = TRUE WHERE usuario_id = %s AND leida = FALSE",
            (usuario_id,)
        )
        conn.commit()
        count = cursor.rowcount
        cursor.close()
        conn.close()
        return count
    except Exception as e:
        print(f"Error marcando notificaciones: {e}")
        return 0

# ========== PREFERENCIAS ==========

def obtener_preferencias(usuario_id):
    """Obtener preferencias del usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM preferencias_usuario WHERE usuario_id = %s",
            (usuario_id,)
        )
        prefs = cursor.fetchone()
        if not prefs:
            # Crear preferencias por defecto
            cursor.execute(
                "INSERT INTO preferencias_usuario (usuario_id) VALUES (%s)",
                (usuario_id,)
            )
            conn.commit()
            cursor.execute(
                "SELECT * FROM preferencias_usuario WHERE usuario_id = %s",
                (usuario_id,)
            )
            prefs = cursor.fetchone()
        cursor.close()
        conn.close()
        return prefs
    except Exception as e:
        print(f"Error obteniendo preferencias: {e}")
        return {
            'color_primario': '#004481',
            'color_secundario': '#ffd100',
            'notificaciones_email': True,
            'notificaciones_push': True,
            'meta_ahorro_mensual': 0.0,
            'ingresos_mensuales': 5000.0
        }

def actualizar_preferencias(usuario_id, **kwargs):
    """Actualizar preferencias"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        campos_permitidos = ['color_primario', 'color_secundario', 'notificaciones_email', 
                            'notificaciones_push', 'meta_ahorro_mensual', 'ingresos_mensuales']
        
        updates = []
        values = []

        ingresos_mensuales = kwargs.get('ingresos_mensuales')
        meta_ahorro_mensual = kwargs.get('meta_ahorro_mensual')

        # Validaciones de negocio para evitar datos inconsistentes
        if ingresos_mensuales is not None:
            ingresos_mensuales = float(ingresos_mensuales)
            if ingresos_mensuales < 0:
                cursor.close()
                conn.close()
                return False

        if meta_ahorro_mensual is not None:
            meta_ahorro_mensual = float(meta_ahorro_mensual)
            if meta_ahorro_mensual < 0:
                cursor.close()
                conn.close()
                return False

        if ingresos_mensuales is not None and meta_ahorro_mensual is not None:
            if meta_ahorro_mensual > ingresos_mensuales:
                cursor.close()
                conn.close()
                return False

        for campo, valor in kwargs.items():
            if campo in campos_permitidos:
                updates.append(f"{campo} = %s")
                values.append(valor)
        
        if not updates:
            cursor.close()
            conn.close()
            return False
        
        values.append(usuario_id)
        query = f"UPDATE preferencias_usuario SET {', '.join(updates)} WHERE usuario_id = %s"
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error actualizando preferencias: {e}")
        return False

# ========== RECUPERACIÓN DE CONTRASEÑA ==========

def crear_token_recuperacion(usuario_id, token, fecha_expiracion):
    """Crear token de recuperación"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tokens_recuperacion (usuario_id, token, fecha_expiracion) VALUES (%s, %s, %s)",
            (usuario_id, token, fecha_expiracion)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error creando token recuperación: {e}")

def obtener_token_recuperacion(token):
    """Obtener token de recuperación"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tokens_recuperacion WHERE token = %s AND usado = FALSE AND fecha_expiracion > NOW()",
            (token,)
        )
        token_data = cursor.fetchone()
        cursor.close()
        conn.close()
        return token_data
    except Exception as e:
        print(f"Error obteniendo token: {e}")
        return None

def marcar_token_usado(token):
    """Marcar token como usado"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tokens_recuperacion SET usado = TRUE WHERE token = %s",
            (token,)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error marcando token: {e}")

def actualizar_password(usuario_id, nueva_password):
    """Actualizar contraseña"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        password_hash = hash_password(nueva_password)
        cursor.execute(
            "UPDATE usuarios SET password_hash = %s WHERE id = %s",
            (password_hash, usuario_id)
        )
        conn.commit()
        actualizado = cursor.rowcount > 0
        cursor.close()
        conn.close()
        return actualizado
    except Exception as e:
        print(f"Error actualizando password: {e}")
        return False

def actualizar_password_por_email(email, nueva_password):
    """Actualizar contraseña directamente por email"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM usuarios WHERE email = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        if not usuario:
            cursor.close()
            conn.close()
            return False

        password_hash = hash_password(nueva_password)
        if usuario['password_hash'] == password_hash:
            cursor.close()
            conn.close()
            return True

        cursor.execute(
            "UPDATE usuarios SET password_hash = %s WHERE email = %s",
            (password_hash, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error actualizando password por email: {e}")
        return False

# ========== CHATBOT ==========

def guardar_conversacion_chatbot(usuario_id, mensaje_usuario, respuesta_bot):
    """Guardar conversación del chatbot"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversaciones_chatbot (usuario_id, mensaje_usuario, respuesta_bot) VALUES (%s, %s, %s)",
            (usuario_id, mensaje_usuario, respuesta_bot)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error guardando conversación: {e}")

def obtener_historial_chatbot(usuario_id, limite=20):
    """Obtener historial de chatbot"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM conversaciones_chatbot WHERE usuario_id = %s ORDER BY fecha DESC LIMIT %s",
            (usuario_id, limite)
        )
        historial = cursor.fetchall()
        cursor.close()
        conn.close()
        return historial
    except Exception as e:
        print(f"Error obteniendo historial: {e}")
        return []

# ========== FUNCIONES DE ADMINISTRADOR ==========

def obtener_estadisticas_usuario_admin(usuario_id):
    """Obtener estadísticas completas de un usuario (para admin)"""
    try:
        usuario = obtener_usuario_por_id(usuario_id)
        if not usuario:
            return None
        
        hoy = datetime.now()
        año = hoy.year
        mes = hoy.month
        
        # Estadísticas del mes actual
        stats_mes = obtener_estadisticas_mes(usuario_id, año, mes)
        
        # Total de ahorros
        total_ahorros = obtener_total_ahorros(usuario_id)
        
        # Racha
        racha = calcular_racha(usuario_id)
        
        # Preferencias (ingresos)
        prefs = obtener_preferencias(usuario_id)
        ingresos = float(prefs.get('ingresos_mensuales', 0))
        
        # Estadísticas de todos los tiempos
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT COUNT(*) as total FROM gastos WHERE usuario_id = %s",
            (usuario_id,)
        )
        total_gastos_lifetime = cursor.fetchone()['total']
        
        cursor.execute(
            "SELECT COUNT(*) as total FROM tickets WHERE usuario_id = %s",
            (usuario_id,)
        )
        total_tickets_lifetime = cursor.fetchone()['total']
        
        cursor.execute(
            "SELECT COUNT(*) as total FROM ahorros WHERE usuario_id = %s",
            (usuario_id,)
        )
        total_ahorros_count = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        
        return {
            'usuario': usuario,
            'estadisticas_mes_actual': stats_mes,
            'total_ahorros': total_ahorros,
            'racha_ahorro': racha,
            'ingresos_mensuales': ingresos,
            'total_gastos_lifetime': total_gastos_lifetime,
            'total_tickets_lifetime': total_tickets_lifetime,
            'total_ahorros_count': total_ahorros_count,
            'fecha_consulta': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error obteniendo estadísticas admin: {e}")
        return None

def obtener_estadisticas_globales():
    """Obtener estadísticas globales de todos los usuarios"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total de usuarios
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total_usuarios = cursor.fetchone()['total']
        
        # Total de usuarios activos (con sesiones en los últimos 7 días)
        cursor.execute(
            "SELECT COUNT(DISTINCT usuario_id) as total FROM sesiones WHERE fecha_expiracion > DATE_SUB(NOW(), INTERVAL 7 DAY)"
        )
        usuarios_activos = cursor.fetchone()['total']
        
        # Total de gastos globales
        cursor.execute("SELECT COALESCE(SUM(cantidad), 0) as total FROM gastos")
        total_gastos = float(cursor.fetchone()['total'])
        
        # Total de tickets
        cursor.execute("SELECT COALESCE(SUM(cantidad), 0) as total FROM tickets")
        total_tickets = float(cursor.fetchone()['total'])
        
        # Total de ahorros
        cursor.execute("SELECT COALESCE(SUM(cantidad), 0) as total FROM ahorros")
        total_ahorros = float(cursor.fetchone()['total'])
        
        # Estadísticas del mes actual
        hoy = datetime.now()
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total FROM gastos WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s",
            (hoy.year, hoy.month)
        )
        gastos_mes = float(cursor.fetchone()['total'])
        
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total FROM tickets WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s",
            (hoy.year, hoy.month)
        )
        tickets_mes = float(cursor.fetchone()['total'])
        
        cursor.execute(
            "SELECT COALESCE(SUM(cantidad), 0) as total FROM ahorros WHERE YEAR(fecha) = %s AND MONTH(fecha) = %s",
            (hoy.year, hoy.month)
        )
        ahorros_mes = float(cursor.fetchone()['total'])
        
        cursor.close()
        conn.close()
        
        return {
            'total_usuarios': total_usuarios,
            'usuarios_activos': usuarios_activos,
            'total_gastos': total_gastos,
            'total_tickets': total_tickets,
            'total_ahorros': total_ahorros,
            'gastos_mes_actual': gastos_mes,
            'tickets_mes_actual': tickets_mes,
            'ahorros_mes_actual': ahorros_mes,
            'fecha_consulta': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error obteniendo estadísticas globales: {e}")
        return None

def obtener_datos_usuario_semanal(usuario_id, fecha_inicio, fecha_fin):
    """Obtener datos semanales de un usuario para reporte"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Gastos del período
        cursor.execute(
            "SELECT * FROM gastos WHERE usuario_id = %s AND fecha BETWEEN %s AND %s ORDER BY fecha DESC",
            (usuario_id, fecha_inicio, fecha_fin)
        )
        gastos = cursor.fetchall()
        
        # Tickets del período
        cursor.execute(
            "SELECT * FROM tickets WHERE usuario_id = %s AND fecha BETWEEN %s AND %s ORDER BY fecha DESC",
            (usuario_id, fecha_inicio, fecha_fin)
        )
        tickets = cursor.fetchall()
        
        # Ahorros del período
        cursor.execute(
            "SELECT * FROM ahorros WHERE usuario_id = %s AND fecha BETWEEN %s AND %s ORDER BY fecha DESC",
            (usuario_id, fecha_inicio, fecha_fin)
        )
        ahorros = cursor.fetchall()
        
        # Totales
        total_gastos = sum(float(g['cantidad']) for g in gastos)
        total_tickets = sum(float(t['cantidad']) for t in tickets)
        total_ahorros = sum(float(a['cantidad']) for a in ahorros)
        
        # Usuario
        usuario = obtener_usuario_por_id(usuario_id)
        prefs = obtener_preferencias(usuario_id)
        
        cursor.close()
        conn.close()
        
        return {
            'usuario': usuario,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'gastos': gastos,
            'tickets': tickets,
            'ahorros': ahorros,
            'total_gastos': total_gastos,
            'total_tickets': total_tickets,
            'total_ahorros': total_ahorros,
            'ingresos_mensuales': float(prefs.get('ingresos_mensuales', 0)),
            'balance': float(prefs.get('ingresos_mensuales', 0)) * (7/30) - total_gastos - total_tickets + total_ahorros
        }
    except Exception as e:
        print(f"Error obteniendo datos semanales: {e}")
        return None

