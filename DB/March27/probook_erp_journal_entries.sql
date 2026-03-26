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
-- Table structure for table `journal_entries`
--

DROP TABLE IF EXISTS `journal_entries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `journal_entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `company_id` int NOT NULL,
  `reference_no` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `narration` varchar(255) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `reversed_from_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `company_id` (`company_id`),
  KEY `reversed_from_id` (`reversed_from_id`),
  KEY `ix_journal_entries_id` (`id`),
  CONSTRAINT `journal_entries_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `companies` (`id`),
  CONSTRAINT `journal_entries_ibfk_2` FOREIGN KEY (`reversed_from_id`) REFERENCES `journal_entries` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `journal_entries`
--

LOCK TABLES `journal_entries` WRITE;
/*!40000 ALTER TABLE `journal_entries` DISABLE KEYS */;
INSERT INTO `journal_entries` VALUES (1,1,'PB-00001','2026-03-26','Purchase Bill','POSTED',NULL),(2,1,'PB-00002','2026-03-26','Purchase Bill','POSTED',NULL),(3,1,'SI-00001','2026-03-26','Sales Invoice SI-00001','POSTED',NULL),(4,1,'SI-00002','2026-03-26','Sales Invoice SI-00002','POSTED',NULL),(5,1,'PB-00003','2026-03-26','Purchase Bill','POSTED',NULL),(6,1,'PB-00004','2026-03-26','Purchase Bill','POSTED',NULL),(7,1,'PB-00005','2026-03-26','Purchase Bill','POSTED',NULL),(8,1,'PB-00006','2026-03-26','Purchase Bill','POSTED',NULL),(9,1,'PB-00007','2026-03-26','Purchase Bill','POSTED',NULL),(10,1,'SI-00003','2026-03-26','Sales Invoice SI-00003','POSTED',NULL),(11,1,'PB-00008','2026-03-26','Purchase Bill','POSTED',NULL),(12,1,'SI-00004','2026-03-26','Sales Invoice SI-00004','POSTED',NULL),(13,1,'SI-00005','2026-03-26','Sales Invoice SI-00005','POSTED',NULL),(14,1,'SI-00006','2026-03-26','Sales Invoice SI-00006','POSTED',NULL),(15,1,'SI-00007','2026-03-26','Sales Invoice SI-00007','POSTED',NULL),(16,1,'SI-00008','2026-03-26','Sales Invoice SI-00008','POSTED',NULL),(17,1,'SI-00009','2026-03-26','Sales Invoice SI-00009','POSTED',NULL),(18,1,'SI-00010','2026-03-26','Sales Invoice SI-00010','POSTED',NULL),(19,1,'SI-00011','2026-03-26','Sales Invoice SI-00011','POSTED',NULL);
/*!40000 ALTER TABLE `journal_entries` ENABLE KEYS */;
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
