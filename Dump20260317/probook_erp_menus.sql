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
-- Table structure for table `menus`
--

DROP TABLE IF EXISTS `menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menus` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `order_no` int DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  KEY `ix_menus_id` (`id`),
  CONSTRAINT `menus_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `menus` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menus`
--

LOCK TABLES `menus` WRITE;
/*!40000 ALTER TABLE `menus` DISABLE KEYS */;
INSERT INTO `menus` VALUES (1,'Dashboard','icon-layout-dashboard','/',NULL,1,1),(2,'Sales','icon-shopping-cart',NULL,NULL,2,1),(3,'Purchase','icon-truck',NULL,NULL,3,1),(4,'Inventory','icon-box',NULL,NULL,4,1),(5,'Products','icon-layers',NULL,NULL,5,1),(6,'Vendors','icon-building-2',NULL,NULL,6,1),(7,'Customers','icon-users',NULL,NULL,7,1),(8,'Reports','icon-file-spreadsheet',NULL,NULL,8,1),(9,'Administration','icon-user-cog',NULL,NULL,9,1),(10,'Settings','icon-cog',NULL,NULL,10,1),(11,'POS Billing','icon-combine','/sales-create',2,1,1),(12,'Sales Orders','icon-file-text','/sales/orders',2,2,1),(13,'Invoices','icon-file-spreadsheet','/sales',2,3,1),(14,'Returns','icon-rotate-ccw','/sales/returns',2,4,1),(15,'Quotations','icon-file-plus','/sales/quotations',2,5,1),(16,'Purchase Orders','icon-shopping-bag','/purchase/po/list',3,1,1),(17,'Goods Received','icon-package-check','/grn/list',3,2,1),(18,'Purchase Bills','icon-receipt','/purchase/create',3,3,1),(19,'Vendor Payments','icon-credit-card','/purchase/payments',3,4,1),(20,'Purchase Returns','icon-rotate-ccw','/purchase/returns',3,5,1),(21,'Stock Summary','icon-box','/stock/summary',4,1,1),(23,'Stock History','icon-repeat','/stock/ledger',4,3,1),(24,'Low Stock Alert','icon-alert-triangle','/stock/low-stock',4,4,1),(25,'Categories','icon-layout-list','/products/categories',5,1,1),(26,'Items','icon-box','/items',5,2,1),(27,'Addons','icon-plus-circle','/products/addons',5,3,1),(28,'Taxes','icon-percent','/products/taxes',5,4,1),(29,'Units','icon-ruler','/products/units',5,5,1),(30,'Vendor List','icon-building-2','/vendors/list',6,1,1),(32,'Vendor Ledger','icon-book','/vendors/ledger',6,3,1),(33,'Customer List','icon-users','/customers',7,1,1),(34,'Add Customer','icon-user-plus','/customer-create',7,2,1),(35,'Customer Ledger','icon-book','/customers/ledger',7,3,1),(36,'Sales Report','icon-file-spreadsheet','/reports/sales',8,1,1),(37,'Purchase Report','icon-trending-up','/reports/purchase',8,2,1),(38,'Stock Report','icon-box','/reports/stock',8,3,1),(39,'Tax Report','icon-percent','/reports/tax',8,4,1),(40,'Profit Report','icon-dollar-sign','/reports/profit',8,5,1),(41,'Users','icon-users','/admin/users',9,1,1),(42,'Roles & Permissions','icon-shield','/admin/roles',9,2,1),(43,'Activity Logs','icon-clock','/admin/logs',9,3,1),(44,'Store Settings','icon-warehouse','/settings/store',10,1,1),(45,'Tax Settings','icon-percent','/settings/tax',10,2,1),(46,'Payment Methods','icon-credit-card','/settings/payment',10,3,1),(47,'Printer Settings','icon-printer','/settings/printer',10,4,1),(48,'Accounting','icon-book-open',NULL,NULL,11,1),(49,'Journal Entry','icon-book','/accounting/journal-create',48,1,1),(50,'Journal List','icon-list','/journals',48,2,1),(51,'Ledger','icon-book','/ledger',48,3,1),(52,'Trial Balance','icon-file-spreadsheet','/trial-balance',48,4,1),(53,'Profit & Loss','icon-trending-up','/profit-loss',48,5,1),(54,'Balance Sheet','icon-layers','/balance-sheet',48,6,1),(55,'Companies','icon-building','/companies',10,5,1),(56,'Chart of Accounts','icon-list','/accounts-page',48,7,1);
/*!40000 ALTER TABLE `menus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-17 16:01:07
