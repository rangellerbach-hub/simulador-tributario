import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Simulador Mini Apê - Tributos", page_icon="📊", layout="centered")

# 2. Instrução do Sistema (Sua inteligência tributária)
SYSTEM_PROMPT = """
Você é um motor de cálculo tributário especializado em Simples Nacional (Anexo III) e Lucro Presumido.
Dê respostas em tabelas Markdown comparando os dois regimes.
Lógica: Locação de bens (móveis/imóveis) no Anexo III NÃO paga ISS (deduzir partilha de ~33%).
Hospedagem no Anexo III PAGA ISS integral.
Lucro Presumido: PIS/COFINS (3,65%), IRPJ (15% sobre base de 32%), CSLL (9% sobre base de 32%).
Adicional IRPJ: 10% sobre base que exceder 20k/mês.
"""

# 3. Interface
st.title("📊 Simulador Tributário Mini Apê")

with st.sidebar:
    st.title("Configurações")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")

faturamento = st.number_input("Faturamento Mensal (R$)", value=65000.0)
atividade = st.selectbox("Atividade", ["Locação de Bens Móveis", "Locação de Bens Imóveis", "Hospedagem"])

if st.button("🚀 Calcular"):
    if not api_key:
        st.error("Insira a API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Tentando o modelo 1.5-flash com nomenclatura padrão
            model = genai.GenerativeModel(
                model_name='gemini-flash-lite-latest',
                system_instruction=SYSTEM_PROMPT
            )
            
            prompt = f"Faturamento: {faturamento}, Atividade: {atividade}"
            response = model.generate_content(prompt)
            st.markdown(response.text)
                
        except Exception as e:
            # Se o 1.5-flash falhar, tentamos o 1.5-pro como backup automático
            try:
                model_backup = genai.GenerativeModel(
                    model_name='gemini-flash-latest',
                    system_instruction=SYSTEM_PROMPT
                )
                response = model_backup.generate_content(f"Faturamento: {faturamento}, Atividade: {atividade}")
                st.markdown(response.text)
            except Exception as e2:
                st.error(f"Erro persistente na API: {e2}")

st.caption("Nota: Verifique se sua API Key é válida no AI Studio.")
