import streamlit as st
import sqlite3
import pandas as pd # Importação da biblioteca pandas

# --- Configuração da Página e Título ---
st.set_page_config(
    page_title="Biblioteca Virtual",
    page_icon="📚",
    layout="centered"
)

# --- Conexão com banco de dados ---
try:
    conexao = sqlite3.connect("biblioteca.db", check_same_thread=False)
    cursor = conexao.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            ano INTEGER,
            disponível TEXT
        )
    """)
    conexao.commit()

except sqlite3.Error as e:
    st.error(f"Erro ao conectar ao banco de dados: {e}")

# --- Funções do banco de dados ---
def cadastrar_livro(titulo, autor, ano):
    cursor.execute("""
        INSERT INTO livros (titulo, autor, ano, disponível)
        VALUES (?, ?, ?, ?)
    """, (titulo, autor, ano, "sim"))
    conexao.commit()

def listar_livros():
    cursor.execute("SELECT * FROM livros")
    return cursor.fetchall()

def atualizar_livro(id_livro, disponibilidade):
    cursor.execute("UPDATE livros SET disponível = ? WHERE id = ?", (disponibilidade.lower(), id_livro))
    conexao.commit()

def remover_livro(id_livro):
    cursor.execute("DELETE FROM livros WHERE id = ?", (id_livro,))
    conexao.commit()

# --- Título e Descrição Principal ---
st.title("📚 Biblioteca Virtual")
st.markdown("Gerencie sua coleção de livros de forma simples e organizada.")
st.markdown("---")

# --- Abas do menu ---
abas = st.tabs(["➕ Cadastrar Livro", "📄 Listar Livros", "🔄 Atualizar Disponibilidade", "❌ Remover Livro"])

# --- Aba: Cadastrar Livro ---
with abas[0]:
    st.header("➕ Cadastro de Novo Livro")
    st.info("Preencha os campos abaixo para adicionar um novo livro à biblioteca.")
    with st.form("form_cadastro"):
        titulo = st.text_input("Título do Livro", placeholder="Ex: O Senhor dos Anéis")
        autor = st.text_input("Autor", placeholder="Ex: J.R.R. Tolkien")
        ano = st.number_input("Ano de Lançamento", min_value=0, step=1, placeholder="Ex: 1954")
        cadastrar = st.form_submit_button("Cadastrar Livro")

        if cadastrar:
            if titulo and autor and ano:
                cadastrar_livro(titulo, autor, ano)
                st.success("✅ Livro cadastrado com sucesso!")
            else:
                st.warning("⚠️ Preencha todos os campos para cadastrar o livro.")

# --- Aba: Listar Livros ---
with abas[1]:
    st.header("📄 Livros Cadastrados")
    livros = listar_livros()

    if livros:
        st.subheader(f"📖 Total de livros: {len(livros)}")
        
        # Uso de colunas para exibir métricas
        col1, col2 = st.columns(2)
        total_disponiveis = sum(1 for livro in livros if livro[4].lower() == 'sim')
        total_indisponiveis = len(livros) - total_disponiveis
        col1.metric("Disponíveis", total_disponiveis)
        col2.metric("Indisponíveis", total_indisponiveis)

        st.markdown("---")

        # Criação do DataFrame e exibição da tabela
        df = pd.DataFrame(livros, columns=["ID", "Título", "Autor", "Ano", "Disponível"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 Nenhum livro cadastrado ainda. Use a aba 'Cadastrar Livro' para começar.")

# --- Aba: Atualizar Disponibilidade ---
with abas[2]:
    st.header("🔄 Atualizar Disponibilidade")
    livros = listar_livros()
    if livros:
        opcoes = {f"ID {livro[0]} - {livro[1]}": livro[0] for livro in livros}
        escolha = st.selectbox("Selecione o livro que deseja atualizar:", list(opcoes.keys()))
        
        livro_selecionado = next((livro for livro in livros if livro[0] == opcoes[escolha]), None)
        disponibilidade_atual = livro_selecionado[4].lower() if livro_selecionado else "sim"

        nova_disponibilidade = st.radio(
            "Defina a nova disponibilidade:",
            ["sim", "não"],
            index=0 if disponibilidade_atual == "sim" else 1
        )

        if st.button("Atualizar"):
            atualizar_livro(opcoes[escolha], nova_disponibilidade)
            st.success("🔄 Disponibilidade atualizada com sucesso!")
    else:
        st.warning("⚠️ Não há livros cadastrados para atualizar a disponibilidade.")

# --- Aba: Remover Livro ---
with abas[3]:
    st.header("❌ Remover Livro")
    livros = listar_livros()
    if livros:
        opcoes = {f"ID {livro[0]} - {livro[1]}": livro[0] for livro in livros}
        escolha = st.selectbox("Selecione o livro para remover:", list(opcoes.keys()))

        if st.button("Remover"):
            remover_livro(opcoes[escolha])
            st.success("🗑️ Livro removido com sucesso!")
            st.rerun() # Adiciona um "rerun" para atualizar a lista após a remoção
    else:
        st.warning("⚠️ Não há livros cadastrados para remover.")
