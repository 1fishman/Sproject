/*
 Navicat Premium Data Transfer

 Source Server         : aaa
 Source Server Type    : MySQL
 Source Server Version : 80011
 Source Host           : localhost:3306
 Source Schema         : myclass

 Target Server Type    : MySQL
 Target Server Version : 80011
 File Encoding         : 65001

 Date: 10/07/2018 21:32:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for class2016201110
-- ----------------------------
DROP TABLE IF EXISTS `class2016201110`;
CREATE TABLE `class2016201110`  (
  `Cid` int(4) NULL DEFAULT NULL,
  `Cname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cteach` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Clast` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Ctime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cadr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Cday` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Cname`, `Ctime`, `Cday`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for class2016201114
-- ----------------------------
DROP TABLE IF EXISTS `class2016201114`;
CREATE TABLE `class2016201114`  (
  `Cid` int(4) NULL DEFAULT NULL,
  `Cname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cteach` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Clast` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Ctime` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `Cadr` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `Cday` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`Cname`, `Ctime`, `Cday`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for score2016201110
-- ----------------------------
DROP TABLE IF EXISTS `score2016201110`;
CREATE TABLE `score2016201110`  (
  `课程名称` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `课程编号` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `开课学期` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `成绩` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `学分` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `总学时` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `考核方式` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `考试性质` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `课程属性` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `课程性质` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `通识教育选修课程类别` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `成绩标记` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`课程名称`, `课程编号`, `开课学期`,`考试性质`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` int(10) NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`, `password`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
