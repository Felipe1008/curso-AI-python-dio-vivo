USE Viagens;

-- Funções Agregadoras --

-- COUNT --
SELECT COUNT(*) as qtdadeUsuarios
FROM usuarios;

SELECT COUNT(*) as qtdadeUsuariosComReserva
FROM usuarios u
INNER JOIN reserva r ON u.ID = r.id_usuario;

-- MAX, DATEDIFF --
SELECT MAX(DATEDIFF(YEAR, dataNascimento, CURRENT_TIMESTAMP)) AS maiorIdade
FROM usuarios;

-- GROUP BY --
SELECT Nome, dataNascimento, DATEDIFF(YEAR, dataNascimento, CURRENT_TIMESTAMP) AS idades
FROM usuarios
GROUP BY Nome, dataNascimento;

-- ORDER BY --
-- Inserindo mais uma reserva para o id_destino 2 --
INSERT INTO reserva(id_usuario, id_destino, dataReserva, statusReserva)
VALUES(2, 1, '2026-07-03', 'Pendente')

SELECT d.nome, COUNT(*) AS qtdadeReservas
FROM reserva r
INNER JOIN destino d ON d.ID = r.id_destino
GROUP BY d.nome
ORDER BY qtdadeReservas DESC;
