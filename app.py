import streamlit as st
import json
import pandas as pd
from datetime import datetime
from signals_engine import gerar_sinal

st.set_page_config(page_title="Ultimate Trader VIP", layout="wide")

# ---------- FUNÇÕES DE ARQUIVO ----------
def carregar_usuarios():
    with open("usuarios.json", "r") as f:
        return json.load(f)

def salvar_operacao(ativo, resultado):
    df = pd.read_csv("historico_operacoes.csv")
    nova = {
        "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ativo": ativo,
        "resultado": resultado
    }
    df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
    df.to_csv("historico_operacoes.csv", index=False)

def carregar_historico():
    return pd.read_csv("historico_operacoes.csv")

# ---------- LOGIN ----------
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""

if not st.session_state.logado:
    st.title("🔐 Login - Ultimate Trader VIP")
    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuarios = carregar_usuarios()
        if user in usuarios and usuarios[user] == senha:
            st.session_state.logado = True
            st.session_state.usuario = user
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")

# ---------- DASHBOARD ----------
else:
    st.title("🚀 Ultimate Trader VIP")
    st.write(f"Bem-vindo, {st.session_state.usuario}")

    st.subheader("📊 Gerar Sinal")
    ativo = st.selectbox("Escolha o ativo", ["EURUSD", "GBPUSD", "USDJPY", "BTCUSD"])

    if st.button("Gerar Sinal Profissional"):
        sinal = gerar_sinal(ativo)
        st.success(f"SINAL: {sinal}")

        col1, col2 = st.columns(2)
        if col1.button("Marcar WIN"):
            salvar_operacao(ativo, "WIN")
            st.success("WIN salvo!")
        if col2.button("Marcar LOSS"):
            salvar_operacao(ativo, "LOSS")
            st.error("LOSS salvo!")

    st.divider()

    st.subheader("📈 Histórico de Operações")
    historico = carregar_historico()
    st.dataframe(historico)

    if not historico.empty:
        total = len(historico)
        wins = len(historico[historico["resultado"] == "WIN"])
        loss = len(historico[historico["resultado"] == "LOSS"])

        st.metric("Total Operações", total)
        st.metric("Wins", wins)
        st.metric("Loss", loss)

        ranking = historico.groupby("ativo")["resultado"].apply(lambda x: (x == "WIN").sum())
        st.subheader("🏆 Ranking de Ativos Mais Lucrativos")
        st.bar_chart(ranking)
