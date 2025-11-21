-- Script de inicialización de la base de datos
-- Este script se ejecuta automáticamente cuando se crea el contenedor de PostgreSQL

-- Crear la tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar usuarios de ejemplo
INSERT INTO users (name, email) VALUES
    ('Juan Pérez', 'juan.perez@example.com'),
    ('María García', 'maria.garcia@example.com'),
    ('Carlos López', 'carlos.lopez@example.com'),
    ('Ana Martínez', 'ana.martinez@example.com'),
    ('Pedro Rodríguez', 'pedro.rodriguez@example.com'),
    ('Lucía Fernández', 'lucia.fernandez@example.com'),
    ('Miguel Sánchez', 'miguel.sanchez@example.com'),
    ('Laura González', 'laura.gonzalez@example.com'),
    ('Diego Torres', 'diego.torres@example.com'),
    ('Sofía Ramírez', 'sofia.ramirez@example.com');

-- Verificar que los datos se insertaron correctamente
SELECT COUNT(*) as total_users FROM users;