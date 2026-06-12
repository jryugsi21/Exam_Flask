CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    precio NUMERIC,
    stock INT
);

INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop', 1200, 10),
('Mouse', 25, 50),
('Teclado', 45, 30),
('Monitor', 300, 15),
('Auriculares', 60, 25);
