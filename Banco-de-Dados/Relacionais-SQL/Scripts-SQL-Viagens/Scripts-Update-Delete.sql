USE Viagens;

INSERT INTO usuarios(Nome, email, dataNascimento, endereco)
VALUES('usuario x', 'usuariox@mail.com', '1970-07-15', 'X')

-- Atualizando email do Usu�rio Jo�o de ID = 2 --
UPDATE usuarios
SET email = 'joao@outlook.com'
WHERE ID = 2;

-- Excluindo Usu�rio gen�rico criado anteriormente com ID = 3 --
DELETE FROM usuarios WHERE ID = 3;

-- Checando dados da tabela usuarios --
SELECT * FROM usuarios;
