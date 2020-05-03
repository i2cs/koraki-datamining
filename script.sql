SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

CREATE TABLE `datamining_product_meta` (
  `id` int(11) NOT NULL,
  `siteid` int(11) NOT NULL,
  `product_id` varchar(20) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `product_url` varchar(100) NOT NULL,
  `product_image` varchar(100) NOT NULL,
  `var1` varchar(100) NOT NULL,
  `var2` varchar(100) NOT NULL,
  `publish_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `datamining_product_visits` (
  `id` int(11) NOT NULL,
  `siteid` int(11) NOT NULL,
  `visitor` varchar(18) NOT NULL,
  `item` varchar(18) NOT NULL,
  `action_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `publish_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `datamining_rules` (
  `id` int(11) NOT NULL,
  `siteid` int(11) NOT NULL,
  `base_items` varchar(100) NOT NULL,
  `suggest` varchar(20) NOT NULL,
  `confidence` float NOT NULL,
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `datamining_product_meta`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `siteid` (`siteid`,`product_id`);

ALTER TABLE `datamining_product_visits`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `siteid` (`siteid`,`visitor`,`item`,`action_time`);

ALTER TABLE `datamining_rules`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `datamining_product_meta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `datamining_product_visits`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
ALTER TABLE `datamining_rules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;