USE Viagens;

-- Desestruturando 'endereco' em 'rua', 'numero', 'cidade' e 'estado' para seguir a Norma 1FN --
ALTER TABLE usuarios
ADD rua VARCHAR(100), 
numero VARCHAR(10),
cidade VARCHAR(50),
estado VARCHAR(20);

-- Migrando dados de 'endereco' para 'rua', 'numero', 'cidade' e 'estado'
UPDATE usuarios
SET rua = LTRIM(RTRIM(SUBSTRING(endereco, 1, CHARINDEX(',', endereco) - 1))),
    numero = LTRIM(RTRIM(SUBSTRING(endereco, CHARINDEX(',', endereco) + 1, 
                          CHARINDEX('-', endereco) - CHARINDEX(',', endereco) - 1))),
    cidade = LTRIM(RTRIM(SUBSTRING(endereco, CHARINDEX('-', endereco) + 2, 
                          CHARINDEX('/', endereco) - CHARINDEX('-', endereco) - 2))),
    estado = LTRIM(RTRIM(RIGHT(endereco, 2)));

-- Excluindo coluna 'endereco' --
ALTER TABLE usuarios
DROP COLUMN endereco;
