USE Viagens;

INSERT INTO usuarios(Nome, email, dataNascimento, endereco)
VALUES('Felipe', 'felipe@mail.com', '1999-07-08', 'Rua XYZ, 99 - Bairro X/SP'),
('João', 'joao@mail.com', '1993-04-02', 'Rua XYZ, 77 - Bairro Y/SP')

INSERT INTO destino(nome, descricao)
VALUES('Maceió', 'Passeio guiado pelos pontos turísticos de Maceió'),
('Gramado', 'Passeio com hospedagem inclusa na cidade do Natal Luz')

INSERT INTO reserva(id_usuario, id_destino, dataReserva, statusReserva)
VALUES(1, 1, '2025-03-05', 'Confirmada'),
(2, 2, '2025-04-12', 'Pendente')

SELECT * FROM usuarios;

SELECT * FROM destino;

SELECT * FROM reserva;

SELECT u.Nome, d.nome as nomeDestino, r.dataReserva, r.statusReserva FROM usuarios u, destino d, reserva r WHERE r.id_usuario = u.ID AND r.id_destino = d.ID;