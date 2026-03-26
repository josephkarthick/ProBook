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
-- Table structure for table `sales_invoice_items`
--

DROP TABLE IF EXISTS `sales_invoice_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_invoice_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `qty` decimal(10,2) DEFAULT NULL,
  `price` decimal(12,2) DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `gst_rate` decimal(5,2) DEFAULT NULL,
  `gst_amount` decimal(12,2) DEFAULT NULL,
  `total` decimal(12,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `invoice_id` (`invoice_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `sales_invoice_items_ibfk_1` FOREIGN KEY (`invoice_id`) REFERENCES `sales_invoices` (`id`),
  CONSTRAINT `sales_invoice_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_invoice_items`
--

LOCK TABLES `sales_invoice_items` WRITE;
/*!40000 ALTER TABLE `sales_invoice_items` DISABLE KEYS */;
INSERT INTO `sales_invoice_items` VALUES (1,1,1,40.00,42.00,1680.00,18.00,302.40,1982.40),(2,2,1,60.00,42.00,2520.00,18.00,453.60,2973.60),(3,3,1,6.00,42.00,252.00,18.00,45.36,297.36),(4,4,1,60.00,42.00,2520.00,18.00,453.60,2973.60),(5,5,1,20.00,42.00,840.00,18.00,151.20,991.20),(6,6,1,60.00,42.00,2520.00,18.00,453.60,2973.60),(7,7,1,70.00,42.00,2940.00,18.00,529.20,3469.20),(8,8,1,60.00,42.00,2520.00,18.00,453.60,2973.60),(9,9,1,10.00,42.00,420.00,18.00,75.60,495.60),(10,10,1,10.00,42.00,420.00,18.00,75.60,495.60),(11,11,1,70.00,42.00,2940.00,18.00,529.20,3469.20);
/*!40000 ALTER TABLE `sales_invoice_items` ENABLE KEYS */;
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
