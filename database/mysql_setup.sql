CREATE DATABASE IF NOT EXISTS facial_attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE facial_attendance_db;

CREATE TABLE IF NOT EXISTS `core_app_user` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `userid` VARCHAR(100) NOT NULL UNIQUE,
  `name` VARCHAR(255),
  `image` LONGBLOB,
  `registered_date` DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `core_app_attendance` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `user_id` INT,
  `capture_image` LONGBLOB,
  `date` DATE DEFAULT (CURRENT_DATE()),
  `time` TIME DEFAULT (CURRENT_TIME()),
  `status` VARCHAR(50) DEFAULT 'Pending',
  FOREIGN KEY (user_id) REFERENCES core_app_user(id) ON DELETE SET NULL
);
