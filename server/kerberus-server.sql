-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 13-08-2013 a las 20:33:36
-- Versión del servidor: 5.5.31
-- Versión de PHP: 5.4.4-14+deb7u2

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `kerberus_db`
--
CREATE DATABASE `kerberus_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `kerberus_db`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cache_urls_aceptadas`
--

CREATE TABLE IF NOT EXISTS `cache_urls_aceptadas` (
  `url` varchar(2048) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hora` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cache_urls_denegadas`
--

CREATE TABLE IF NOT EXISTS `cache_urls_denegadas` (
  `url` varchar(2048) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hora` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `dominios`
--

CREATE TABLE IF NOT EXISTS `dominios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` char(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `estado` int(11) NOT NULL,
  `ultima_revision` datetime NOT NULL,
  `verificador` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `verificador` (`verificador`),
  KEY `estado` (`estado`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=43185 ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estado`
--

CREATE TABLE IF NOT EXISTS `estado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Especifica el estado de los dominios (habilitados, denegados' AUTO_INCREMENT=4 ;

--
-- Volcado de datos para la tabla `estado`
--

INSERT INTO `estado` (`id`, `estado`) VALUES
(1, 'Permitido'),
(2, 'Denegado'),
(3, 'Gris');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informar_baja_usuario`
--

CREATE TABLE IF NOT EXISTS `informar_baja_usuario` (
  `nodo` int(11) NOT NULL,
  `server_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informar_cambios_de_password`
--

CREATE TABLE IF NOT EXISTS `informar_cambios_de_password` (
  `nodo` int(11) NOT NULL,
  `server_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `nuevaPassword` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`nodo`,`server_id`,`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `informar_nuevo_usuario`
--

CREATE TABLE IF NOT EXISTS `informar_nuevo_usuario` (
  `nodo` int(11) NOT NULL,
  `server_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `ip` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `version` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  UNIQUE KEY `nodo` (`nodo`,`server_id`,`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parametros`
--

CREATE TABLE IF NOT EXISTS `parametros` (
  `tiempo_actualizacion_clientes` char(4) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tiempo_de_recarga_completa_clientes` char(6) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `parametros`
--

INSERT INTO `parametros` (`tiempo_actualizacion_clientes`, `tiempo_de_recarga_completa_clientes`) VALUES
('1440', '14400');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ranking_servidores`
--

CREATE TABLE IF NOT EXISTS `ranking_servidores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `puerto` int(11) NOT NULL,
  `ranking` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `ranking_servidores`
--

INSERT INTO `ranking_servidores` (`id`, `ip`, `puerto`, `ranking`) VALUES
(1, 'validador1.kerberus.com.ar', 443, 1),
(2, 'validador2.kerberus.com.ar', 443, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servidores`
--

CREATE TABLE IF NOT EXISTS `servidores` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IP` text COLLATE utf8_unicode_ci NOT NULL,
  `Puerto` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `servidores`
--

INSERT INTO `servidores` (`ID`, `IP`, `Puerto`) VALUES
(1, 'nodo1.kerberus.com.ar', 80),
(2, 'nodo2.kerberus.com.ar', 80);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE IF NOT EXISTS `usuarios` (
  `id` int(11) NOT NULL,
  `server_id` int(11) NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ultima_ip` char(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `version` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`server_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


--
-- Estructura de tabla para la tabla `verificador`
--

CREATE TABLE IF NOT EXISTS `verificador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3 ;

--
-- Volcado de datos para la tabla `verificador`
--

INSERT INTO `verificador` (`id`, `nombre`, `descripcion`) VALUES
(1, 'Filtrado por DNS', 'Verifica la aptitud a nivel de dominio completo sin verificar cada página en particular.'),
(2, 'Filtrado de contenidos', 'Examina cada página detenidamente y determina si esta es válida.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `versiones_cliente`
--

CREATE TABLE IF NOT EXISTS `versiones_cliente` (
  `version_desde` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `version_destino` varchar(4) COLLATE utf8_unicode_ci NOT NULL,
  `URL_actualizador` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `md5sum_actualizador` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `plataforma` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dominios`
--
ALTER TABLE `dominios`
  ADD CONSTRAINT `dominios_ibfk_1` FOREIGN KEY (`estado`) REFERENCES `estado` (`id`),
  ADD CONSTRAINT `dominios_ibfk_2` FOREIGN KEY (`verificador`) REFERENCES `verificador` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
