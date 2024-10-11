-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS db_books;

-- Usar la base de datos
USE db_books;

-- Crear la tabla de Autores
CREATE TABLE IF NOT EXISTS Autor (
    ID_autor INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Fecha_nacimiento DATE,
    Nacionalidad VARCHAR(50),
    Biografía TEXT
);

-- Crear la tabla de Libros
CREATE TABLE IF NOT EXISTS Libros (
    ID_libro INT AUTO_INCREMENT PRIMARY KEY,
    Título VARCHAR(200) NOT NULL,
    ID_autor INT,
    ISBN VARCHAR(20) NOT NULL,
    Género VARCHAR(50),
    Fecha_publicación DATE,
    Número_páginas INT,
    Editorial VARCHAR(100),
    Idioma VARCHAR(50),
    Resumen TEXT,
    Disponibilidad BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ID_autor) REFERENCES Autor(ID_autor) ON DELETE SET NULL
);

-- Crear la tabla de Clientes
CREATE TABLE IF NOT EXISTS Clientes (
    ID_cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) UNIQUE NOT NULL,
    Teléfono VARCHAR(20),
    Fecha_registro DATE DEFAULT CURRENT_DATE
);

-- Crear la tabla de Valoraciones
CREATE TABLE IF NOT EXISTS Valoraciones (
    ID_valoracion INT AUTO_INCREMENT PRIMARY KEY,
    ID_libro INT,
    ID_cliente INT,
    Puntuacion INT CHECK (Puntuacion BETWEEN 1 AND 5),
    Comentario TEXT,
    Fecha DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (ID_libro) REFERENCES Libros(ID_libro) ON DELETE CASCADE,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente) ON DELETE CASCADE
);

-- Crear la tabla de Reservas
CREATE TABLE IF NOT EXISTS Reservas (
    ID_reserva INT AUTO_INCREMENT PRIMARY KEY,
    ID_libro INT,
    ID_cliente INT,
    Fecha_reserva DATE DEFAULT CURRENT_DATE,
    Estado ENUM('Pendiente', 'Confirmada', 'Cancelada') DEFAULT 'Pendiente',
    FOREIGN KEY (ID_libro) REFERENCES Libros(ID_libro) ON DELETE CASCADE,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente) ON DELETE CASCADE
);

-- Crear la tabla de Historial_cliente (opcional)
CREATE TABLE IF NOT EXISTS Historial_cliente (
    ID_historial INT AUTO_INCREMENT PRIMARY KEY,
    ID_cliente INT,
    ID_libro INT,
    Fecha DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (ID_cliente) REFERENCES Clientes(ID_cliente) ON DELETE CASCADE,
    FOREIGN KEY (ID_libro) REFERENCES Libros(ID_libro) ON DELETE CASCADE
);

-- Datos de ejemplo para la tabla Autor
INSERT INTO Autor (Nombre, Fecha_nacimiento, Nacionalidad, Biografía) VALUES
('Gabriel García Márquez', '1927-03-06', 'Colombiana', 'Escritor colombiano, ganador del Premio Nobel de Literatura.'),
('Isabel Allende', '1942-08-02', 'Chilena', 'Novelista chilena, conocida por obras como "La casa de los espíritus".'),
('J.K. Rowling', '1965-07-31', 'Británica', 'Autora de la famosa serie de Harry Potter.');

-- Datos de ejemplo para la tabla Libros
INSERT INTO Libros (Título, ID_autor, ISBN, Género, Fecha_publicación, Número_páginas, Editorial, Idioma, Resumen, Disponibilidad) VALUES
('Cien años de soledad', 1, '978-84-349-2909-1', 'Realismo mágico', '1967-05-30', 417, 'Editorial Sudamericana', 'Español', 'Una historia de la familia Buendía en el pueblo ficticio de Macondo.', TRUE),
('La casa de los espíritus', 2, '978-84-204-8170-0', 'Novela histórica', '1982-10-08', 368, 'Plaza & Janés', 'Español', 'La historia de varias generaciones de la familia Trueba.', TRUE),
('Harry Potter y la piedra filosofal', 3, '978-0-7475-3274-0', 'Fantasía', '1997-06-26', 223, 'Bloomsbury', 'Inglés', 'Las aventuras de un joven mago en la escuela de magia Hogwarts.', TRUE);

-- Datos de ejemplo para la tabla Clientes
INSERT INTO Clientes (Nombre, Apellido, Correo, Teléfono) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '123456789'),
('María', 'González', 'maria.gonzalez@example.com', '987654321'),
('Luis', 'Martínez', 'luis.martinez@example.com', '456123789');

-- Datos de ejemplo para la tabla Valoraciones
INSERT INTO Valoraciones (ID_libro, ID_cliente, Puntuacion, Comentario, Fecha) VALUES
(1, 1, 5, 'Una obra maestra de la literatura.', '2023-09-01'),
(2, 2, 4, 'Una novela cautivadora, aunque un poco larga.', '2023-09-05'),
(3, 3, 5, 'Me encantó cada página de este libro.', '2023-09-10');

-- Datos de ejemplo para la tabla Reservas
INSERT INTO Reservas (ID_libro, ID_cliente, Fecha_reserva, Estado) VALUES
(1, 1, '2024-10-01', 'Pendiente'),
(2, 2, '2024-10-02', 'Confirmada'),
(3, 3, '2024-10-03', 'Cancelada');

-- Datos de ejemplo para la tabla Historial_cliente (opcional)
INSERT INTO Historial_cliente (ID_cliente, ID_libro, Fecha) VALUES
(1, 1, '2024-09-20'),
(2, 2, '2024-09-21'),
(3, 3, '2024-09-22');
