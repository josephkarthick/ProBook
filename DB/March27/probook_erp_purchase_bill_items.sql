-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: probook_erp
-- ------------------------------------------------------
-- Server version	8.0.39

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase_bill_items`
--

LOCK TABLES `purchase_bill_items` WRITE;
/*!40000 ALTER TABLE `purchase_bill_items` DISABLE KEYS */;
INSERT INTO `purchase_bill_items` VALUES (1,1,1,100.00,24.00,2400.00,18.00,432.00,2832.00),(2,2,1,100.00,24.00,2400.00,18.00,432.00,2832.00),(3,3,1,28.00,24.00,672.00,18.00,120.96,792.96),(4,5,1,10.00,24.00,240.00,18.00,43.20,283.20),(5,6,1,288.00,2.00,576.00,18.00,103.68,679.68),(6,7,1,288.00,4.00,1152.00,18.00,207.36,1359.36),(7,12,1,6.00,24.00,144.00,18.00,25.92,169.92),(8,13,1,2.00,24.00,48.00,18.00,8.64,56.64);
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

-- Dump completed on 2026-03-27  2:56:36
