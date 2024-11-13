-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db:3306
-- Generation Time: Nov 13, 2024 at 09:37 AM
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
-- Table structure for table `tasks`
--

CREATE TABLE `tasks` (
  `id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text,
  `status` enum('pending','in_progress','completed') DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tasks`
--

INSERT INTO `tasks` (`id`, `title`, `description`, `status`, `created_at`) VALUES
(1, 'Finish project report', 'Complete the final report for the project and submit it to the client.', 'pending', '2024-11-13 09:37:33'),
(2, 'Team meeting preparation', 'Prepare the agenda and documents for the weekly team meeting.', 'in_progress', '2024-11-13 09:37:33'),
(3, 'Code review', 'Review the recent code changes in the repository and provide feedback.', 'completed', '2024-11-13 09:37:33'),
(4, 'Design website layout', 'Create wireframes and design layouts for the new client website.', 'pending', '2024-11-13 09:37:33'),
(5, 'Update documentation', 'Add new API endpoints and update the documentation for the project.', 'in_progress', '2024-11-13 09:37:33'),
(6, 'Client follow-up', 'Follow up with the client regarding their feedback on the last deliverable.', 'completed', '2024-11-13 09:37:33'),
(7, 'Test new features', 'Test the new features in the staging environment before deployment.', 'in_progress', '2024-11-13 09:37:33'),
(8, 'Data backup', 'Run a complete data backup and ensure all files are secure.', 'completed', '2024-11-13 09:37:33'),
(9, 'Plan marketing strategy', 'Draft the quarterly marketing plan and set goals for the campaign.', 'pending', '2024-11-13 09:37:33'),
(10, 'Organize files', 'Organize and archive completed project files for future reference.', 'completed', '2024-11-13 09:37:33');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tasks`
--
ALTER TABLE `tasks`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
