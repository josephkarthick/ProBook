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
-- Table structure for table `sales_invoices`
--

DROP TABLE IF EXISTS `sales_invoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_invoices` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_id` int DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `sales_order_id` int DEFAULT NULL,
  `invoice_no` varchar(20) DEFAULT NULL,
  `invoice_date` date DEFAULT NULL,
  `total_amount` decimal(12,2) DEFAULT NULL,
  `tax_amount` decimal(12,2) DEFAULT NULL,
  `grand_total` decimal(12,2) DEFAULT NULL,
  `paid_amount` decimal(12,2) DEFAULT NULL,
  `balance_amount` decimal(12,2) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  KEY `customer_id` (`customer_id`),
  KEY `sales_order_id` (`sales_order_id`),
  CONSTRAINT `sales_invoices_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `sales_invoices_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `sales_invoices_ibfk_3` FOREIGN KEY (`sales_order_id`) REFERENCES `sales_orders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_invoices`
--

LOCK TABLES `sales_invoices` WRITE;
/*!40000 ALTER TABLE `sales_invoices` DISABLE KEYS */;
INSERT INTO `sales_invoices` VALUES (1,1,1,NULL,'SI-00001','2026-03-26',1680.00,302.40,1982.40,0.00,1982.40,'UNPAID','POSTED'),(2,1,1,NULL,'SI-00002','2026-03-26',2520.00,453.60,2973.60,0.00,2973.60,'UNPAID','POSTED'),(3,1,1,NULL,'SI-00003','2026-03-26',252.00,45.36,297.36,0.00,297.36,'UNPAID','POSTED'),(4,1,1,NULL,'SI-00004','2026-03-26',2520.00,453.60,2973.60,0.00,2973.60,'UNPAID','POSTED'),(5,1,1,NULL,'SI-00005','2026-03-26',840.00,151.20,991.20,0.00,991.20,'UNPAID','POSTED'),(6,1,1,NULL,'SI-00006','2026-03-26',2520.00,453.60,2973.60,0.00,2973.60,'UNPAID','POSTED'),(7,1,1,NULL,'SI-00007','2026-03-26',2940.00,529.20,3469.20,0.00,3469.20,'UNPAID','POSTED'),(8,1,1,NULL,'SI-00008','2026-03-26',2520.00,453.60,2973.60,0.00,2973.60,'UNPAID','POSTED'),(9,1,1,NULL,'SI-00009','2026-03-26',420.00,75.60,495.60,0.00,495.60,'UNPAID','POSTED'),(10,1,1,NULL,'SI-00010','2026-03-26',420.00,75.60,495.60,0.00,495.60,'UNPAID','POSTED'),(11,1,1,NULL,'SI-00011','2026-03-26',2940.00,529.20,3469.20,0.00,3469.20,'UNPAID','POSTED');
/*!40000 ALTER TABLE `sales_invoices` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-27  2:56:37
