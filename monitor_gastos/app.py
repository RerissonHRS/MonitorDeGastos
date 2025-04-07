import streamlit as st
from funcoes import Transacao, carregar_dados
import plotly.express as px

st.set_page_config(page_title="Controle de Gastos", layout="centered")
st.title("💰 Sistema de Monitoramento de Gastos")

# ---------- FORMULÁRIO ----------
st.header("Adicionar novo registro")

tipo = st.radio("Tipo", ["Receita", "Despesa"])
categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Educação", "Lazer", "Salário", "Outros"])
descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Salvar"):
    if valor > 0 and descricao:
        nova_transacao = Transacao(tipo, categoria, descricao, valor)
        nova_transacao.salvar()
        st.success("Registro salvo com sucesso!")
        st.experimental_rerun()  # Atualiza a página após salvar
    else:
        st.error("Preencha todos os campos!")

# ---------- TABELA DE DADOS ----------
st.header("📊 Histórico de Registros")
df = carregar_dados()

if not df.empty:
    df["Data"] = df["data"]  # Para manter compatibilidade com o gráfico
    df_exibicao = df[["data", "tipo", "categoria", "descricao", "valor"]]
    df_exibicao.columns = ["Data", "Tipo", "Categoria", "Descrição", "Valor"]
    st.dataframe(df_exibicao, use_container_width=True)

    # ---------- GRÁFICOS ----------
    st.header("📈 Demonstrativo de Gastos e Receitas")

    # Pizza
    resumo = df.groupby("tipo")["valor"].sum().reset_index()
    fig_pie = px.pie(resumo, names="tipo", values="valor", title="Distribuição entre Receitas e Despesas")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Barras por categoria
    st.subheader("💡 Gastos por Categoria (apenas Despesas)")
    df_despesas = df[df["tipo"] == "Despesa"]
    if not df_despesas.empty:
        graf_cat = df_despesas.groupby("categoria")["valor"].sum().reset_index()
        fig_bar = px.bar(graf_cat, x="categoria", y="valor", title="Total de Gastos por Categoria")
        st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.info("Nenhum dado encontrado. Adicione registros para visualizar os gráficos.")
