import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURAÇÃO DA PÁGINA (CORRIGIDO) ---
# Deve ser sempre a primeira linha de comando Streamlit
st.set_page_config(
    page_title="Dashboard Olist - Case Dadosfera",
    layout="wide",
    page_icon="🛒"
)

# --- 2. LEITURA DOS DADOS ---
@st.cache_data
def load_data():
    # Lê o arquivo ZIP
    df_vendas = pd.read_csv("data/fct_vendas.zip", compression='zip') 
    
    # Lê as dimensões
    df_produtos = pd.read_csv("data/dim_produtos.csv")
    
    # Tratamento de datas
    df_vendas['dt_compra'] = pd.to_datetime(df_vendas['dt_compra'])
    
    # Merge (Join) para trazer o nome da categoria
    # Garante que as colunas existem antes de fazer o merge
    if 'id_produto' in df_vendas.columns and 'id_produto' in df_produtos.columns:
        df_merged = df_vendas.merge(df_produtos[['id_produto', 'desc_categoria_pt']], on='id_produto', how='left')
    else:
        st.error("Erro: Coluna 'id_produto' não encontrada para cruzamento.")
        return df_vendas
    
    return df_merged

try:
    with st.spinner("Carregando dados..."):
        df = load_data()
except Exception as e:
    st.error(f"Erro ao ler arquivos. Verifique se 'data/fct_vendas.zip' existe. Detalhe: {e}")
    st.stop()

# --- 3. BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros do Dashboard")

# Filtro de Data (Corrigido)
min_date = df['dt_compra'].min().date()
max_date = df['dt_compra'].max().date()

# Pega o retorno do calendário
date_range = st.sidebar.date_input(
    "Período de Análise",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Validação: Só prossegue se tiver as 2 datas (Inicio e Fim)
if len(date_range) != 2:
    st.warning("⚠️ Por favor, selecione a data final no calendário.")
    st.stop() # Para a execução aqui até o usuário escolher a segunda data

start_date, end_date = date_range

# Filtro de Categoria
if 'desc_categoria_pt' in df.columns:
    categorias = df['desc_categoria_pt'].dropna().unique()
    categorias_selecionadas = st.sidebar.multiselect(
        "Categorias",
        options=categorias,
        default=list(categorias)[:3] # Seleciona 3 por padrão
    )
else:
    st.warning("Coluna de Categoria não encontrada.")
    categorias_selecionadas = []

# --- 4. APLICAÇÃO DOS FILTROS ---
df_filtered = df[
    (df['dt_compra'].dt.date >= start_date) &
    (df['dt_compra'].dt.date <= end_date)
]

if categorias_selecionadas:
    df_filtered = df_filtered[df_filtered['desc_categoria_pt'].isin(categorias_selecionadas)]

# --- 5. DASHBOARD ---
st.title("🛒 Dashboard E-commerce Olist")
st.markdown("---")

# --- FUNÇÃO FORMATADORA ---
def format_big_number(value, prefix=""):
    if value >= 1_000_000_000:
        return f"{prefix} {value / 1_000_000_000:.2f} Bi"
    elif value >= 1_000_000:
        return f"{prefix} {value / 1_000_000:.2f} Mi"
    elif value >= 1_000:
        return f"{prefix} {value / 1_000:.2f} K"
    return f"{prefix} {value:.2f}"

# Linha 1: KPIs
col1, col2, col3, col4 = st.columns(4)

total_vendas = df_filtered['vl_total_item'].sum()
qtd_pedidos = df_filtered['id_pedido'].nunique()
ticket_medio = total_vendas / qtd_pedidos if qtd_pedidos > 0 else 0

# APLICAÇÃO DA FORMATAÇÃO
col1.metric("💰 Receita Total", format_big_number(total_vendas, "R$"))
col2.metric("📦 Qtd Pedidos", f"{qtd_pedidos}")
col3.metric("🎫 Ticket Médio", f"R$ {ticket_medio:,.2f}")

# KPI de IA (Ajustado para mostrar N/A se for muito pouco)
if 'sentimento_ia' in df_filtered.columns:
    df_ia_valid = df_filtered[df_filtered['sentimento_ia'].isin(['Positivo', 'Negativo', 'Neutro'])]
    total_ia = df_ia_valid.shape[0]
    
    if total_ia > 0:
        positivos = df_ia_valid[df_ia_valid['sentimento_ia'] == 'Positivo'].shape[0]
        pct_positivo = (positivos / total_ia * 100)
        col4.metric("🤖 IA Positiva (Amostra)", f"{pct_positivo:.1f}%")
    else:
        col4.metric("🤖 IA Positiva", "N/A (S/ Dados)")
else:
    col4.metric("🤖 IA", "N/A")

st.markdown("---")

# Linha 2: Gráficos
col_left, col_right = st.columns(2)

# Gráfico Temporal (Ajustado)
# Agrupa por Mês (M) e preenche vazios com 0 (fillna)
vendas_tempo = df_filtered.set_index('dt_compra').resample('M')['vl_total_item'].sum().fillna(0).reset_index()

# Formata a data para ficar bonitinho no gráfico (Ano-Mês)
vendas_tempo['periodo'] = vendas_tempo['dt_compra'].dt.strftime('%b/%Y')

fig_line = px.area(
    vendas_tempo, 
    x='dt_compra', 
    y='vl_total_item', 
    title='Evolução de Vendas (Mensal)',
    labels={'dt_compra': 'Mês', 'vl_total_item': 'Receita (R$)'} # Nomes amigáveis
)
col_left.plotly_chart(fig_line, use_container_width=True)

# Gráfico Categorias
if 'desc_categoria_pt' in df_filtered.columns:
    vendas_cat = df_filtered.groupby('desc_categoria_pt')['vl_total_item'].sum().reset_index().sort_values(by='vl_total_item', ascending=False).head(10)
    fig_bar = px.bar(vendas_cat, x='vl_total_item', y='desc_categoria_pt', orientation='h', title='Top 10 Categorias')
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
    col_right.plotly_chart(fig_bar, use_container_width=True)
