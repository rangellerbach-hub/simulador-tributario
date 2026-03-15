import streamlit as st
import google.generativeai as genai

# 1. Configuração da Página
st.set_page_config(page_title="Simulador Mini Apê - Tributos", page_icon="📊", layout="centered")

# 2. Definição da Inteligência Tributária (System Instruction)
SYSTEM_PROMPT = """
Você é um motor de cálculo tributário especializado em comparar Simples Nacional (Anexo III) vs. Lucro Presumido para os setores de locação e hospedagem.

### INPUTS DO USUÁRIO:
1. Faturamento Mensal (FM).
2. Atividade: [Locação de Bens Móveis / Locação de Bens Imóveis / Hospedagem].
3. Alíquota ISS Municipal (Apenas se a atividade for Hospedagem).

### PREMISSAS DE CÁLCULO:
1. RBT12 (Anualização): FM * 12.
2. Margem de Lucro Real do negócio (para fins informativos): 50% do FM.

### LÓGICA 1: SIMPLES NACIONAL (ANEXO III)
- Tabela Progressiva:
  * Até 180k: 6% (Ded. 0) | ISS 33,5%
  * 180k a 360k: 11,2% (Ded. 9.360) | ISS 33,5%
  * 360k a 720k: 13,5% (Ded. 17.640) | ISS 33,5%
  * 720k a 1.8M: 16,0% (Ded. 35.640) | ISS 33,5%
  * 1.8M a 3.6M: 21,0% (Ded. 125.640) | ISS 32,5%
- AEB (Alíquota Efetiva Bruta) = ((RBT12 * Alíquota Nominal) - Parcela a Deduzir) / RBT12.
- Se "Locação" (Móvel ou Imóvel): Alíquota Final = AEB * (1 - Partilha ISS).
- Se "Hospedagem": Alíquota Final = AEB total.
- Imposto Simples = FM * Alíquota Final.

### LÓGICA 2: LUCRO PRESUMIDO
- PIS/COFINS: 3,65%.
- IRPJ: Base 32%. Alíquota 15%.
- ADICIONAL IRPJ: Se (FM * 32%) > 20.000, aplica-se 10% sobre o excedente.
- CSLL: Base 32%. Alíquota 9%.
- ISS: Se "Hospedagem", usa alíquota do input. Se "Locação", 0%.
- Total Presumido = Soma de todos acima.

### OUTPUT:
Retorne uma tabela Markdown comparando os dois regimes, destacando a economia mensal e o Veredito.
"""

# 3. Interface do Usuário
st.title("📊 Simulador Tributário Mini Apê")
st.markdown("---")

# Barra lateral para API Key
with st.sidebar:
    st.title("Configurações")
    api_key = st.text_input("Insira sua Gemini API Key", type="password")
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
        st.error("Por favor, insira sua API Key na barra lateral.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
            
            prompt = f"Faturamento Mensal: R$ {faturamento}, Atividade: {atividade}, ISS informado: {iss_input}%"
            
            with st.spinner("Analisando as regras fiscais..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")

st.markdown("---")
st.caption("Nota: Este simulador é uma ferramenta de apoio e não substitui a consultoria de um contador especializado.")
