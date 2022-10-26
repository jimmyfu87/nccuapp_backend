-- MySQL dump 10.13  Distrib 8.0.30, for macos12 (x86_64)
--
-- Host: 127.0.0.1    Database: nccuapp
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Channel`
--

DROP TABLE IF EXISTS `Channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Channel` (
  `id` int NOT NULL AUTO_INCREMENT,
  `channel_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
  `channel_url` longtext CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `channel_name` (`channel_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Channel`
--

LOCK TABLES `Channel` WRITE;
/*!40000 ALTER TABLE `Channel` DISABLE KEYS */;
INSERT INTO `Channel` VALUES (1,'Momo','https://m.momoshop.com.tw/main.momo?mdiv=1000200000-bt_0_229_01-bt_0_229_01_P1_5_e1&ctype=B'),(2,'Pchome','https://24h.m.pchome.com.tw/'),(3,'Yahoo購物中心','https://tw.buy.yahoo.com/'),(4,'蝦皮購物','https://shopee.tw/');
/*!40000 ALTER TABLE `Channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Product`
--

DROP TABLE IF EXISTS `Product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_price` int NOT NULL,
  `product_url` longtext CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL COMMENT '商品網址',
  `member_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL COMMENT '使用者帳號',
  `channel_name` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL COMMENT '商店名稱',
  `upload_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  KEY `channel_name` (`channel_name`),
  CONSTRAINT `Product_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `User` (`member_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Product_ibfk_2` FOREIGN KEY (`channel_name`) REFERENCES `Channel` (`channel_name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Product`
--

LOCK TABLES `Product` WRITE;
/*!40000 ALTER TABLE `Product` DISABLE KEYS */;
INSERT INTO `Product` VALUES (2,'日本KIU 64125 萬花筒 空氣感雨衣/親子雨披/防水斗篷 騎車露營必備 附收納袋(男女適用)',1390,'https://24h.pchome.com.tw/prod/DXAB09-A9008V3WU?fq=/S/DXAB90','jimmy','Pchome','2022-10-13 14:47:33'),(5,'【Phiten®銀谷】X30項圈 (黑灰紅/55cm)',990,'https://24h.pchome.com.tw/prod/DEAQNY-A900AVFVO?fq=/S/DEAQM7','jimmy','Pchome','2022-10-13 14:47:34'),(7,'任天堂 Switch 紅藍/灰黑主機 (電池加強版)',7380,'https://shopee.tw/%E4%BB%BB%E5%A4%A9%E5%A0%82-Switch-%E7%B4%85%E8%97%8D-%E7%81%B0%E9%BB%91%E4%B8%BB%E6%A9%9F-(%E9%9B%BB%E6%B1%A0%E5%8A%A0%E5%BC%B7%E7%89%88)-i.54598032.2295508467?xptdk=61a1e523-c741-4278-b6a7-b545dbe5af3e','jimmy','蝦皮購物','2022-10-13 14:47:34'),(13,'Fitbit Luxe 智慧手環',3999,'https://24h.pchome.com.tw/prod/DEAQDO-A900BJJIR?fq=/S/DEAQMF','jimmyfu','Pchome','2022-10-08 13:33:01'),(14,'APPLE iPhone 12 Pro 512G 神腦生活',29900,'https://shopee.tw/APPLE-iPhone-12-Pro-512G-%E7%A5%9E%E8%85%A6%E7%94%9F%E6%B4%BB-i.54598032.5957085099?xptdk=181dcd04-c36d-41c6-a0ba-1ce6003004da','jimmyfu','蝦皮購物','2022-10-08 13:33:00'),(17,'SPORTCRAFT-風靡歐美室內遊戲組-迷你掛門籃板',629,'https://24h.pchome.com.tw/prod/DXAG22-A90094CJ2?fq=/S/DXAFD0','jimmy','Pchome','2022-10-13 14:47:35'),(20,'SPALDING 斯伯丁 TF-1000 Legacy 新一代ZK合成皮 6號',2295,'https://24h.pchome.com.tw/prod/DXAG2J-A9007VNNA?fq=/S/DXAFGO','jane','Pchome','2022-10-08 14:54:16'),(26,'Fitbit Luxe 智慧手環',3999,'https://24h.pchome.com.tw/prod/DEAQDO-A900BJJIR?fq=/S/DEAQMF','jimmy','Pchome','2022-10-13 14:49:26'),(31,'SPALDING 斯伯丁 TF-1000 Legacy 新一代ZK合成皮 6號',2295,'https://24h.pchome.com.tw/prod/DXAG2J-A9007VNNA?fq=/S/DXAFGO','jimmy','Pchome','2022-10-13 14:47:36');
/*!40000 ALTER TABLE `Product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `member_id` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL COMMENT '使用者英文帳號',
  `member_email` varchar(50) CHARACTER SET utf8mb3 COLLATE utf8_bin NOT NULL,
  `member_password` varchar(500) CHARACTER SET utf8mb3 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `member_id` (`member_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3 COLLATE=utf8_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'jimmyfu','jimmom','$2b$10$ncc.ap.ncc/app4cc3/pp./OeRUP5G9eXCTjwjl4EGi4c9rXTgdmu'),(2,'jimmyfuw','abcd','123456'),(3,'jk','jdjsjsj','12345'),(4,'sbsbbbbbbbbbbbbbbbbb','natasha.tsai.ta.nccu@gmail.com','123'),(20,'jimmy','jimmyfu87@gmail.com','$2b$10$ncc.ap.ncc/app4cc3/pp.sW8dJAyqm2sKcDV3qzlQ3eE997HR6DO'),(21,'jane','jane','$2b$10$ncc.ap.ncc/app4cc3/pp.kjaOWRgq3h4ABDDfjm5W1SzNbrPpWSi'),(22,'ken','dsfaf','$2b$10$ncc.ap.ncc/app4cc3/pp.sW8dJAyqm2sKcDV3qzlQ3eE997HR6DO'),(23,'kk','132121','$2b$10$ncc.ap.ncc/app4cc3/pp.zi.6AAEH9ssbYik461DxbB2UrMqUQD.'),(26,'kyrie','ji','$2b$10$ncc.ap.ncc/app4cc3/pp.sW8dJAyqm2sKcDV3qzlQ3eE997HR6DO');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-15 21:13:52
