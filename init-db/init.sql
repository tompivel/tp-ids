CREATE TABLE IF NOT EXISTS tabla_ejemplo(
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    edad INT NOT NULL
);
INSERT INTO tabla_ejemplo (nombre, edad) VALUES
('Juan Perez', 30),
('Maria Garcia', 25),
('Carlos Sanchez', 35);
