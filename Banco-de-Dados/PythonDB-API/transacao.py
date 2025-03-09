import sqlite3
con = sqlite3.connect('meu_banco.sqlite')
cur = con.cursor()
cur.row_factory = sqlite3.Row

# Esses dados só vão ser inseridos se todos os comandos executarem sem erro
try:
    cur.execute('INSERT INTO clientes(nome, email) VALUES(?, ?)', ("Teste1", "teste1@gmail.com"))
    cur.execute('INSERT INTO clientes(id, nome, email) VALUES(?, ?, ?)', (2, "Teste2", "teste2@gmail.com"))
    con.commit()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    con.rollback()
