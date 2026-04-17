-- FinanIA - Script para actualizar la base de datos con nuevas funcionalidades
-- Ejecuta este script DESPUÉS de crear_base_datos.sql

USE finania;

-- Tabla de ahorros (con cantidades)
CREATE TABLE IF NOT EXISTS ahorros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    cantidad DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_fecha (usuario_id, fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de notificaciones
CREATE TABLE IF NOT EXISTS notificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'info',
    leida BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_leida (usuario_id, leida)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de preferencias de usuario
CREATE TABLE IF NOT EXISTS preferencias_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    color_primario VARCHAR(7) DEFAULT '#004481',
    color_secundario VARCHAR(7) DEFAULT '#ffd100',
    notificaciones_email BOOLEAN DEFAULT TRUE,
    notificaciones_push BOOLEAN DEFAULT TRUE,
    meta_ahorro_mensual DECIMAL(10, 2) DEFAULT 0,
    ingresos_mensuales DECIMAL(10, 2) DEFAULT 5000,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Reglas de validación para despliegue en servidor
-- 1) ingresos_mensuales no puede ser negativo
-- 2) meta_ahorro_mensual no puede ser negativa ni mayor a ingresos_mensuales
ALTER TABLE preferencias_usuario
    ADD CONSTRAINT chk_ingresos_no_negativos CHECK (ingresos_mensuales >= 0),
    ADD CONSTRAINT chk_ahorro_no_negativo CHECK (meta_ahorro_mensual >= 0),
    ADD CONSTRAINT chk_ahorro_no_mayor_ingresos CHECK (meta_ahorro_mensual <= ingresos_mensuales);

-- Tabla de tokens de recuperación de contraseña
CREATE TABLE IF NOT EXISTS tokens_recuperacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_expiracion TIMESTAMP NOT NULL,
    usado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_token (token),
    INDEX idx_expiracion (fecha_expiracion)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de conversaciones del chatbot
CREATE TABLE IF NOT EXISTS conversaciones_chatbot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    mensaje_usuario TEXT NOT NULL,
    respuesta_bot TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario_fecha (usuario_id, fecha)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

