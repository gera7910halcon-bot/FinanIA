-- Script para agregar funcionalidad de administrador a FinanIA

USE finania;

-- Agregar campo es_administrador a la tabla usuarios si no existe
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS es_administrador BOOLEAN DEFAULT FALSE;

-- Crear índice para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_es_administrador ON usuarios(es_administrador);

-- NOTA: Para crear el usuario administrador, ejecuta el script Python:
-- python crear_admin.py
-- Esto asegura que la contraseña se hashee correctamente usando el mismo método que la aplicación

-- Crear tabla de reportes semanales si no existe
CREATE TABLE IF NOT EXISTS reportes_semanales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL, -- NULL para reporte global de admin
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    ruta_pdf VARCHAR(500),
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_fecha (usuario_id, fecha_inicio, fecha_fin),
    INDEX idx_fecha_generacion (fecha_generacion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Crear tabla de días de ahorro si no existe (para la racha)
CREATE TABLE IF NOT EXISTS dias_ahorro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    fecha DATE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_dia_usuario (usuario_id, fecha),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_fecha (usuario_id, fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Asegurar que todas las tablas necesarias existen
-- Tabla de usuarios (asumiendo que ya existe pero verificamos campos)
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Mensaje de confirmación
SELECT 'Configuración de administrador completada' AS mensaje;

