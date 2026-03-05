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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  `account_type` varchar(20) DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `is_group` tinyint(1) DEFAULT NULL,
  `is_system` tinyint(1) DEFAULT NULL,
  `opening_balance` decimal(12,2) DEFAULT NULL,
  `opening_type` varchar(10) DEFAULT NULL,
  `account_code` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_accounts_id` (`id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `accounts_ibfk_2` FOREIGN KEY (`parent_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (9,5,'Available Stocks','LIABILITY',NULL,1,0,0.00,NULL,NULL),(10,1,'Karthick','INCOME',NULL,0,0,0.00,NULL,NULL),(11,7,'Assets','ASSET',NULL,1,1,0.00,NULL,NULL),(12,7,'Liabilities','LIABILITY',NULL,1,1,0.00,NULL,NULL),(13,7,'Equity','EQUITY',NULL,1,1,0.00,NULL,NULL),(14,7,'Income','INCOME',NULL,1,1,0.00,NULL,NULL),(15,7,'Expense','EXPENSE',NULL,1,1,0.00,NULL,NULL),(16,7,'Current Assets','ASSET',11,1,1,0.00,NULL,NULL),(17,7,'Fixed Assets','ASSET',11,1,1,0.00,NULL,NULL),(18,7,'Current Liabilities','LIABILITY',12,1,1,0.00,NULL,NULL),(19,7,'Direct Income','INCOME',14,1,1,0.00,NULL,NULL),(20,7,'Direct Expense','EXPENSE',15,1,1,0.00,NULL,NULL),(21,7,'Indirect Expense','EXPENSE',15,1,1,0.00,NULL,NULL),(22,7,'Cash','ASSET',16,0,1,0.00,NULL,NULL),(23,7,'Bank','ASSET',16,0,1,0.00,NULL,NULL),(24,7,'Accounts Receivable','ASSET',16,0,1,0.00,NULL,NULL),(25,7,'Inventory','ASSET',16,0,1,0.00,NULL,NULL),(26,7,'Accounts Payable','LIABILITY',18,0,1,0.00,NULL,NULL),(27,7,'GST Payable','LIABILITY',18,0,1,0.00,NULL,NULL),(28,7,'Sales','INCOME',19,0,1,0.00,NULL,NULL),(29,7,'Purchase','EXPENSE',20,0,1,0.00,NULL,NULL),(30,7,'Cost of Goods Sold','EXPENSE',20,0,1,0.00,NULL,NULL),(31,7,'Capital','EQUITY',13,0,1,0.00,NULL,NULL),(33,7,'Karthick','LIABILITY',26,0,0,0.00,NULL,NULL),(34,7,'Karthick','LIABILITY',26,0,0,0.00,NULL,NULL),(35,7,'Karthick','LIABILITY',26,0,0,0.00,NULL,NULL);
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

-- Dump completed on 2026-03-05 16:30:11
