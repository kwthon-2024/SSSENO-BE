CREATE TABLE `classroom_inf` (
  `capacity` int,
  `reserved_time` datetime,
  `place_name` varchar(100),
  `image_id` varchar(50),
  `type` varchar(50),
  `has_mic` boolean,
  `has_projector` varchar(50),
  `building_name` varchar(100),
  `description` text,
  `reserved` boolean,
  `desk_type` varchar(50),
  `rating` float
);

CREATE TABLE `classroom_review` (
  `mic_status` decimal(3,1),
  `clean_status` decimal(3,1),
  `air_conditioner_status` decimal(3,1),
  `size_satisfaction` decimal(3,1),
  `user_id` int
);
