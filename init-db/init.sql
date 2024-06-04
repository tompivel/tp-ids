-- Configurar la base de datos para usar utf8mb4
ALTER DATABASE hospedaje_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS cabins(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    descripcion TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    imagen TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
);

CREATE TABLE IF NOT EXISTS habitaciones(
    id INT AUTO_INCREMENT PRIMARY KEY,
    cabin_id INT,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    imagen TEXT,
    FOREIGN KEY (cabin_id) REFERENCES cabins(id)
);

-- Asegurar de que las tablas existentes usen utf8mb4
ALTER DATABASE hospedaje_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE habitaciones CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE cabins CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO cabins (nombre, descripcion, imagen) VALUES
('Cabaña 1', 'Cabaña de 2 habitaciones', 'https://cf.bstatic.com/xdata/images/hotel/max1024x768/383403441.jpg?k=0d70432ce7823f8c3db9ab7f5f71776f2c2d1ea51894802ef3932f147d0cdcfe&o=&hp=1'),
('Cabaña 2', 'Cabaña de 3 habitaciones', 'https://cf.bstatic.com/xdata/images/hotel/max1024x768/383403441.jpg?k=0d70432ce7823f8c3db9ab7f5f71776f2c2d1ea51894802ef3932f147d0cdcfe&o=&hp=1'),
('Cabaña 3', 'Cabaña de 4 habitaciones', 'https://cf.bstatic.com/xdata/images/hotel/max1024x768/383403441.jpg?k=0d70432ce7823f8c3db9ab7f5f71776f2c2d1ea51894802ef3932f147d0cdcfe&o=&hp=1');

INSERT INTO habitaciones (cabin_id, nombre, descripcion, precio, imagen) VALUES
(1, 'Habitación 1', 'Habitación con cama matrimonial', 10000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(1, 'Habitación 2', 'Habitación con 2 camas individuales', 15000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(2, 'Habitación 1', 'Habitación con cama matrimonial', 10000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(2, 'Habitación 2', 'Habitación con 2 camas individuales', 15000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(2, 'Habitación 3', 'Habitación con 3 camas individuales', 17500.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(3, 'Habitación 1', 'Habitación con cama matrimonial', 10000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(3, 'Habitación 2', 'Habitación con 2 camas individuales', 15000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(3, 'Habitación 3', 'Habitación con 3 camas individuales', 17500.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg'),
(3, 'Habitación 4', 'Habitación con 4 camas individuales', 20000.00, 'https://media.architecturaldigest.com/photos/6234c3983d920840570d64d6/master/w_1600%2Cc_limit/TOM%2520FELDMAN%2520Kyle%2520Smith%2520:%2520@dipsauce.jpg');

