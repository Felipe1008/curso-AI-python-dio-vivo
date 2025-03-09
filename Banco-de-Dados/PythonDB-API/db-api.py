import sqlite3

# Estabelecendo conexão
con = sqlite3.connect('meu_banco.sqlite')

# Cursor
cur = con.cursor()
## cur.row_factory = sqlite3.Row # --> Posso deixar o row_factory como padrão em todo o código se descomentar essa linha (retornará Row, legíveis por dicionários)
# Criando Tabela
## Criando uma função para não ficar executando toda vez
def criar_tabela(cur):
    cur.execute("CREATE TABLE clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))")

# Inserindo registros
def inserir_registro(con, cur, nome, email):
    data = (nome, email)
    cur.execute("INSERT INTO clientes(nome, email) VALUES(?, ?)", data)
    con.commit()

# Atualizando registros
def atualizar_registro(con, cur, nome, email, id):
    data_update = (nome, email, id)
    cur.execute("UPDATE clientes SET nome=?, email=? WHERE id=?", data_update)
    con.commit()

## atualizar_registro(con, cur, "Marcos", "marcos@mail.com", 3)

# Removendo registros
def excluir_registro(con, cur, id):
    data = (id, )
    cur.execute("DELETE FROM clientes WHERE id=?", data)
    con.commit()

# Inserindo um cliente duplicado
## inserir_registro(con, cur, "Felipe", "felipe@mail.com")
# Excluindo esse registro de id = 4
## excluir_registro(con, cur, 4)

def inserir_lote(con, cur, dados):
    cur.executemany('INSERT INTO clientes(nome, email) VALUES(?, ?)', dados)
    con.commit()
## inserir_lote(con, cur, [("Gomez", "gustavo@mail.com"), ("Raphael", "raphael@mail.com"), ("Evair", "evair@mail.com")])

def recuperar_cliente(cur, id):
    cur.execute("SELECT * FROM clientes WHERE id=?", (id, ))
    return cur.fetchone()

## cliente = recuperar_cliente(cur, 1)
## print(cliente)

def listar_clientes(cur):
    cur.execute("SELECT * FROM clientes ORDER BY nome")
    return cur.fetchall()

## clientes = listar_clientes(cur)
## for cliente in clientes:
##    print(cliente)

def recuperar_cliente_row_factory(cur, id):
    cur.row_factory = sqlite3.Row
    cur.execute("SELECT * FROM clientes WHERE id=?", (id, ))
    return cur.fetchone()

## cliente = recuperar_cliente_row_factory(cur, 2)
## print(dict(cliente))
## print(cliente['nome'])
