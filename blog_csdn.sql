/*
 Navicat Premium Data Transfer

 Source Server         : 本地
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : localhost
 Source Database       : blog_csdn

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : utf-8

 Date: 05/27/2017 01:02:07 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `id_title`
-- ----------------------------
DROP TABLE IF EXISTS `id_title`;
CREATE TABLE `id_title` (
  `id` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `read_number`
-- ----------------------------
DROP TABLE IF EXISTS `read_number`;
CREATE TABLE `read_number` (
  `id` int(11) NOT NULL,
  `number` int(11) NOT NULL DEFAULT '0',
  `record_time` date NOT NULL,
  PRIMARY KEY (`id`,`record_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
