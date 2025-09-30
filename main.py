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

# cadastrar_livro()

#Etapa 3
def listar_livros():
     cursor.execute("SELECT * FROM livros")
     for linha in cursor.fetchall():
        print(f"ID: {linha[0]} | TITULO: {linha[1]} | AUTOR: {linha[2]} | ANO: {linha[3]} | DISPONIVEL: {linha[4]}")



#Etapa 4
def atualizar_livros():
    id_livro = input("Digite o ID do livro que deseja atualizar: ")
    disponivel = input("O livro está disponível? (Sim / Não): ").lower()
    if disponivel not in ["sim", "não", "nao"]:
        print("Digite apenas 'Sim' ou 'Não'").lower()
        return
    
    cursor.execute("""
    UPDATE livros
    SET  disponível = ?          
    WHERE id = ?
    """, (disponivel, id_livro) )

    conexao.commit()
    print("Dados atualizados com sucesso!")



#Etapa 5
def remover_livro():
    try:
        id = int(input("Digite o ID do livro para removê-lo: "))
        cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
        if cursor.rowcount > 0:
            print("Livro removido com sucesso!")
        else:
            print("Nenhum livro cadastrado com o ID fornecido!")
        conexao.commit()
    except Exception as erro:
        print(f"Erro ao tentar excluir o livro: {erro}")


#Etapa 6
def menu():
    print("Seja bem vindo a nossa biblioteca virtual! Por favor escolha uma das opções abaixo")

    print(f"\n === Plataforma ===")
    print("1. Cadastrar livro")
    print("2. Listagem de Livros")
    print("3. Atualização de Disponibilidade")
    print("4. Remoção de Livros")
    print("5. Sair do sistema")

while True:
    menu()
    opcao = input("Escolha uma opção: ")
    if opcao == "1":
        cadastrar_livro()
    elif opcao == "2":
        listar_livros()
    elif opcao == "3":
        atualizar_livros()
    elif opcao == "4":
        remover_livro()
    elif opcao == "5":
        print("Saindo do sistema . . .")
        break
    else:
       print("Opção inválida!")
