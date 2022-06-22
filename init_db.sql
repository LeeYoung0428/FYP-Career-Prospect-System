DROP TABLE IF EXISTS `publications_tab`;

CREATE TABLE `publications_tab` (
  `id` int(9) unsigned NOT NULL AUTO_INCREMENT,
  `author` varchar(512) NOT NULL,
  `vector` blob NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;