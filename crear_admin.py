"""
Script para crear usuario administrador en FinanIA
Ejecuta este script después de ejecutar crear_admin.sql
"""

import database as db
import sys

def crear_usuario_admin():
    """Crear usuario administrador si no existe"""
    email = 'admin@finania.com'
    password = 'admin123'
    nombre = 'Administrador'
    
    # Verificar si ya existe
    usuario_existente = db.obtener_usuario_por_email(email)
    
    if usuario_existente:
        print(f"❌ El usuario {email} ya existe.")
        # Actualizar a administrador si no lo es
        if not usuario_existente.get('es_administrador'):
            print("⚠️  Actualizando usuario existente a administrador...")
            # Aquí necesitaríamos una función para actualizar, pero por ahora
            # podemos usar SQL directamente o simplemente informar
            print("⚠️  Por favor, ejecuta en MySQL:")
            print(f"   UPDATE usuarios SET es_administrador = TRUE WHERE email = '{email}';")
        else:
            print("✅ El usuario ya es administrador.")
        return False
    
    # Crear usuario
    usuario_id = db.crear_usuario(nombre, email, password)
    
    if usuario_id:
        # Marcar como administrador usando la función de la base de datos
        if db.marcar_como_administrador(usuario_id):
            print("✅ Usuario administrador creado exitosamente!")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
            print("   ⚠️  IMPORTANTE: Cambia la contraseña después del primer inicio de sesión.")
            return True
    else:
        print("❌ Error al crear usuario administrador.")
        return False

if __name__ == '__main__':
    print("=" * 50)
    print("Creando usuario administrador para FinanIA")
    print("=" * 50)
    print()
    
    try:
        crear_usuario_admin()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

