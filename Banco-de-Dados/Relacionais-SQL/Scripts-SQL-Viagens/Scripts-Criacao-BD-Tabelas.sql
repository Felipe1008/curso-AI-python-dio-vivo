CREATE DATABASE Viagens;

USE Viagens;

CREATE TABLE usuarios(
	ID SMALLINT IDENTITY PRIMARY KEY,
	Nome VARCHAR(30) NOT NULL,
	email VARCHAR(50) NOT NULL UNIQUE,
	endereco VARCHAR(100) NOT NULL,
	dataNascimento date NOT NULL
)

CREATE TABLE destino(
	ID SMALLINT IDENTITY PRIMARY KEY,
	nome VARCHAR(255) NOT NULL,
	descricao VARCHAR(255)
)

CREATE TABLE reserva(
	ID SMALLINT IDENTITY PRIMARY KEY,
	id_usuario SMALLINT NOT NULL REFERENCES usuarios(ID),
	id_destino SMALLINT NOT NULL REFERENCES destino(ID),
	dataReserva DATE,
	statusReserva VARCHAR(255) DEFAULT('Pendente') CHECK(statusReserva = 'Confirmada' OR statusReserva = 'Pendente' OR statusReserva = 'Cnacelada')

)
