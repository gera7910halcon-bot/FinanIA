# FinanIA - Sistema de Administrador y Reportes PDF

## 📋 Características Implementadas

### 1. Sistema de Administrador
- Panel de administrador completo (`admin_dashboard.html`)
- Gestión de usuarios con vista de datos financieros
- Estadísticas globales del sistema
- Generación de reportes semanales globales en PDF
- Generación de reportes individuales por usuario en PDF

### 2. Generación de Reportes PDF
- Reportes semanales para cada usuario
- Reportes mensuales para cada usuario
- Reportes semanales globales (solo administrador)
- Descarga directa de PDFs desde el navegador

### 3. Seguridad
- Sistema de roles (administrador/usuario regular)
- Decorador `require_admin()` para proteger endpoints
- Verificación de permisos en todas las funciones administrativas

## 🚀 Instalación y Configuración

### Paso 1: Instalar Dependencias

```bash
pip install -r requirements.txt
```

O instala manualmente:
```bash
pip install Flask Flask-CORS PyMySQL reportlab Werkzeug
```

### Paso 2: Configurar Base de Datos

1. Asegúrate de que MySQL esté corriendo (XAMPP, WAMP, etc.)

2. Ejecuta el script SQL para crear/actualizar las tablas:
```bash
mysql -u root -p finania < crear_admin.sql
```

O desde MySQL Workbench/phpMyAdmin, ejecuta el contenido de `crear_admin.sql`

### Paso 3: Crear Usuario Administrador

Ejecuta el script Python para crear el usuario administrador:

```bash
python crear_admin.py
```

**Credenciales por defecto:**
- Email: `admin@finania.com`
- Password: `admin123`
- ⚠️ **IMPORTANTE**: Cambia la contraseña después del primer inicio de sesión

### Paso 4: Iniciar el Servidor

```bash
python app.py
```

O usa el script batch:
```bash
iniciar_servidor.bat
```

El servidor estará disponible en: `http://localhost:5000`

## 📖 Uso del Sistema

### Acceso de Administrador

1. Inicia sesión con las credenciales de administrador
2. Serás redirigido automáticamente al panel de administrador
3. Desde ahí puedes:
   - Ver todos los usuarios del sistema
   - Ver estadísticas globales
   - Generar reportes semanales globales en PDF
   - Generar reportes individuales de usuarios en PDF

### Panel de Administrador

#### Sección de Usuarios
- Lista todos los usuarios registrados
- Muestra si son administradores o usuarios regulares
- Botón para ver detalles financieros de cada usuario

#### Sección de Estadísticas Globales
- Total de usuarios
- Usuarios activos (últimos 7 días)
- Total de gastos y ahorros del sistema
- Estadísticas del mes actual

#### Sección de Reportes
- **Reporte Semanal Global**: Genera un PDF con estadísticas de todos los usuarios de la semana pasada
- **Reporte de Usuario**: Selecciona un usuario específico y genera su reporte (semanal o mensual)

### Reportes para Usuarios Regulares

Los usuarios regulares pueden generar sus propios reportes en PDF desde el dashboard:
1. Ir a la pestaña "Reportes"
2. Seleccionar tipo de reporte (mensual/anual)
3. Seleccionar el mes/año
4. Hacer clic en "Generar Reporte"
5. Descargar el PDF generado

## 📁 Estructura de Archivos

```
FinanIA/
├── app.py                      # Servidor Flask principal
├── database.py                 # Módulo de base de datos
├── pdf_generator.py            # Generador de reportes PDF
├── crear_admin.sql             # Script SQL para configurar admin
├── crear_admin.py              # Script para crear usuario admin
├── admin_dashboard.html        # Panel de administrador
├── dashboard.html              # Dashboard de usuarios
├── login.html                  # Página de inicio de sesión
├── requirements.txt            # Dependencias Python
├── reports/                    # Carpeta para reportes PDF generados
└── uploads/                    # Carpeta para tickets/imágenes
```

## 🔐 Seguridad

- Todas las rutas de administrador están protegidas con `require_admin()`
- Solo usuarios con `es_administrador = TRUE` pueden acceder
- Las contraseñas se hashean con SHA256
- Los tokens de sesión expiran después de 7 días

## 📊 Endpoints API del Administrador

### Obtener Usuarios
```
GET /api/admin/usuarios
Authorization: Bearer <token>
```

### Estadísticas Globales
```
GET /api/admin/estadisticas-globales
Authorization: Bearer <token>
```

### Datos de Usuario Específico
```
GET /api/admin/usuario/<usuario_id>
Authorization: Bearer <token>
```

### Generar Reporte Semanal Global
```
POST /api/admin/reporte-semanal-global
Authorization: Bearer <token>
```

### Generar Reporte de Usuario
```
POST /api/admin/reporte-usuario/<usuario_id>
Authorization: Bearer <token>
Body: { "tipo": "semanal" | "mensual" }
```

### Descargar Reporte
```
GET /api/admin/descargar-reporte/<filename>
Authorization: Bearer <token>
```

## 🐛 Solución de Problemas

### Error: "No autorizado" o "Acceso denegado"
- Verifica que el usuario tenga `es_administrador = TRUE` en la base de datos
- Asegúrate de que el token de sesión sea válido
- Cierra sesión y vuelve a iniciar sesión

### Error al generar PDFs
- Verifica que la carpeta `reports/` exista y tenga permisos de escritura
- Asegúrate de que `reportlab` esté instalado: `pip install reportlab`

### Error de conexión a la base de datos
- Verifica que MySQL esté corriendo
- Confirma las credenciales en `database.py` (host, user, password, database)
- Asegúrate de que la base de datos `finania` exista

## 📝 Notas Importantes

1. **Primera vez**: Ejecuta `crear_admin.sql` y luego `crear_admin.py` para configurar el sistema
2. **Contraseña del admin**: Cambia la contraseña por defecto después del primer login
3. **Reportes PDF**: Se guardan en la carpeta `reports/` - asegúrate de tener espacio en disco
4. **Conexión a BD**: Los valores por defecto son para XAMPP (root, sin password). Actualiza según tu configuración

## 🎯 Próximas Mejoras Sugeridas

- [ ] Programar generación automática de reportes semanales
- [ ] Envío automático de reportes por email
- [ ] Exportar datos a Excel
- [ ] Gráficas comparativas entre usuarios
- [ ] Filtros avanzados en el panel de administrador
- [ ] Sistema de notificaciones para administradores

## 📞 Soporte

Si encuentras algún problema, revisa:
1. Los logs del servidor (consola donde corre `app.py`)
2. Los errores en la consola del navegador (F12)
3. Los mensajes de error en MySQL

---

**FinanIA** - Sistema de Gestión Financiera Personal v2.0

