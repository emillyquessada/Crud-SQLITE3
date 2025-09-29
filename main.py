import sqlite3

conexao = sqlite3.connect("biblioteca.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    título TEXT NOT NULL,
    autor TEXT NOT NULL,
    ano INTEGER,
    disponível TEXT NOT NULL
    )
""")
print("Tabela criada com sucesso!")

#Etapa 2
def cadastrar_livro(): 
    titulo = input("Digite o nome do livro que deseja cadastrar: ")
    autor = input("Digite o nome do autor: ")
    ano = int(input("Digite o ano de lançamento: "))

    cursor.execute("""
    INSERT INTO livros (título, autor, ano, disponível)
    VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, "sim" )
    )
    conexao.commit()

cadastrar_livro()