/*
 Navicat Premium Data Transfer

 Source Server         : LA
 Source Server Type    : MySQL
 Source Server Version : 50554
 Source Host           : localhost
 Source Database       : blog_data

 Target Server Type    : MySQL
 Target Server Version : 50554
 File Encoding         : utf-8

 Date: 04/04/2017 23:40:19 PM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `id_title`
-- ----------------------------
DROP TABLE IF EXISTS `id_title`;
CREATE TABLE `id_title` (
  `id` int(11) NOT NULL,
  `title` varchar(35) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `read_number`
-- ----------------------------
DROP TABLE IF EXISTS `read_number`;
CREATE TABLE `read_number` (
  `id` int(11) NOT NULL DEFAULT '0',
  `read_number` int(11) DEFAULT NULL,
  `record_time` date NOT NULL DEFAULT '0000-00-00',
  PRIMARY KEY (`id`,`record_time`),
  CONSTRAINT `read_number_ibfk_1` FOREIGN KEY (`id`) REFERENCES `id_title` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
