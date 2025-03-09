USE Viagens;

-- Adicionando constraints com ON DELETE CASCADE --
ALTER TABLE reserva
ADD CONSTRAINT fk_usuarios
FOREIGN KEY(id_usuario) REFERENCES usuarios(ID)
ON DELETE CASCADE;

ALTER TABLE reserva
ADD CONSTRAINT fk_destino
FOREIGN KEY(id_destino) REFERENCES destino(ID)
ON DELETE CASCADE;

-- Checando as constraints --
SELECT 
    con.name AS constraint_name,
    con.type_desc AS constraint_type,
    tab.name AS table_name,
    col.name AS column_name
FROM sys.foreign_keys AS con
JOIN sys.tables AS tab ON con.parent_object_id = tab.object_id
JOIN sys.foreign_key_columns AS fk_col ON con.object_id = fk_col.constraint_object_id
JOIN sys.columns AS col ON fk_col.parent_column_id = col.column_id AND fk_col.parent_object_id = col.object_id
WHERE tab.name = 'reserva';

-- Excluindo constraints anteriores --
ALTER TABLE reserva DROP CONSTRAINT FK__reserva__id_usua__3C69FB99;
ALTER TABLE reserva DROP CONSTRAINT FK__reserva__id_dest__3D5E1FD2;