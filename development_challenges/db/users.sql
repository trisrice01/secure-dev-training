-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Nov 12, 2024 at 12:06 PM
-- Server version: 9.1.0
-- PHP Version: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `php_docker`
--

-- --------------------------------------------------------

--
-- Table structure for table `logins`
--

CREATE TABLE `logins` (
  `login_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `logins`
--

INSERT INTO `logins` (`login_id`, `user_id`, `username`, `password`, `last_login`) VALUES
(1, 1, 'bradpitt63', 'bradpass123', '2024-11-12 08:15:00'),
(2, 2, 'angelinajolie75', 'joliepass456', '2024-11-12 08:30:00'),
(3, 3, 'tomhanks56', 'hanks1234', '2024-11-12 09:00:00'),
(4, 4, 'leodicaprio74', 'leonardo456', '2024-11-12 09:30:00'),
(5, 5, 'merylstreep49', 'meryl7890', '2024-11-12 10:00:00'),
(6, 6, 'scarlettjohansson84', 'scarlett1234', '2024-11-12 10:30:00'),
(7, 7, 'robertdowneyjr65', 'ironman2024', '2024-11-12 11:00:00'),
(8, 8, 'jenniferlawrence90', 'jenniferpass', '2024-11-12 11:30:00'),
(9, 9, 'willsmith68', 'willsmith789', '2024-11-12 12:00:00'),
(10, 10, 'jadapinkett71', 'jada1234', '2024-11-12 12:30:00'),
(11, 11, 'chrishemsworth83', 'thorpassword1', '2024-11-12 13:00:00'),
(12, 12, 'tomcruise62', 'missionimpossible', '2024-11-12 13:30:00'),
(13, 13, 'emmastone88', 'stonepass2024', '2024-11-12 14:00:00'),
(14, 14, 'ryanreynolds76', 'deadpool123', '2024-11-12 14:30:00'),
(15, 15, 'johnnydepp63', 'piratespass123', '2024-11-12 15:00:00'),
(16, 16, 'juliaroberts67', 'juliaroberts1', '2024-11-12 15:30:00'),
(17, 17, 'keanureeves64', 'keanupassword', '2024-11-12 16:00:00'),
(18, 18, 'nicolekidman67', 'nicolekidman22', '2024-11-12 16:30:00'),
(19, 19, 'matthewmcconaughey69', 'alrightalright', '2024-11-12 17:00:00'),
(20, 20, 'beyonce1981', 'beyonce1234', '2024-11-12 17:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `zip_code` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `dob`, `address`, `city`, `state`, `zip_code`) VALUES
(1, 'Brad', 'Pitt', '1963-12-18', '123 Hollywood Blvd', 'Los Angeles', 'CA', '90028'),
(2, 'Angelina', 'Jolie', '1975-06-04', '456 Sunset Ave', 'Los Angeles', 'CA', '90046'),
(3, 'Tom', 'Hanks', '1956-07-09', '789 Beverly Blvd', 'Los Angeles', 'CA', '90036'),
(4, 'Leonardo', 'DiCaprio', '1974-11-11', '101 Melrose Ave', 'Los Angeles', 'CA', '90038'),
(5, 'Meryl', 'Streep', '1949-06-22', '202 Park Ave', 'New York', 'NY', '10016'),
(6, 'Scarlett', 'Johansson', '1984-11-22', '303 Fifth Ave', 'New York', 'NY', '10001'),
(7, 'Robert', 'Downey Jr.', '1965-04-04', '404 Park Ave', 'New York', 'NY', '10010'),
(8, 'Jennifer', 'Lawrence', '1990-08-15', '505 Madison Ave', 'New York', 'NY', '10019'),
(9, 'Will', 'Smith', '1968-09-25', '606 Broadway St', 'Philadelphia', 'PA', '19107'),
(10, 'Jada', 'Pinkett', '1971-09-18', '707 Pine St', 'Baltimore', 'MD', '21201'),
(11, 'Chris', 'Hemsworth', '1983-08-11', '808 Ocean Dr', 'Miami', 'FL', '33139'),
(12, 'Tom', 'Cruise', '1962-07-03', '909 Hollywood Blvd', 'Los Angeles', 'CA', '90028'),
(13, 'Emma', 'Stone', '1988-11-06', '1010 Sunset Blvd', 'Los Angeles', 'CA', '90046'),
(14, 'Ryan', 'Reynolds', '1976-10-23', '1111 Vine St', 'Los Angeles', 'CA', '90028'),
(15, 'Johnny', 'Depp', '1963-06-09', '1212 Pacific Coast Hwy', 'Los Angeles', 'CA', '90069'),
(16, 'Julia', 'Roberts', '1967-10-28', '1313 Ocean Blvd', 'Malibu', 'CA', '90265'),
(17, 'Keanu', 'Reeves', '1964-09-02', '1414 Maple Ave', 'Los Angeles', 'CA', '90069'),
(18, 'Nicole', 'Kidman', '1967-06-20', '1515 Wilshire Blvd', 'Los Angeles', 'CA', '90017'),
(19, 'Matthew', 'McConaughey', '1969-11-04', '1616 Pacific Ave', 'Austin', 'TX', '73301'),
(20, 'Beyoncé', 'Knowles', '1981-09-04', '1717 Queen St', 'Houston', 'TX', '77001');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `logins`
--
ALTER TABLE `logins`
  ADD PRIMARY KEY (`login_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `logins`
--
ALTER TABLE `logins`
  ADD CONSTRAINT `logins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
