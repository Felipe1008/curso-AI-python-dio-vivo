USE Viagens;

-- INNER JOIN --
SELECT * 
FROM usuarios u
INNER JOIN reserva r
ON u.ID = r.id_usuario;

SELECT *
FROM destino d
INNER JOIN reserva r
ON d.ID = r.id_destino;

SELECT *
FROM usuarios u
INNER JOIN reserva r ON u.ID = r.id_usuario
INNER JOIN destino d ON d.ID = r.id_destino

-- LEFT JOIN --
-- Inserindo um usuário sem reserva --
INSERT INTO usuarios(Nome, email, dataNascimento, rua, numero, cidade, estado)
VALUES('Maria', 'maria@mail.com', '2000-10-11', 'Rua X', '120', 'São Paulo', 'SP');

SELECT *
FROM usuarios u 
LEFT JOIN reserva r ON u.ID = r.id_usuario;

-- RIGHT JOIN --
-- Inserindo um destino sem reserva --
INSERT INTO destino(nome, descricao)
VALUES('Fernando de Noronha', 'Arquipélago vulcânico em Pernambuco');

SELECT *
FROM reserva r 
RIGHT JOIN destino d ON r.id_destino = d.ID;

-- FULL JOIN --
SELECT *
FROM usuarios u
FULL JOIN reserva r ON u.ID = r.id_usuario
FULL JOIN destino d ON d.ID = r.id_destino

