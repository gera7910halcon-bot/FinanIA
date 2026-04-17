-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-12-2025 a las 22:24:35
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `finania`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ahorros`
--

CREATE TABLE `ahorros` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `fecha` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `ahorros`
--

INSERT INTO `ahorros` (`id`, `usuario_id`, `cantidad`, `descripcion`, `fecha`, `timestamp`) VALUES
(2, 5, 20.00, 'Ahorro de semana', '2025-11-19', '2025-11-19 02:25:05'),
(3, 6, 50.00, 'Ahorro semanal', '2025-11-19', '2025-11-19 22:24:33'),
(4, 8, 10.00, 'ahorro de noviembre', '2025-11-25', '2025-11-25 13:53:56'),
(5, 7, 5000.00, '', '2025-12-01', '2025-12-01 21:12:12');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `conversaciones_chatbot`
--

CREATE TABLE `conversaciones_chatbot` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `mensaje_usuario` text NOT NULL,
  `respuesta_bot` text NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `conversaciones_chatbot`
--

INSERT INTO `conversaciones_chatbot` (`id`, `usuario_id`, `mensaje_usuario`, `respuesta_bot`, `fecha`) VALUES
(2, 5, 'como puedo ahorrrar', 'No estoy seguro de entender. ¿Quieres saber sobre tus gastos, ahorros o necesitas algún consejo?', '2025-11-19 02:29:19'),
(3, 5, 'necesito consejos', '💡 Tip: Marca tus días de ahorro para mantener la motivación.', '2025-11-19 02:29:30'),
(4, 5, 'que mas', 'Puedo ayudarte con: ver tus gastos, registrar ahorros, ver estadísticas, o darte consejos financieros. ¿Qué necesitas?', '2025-11-19 02:29:39'),
(5, 6, 'en que ´puedo ahorrar', '¡Excelente! Has ahorrado $50.00 en total. Tu racha actual es de 0 días. ¡Sigue así! 🎯', '2025-11-19 22:25:46'),
(7, 7, 'hola, como puedo juntar 100 pesos en una semana si gasto 50 pesos por dia', '¡Hola! 👋 Soy tu asistente financiero de FinanIA. ¿En qué puedo ayudarte hoy? Puedo ayudarte con tus gastos, ahorros, estadísticas y más.', '2025-11-24 20:12:01'),
(8, 7, 'Como puedo juntar 100 pesos a fin de semana si apenas voy iniciando', 'Entiendo. ¿Puedes ser más específico? Puedo ayudarte con gastos, ahorros, estadísticas o consejos.', '2025-11-24 20:12:41'),
(11, 8, 'como puedo ahorrar', '¡Excelente! Has ahorrado $10.00 en total. Tu racha actual es de 1 días. ¡Sigue así! 🎯', '2025-11-25 13:55:23'),
(12, 8, 'quiero consejos de inversion', '💡 Tip: Establece una meta de ahorro mensual y revísala regularmente.', '2025-11-25 13:55:36');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dias_ahorro`
--

CREATE TABLE `dias_ahorro` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `dias_ahorro`
--

INSERT INTO `dias_ahorro` (`id`, `usuario_id`, `fecha`, `timestamp`) VALUES
(3, 5, '2025-11-19', '2025-11-19 02:24:48'),
(6, 7, '2025-11-24', '2025-11-24 20:11:07'),
(7, 8, '2025-11-25', '2025-11-25 13:54:08'),
(8, 7, '2025-12-01', '2025-12-01 21:12:16');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `gastos`
--

CREATE TABLE `gastos` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `gastos`
--

INSERT INTO `gastos` (`id`, `usuario_id`, `descripcion`, `cantidad`, `categoria`, `fecha`, `timestamp`) VALUES
(4, 5, 'Salida con amigas', 1500.00, 'Entretenimiento', '2025-11-19', '2025-11-19 02:24:05'),
(5, 5, 'Pago de servicios', 800.00, 'Servicios', '2025-11-19', '2025-11-19 02:27:09'),
(6, 5, 'Compra de despensa', 2000.00, 'Alimentación', '2025-11-19', '2025-11-19 02:28:22'),
(7, 6, 'Compra en supermercado', 500.00, 'Alimentación', '2025-11-19', '2025-11-19 22:23:58'),
(9, 8, 'Compra de despensa', 200.00, 'Alimentación', '2025-11-25', '2025-11-25 13:52:38'),
(10, 8, 'Cine', 500.00, 'Entretenimiento', '2025-11-25', '2025-11-25 13:53:24'),
(11, 7, 'Compra de despensa', 800.00, 'Alimentación', '2025-12-01', '2025-12-01 21:11:48'),
(12, 7, 'Salida con amigas', 2000.00, 'Entretenimiento', '2025-12-01', '2025-12-01 21:12:03');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `mensaje` text NOT NULL,
  `tipo` varchar(50) NOT NULL DEFAULT 'info',
  `leida` tinyint(1) DEFAULT 0,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `titulo`, `mensaje`, `tipo`, `leida`, `fecha_creacion`) VALUES
(2, 5, 'Ahorro registrado', 'Has registrado $20.00 en ahorros. ¡Sigue así!', 'success', 1, '2025-11-19 02:25:05'),
(3, 6, 'Ahorro registrado', 'Has registrado $50.00 en ahorros. ¡Sigue así!', 'success', 1, '2025-11-19 22:24:33'),
(4, 8, 'Ahorro registrado', 'Has registrado $10.00 en ahorros. ¡Sigue así!', 'success', 0, '2025-11-25 13:53:56'),
(5, 7, 'Ahorro registrado', 'Has registrado $5000.00 en ahorros. ¡Sigue así!', 'success', 0, '2025-12-01 21:12:12');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preferencias_usuario`
--

CREATE TABLE `preferencias_usuario` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `color_primario` varchar(7) DEFAULT '#004481',
  `color_secundario` varchar(7) DEFAULT '#ffd100',
  `notificaciones_email` tinyint(1) DEFAULT 1,
  `notificaciones_push` tinyint(1) DEFAULT 1,
  `meta_ahorro_mensual` decimal(10,2) DEFAULT 0.00,
  `ingresos_mensuales` decimal(10,2) DEFAULT 5000.00,
  `fecha_actualizacion` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `preferencias_usuario`
--

INSERT INTO `preferencias_usuario` (`id`, `usuario_id`, `color_primario`, `color_secundario`, `notificaciones_email`, `notificaciones_push`, `meta_ahorro_mensual`, `ingresos_mensuales`, `fecha_actualizacion`) VALUES
(2, 4, '#004481', '#ffd100', 1, 1, 0.00, 5000.00, '2025-11-19 02:19:16'),
(3, 5, '#004481', '#ffd100', 1, 1, 100.00, 500.00, '2025-11-19 02:26:05'),
(4, 6, '#004481', '#ffd100', 1, 1, 0.00, 5000.00, '2025-11-19 22:23:17'),
(5, 7, '#004481', '#ffd100', 1, 1, 0.00, 5000.00, '2025-11-24 20:09:35'),
(6, 8, '#004481', '#ffd100', 1, 1, 0.00, 100.00, '2025-11-25 13:56:04'),
(7, 9, '#004481', '#ffd100', 1, 1, 0.00, 5000.00, '2025-11-30 23:43:27');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reportes_semanales`
--

CREATE TABLE `reportes_semanales` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `ruta_pdf` varchar(500) DEFAULT NULL,
  `fecha_generacion` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sesiones`
--

CREATE TABLE `sesiones` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `fecha_expiracion` timestamp NOT NULL DEFAULT (current_timestamp() + interval 1 hour)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `sesiones`
--

INSERT INTO `sesiones` (`id`, `usuario_id`, `token`, `fecha_creacion`, `fecha_expiracion`) VALUES
(5, 5, 'yQ9Zs54QkCM5nDvhJfJcvChi_4dx7nJ8Xf7CCgYpunM', '2025-11-19 02:23:30', '2025-11-26 02:23:30'),
(13, 8, 'JldPvwB-fHe2OZRzyV8J47TMLmYtkeSkGf2NYsDTYWA', '2025-11-25 13:52:13', '2025-12-02 13:52:13'),
(17, 7, 'jqOEp-8CEYt3Z3Cj8p4x89nct_tgf4w384lCPWL1pes', '2025-12-01 21:11:33', '2025-12-08 21:11:33'),
(18, 9, '82Itnkt5mzjReGeioUQm0hMeRTjM3JVjwE3414rWSWQ', '2025-12-01 21:13:45', '2025-12-08 21:13:45');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tickets`
--

CREATE TABLE `tickets` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `imagen_path` varchar(500) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` varchar(100) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `tickets`
--

INSERT INTO `tickets` (`id`, `usuario_id`, `imagen_path`, `descripcion`, `categoria`, `cantidad`, `fecha`, `timestamp`) VALUES
(2, 5, 'uploads\\5_20251118_202434_tiket.jpg', 'Boleto', 'Otros', 2.00, '2025-11-19', '2025-11-19 02:24:34');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  `es_administrador` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `email`, `password_hash`, `fecha_registro`, `es_administrador`) VALUES
(4, 'Pablo', 'pablitoLP@gmail.com', '7a2ec40ff8a1247c532309355f798a779e00acff579c63eec3636ffb2902c1ac', '2025-11-19 02:18:23', 0),
(5, 'Lorena', 'lorelpMM@hotmail.com', '7d1a54127b222502f5b79b5fb0803061152a44f92b37e23c6527baf665d4da9a', '2025-11-19 02:22:38', 0),
(6, 'Gio Armas', 'lm4793313@gmail.com', '2600c982b635df5b9ef17f35db14b6ba8f35beecc9f53a73e4077b7cb6f8302f', '2025-11-19 22:22:52', 0),
(7, 'Gerar', 'gera7910halcon@gmail.com', 'd74f202fd425ae226b91396414947d275fae84791e20b7cc3f67a1b331201175', '2025-11-24 20:09:14', 0),
(8, 'Sandra', 'sandra12@gmail.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', '2025-11-25 13:52:00', 0),
(9, 'Administrador', 'admin@finania.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', '2025-11-30 23:43:27', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ahorros`
--
ALTER TABLE `ahorros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha`);

--
-- Indices de la tabla `conversaciones_chatbot`
--
ALTER TABLE `conversaciones_chatbot`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha`);

--
-- Indices de la tabla `dias_ahorro`
--
ALTER TABLE `dias_ahorro`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_usuario_fecha` (`usuario_id`,`fecha`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha`);

--
-- Indices de la tabla `gastos`
--
ALTER TABLE `gastos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_leida` (`usuario_id`,`leida`);

--
-- Indices de la tabla `preferencias_usuario`
--
ALTER TABLE `preferencias_usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `reportes_semanales`
--
ALTER TABLE `reportes_semanales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha_inicio`,`fecha_fin`),
  ADD KEY `idx_fecha_generacion` (`fecha_generacion`);

--
-- Indices de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `idx_token` (`token`),
  ADD KEY `idx_expiracion` (`fecha_expiracion`);

--
-- Indices de la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_usuario_fecha` (`usuario_id`,`fecha`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_es_administrador` (`es_administrador`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ahorros`
--
ALTER TABLE `ahorros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `conversaciones_chatbot`
--
ALTER TABLE `conversaciones_chatbot`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `dias_ahorro`
--
ALTER TABLE `dias_ahorro`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `gastos`
--
ALTER TABLE `gastos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `preferencias_usuario`
--
ALTER TABLE `preferencias_usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `reportes_semanales`
--
ALTER TABLE `reportes_semanales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sesiones`
--
ALTER TABLE `sesiones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `tickets`
--
ALTER TABLE `tickets`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ahorros`
--
ALTER TABLE `ahorros`
  ADD CONSTRAINT `ahorros_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `conversaciones_chatbot`
--
ALTER TABLE `conversaciones_chatbot`
  ADD CONSTRAINT `conversaciones_chatbot_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `dias_ahorro`
--
ALTER TABLE `dias_ahorro`
  ADD CONSTRAINT `dias_ahorro_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `gastos`
--
ALTER TABLE `gastos`
  ADD CONSTRAINT `gastos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD CONSTRAINT `notificaciones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `preferencias_usuario`
--
ALTER TABLE `preferencias_usuario`
  ADD CONSTRAINT `preferencias_usuario_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `reportes_semanales`
--
ALTER TABLE `reportes_semanales`
  ADD CONSTRAINT `reportes_semanales_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `sesiones`
--
ALTER TABLE `sesiones`
  ADD CONSTRAINT `sesiones_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `tickets_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
