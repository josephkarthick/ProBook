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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `account_code` varchar(20) DEFAULT NULL,
  `name` varchar(150) NOT NULL,
  `account_type` varchar(20) DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `is_group` tinyint(1) DEFAULT NULL,
  `is_system` tinyint(1) DEFAULT NULL,
  `opening_balance` decimal(12,2) DEFAULT NULL,
  `opening_type` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_accounts_id` (`id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `accounts_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,NULL,'Assets','ASSET',NULL,1,1,0.00,NULL),(2,1,NULL,'Liabilities','LIABILITY',NULL,1,1,0.00,NULL),(3,1,NULL,'Equity','EQUITY',NULL,1,1,0.00,NULL),(4,1,NULL,'Income','INCOME',NULL,1,1,0.00,NULL),(5,1,NULL,'Expense','EXPENSE',NULL,1,1,0.00,NULL),(6,1,NULL,'Current Assets','ASSET',1,1,1,0.00,NULL),(7,1,NULL,'Fixed Assets','ASSET',1,1,1,0.00,NULL),(8,1,NULL,'Current Liabilities','LIABILITY',2,1,1,0.00,NULL),(9,1,NULL,'Direct Income','INCOME',4,1,1,0.00,NULL),(10,1,NULL,'Direct Expense','EXPENSE',5,1,1,0.00,NULL),(11,1,NULL,'Indirect Expense','EXPENSE',5,1,1,0.00,NULL),(12,1,NULL,'Cash','ASSET',6,0,1,0.00,NULL),(13,1,NULL,'Bank','ASSET',6,0,1,0.00,NULL),(14,1,NULL,'Accounts Receivable','ASSET',6,0,1,0.00,NULL),(15,1,NULL,'Inventory','ASSET',6,0,1,0.00,NULL),(16,1,NULL,'Input GST','ASSET',6,0,1,0.00,NULL),(17,1,NULL,'Accounts Payable','LIABILITY',8,0,1,0.00,NULL),(18,1,NULL,'GST Payable','LIABILITY',8,0,1,0.00,NULL),(19,1,NULL,'Sales','INCOME',9,0,1,0.00,NULL),(20,1,NULL,'Purchase','EXPENSE',10,0,1,0.00,NULL),(21,1,NULL,'Cost of Goods Sold','EXPENSE',10,0,1,0.00,NULL),(22,1,NULL,'Capital','EQUITY',3,0,1,0.00,NULL),(23,1,NULL,'Karthick','LIABILITY',17,0,0,0.00,NULL);
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-17 16:01:06
