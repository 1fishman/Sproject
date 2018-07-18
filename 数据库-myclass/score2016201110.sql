/*
 Navicat Premium Data Transfer

 Source Server         : aaa
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : test1

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 16/07/2018 08:40:08
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for score2016201110
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score2016201110`  (
  `开课学期` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `课程编号` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `课程名称` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `成绩` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `学分` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `总学时` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `考核方式` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `考试性质` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `课程属性` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `课程性质` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `通识教育选修课程类别` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `成绩标记` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`课程名称`, `课程编号`, `开课学期`, `考试性质`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
