import streamlit as st
import google.generativeai as genai

# Configuração da Página
st.set_page_config(page_title="Simulador Tributário: Containers", layout="centered")

# Configurar a API Key (Você pega no AI Studio)
st.sidebar.title("Configurações")
api_key = st.sidebar.text_input("Insira sua Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction="COLE_AQUI_A_SUA_INSTRUCAO_DO_SISTEMA")

    st.title("📊 Simulador Simples Nacional vs. Lucro Presumido")
    st.write("Calcule a melhor opção para seu negócio de containers e alojamento.")

    # Campos de entrada
    col1, col2 = st.columns(2)
    with col1:
        faturamento = st.number_input("Faturamento Mensal (R$)", min_value=0.0, value=65000.0)
    with col2:
        atividade = st.selectbox("Atividade", ["Locação de Bens Móveis", "Locação de Bens Imóveis", "Hospedagem"])

    iss_municipal = 0.0
    if atividade == "Hospedagem":
        iss_municipal = st.slider("Alíquota ISS do Município (%)", 2.0, 5.0, 3.0)

    if st.button("Calcular Melhor Opção"):
        prompt = f"Faturamento: {faturamento}, Atividade: {atividade}, ISS: {iss_municipal}%"
        
        with st.spinner("Analisando impostos..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
else:
    st.info("Por favor, insira sua API Key na barra lateral para começar.")
