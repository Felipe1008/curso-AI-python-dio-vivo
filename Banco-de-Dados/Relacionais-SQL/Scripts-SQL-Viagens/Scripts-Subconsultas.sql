USE Viagens;

-- Subconsultas --
SELECT * 
FROM destino
WHERE ID NOT IN(SELECT id_destino FROM reserva);

SELECT * 
FROM usuarios
WHERE ID NOT IN(SELECT id_usuario FROM reserva);

SELECT Nome, (SELECT COUNT(*) FROM reserva WHERE id_usuario = u.id) AS totalReservas
FROM usuarios u;