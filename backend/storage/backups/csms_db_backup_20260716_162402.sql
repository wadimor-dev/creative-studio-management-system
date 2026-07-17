-- MySQL dump 10.13  Distrib 9.4.0, for macos26.0 (arm64)
--
-- Host: localhost    Database: csms_db
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action_type` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_activity_logs_action_type` (`action_type`),
  KEY `ix_activity_logs_id` (`id`),
  CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_logs`
--

LOCK TABLES `activity_logs` WRITE;
/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
INSERT INTO `activity_logs` VALUES (1,1,'SYSTEM_BACKUP','Triggered manual system backup',NULL,NULL,'2026-07-15 20:24:53'),(2,1,'EXPORT_REPORT','Exported daily report to PDF',NULL,NULL,'2026-07-16 12:48:08'),(3,14,'EXPORT_REPORT','Exported daily report to PDF',NULL,NULL,'2026-07-16 15:57:56'),(4,1,'SYSTEM_BACKUP','Triggered manual system backup',NULL,NULL,'2026-07-16 16:24:02');
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('78081b401cbd');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `table_name` varchar(100) NOT NULL,
  `record_id` int NOT NULL,
  `action` varchar(20) NOT NULL,
  `old_value` json DEFAULT NULL,
  `new_value` json DEFAULT NULL,
  `created_at` datetime DEFAULT (now()),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_audit_logs_id` (`id`),
  KEY `ix_audit_logs_record_id` (`record_id`),
  KEY `ix_audit_logs_table_name` (`table_name`),
  CONSTRAINT `audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,1,'product_placement_stocks',1,'UPDATE','{\"quantity\": 1}','{\"quantity\": 0}','2026-07-16 14:36:16'),(2,1,'product_placement_stocks',1,'UPDATE','{\"quantity\": 0}','{\"quantity\": 15}','2026-07-16 14:37:03');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_categories_name` (`name`),
  KEY `ix_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Camera',''),(2,'Lighting','');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `divisions`
--

DROP TABLE IF EXISTS `divisions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `divisions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_divisions_name` (`name`),
  KEY `ix_divisions_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `divisions`
--

LOCK TABLES `divisions` WRITE;
/*!40000 ALTER TABLE `divisions` DISABLE KEYS */;
INSERT INTO `divisions` VALUES (4,'Administration'),(1,'Creative'),(5,'Management'),(2,'Marketing'),(3,'Production');
/*!40000 ALTER TABLE `divisions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `export_logs`
--

DROP TABLE IF EXISTS `export_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `export_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `type` varchar(50) NOT NULL,
  `format` varchar(10) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_export_logs_id` (`id`),
  CONSTRAINT `export_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `export_logs`
--

LOCK TABLES `export_logs` WRITE;
/*!40000 ALTER TABLE `export_logs` DISABLE KEYS */;
INSERT INTO `export_logs` VALUES (1,1,'daily','PDF','2026-07-16 12:48:09'),(2,14,'daily','PDF','2026-07-16 15:57:57');
/*!40000 ALTER TABLE `export_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_transactions`
--

DROP TABLE IF EXISTS `inventory_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `user_id` int NOT NULL,
  `quantity` int NOT NULL,
  `type` enum('IN','OUT','TRANSFER','ADJUSTMENT') COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_location_id` int DEFAULT NULL,
  `destination_location_id` int DEFAULT NULL,
  `reference` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_inventory_transactions_id` (`id`),
  KEY `destination_location_id` (`destination_location_id`),
  KEY `source_location_id` (`source_location_id`),
  CONSTRAINT `inventory_transactions_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  CONSTRAINT `inventory_transactions_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `inventory_transactions_ibfk_3` FOREIGN KEY (`destination_location_id`) REFERENCES `locations` (`id`),
  CONSTRAINT `inventory_transactions_ibfk_4` FOREIGN KEY (`source_location_id`) REFERENCES `locations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_transactions`
--

LOCK TABLES `inventory_transactions` WRITE;
/*!40000 ALTER TABLE `inventory_transactions` DISABLE KEYS */;
INSERT INTO `inventory_transactions` VALUES (1,1,1,50,'IN',NULL,1,NULL,'2026-07-09 13:51:59','Testing via script'),(2,1,1,10,'OUT',1,NULL,NULL,'2026-07-09 13:51:59','Testing OUT via script'),(3,1,1,5,'TRANSFER',1,4,'','2026-07-09 00:00:00',''),(4,3,1,150,'IN',NULL,1,NULL,'2026-07-09 14:02:44','Initial stock on creation'),(5,3,1,50,'ADJUSTMENT',NULL,1,NULL,'2026-07-09 14:09:29','Manual adjustment from item edit'),(6,5,1,1,'IN',NULL,4,NULL,'2026-07-09 14:14:17','Initial stock on creation'),(7,4,1,5,'ADJUSTMENT',NULL,4,NULL,'2026-07-09 14:18:35','Manual adjustment from item edit'),(8,1,1,1,'OUT',1,NULL,'ACT-20260710-00006','2026-07-10 08:50:50','Used in Work Activity Test Borrow Camera'),(9,1,1,1,'OUT',1,NULL,'ACT-20260710-00007','2026-07-10 08:51:27','Used in Work Activity Test Borrow Camera'),(10,1,1,1,'OUT',1,NULL,'ACT-20260710-00008','2026-07-10 08:52:15','Used in Work Activity Test Borrow Camera'),(11,1,1,1,'IN',NULL,1,'ACT-20260710-00008-RETURN','2026-07-10 08:52:15','Returned from Work Activity');
/*!40000 ALTER TABLE `inventory_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_stocks`
--

DROP TABLE IF EXISTS `item_stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_stocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `location_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_item_location_stock` (`item_id`,`location_id`),
  KEY `location_id` (`location_id`),
  KEY `ix_item_stocks_id` (`id`),
  CONSTRAINT `item_stocks_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  CONSTRAINT `item_stocks_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_stocks`
--

LOCK TABLES `item_stocks` WRITE;
/*!40000 ALTER TABLE `item_stocks` DISABLE KEYS */;
INSERT INTO `item_stocks` VALUES (1,1,1,10),(2,1,4,5),(3,3,1,200),(4,5,4,1),(5,4,4,5);
/*!40000 ALTER TABLE `item_stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sku` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `stock_qty` int NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `category_id` int DEFAULT NULL,
  `unit_id` int DEFAULT NULL,
  `location_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_items_sku` (`sku`),
  KEY `category_id` (`category_id`),
  KEY `location_id` (`location_id`),
  KEY `unit_id` (`unit_id`),
  KEY `ix_items_id` (`id`),
  KEY `ix_items_name` (`name`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `items_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`),
  CONSTRAINT `items_ibfk_3` FOREIGN KEY (`unit_id`) REFERENCES `units` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'CMR-1','Grandmaster SEI','CAMERA SONY',15,1,1,NULL,NULL),(3,'TEST-SKU-001','Test Item with Stock',NULL,200,1,NULL,NULL,1),(4,'LGT-2026','Lighting Godok',NULL,5,1,2,NULL,4),(5,'LGT-2025','Lighting Godok',NULL,1,1,2,NULL,4);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `locations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_locations_name` (`name`),
  KEY `ix_locations_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `locations`
--

LOCK TABLES `locations` WRITE;
/*!40000 ALTER TABLE `locations` DISABLE KEYS */;
INSERT INTO `locations` VALUES (1,'Showroom Pabrik','Showroom Pabrik'),(2,'WIP','WIP Sukorintex'),(3,'Packaging','Packaging Pabrik'),(4,'Studio Pabrik','Studio Foto Pabrik'),(5,'Showroom Rack','Sebelah Kiri Pintu - Rak Besar');
/*!40000 ALTER TABLE `locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `placement_types`
--

DROP TABLE IF EXISTS `placement_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `placement_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `icon` varchar(50) DEFAULT NULL,
  `color` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_placement_types_name` (`name`),
  KEY `ix_placement_types_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `placement_types`
--

LOCK TABLES `placement_types` WRITE;
/*!40000 ALTER TABLE `placement_types` DISABLE KEYS */;
INSERT INTO `placement_types` VALUES (1,'Rak',NULL,NULL),(2,'Showroom',NULL,NULL);
/*!40000 ALTER TABLE `placement_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_categories`
--

DROP TABLE IF EXISTS `product_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_categories_code` (`code`),
  UNIQUE KEY `ix_product_categories_name` (`name`),
  KEY `ix_product_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_categories`
--

LOCK TABLES `product_categories` WRITE;
/*!40000 ALTER TABLE `product_categories` DISABLE KEYS */;
INSERT INTO `product_categories` VALUES (1,'Grandmaster','GM','Sarung Grandmaster'),(3,'Primer','PR','Sarung Primer'),(4,'Viscose','VC','Sarung Viscose'),(5,'Dobby Special','DBS','Sarung Dobby Special'),(6,'Jacquard','JC','Sarung Jacquard'),(7,'Mercerized','MC','Sarung Mercerized'),(8,'Balimoon','BM','Sarung Balimoon'),(9,'Bali','BL','Sarung Bali'),(10,'Songket','SKT','Sarung Songket'),(11,'Kembang','KMB','Sarung Kembang'),(12,'Tumpal Kembang','TKMB','Sarung Tumpal Kembang'),(13,'Gerimis','GRM','Sarung Gerimis'),(14,'Pen Mode Sutra','PMS','Sarung Pen Mode Sutra'),(15,'Timbul','TMB','Sarung Timbul'),(16,'Madrid','MDR','Sarung Madrid'),(17,'Sulam','SLM','Sarung Sulam'),(18,'Madras','MDS','Sarung Madras'),(19,'Dobby Excellent','DBE','Sarung Dobby Excellent'),(20,'Batik','BTK','Sarung Batik');
/*!40000 ALTER TABLE `product_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_colors`
--

DROP TABLE IF EXISTS `product_colors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_colors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_colors_code` (`code`),
  UNIQUE KEY `ix_product_colors_name` (`name`),
  KEY `ix_product_colors_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_colors`
--

LOCK TABLES `product_colors` WRITE;
/*!40000 ALTER TABLE `product_colors` DISABLE KEYS */;
INSERT INTO `product_colors` VALUES (1,'Merah','MRH','Warna Merah'),(2,'Test','TST',NULL);
/*!40000 ALTER TABLE `product_colors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_motifs`
--

DROP TABLE IF EXISTS `product_motifs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_motifs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_motifs_code` (`code`),
  UNIQUE KEY `ix_product_motifs_name` (`name`),
  KEY `ix_product_motifs_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_motifs`
--

LOCK TABLES `product_motifs` WRITE;
/*!40000 ALTER TABLE `product_motifs` DISABLE KEYS */;
INSERT INTO `product_motifs` VALUES (1,'SEI','SEI','Motif SEI'),(2,'Test','TST',NULL),(3,'Strimin','STM','Strimin');
/*!40000 ALTER TABLE `product_motifs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_movements`
--

DROP TABLE IF EXISTS `product_movements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_movements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `type` enum('IN','OUT','TRANSFER') COLLATE utf8mb4_unicode_ci NOT NULL,
  `quantity` int NOT NULL,
  `reference` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  `notes` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_id` int NOT NULL,
  `reason` enum('RECEIVE_FROM_FACTORY','SHOWROOM_TRANSFER','GIFT','SALES_SAMPLE','PHOTO_SHOOT','TV_STUDIO','DAMAGED','MISSING','STOCK_OPNAME','OTHER') COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_placement_id` int DEFAULT NULL,
  `destination_placement_id` int DEFAULT NULL,
  `reference_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `reference_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_product_movements_id` (`id`),
  KEY `destination_placement_id` (`destination_placement_id`),
  KEY `source_placement_id` (`source_placement_id`),
  CONSTRAINT `product_movements_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_movements_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `product_movements_ibfk_5` FOREIGN KEY (`destination_placement_id`) REFERENCES `product_placements` (`id`),
  CONSTRAINT `product_movements_ibfk_6` FOREIGN KEY (`source_placement_id`) REFERENCES `product_placements` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_movements`
--

LOCK TABLES `product_movements` WRITE;
/*!40000 ALTER TABLE `product_movements` DISABLE KEYS */;
INSERT INTO `product_movements` VALUES (1,1,'IN',1,'','2026-07-07 16:50:07','',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(2,3,'IN',1,'','2026-07-07 16:51:08','',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(3,1,'IN',1,'','2026-07-07 17:06:00','',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(4,1,'TRANSFER',1,'','2026-07-07 17:06:15','',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(5,1,'IN',-1,NULL,'2026-07-07 17:27:40','Stock Opname Adjustment',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(6,1,'TRANSFER',1,'','2026-07-09 10:20:22','Dipinjam untuk Foto',1,'RECEIVE_FROM_FACTORY',NULL,NULL,NULL,NULL),(7,1,'IN',11,NULL,'2026-07-15 19:46:07','Masuk',1,'RECEIVE_FROM_FACTORY',NULL,1,NULL,NULL),(8,1,'IN',11,NULL,'2026-07-15 19:56:32','Ok',1,'RECEIVE_FROM_FACTORY',NULL,1,NULL,NULL),(9,1,'OUT',1,NULL,'2026-07-15 19:57:06','',1,'OTHER',1,NULL,NULL,NULL),(10,1,'IN',1,NULL,'2026-07-15 19:57:32','',1,'RECEIVE_FROM_FACTORY',NULL,1,NULL,NULL),(11,1,'OUT',5,NULL,'2026-07-15 20:00:34','Dibawa tamu',1,'OTHER',1,NULL,NULL,NULL),(12,1,'IN',1,NULL,'2026-07-15 20:01:11','',1,'RECEIVE_FROM_FACTORY',NULL,1,NULL,NULL),(13,1,'OUT',17,NULL,'2026-07-15 20:04:32','Tamu',1,'STOCK_OPNAME',1,NULL,NULL,NULL),(14,1,'OUT',1,NULL,'2026-07-16 14:36:17','',1,'OTHER',1,NULL,NULL,NULL),(15,1,'IN',15,NULL,'2026-07-16 14:37:03','',1,'RECEIVE_FROM_FACTORY',NULL,1,NULL,NULL);
/*!40000 ALTER TABLE `product_movements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_placement_stocks`
--

DROP TABLE IF EXISTS `product_placement_stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_placement_stocks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `placement_id` int NOT NULL,
  `quantity` int NOT NULL,
  `reserved_quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uix_product_placement_stock` (`product_id`,`placement_id`),
  KEY `placement_id` (`placement_id`),
  KEY `ix_product_placement_stocks_id` (`id`),
  CONSTRAINT `product_placement_stocks_ibfk_1` FOREIGN KEY (`placement_id`) REFERENCES `product_placements` (`id`),
  CONSTRAINT `product_placement_stocks_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_placement_stocks`
--

LOCK TABLES `product_placement_stocks` WRITE;
/*!40000 ALTER TABLE `product_placement_stocks` DISABLE KEYS */;
INSERT INTO `product_placement_stocks` VALUES (1,1,1,15,0);
/*!40000 ALTER TABLE `product_placement_stocks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_placements`
--

DROP TABLE IF EXISTS `product_placements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_placements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `code` varchar(50) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `type_id` int NOT NULL,
  `parent_id` int DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `level` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_placements_code` (`code`),
  KEY `parent_id` (`parent_id`),
  KEY `type_id` (`type_id`),
  KEY `ix_product_placements_id` (`id`),
  KEY `ix_product_placements_name` (`name`),
  CONSTRAINT `product_placements_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `product_placements` (`id`),
  CONSTRAINT `product_placements_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `placement_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_placements`
--

LOCK TABLES `product_placements` WRITE;
/*!40000 ALTER TABLE `product_placements` DISABLE KEYS */;
INSERT INTO `product_placements` VALUES (1,'RAK-A01','Rak Kanan',1,NULL,1,1),(2,'A01','Unit A01',2,NULL,1,1);
/*!40000 ALTER TABLE `product_placements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_sub_motifs`
--

DROP TABLE IF EXISTS `product_sub_motifs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_sub_motifs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_sub_motifs_code` (`code`),
  UNIQUE KEY `ix_product_sub_motifs_name` (`name`),
  KEY `ix_product_sub_motifs_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_sub_motifs`
--

LOCK TABLES `product_sub_motifs` WRITE;
/*!40000 ALTER TABLE `product_sub_motifs` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_sub_motifs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_types`
--

DROP TABLE IF EXISTS `product_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_types` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_product_types_code` (`code`),
  UNIQUE KEY `ix_product_types_name` (`name`),
  KEY `ix_product_types_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_types`
--

LOCK TABLES `product_types` WRITE;
/*!40000 ALTER TABLE `product_types` DISABLE KEYS */;
INSERT INTO `product_types` VALUES (1,'Sarung','SRG','Sarung Wadimor\n'),(2,'Test','TST',NULL);
/*!40000 ALTER TABLE `product_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type_id` int NOT NULL,
  `category_id` int NOT NULL,
  `motif_id` int NOT NULL,
  `sub_motif_id` int DEFAULT NULL,
  `color_id` int NOT NULL,
  `variant` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `image_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `sku` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `display_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` enum('ACTIVE','INACTIVE','DISCONTINUED') COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_products_sku` (`sku`),
  KEY `category_id` (`category_id`),
  KEY `color_id` (`color_id`),
  KEY `motif_id` (`motif_id`),
  KEY `sub_motif_id` (`sub_motif_id`),
  KEY `type_id` (`type_id`),
  KEY `ix_products_id` (`id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `product_categories` (`id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`color_id`) REFERENCES `product_colors` (`id`),
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`motif_id`) REFERENCES `product_motifs` (`id`),
  CONSTRAINT `products_ibfk_4` FOREIGN KEY (`sub_motif_id`) REFERENCES `product_sub_motifs` (`id`),
  CONSTRAINT `products_ibfk_5` FOREIGN KEY (`type_id`) REFERENCES `product_types` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,1,1,1,NULL,1,NULL,'https://api.wadimor.co.id/storage/images/gallery/900e4a2f-ff22-4b3d-83c2-5683a287c7a7.webp','SRG-GM-SEI-MRH-0001','Sarung Grandmaster SEI Merah','ACTIVE'),(3,1,1,1,NULL,1,NULL,NULL,'SRG-GM-SEI-MRH-0003','Sarung Grandmaster SEI Merah','ACTIVE'),(4,1,8,1,NULL,2,NULL,NULL,'SRG-BM-SEI-TST-0004','Sarung Balimoon SEI Test','ACTIVE'),(5,1,1,1,NULL,1,NULL,NULL,'SRG-GM-SEI-MRH-0005','Sarung Grandmaster SEI Merah','ACTIVE');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_roles_name` (`name`),
  KEY `ix_roles_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'ADMIN','System Administrator'),(2,'MANAGER','System Manager'),(3,'STAFF','System Staff'),(4,'CREATIVE','System Creative');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `units`
--

DROP TABLE IF EXISTS `units`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `units` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_units_name` (`name`),
  KEY `ix_units_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `units`
--

LOCK TABLES `units` WRITE;
/*!40000 ALTER TABLE `units` DISABLE KEYS */;
/*!40000 ALTER TABLE `units` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hashed_password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `role_id` int NOT NULL,
  `division_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `role_id` (`role_id`),
  KEY `ix_users_id` (`id`),
  KEY `division_id` (`division_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `users_ibfk_2` FOREIGN KEY (`division_id`) REFERENCES `divisions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'adminsuper','admin@cd.wadimor.co.id','$2b$12$J2DNwqVmLd9.ytgv.3TGue4Dm0H1VkbvcB9J3rsMcBFcgbJl.EFe2','Super Administrator',1,1,1),(2,'creative','creative@example.com','$2b$12$P1ZjqNAL2S8PhaK3PmPxxePIpAEW/615UuEypDKnN6tyU8RewH4Ry','creative',1,4,1),(3,'test_user','test_user@example.com','$2b$12$cWzo/rMDik0uuY4NlvoiBuhwf6GFKwQGUX6mm9wnOiTd4/0BKOj7e','Test User3',1,4,1),(8,'wafi','wafi@cd.wadimor.co.id','$2b$12$kzUMPJK9a0EO6Zq3T485XuV.IX1b19ga3xcEEQyXhjUP15V.v1sN.','Abdul Wafi',1,4,1),(9,'Fajar','Fajar@cd.wadimor.co.id','$2b$12$ICyVKHauEtkXv9ttFDoP3ulZw2BZGEjXVTae5IuJvtFejhcmjO31e','Ahmad Fajar Fedrianto',1,4,1),(10,'irhas','irhas@cd.wadimor.co.id','$2b$12$mh2U2UX4pSMASe/w5yoTp.kyD5BBW3da9SDbSeq8MHjgbq4p45myi','Irhas Mauludi',1,4,1),(11,'miko','miko@cd.wadimor.co.id','$2b$12$g3h7.9qRuz1Jb.mhxFSf6.G6n9WFSDiT/bG0mGgcNeVUobfY./Avq','Sujatmiko',1,4,1),(12,'rizal','rizal@cd.wadimor.co.id','$2b$12$oZzz54RbfskCfuv9yNCmp.PFO1OLqYD/9ooJBv/MzSvloL9jK25Tu','Muhammad Rizal',1,4,1),(13,'anda','anda@cd.wadimor.co.id','$2b$12$c8ddeUgmeigqw3hf7oN2DeThxv2LuH21VOdLLoKCDxdzlOcGuahxm','Anda Rahmad',1,1,1),(14,'irsyad','irsyad@cd.wadimor.co.id','$2b$12$1JntJ7m.jmSibmilugObieSl3swan2fSKnpM99S48E9kfupPGaiP6','Irsyad Maulana',1,1,1),(15,'tarmunah','tarmunah@cd.wadimor.co.id','$2b$12$Xj7m3OScJoF4sIENqsXQCuG/TN8LLyEqbSc7mVrGsvI/.oybXza5i','Tarmunah',1,4,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_activities`
--

DROP TABLE IF EXISTS `work_activities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_activities` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `category_id` int NOT NULL,
  `activity_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `notes` text COLLATE utf8mb4_unicode_ci,
  `status` enum('READY','WORKING','PAUSED','COMPLETED','CANCELLED') COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `updated_by` int DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  `worked_seconds` int NOT NULL DEFAULT '0',
  `current_session_started_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `created_by` (`created_by`),
  KEY `updated_by` (`updated_by`),
  KEY `user_id` (`user_id`),
  KEY `ix_work_activities_id` (`id`),
  CONSTRAINT `work_activities_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `work_categories` (`id`),
  CONSTRAINT `work_activities_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`),
  CONSTRAINT `work_activities_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`),
  CONSTRAINT `work_activities_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_activities`
--

LOCK TABLES `work_activities` WRITE;
/*!40000 ALTER TABLE `work_activities` DISABLE KEYS */;
INSERT INTO `work_activities` VALUES (18,1,1,'Editing - Quotes Jawa','','COMPLETED','2026-07-10 23:32:58','2026-07-10 23:33:23',1,1,0,NULL,'2026-07-10 23:32:42','2026-07-10 23:33:23',25,NULL),(19,1,1,'Editing - Quotes Jawa','','CANCELLED','2026-07-10 23:38:22','2026-07-10 23:38:37',1,1,0,NULL,'2026-07-10 23:38:14','2026-07-10 23:38:37',0,NULL),(20,1,1,'Editing - Quotes Jawa','','CANCELLED','2026-07-10 23:39:27','2026-07-11 20:17:17',1,1,0,NULL,'2026-07-10 23:39:20','2026-07-11 20:17:17',0,NULL),(21,1,1,'Editing - Quotes Jawa','','COMPLETED','2026-07-11 20:17:44','2026-07-11 20:38:56',1,1,0,NULL,'2026-07-11 20:17:28','2026-07-11 20:38:56',1272,NULL),(22,1,1,'Editing - Quotes Jawa','','COMPLETED','2026-07-13 21:26:58','2026-07-13 21:30:51',1,1,0,NULL,'2026-07-13 21:26:28','2026-07-13 21:30:51',233,NULL),(23,1,1,'Editing Video Quotes Jawa','','COMPLETED','2026-07-14 19:28:00','2026-07-14 19:28:45',1,1,0,NULL,'2026-07-14 19:24:45','2026-07-14 19:28:45',45,NULL),(24,1,1,'teaser video','','COMPLETED','2026-07-14 19:36:30','2026-07-14 19:44:58',1,1,0,NULL,'2026-07-14 19:35:35','2026-07-14 19:44:58',508,NULL),(25,1,1,'TVC','','CANCELLED','2026-07-15 00:04:50','2026-07-15 00:05:07',1,1,0,NULL,'2026-07-15 00:03:58','2026-07-15 00:05:07',0,NULL),(26,1,1,'Rert','','CANCELLED','2026-07-15 09:46:39','2026-07-15 09:48:24',1,1,0,NULL,'2026-07-15 09:46:09','2026-07-15 09:48:24',0,NULL),(27,1,1,',','A,','COMPLETED','2026-07-15 10:04:39','2026-07-15 10:06:06',1,1,0,NULL,'2026-07-15 10:04:19','2026-07-15 10:06:06',87,NULL),(28,10,1,'Edit video','','COMPLETED','2026-07-15 21:22:50','2026-07-15 21:23:38',10,10,0,NULL,'2026-07-15 21:14:52','2026-07-15 21:23:38',47,NULL),(33,9,3,'kjhjk','','READY',NULL,NULL,9,9,0,NULL,'2026-07-16 08:25:27','2026-07-16 08:25:27',0,NULL),(38,9,4,'xzczxcxzc','','READY',NULL,NULL,9,9,0,NULL,'2026-07-16 08:30:04','2026-07-16 08:30:04',0,NULL),(39,10,1,'cvbcvbc','','READY',NULL,NULL,10,10,0,NULL,'2026-07-16 08:33:01','2026-07-16 08:33:01',0,NULL),(40,10,22,'zczczczcx','','READY',NULL,NULL,10,10,0,NULL,'2026-07-16 08:57:12','2026-07-16 08:57:12',0,NULL),(41,10,11,'JACQUARD ANTIK 2026','','COMPLETED','2026-07-16 08:59:59','2026-07-16 09:06:04',10,10,0,NULL,'2026-07-16 08:57:54','2026-07-16 09:06:04',360,NULL),(42,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 09:08:12','2026-07-16 09:08:41',10,10,0,NULL,'2026-07-16 09:07:19','2026-07-16 09:08:41',29,NULL),(43,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 09:09:41','2026-07-16 09:11:22',10,10,0,NULL,'2026-07-16 09:09:24','2026-07-16 09:11:22',101,NULL),(44,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 09:12:33','2026-07-16 09:12:54',10,10,0,NULL,'2026-07-16 09:12:07','2026-07-16 09:12:54',21,NULL),(45,14,33,'Membuat Daftar Motif','Category, Motifs, dan Sub Motifs','COMPLETED','2026-07-16 09:14:37','2026-07-16 15:57:47',14,14,0,NULL,'2026-07-16 09:13:09','2026-07-16 15:57:47',11617,NULL),(46,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 09:14:09','2026-07-16 09:31:28',10,10,0,NULL,'2026-07-16 09:13:34','2026-07-16 09:31:28',1038,NULL),(47,8,29,'Ke departemen printing','Menemui pak Abdullah basorah','READY',NULL,NULL,8,8,0,NULL,'2026-07-16 09:24:24','2026-07-16 09:24:24',0,NULL),(48,8,29,'Ke departemen printing','Menemui pak Abdullah Basorah','COMPLETED','2026-07-16 09:26:21','2026-07-16 09:42:14',8,8,0,NULL,'2026-07-16 09:25:21','2026-07-16 09:42:14',953,NULL),(49,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 09:43:43','2026-07-16 10:19:20',10,10,0,NULL,'2026-07-16 09:43:19','2026-07-16 10:19:20',2136,NULL),(50,8,22,'Menyetime sarung untuk foto katalog supaya hasil foto sarung tampak bagus tnpa ada lipatan dalam kain sarung','','COMPLETED','2026-07-16 09:52:30','2026-07-16 10:31:36',8,8,0,NULL,'2026-07-16 09:51:21','2026-07-16 10:31:36',2346,NULL),(51,8,22,'Menyetime sarung untuk foto katalog supaya hasil foto sarung tampak bagus tnpa ada lipatan dalam kain sarung','','READY',NULL,NULL,8,8,0,NULL,'2026-07-16 09:51:49','2026-07-16 09:51:49',0,NULL),(52,9,3,'Foto studio ','Menata sarung untuk foto catalog ','COMPLETED','2026-07-16 10:06:24','2026-07-16 11:47:48',9,9,0,NULL,'2026-07-16 10:01:32','2026-07-16 11:47:48',6084,NULL),(53,13,1,'Editing Video Konten Jawa Kuno','- JK Aratula\n- JK Mangir\n- JK Catur Mukti','COMPLETED','2026-07-16 10:03:13','2026-07-16 15:58:19',13,13,0,NULL,'2026-07-16 10:01:59','2026-07-16 15:58:19',21305,NULL),(54,9,3,'Foto studio ','Menata sarung untuk catalog ','CANCELLED','2026-07-16 10:04:48','2026-07-16 10:04:57',9,9,0,NULL,'2026-07-16 10:02:17','2026-07-16 10:04:57',9,NULL),(55,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 10:20:43','2026-07-16 10:55:10',10,10,0,NULL,'2026-07-16 10:20:20','2026-07-16 10:55:10',2067,NULL),(56,11,3,'Set camera ','Persiapan foto sarung untuk catalog ','COMPLETED','2026-07-16 10:28:15','2026-07-16 15:56:18',11,11,0,NULL,'2026-07-16 10:27:27','2026-07-16 15:56:18',13345,NULL),(57,15,22,'Menyetrika Sarung Catalog','Menyetrika Sarung materi Catalog Produk','COMPLETED','2026-07-16 10:29:22','2026-07-16 11:52:38',15,15,0,NULL,'2026-07-16 10:28:54','2026-07-16 11:52:38',4995,NULL),(58,8,21,'Foto  sarung wadimor untuk katalog','','READY',NULL,NULL,8,8,0,NULL,'2026-07-16 10:32:01','2026-07-16 10:32:01',0,NULL),(59,8,21,'Foto  sarung wadimor untuk katalog','','COMPLETED','2026-07-16 10:35:50','2026-07-16 11:46:42',8,8,0,NULL,'2026-07-16 10:32:20','2026-07-16 11:46:42',4251,NULL),(60,10,11,'Jacquard antik 2026','','COMPLETED','2026-07-16 10:56:31','2026-07-16 11:31:12',10,10,0,NULL,'2026-07-16 10:56:10','2026-07-16 11:31:12',2080,NULL),(61,9,2,'Meminta grafis di ppic ','','COMPLETED','2026-07-16 13:12:06','2026-07-16 14:33:14',9,9,0,NULL,'2026-07-16 13:11:18','2026-07-16 14:33:14',4867,NULL),(62,8,21,'Foto sarung untuk katalog','','READY',NULL,NULL,8,8,0,NULL,'2026-07-16 13:35:54','2026-07-16 13:35:54',0,NULL),(63,8,21,'Foto sarung untuk katalog','','COMPLETED','2026-07-16 13:37:01','2026-07-16 15:55:54',8,8,0,NULL,'2026-07-16 13:36:09','2026-07-16 15:55:54',8333,NULL);
/*!40000 ALTER TABLE `work_activities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_assets`
--

DROP TABLE IF EXISTS `work_assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_assets` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_activity_id` int NOT NULL,
  `item_id` int NOT NULL,
  `location_id` int NOT NULL,
  `quantity` int NOT NULL,
  `status` varchar(50) NOT NULL,
  `borrowed_at` datetime DEFAULT NULL,
  `returned_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  KEY `location_id` (`location_id`),
  KEY `work_activity_id` (`work_activity_id`),
  KEY `ix_work_assets_id` (`id`),
  CONSTRAINT `work_assets_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  CONSTRAINT `work_assets_ibfk_2` FOREIGN KEY (`location_id`) REFERENCES `locations` (`id`),
  CONSTRAINT `work_assets_ibfk_3` FOREIGN KEY (`work_activity_id`) REFERENCES `work_activities` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_assets`
--

LOCK TABLES `work_assets` WRITE;
/*!40000 ALTER TABLE `work_assets` DISABLE KEYS */;
/*!40000 ALTER TABLE `work_assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_categories`
--

DROP TABLE IF EXISTS `work_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_work_categories_name` (`name`),
  KEY `ix_work_categories_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_categories`
--

LOCK TABLES `work_categories` WRITE;
/*!40000 ALTER TABLE `work_categories` DISABLE KEYS */;
INSERT INTO `work_categories` VALUES (18,'Asset Management'),(39,'Brand Guidline'),(5,'Briefing & Coordination\r\n'),(36,'Budget Management'),(7,'Campaign & Branding'),(8,'Content Planning'),(9,'Copywriting'),(40,'Customer Experience'),(19,'Data Backup'),(15,'Digital Marketing'),(25,'Display & Visual Merchandising'),(33,'Documentation'),(21,'Equipment Management'),(31,'External Communication'),(2,'Graphic Design'),(20,'Inventory Management'),(35,'KPI & Performance Review'),(29,'Logistics'),(17,'Marketplace Management'),(30,'Media Relations'),(12,'Motion Graphic'),(11,'Photo Editing'),(3,'Photography'),(28,'Production Support'),(6,'Project Management'),(22,'Property Management'),(32,'Quality Control'),(34,'Reporting'),(37,'Research & Development'),(24,'Showroom Management'),(16,'Social Media Content'),(38,'SOP & Workflow'),(23,'Studio Management'),(26,'Styling'),(27,'Talent Management'),(10,'Translation'),(1,'Video Editing'),(4,'Videography'),(14,'Web Development'),(13,'Website Management');
/*!40000 ALTER TABLE `work_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `work_evidences`
--

DROP TABLE IF EXISTS `work_evidences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `work_evidences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `work_activity_id` int NOT NULL,
  `type` enum('BEFORE','PROGRESS','AFTER') NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_size` int NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `evidence_order` int NOT NULL,
  `uploaded_by` int NOT NULL,
  `uploaded_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `uploaded_by` (`uploaded_by`),
  KEY `work_activity_id` (`work_activity_id`),
  KEY `ix_work_evidences_id` (`id`),
  CONSTRAINT `work_evidences_ibfk_1` FOREIGN KEY (`uploaded_by`) REFERENCES `users` (`id`),
  CONSTRAINT `work_evidences_ibfk_2` FOREIGN KEY (`work_activity_id`) REFERENCES `work_activities` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `work_evidences`
--

LOCK TABLES `work_evidences` WRITE;
/*!40000 ALTER TABLE `work_evidences` DISABLE KEYS */;
INSERT INTO `work_evidences` VALUES (5,41,'BEFORE','uploads/work_activity/41/before_1784167198_Screenshot (7).png','Screenshot (7).png',1946533,'image/png',NULL,1,10,'2026-07-16 08:59:58'),(6,41,'AFTER','uploads/work_activity/41/after_1784167563_image.jpg','image.jpg',2508617,'image/jpeg',NULL,1,10,'2026-07-16 09:06:04'),(7,42,'BEFORE','uploads/work_activity/42/before_1784167691_image.jpg','image.jpg',3621732,'image/jpeg',NULL,1,10,'2026-07-16 09:08:11'),(8,42,'AFTER','uploads/work_activity/42/after_1784167720_image.jpg','image.jpg',3227767,'image/jpeg',NULL,1,10,'2026-07-16 09:08:40'),(9,43,'BEFORE','uploads/work_activity/43/before_1784167780_image.jpg','image.jpg',3613904,'image/jpeg',NULL,1,10,'2026-07-16 09:09:40'),(10,43,'AFTER','uploads/work_activity/43/after_1784167882_image.jpg','image.jpg',2999685,'image/jpeg',NULL,1,10,'2026-07-16 09:11:22'),(11,44,'BEFORE','uploads/work_activity/44/before_1784167951_image.jpg','image.jpg',3598308,'image/jpeg',NULL,1,10,'2026-07-16 09:12:31'),(12,44,'AFTER','uploads/work_activity/44/after_1784167973_image.jpg','image.jpg',2932593,'image/jpeg',NULL,1,10,'2026-07-16 09:12:54'),(13,46,'BEFORE','uploads/work_activity/46/before_1784168048_image.jpg','image.jpg',3730440,'image/jpeg',NULL,1,10,'2026-07-16 09:14:09'),(14,45,'BEFORE','uploads/work_activity/45/before_1784168071_17841679997536812425376029161188.jpg','17841679997536812425376029161188.jpg',2615754,'image/jpeg','Category, Motifs, dan Sub Motifs',1,14,'2026-07-16 09:14:32'),(15,48,'BEFORE','uploads/work_activity/48/before_1784168780_17841687526047676146375001658852.jpg','17841687526047676146375001658852.jpg',2909202,'image/jpeg',NULL,1,8,'2026-07-16 09:26:20'),(16,46,'AFTER','uploads/work_activity/46/after_1784169087_image.jpg','image.jpg',3003374,'image/jpeg',NULL,1,10,'2026-07-16 09:31:27'),(17,48,'AFTER','uploads/work_activity/48/after_1784169734_17841697012826233717875090046759.jpg','17841697012826233717875090046759.jpg',3502906,'image/jpeg','Ambil foto sampel sarung untuk katalog dari pak Abdullah basorah',1,8,'2026-07-16 09:42:14'),(18,49,'BEFORE','uploads/work_activity/49/before_1784169822_image.jpg','image.jpg',3785682,'image/jpeg',NULL,1,10,'2026-07-16 09:43:42'),(19,50,'BEFORE','uploads/work_activity/50/before_1784170349_17841703265197131909343658042511.jpg','17841703265197131909343658042511.jpg',3306983,'image/jpeg',NULL,1,8,'2026-07-16 09:52:29'),(20,53,'BEFORE','uploads/work_activity/53/before_1784170992_image.jpg','image.jpg',2858891,'image/jpeg',NULL,1,13,'2026-07-16 10:03:12'),(21,54,'BEFORE','uploads/work_activity/54/before_1784171087_17841710765976063460522990374241.jpg','17841710765976063460522990374241.jpg',3067816,'image/jpeg',NULL,1,9,'2026-07-16 10:04:48'),(22,52,'BEFORE','uploads/work_activity/52/before_1784171183_17841711096732003552387259890497.jpg','17841711096732003552387259890497.jpg',2749842,'image/jpeg','Menata sarung untuk foto catalog ',1,9,'2026-07-16 10:06:24'),(23,49,'AFTER','uploads/work_activity/49/after_1784171959_image.jpg','image.jpg',3227381,'image/jpeg',NULL,1,10,'2026-07-16 10:19:20'),(24,55,'BEFORE','uploads/work_activity/55/before_1784172042_image.jpg','image.jpg',3764398,'image/jpeg',NULL,1,10,'2026-07-16 10:20:43'),(25,45,'PROGRESS','uploads/work_activity/45/progress_1784172295_WhatsApp Image 2026-07-16 at 10.24.34.jpeg','WhatsApp Image 2026-07-16 at 10.24.34.jpeg',388586,'image/jpeg',NULL,1,14,'2026-07-16 10:24:55'),(26,56,'BEFORE','uploads/work_activity/56/before_1784172494_image.jpg','image.jpg',1899201,'image/jpeg',NULL,1,11,'2026-07-16 10:28:15'),(27,57,'BEFORE','uploads/work_activity/57/before_1784172562_WhatsApp Image 2026-07-16 at 10.23.45.jpeg','WhatsApp Image 2026-07-16 at 10.23.45.jpeg',121782,'image/jpeg','Menyetrika Produk Sarung',1,15,'2026-07-16 10:29:22'),(28,50,'AFTER','uploads/work_activity/50/after_1784172695_17841726392864762582209067565374.jpg','17841726392864762582209067565374.jpg',3114599,'image/jpeg','Hasil steam sarung untuk foto katalog supaya hasil bagus dan maksimal dalam tampilan di katalog',1,8,'2026-07-16 10:31:36'),(29,56,'PROGRESS','uploads/work_activity/56/progress_1784172745_image.jpg','image.jpg',2873246,'image/jpeg','Foto  sarung WD.BALI NICE ',1,11,'2026-07-16 10:32:26'),(30,59,'BEFORE','uploads/work_activity/59/before_1784172948_1784172889657563826361949646342.jpg','1784172889657563826361949646342.jpg',2687226,'image/jpeg',NULL,1,8,'2026-07-16 10:35:49'),(31,55,'AFTER','uploads/work_activity/55/after_1784174110_image.jpg','image.jpg',3780344,'image/jpeg',NULL,1,10,'2026-07-16 10:55:10'),(32,60,'BEFORE','uploads/work_activity/60/before_1784174189_image.jpg','image.jpg',3718232,'image/jpeg',NULL,1,10,'2026-07-16 10:56:30'),(33,56,'PROGRESS','uploads/work_activity/56/progress_1784174467_image.jpg','image.jpg',2262772,'image/jpeg','Foto sarung Bali moon nalar ',2,11,'2026-07-16 11:01:08'),(34,60,'AFTER','uploads/work_activity/60/after_1784176271_Screenshot (8).png','Screenshot (8).png',3228740,'image/png',NULL,1,10,'2026-07-16 11:31:11'),(35,45,'PROGRESS','uploads/work_activity/45/progress_1784177118_image.png','image.png',192587,'image/png','Pause, lanjut lagi nanti setelah istirahat',2,14,'2026-07-16 11:45:18'),(36,59,'AFTER','uploads/work_activity/59/after_1784177201_17841771780942585270132950212956.jpg','17841771780942585270132950212956.jpg',4492876,'image/jpeg',NULL,1,8,'2026-07-16 11:46:42'),(37,52,'AFTER','uploads/work_activity/52/after_1784177267_17841772028973459806466175857605.jpg','17841772028973459806466175857605.jpg',3144440,'image/jpeg','selesai ',1,9,'2026-07-16 11:47:48'),(38,57,'AFTER','uploads/work_activity/57/after_1784177557_WhatsApp Image 2026-07-16 at 11.45.50.jpeg','WhatsApp Image 2026-07-16 at 11.45.50.jpeg',125897,'image/jpeg','Hasil setrika untuk foto katalog agar hasil di kamera tmpak maksimal',1,15,'2026-07-16 11:52:38'),(39,61,'BEFORE','uploads/work_activity/61/before_1784182325_17841822940376426464934470165741.jpg','17841822940376426464934470165741.jpg',3012076,'image/jpeg',NULL,1,9,'2026-07-16 13:12:05'),(40,63,'BEFORE','uploads/work_activity/63/before_1784183820_1784183781295618331320139358220.jpg','1784183781295618331320139358220.jpg',3375319,'image/jpeg',NULL,1,8,'2026-07-16 13:37:01'),(41,61,'AFTER','uploads/work_activity/61/after_1784187193_17841871280421031865318359363831.jpg','17841871280421031865318359363831.jpg',2957348,'image/jpeg','selesai \r\n',1,9,'2026-07-16 14:33:13'),(42,56,'PROGRESS','uploads/work_activity/56/progress_1784192146_image.jpg','image.jpg',2310906,'image/jpeg','Done',3,11,'2026-07-16 15:55:46'),(43,63,'AFTER','uploads/work_activity/63/after_1784192153_17841921159213567822396562370200.jpg','17841921159213567822396562370200.jpg',3710806,'image/jpeg','Telah selesai untuk hari ini',1,8,'2026-07-16 15:55:54'),(44,56,'AFTER','uploads/work_activity/56/after_1784192177_image.jpg','image.jpg',2454751,'image/jpeg','Done',1,11,'2026-07-16 15:56:18'),(45,45,'AFTER','uploads/work_activity/45/after_1784192266_17841922434283752504548178248270.jpg','17841922434283752504548178248270.jpg',2344540,'image/jpeg',NULL,1,14,'2026-07-16 15:57:47'),(46,53,'PROGRESS','uploads/work_activity/53/progress_1784192268_image.jpg','image.jpg',2135309,'image/jpeg','Done',1,13,'2026-07-16 15:57:48'),(47,53,'AFTER','uploads/work_activity/53/after_1784192298_image.jpg','image.jpg',2153944,'image/jpeg','Done',1,13,'2026-07-16 15:58:18');
/*!40000 ALTER TABLE `work_evidences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'csms_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-16 16:24:03
