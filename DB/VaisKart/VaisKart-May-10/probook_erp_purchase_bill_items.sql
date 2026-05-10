-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: probook_erp
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `purchase_bill_items`
--

DROP TABLE IF EXISTS `purchase_bill_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase_bill_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `purchase_id` int NOT NULL,
  `item_id` int NOT NULL,
  `qty` decimal(10,2) NOT NULL,
  `rate` decimal(12,2) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `gst_rate` decimal(5,2) DEFAULT NULL,
  `gst_amount` decimal(12,2) DEFAULT NULL,
  `total` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `purchase_id` (`purchase_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `purchase_bill_items_ibfk_1` FOREIGN KEY (`purchase_id`) REFERENCES `purchase_bills` (`id`),
  CONSTRAINT `purchase_bill_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_bill_items`
--

LOCK TABLES `purchase_bill_items` WRITE;
/*!40000 ALTER TABLE `purchase_bill_items` DISABLE KEYS */;
INSERT INTO `purchase_bill_items` VALUES (1,1,1,288.00,19.49,5613.12,18.00,1010.36,6623.48),(2,1,2,288.00,22.88,6589.44,18.00,1186.10,7775.54),(3,1,3,288.00,26.27,7565.76,18.00,1361.84,8927.60);
/*!40000 ALTER TABLE `purchase_bill_items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-11  1:38:46
