CREATE DATABASE IF NOT EXISTS task_app;
USE task_app;
CREATE TABLE IF NOT EXISTS task_app.task (
`id` int NOT NULL AUTO_INCREMENT,
`task_name` varchar(255) NOT NULL,
`task_description` mediumtext NOT NULL,
`due_date` datetime DEFAULT NULL,
`completed_at` datetime DEFAULT NULL,
`deleted_at` datetime DEFAULT NULL,
`updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
`created_at` datetime DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO task_app.task (`task_name`,`task_description`,`due_date`,`completed_at`,`deleted_at`,`updated_at`,`created_at`) VALUES ('initialize docker ','get test project ready','2023-09-06 10:49:00',NULL,NULL,'2023-09-06 10:49:22','2023-09-06 10:49:22');
INSERT INTO task_app.task (`task_name`,`task_description`,`due_date`,`completed_at`,`deleted_at`,`updated_at`,`created_at`) VALUES ('init database for testing purposes','init','2023-09-06 10:49:00',NULL,NULL,'2023-09-06 10:49:39','2023-09-06 10:49:39');
INSERT INTO task_app.task (`task_name`,`task_description`,`due_date`,`completed_at`,`deleted_at`,`updated_at`,`created_at`) VALUES ('live reload unicorn','task','2023-09-06 10:49:00',NULL,NULL,'2023-09-06 10:49:58','2023-09-06 10:49:58');
