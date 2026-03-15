import streamlit as st
import google.generativeai as genai
import os

# 1. Configuração da Página
st.set_page_config(page_title="Simulador Mini Apê - Tributos", page_icon="📊", layout="centered")

# 2. Definição da Inteligência Tributária (System Instruction)
SYSTEM_PROMPT = """
Você é um motor de cálculo tributário especializado em comparar Simples Nacional (Anexo III) vs. Lucro Presumido para os setores de locação e hospedagem no Brasil.

### INPUTS DO USUÁRIO:
1. Faturamento Mensal (FM).
2. Atividade: [Locação de Bens Móveis / Locação de Bens Imóveis / Hospedagem].
3. Alíquota ISS Municipal (Apenas se a atividade for Hospedagem).

### LÓGICA DE CÁLCULO:
- RBT12: FM * 12.
- Simples Anexo III: Calcular alíquota efetiva e SUBTRAIR a partilha do ISS se for Locação.
- Lucro Presumido: PIS/COFINS (3,65%), IRPJ (15% sobre base de 32%), CSLL (9% sobre base de 32%). 
- Adicional IRPJ: 10% sobre a parcela da base (FM * 32%) que exceder R$ 20.000,00.

### OUTPUT:
Retorne uma tabela Markdown comparando os dois regimes e dê um veredito claro.
"""

# 3. Interface do Usuário
st.title("📊 Simulador Tributário Mini Apê")
st.markdown("---")

# Tentativa de pegar a chave automaticamente dos Secrets ou do campo lateral
with st.sidebar:
    st.title("Configurações")
    # Busca a chave nos Secrets do Streamlit primeiro
    secret_key = st.secrets.get("GEMINI_API_KEY", "")
    api_key = st.text_input("Gemini API Key", value=secret_key, type="password")
    if not api_key:
        st.info("Obtenha sua chave em: https://aistudio.google.com/app/apikey")

# Campos de entrada
col1, col2 = st.columns(2)
with col1:
    faturamento = st.number_input("Faturamento Mensal (R$)", min_value=0.0, value=65000.0, step=1000.0)
with col2:
    atividade = st.selectbox("Atividade", ["Locação de Bens Móveis", "Locação de Bens Imóveis", "Hospedagem"])

iss_input = 0.0
if atividade == "Hospedagem":
    iss_input = st.slider("Alíquota ISS do seu Município (%)", 2.0, 5.0, 3.0)

# 4. Execução do Cálculo
if st.button("🚀 Calcular Melhor Opção"):
    if not api_key:
        st.error("Por favor, insira sua API Key.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # ALTERAÇÃO AQUI: Usando o nome estável do modelo
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=SYSTEM_PROMPT
            )
            
            prompt = f"Faturamento Mensal: R$ {faturamento}, Atividade: {atividade}, ISS informado: {iss_input}%"
            
            with st.spinner("Analisando as regras fiscais..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Erro na API: {e}")

st.markdown("---")
st.caption("Nota: Este simulador é uma ferramenta de apoio e não substitui um contador.")
