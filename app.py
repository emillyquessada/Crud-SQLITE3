import streamlit as st
import sqlite3

# python -m streamlit run app.py


# Funções de antes
conexao = sqlite3.connect("biblioteca.db", check_same_thread=False)
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
conexao.commit()

def cadastrar_livro(titulo, autor, ano):
    cursor.execute("""
        INSERT INTO livros (título, autor, ano, disponível)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, "sim"))
    conexao.commit()

def listar_livros():
    cursor.execute("SELECT * FROM livros")
    return cursor.fetchall()

def atualizar_disponibilidade(id_livro, disponibilidade):
    cursor.execute("""
        UPDATE livros
        SET disponível = ?
        WHERE id = ?
    """, (disponibilidade.lower(), id_livro))
    conexao.commit()

def remover_livro(id_livro):
    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conexao.commit()
    return cursor.rowcount > 0


# Começando o aplicativo
st.set_page_config(page_title="Biblioteca Virtual", page_icon="📚")

st.title("📕 Biblioteca Virtual")
st.markdown("Seja bem vindo! Aqui você poderá cadastrar livros, atualiza-los e até mesmo removê-los!")

abas = st.tabs(["➕ Cadastrar Livro", "📚 Listar Livros", "🔄 Atualizar Disponibilidade", "❌ Remover Livro"])

# Páginas para as funções
with abas[0]:
    st.subheader("➕ Cadastrar Novo Livro")
    with st.form("form_cadastro"):
        titulo = st.text_input("Título do livro")
        autor = st.text_input("Autor")
        ano = st.number_input("Ano de lançamento", min_value=0, step=1)
        submit = st.form_submit_button("Cadastrar")

        if submit:
            if titulo and autor:
                cadastrar_livro(titulo, autor, ano)
                st.success("✅ Livro cadastrado com sucesso!")
            else:
                st.warning("⚠️ Preencha todos os campos obrigatórios.")

with abas[1]:
    st.subheader("📖 Lista de Livros Cadastrados")
    livros = listar_livros()

    if livros:
        total = len(livros)
        disponiveis = sum(1 for livro in livros if livro[4].lower() == "sim")
        indisponiveis = total - disponiveis

        st.write(f"📖 Total de livros: {total}")
        st.write(f"✔ Disponíveis: {disponiveis} | ❌ Indisponíveis: {indisponiveis}")
        st.markdown("---")

        # Montar os dados da tabela como lista de dicionários
        dados_tabela = []
        for livro in livros:
            dados_tabela.append({
                "ID": livro[0],
                "Título": livro[1],
                "Autor": livro[2],
                "Ano": livro[3],
                "Disponível": "Sim" if livro[4].lower() == "sim" else "Não"
            })

        st.table(dados_tabela)

    else:
        st.info("📭 Nenhum livro cadastrado.")

with abas[2]:
    st.subheader("🔄 Atualizar Disponibilidade")
    livros = listar_livros()
    if livros:
        opcoes = {f"ID {livro[0]} - {livro[1]}": livro[0] for livro in livros}
        selecionado = st.selectbox("Selecione o livro:", list(opcoes.keys()))
        id_livro = opcoes[selecionado]

        nova_disp = st.radio("Novo status:", ["sim", "não"])

        if st.button("Atualizar"):
            atualizar_disponibilidade(id_livro, nova_disp)
            st.success("🔄 Disponibilidade atualizada com sucesso!")
            st.rerun()
    else:
        st.warning("Nenhum livro cadastrado para atualizar.")

with abas[3]:
    st.subheader("❌ Remover Livro")
    livros = listar_livros()
    if livros:
        opcoes = {f"ID {livro[0]} - {livro[1]}": livro[0] for livro in livros}
        selecionado = st.selectbox("Selecione o livro:", list(opcoes.keys()), key="select_atualizar")
        id_livro = opcoes[selecionado]

        if st.button("Remover"):
            sucesso = remover_livro(id_livro)
            if sucesso:
                st.success("🗑️ Livro removido com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao remover o livro.")
    else:
        st.warning("Nenhum livro cadastrado para remover.")

# python -m streamlit run app.py