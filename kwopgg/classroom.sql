CREATE TABLE `classroom_inf_dev` (
  `id` INT AUTO_INCREMENT PRIMARY KEY, 
  `capacity` int NULL,                  
  `capacity_max` int NULL,              
  `reserved_time` datetime NULL,        
  `place_name` varchar(100) NULL,       
  `image_id` varchar(50) NULL,          
  `type` varchar(50) NULL,              
  `has_mic` boolean NULL,               
  `has_projector` varchar(50) NULL,     
  `building_name` varchar(100) NULL,    
  `description` text NULL,              
  `reserved` boolean NULL,              
  `desk_type` varchar(50) NULL,         
  `rating` float NULL                   
);

CREATE TABELE 