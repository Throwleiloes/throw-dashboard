import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar
import math

# Configuração da página
st.set_page_config(
    page_title="Throw Leilões - Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado (continuação do código anterior com ajustes nas cores dos descontos)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    
    /* Aplicar fonte DM Sans globalmente */
    * {
        font-family: 'DM Sans', sans-serif !important;
    }
    
    .stApp { background-color: #0e0e0e; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tabs minimalistas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
        padding: 0;
        border-bottom: 1px solid #333;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #666;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #fff;
        border-bottom: 2px solid #5bc0a5;
    }
    
    /* Filtros minimalistas - FIXOS no topo */
    .filter-section {
        background-color: #1a1a1a;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #2a2a2a;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .filter-title {
        color: #fff;
        font-size: 0.9rem;
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    .stTextInput label, .stSelectbox label, .stSlider label {
        color: #999 !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
    }
    
    .stTextInput input, .stSelectbox select {
        background-color: #0e0e0e !important;
        color: #fff !important;
        border: 1px solid #333 !important;
        border-radius: 6px !important;
    }
    
    .stButton button {
        background-color: transparent;
        color: #999;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 400;
    }
    
    .stButton button:hover {
        background-color: #1a1a1a;
        color: #fff;
        border-color: #5bc0a5;
    }
    
    /* Tabela */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1a1a1a;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .custom-table thead {
        background-color: #0e0e0e;
        position: sticky;
        top: 0;
        z-index: 10;
    }
    
    .custom-table th {
        color: #999;
        font-weight: 500;
        text-align: left;
        padding: 0.75rem 0.5rem;
        font-size: 0.8rem;
        text-transform: uppercase;
        border-bottom: 1px solid #2a2a2a;
    }
    
    /* Coluna de data mais estreita */
    .custom-table th:first-child,
    .custom-table td:first-child {
        width: 90px;
        max-width: 90px;
        padding: 0.75rem 0.4rem;
    }
    
    .sortable-header {
        cursor: pointer;
        user-select: none;
        transition: color 0.2s;
    }
    
    .sortable-header:hover {
        color: #5bc0a5;
    }
    
    .custom-table tbody tr {
        border-bottom: 1px solid #2a2a2a;
    }
    
    .custom-table tbody tr:nth-child(even) {
        background-color: #151515;
    }
    
    .custom-table tbody tr:nth-child(odd) {
        background-color: #1a1a1a;
    }
    
    .custom-table tbody tr:hover {
        background-color: #252525;
    }
    
    .custom-table td {
        color: #ddd;
        padding: 0.75rem 0.5rem;
        font-size: 0.85rem;
    }
    
    .valor-verde {
        color: #5bc0a5;
        font-weight: 600;
    }
    
    /* Badges para tipos de imóvel */
    .badge-tipo {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .badge-apartamento { background-color: #5bc0a5; color: white; }
    .badge-casa { background-color: #ff6b6b; color: white; }
    .badge-terreno { background-color: #4ecdc4; color: white; }
    .badge-comercial { background-color: #ffd93d; color: #000; }
    .badge-chacara { background-color: #95e1d3; color: #000; }
    .badge-fazenda { background-color: #f38181; color: white; }
    .badge-imovel-rural { background-color: #aa96da; color: white; }
    .badge-default { background-color: #666; color: white; }
    
    .badge-modalidade {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        background-color: #5bc0a5;
        color: white;
    }
    
    /* Descontos com cores CORRIGIDAS */
    .desconto {
        font-weight: 600;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
    }
    
    /* Laranja: até 30% */
    .desconto-baixo { color: #ff6b35; }
    
    /* Amarelo: 30% a 50% */
    .desconto-medio { color: #ffd93d; }
    
    /* Verde: 50% ou mais */
    .desconto-alto { color: #5bc0a5; }
    
    /* Vermelho: Desconto suspeito (erro de dados) */
    .desconto-erro { 
        color: #ff4444 !important; 
        font-weight: 700;
        background-color: rgba(255, 68, 68, 0.1);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        cursor: help;
    }
    
    .link-icon {
        color: #5bc0a5;
        font-size: 1.2rem;
        text-decoration: none;
    }
    
    .table-container {
        max-height: 70vh;
        overflow-y: auto;
        border-radius: 8px;
        border: 1px solid #2a2a2a;
    }
    
    .table-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .table-container::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    .table-container::-webkit-scrollbar-thumb {
        background: #5bc0a5;
        border-radius: 4px;
    }
    
    /* Calendário */
    .calendar-container {
        background-color: #1a1a1a;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #2a2a2a;
    }
    
    .calendar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }
    
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 1px;
        background-color: #2a2a2a;
        border: 1px solid #2a2a2a;
    }
    
    .calendar-day-header {
        background-color: #0e0e0e;
        color: #999;
        text-align: center;
        padding: 0.75rem;
        font-size: 0.8rem;
        font-weight: 500;
        text-transform: lowercase;
    }
    
    .calendar-day {
        background-color: #1a1a1a;
        min-height: 120px;
        padding: 0.5rem;
        position: relative;
    }
    
    .calendar-day-number {
        color: #999;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    .calendar-day.other-month {
        background-color: #151515;
    }
    
    .calendar-day.other-month .calendar-day-number {
        color: #555;
    }
    
    .calendar-event {
        background-color: #5bc0a5;
        color: white;
        padding: 0.3rem 0.5rem;
        margin-bottom: 0.3rem;
        border-radius: 4px;
        font-size: 0.7rem;
        cursor: pointer;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .calendar-event:hover {
        background-color: #4aa892;
    }
    
    /* OTIMIZAÇÕES MOBILE */
    @media (max-width: 768px) {
        /* Filtros em layout vertical no mobile */
        .filter-section {
            padding: 1rem;
        }
        
        /* Reduzir tamanhos de fonte no mobile */
        .custom-table th {
            font-size: 0.7rem;
            padding: 0.5rem 0.3rem;
        }
        
        .custom-table td {
            font-size: 0.75rem;
            padding: 0.5rem 0.3rem;
        }
        
        /* Data ainda mais compacta no mobile */
        .custom-table th:first-child,
        .custom-table td:first-child {
            width: 70px;
            max-width: 70px;
            padding: 0.5rem 0.25rem;
            font-size: 0.7rem;
        }
        
        /* Badges menores no mobile */
        .badge-tipo {
            padding: 0.2rem 0.4rem;
            font-size: 0.65rem;
        }
        
        .badge-modalidade {
            padding: 0.2rem 0.4rem;
            font-size: 0.65rem;
        }
        
        /* Descontos menores */
        .desconto {
            font-size: 0.7rem;
            padding: 0.15rem 0.35rem;
        }
        
        /* Scroll horizontal suave na tabela */
        .table-container {
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        
        /* Largura mínima da tabela para permitir scroll horizontal */
        .custom-table {
            min-width: 900px;
        }
    }
    
    @media (max-width: 480px) {
        /* Mobile muito pequeno - ajustes extras */
        .custom-table th {
            font-size: 0.65rem;
            padding: 0.4rem 0.25rem;
        }
        
        .custom-table td {
            font-size: 0.7rem;
            padding: 0.4rem 0.25rem;
        }
        
        .custom-table th:first-child,
        .custom-table td:first-child {
            width: 65px;
            max-width: 65px;
            font-size: 0.65rem;
        }
        
        .filter-section {
            padding: 0.75rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
def formatar_moeda(valor):
    try:
        if pd.isna(valor) or valor == 0:
            return "-"
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "-"

def formatar_desconto(desconto):
    try:
        if pd.isna(desconto):
            return "-"
        
        desc_abs = abs(desconto)
        
        # Detectar descontos suspeitos (erro de dados) - apenas > 100%
        if desc_abs > 100:
            return f'<span class="desconto desconto-erro" title="Desconto suspeito - possível erro nos dados">⚠️ {desc_abs:.0f}%</span>'
        
        # CORES CORRIGIDAS:
        # Laranja: até 30%
        # Amarelo: 30% a 50%
        # Verde: 50% ou mais
        if desc_abs >= 50:
            classe = "desconto-alto"  # Verde
        elif desc_abs >= 30:
            classe = "desconto-medio"  # Amarelo
        else:
            classe = "desconto-baixo"  # Laranja
        
        return f'<span class="desconto {classe}">{desc_abs:.0f}%</span>'
    except:
        return "-"

def get_badge_tipo(tipo):
    tipo_lower = str(tipo).lower()
    if 'apartamento' in tipo_lower:
        return 'badge-apartamento'
    elif 'casa' in tipo_lower:
        return 'badge-casa'
    elif 'terreno' in tipo_lower:
        return 'badge-terreno'
    elif 'comercial' in tipo_lower:
        return 'badge-comercial'
    elif 'chacara' in tipo_lower or 'chácara' in tipo_lower:
        return 'badge-chacara'
    elif 'fazenda' in tipo_lower:
        return 'badge-fazenda'
    elif 'rural' in tipo_lower:
        return 'badge-imovel-rural'
    else:
        return 'badge-default'

# Carregar dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv('leiloes.csv')
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()
    
    for col in ['DATA DO LEILÃO']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce')
    
    for col in ['LANCE INICIAL (R$)', 'AVALIAÇÃO (R$)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'DESCONTO (%)' not in df.columns or df['DESCONTO (%)'].isna().all():
        df['DESCONTO (%)'] = ((df['AVALIAÇÃO (R$)'] - df['LANCE INICIAL (R$)']) / df['AVALIAÇÃO (R$)'] * 100)
    else:
        df['DESCONTO (%)'] = pd.to_numeric(df['DESCONTO (%)'], errors='coerce')
    
    return df

# Função para gerar tabela HTML com ordenação clicável
def gerar_tabela_html(df, page, per_page=50, sort_column=None, sort_order='asc'):
    # Aplicar ordenação se houver coluna selecionada
    if sort_column:
        ascending = (sort_order == 'asc')
        
        # Mapear nomes de colunas do cabeçalho para nomes reais do DataFrame
        column_map = {
            'DATA': 'DATA DO LEILÃO',
            'MUNICÍPIO': 'CIDADE/UF',
            'UF': 'CIDADE/UF',
            'BAIRRO': 'BAIRRO',
            'ENDEREÇO': 'ENDEREÇO',
            'TIPO': 'TIPO',
            'M²': 'M²',
            'AVALIAÇÃO': 'AVALIAÇÃO (R$)',
            'LANCE INICIAL': 'LANCE INICIAL (R$)',
            'DESCONTO': 'DESCONTO (%)',
            'LEILÃO': 'MODALIDADE'
        }
        
        if sort_column in column_map:
            real_column = column_map[sort_column]
            df = df.sort_values(by=real_column, ascending=ascending, na_position='last')
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    df_page = df.iloc[start_idx:end_idx]
    
    html = '<div class="table-container"><table class="custom-table">'
    
    # Cabeçalho com ordenação clicável
    html += '<thead><tr>'
    
    colunas = ['DATA', 'MUNICÍPIO', 'UF', 'BAIRRO', 'ENDEREÇO', 'TIPO', 'M²', 'AVALIAÇÃO', 'LANCE INICIAL', 'DESCONTO', '2ª PRAÇA', 'VALOR 2ª', 'LEILÃO', 'LINK']
    colunas_ordenaveis = ['DATA', 'MUNICÍPIO', 'UF', 'BAIRRO', 'TIPO', 'M²', 'AVALIAÇÃO', 'LANCE INICIAL', 'DESCONTO', 'LEILÃO']
    
    for col in colunas:
        if col in colunas_ordenaveis:
            # Determinar ícone de ordenação
            icon = ''
            if sort_column == col:
                icon = ' ↑' if sort_order == 'asc' else ' ↓'
            
            html += f'<th style="cursor: pointer; user-select: none;" class="sortable-header" data-column="{col}">{col}{icon}</th>'
        else:
            html += f'<th>{col}</th>'
    
    html += '</tr></thead>'
    
    html += '<tbody>'
    for idx, row in df_page.iterrows():
        html += '<tr>'
        
        data = row['DATA DO LEILÃO'].strftime('%d/%m/%Y') if pd.notna(row['DATA DO LEILÃO']) else '-'
        html += f'<td>{data}</td>'
        
        municipio = row['CIDADE/UF'].split('/')[0].strip().upper() if pd.notna(row['CIDADE/UF']) else '-'
        html += f'<td>{municipio}</td>'
        
        uf = row['CIDADE/UF'].split('/')[1].strip().upper() if pd.notna(row['CIDADE/UF']) and '/' in str(row['CIDADE/UF']) else '-'
        html += f'<td>{uf}</td>'
        
        bairro = row['BAIRRO'] if pd.notna(row['BAIRRO']) else '-'
        html += f'<td>{bairro}</td>'
        
        endereco = row['ENDEREÇO'] if pd.notna(row['ENDEREÇO']) else '-'
        if len(str(endereco)) > 40:
            endereco = str(endereco)[:37] + '...'
        html += f'<td>{endereco}</td>'
        
        tipo = row['TIPO'].upper() if pd.notna(row['TIPO']) else '-'
        badge_class = get_badge_tipo(tipo)
        html += f'<td><span class="badge-tipo {badge_class}">{tipo}</span></td>'
        
        m2 = int(row['M²']) if pd.notna(row['M²']) else '-'
        html += f'<td>{m2}</td>'
        
        aval = formatar_moeda(row['AVALIAÇÃO (R$)'])
        html += f'<td>{aval}</td>'
        
        lance = formatar_moeda(row['LANCE INICIAL (R$)'])
        html += f'<td><span class="valor-verde">{lance}</span></td>'
        
        desc = formatar_desconto(row['DESCONTO (%)'])
        html += f'<td>{desc}</td>'
        
        html += '<td>-</td><td>-</td>'
        
        modalidade = row['MODALIDADE'] if pd.notna(row['MODALIDADE']) else '-'
        html += f'<td><span class="badge-modalidade">{modalidade.upper()}</span></td>'
        
        link = row['LINK DETALHES'] if pd.notna(row['LINK DETALHES']) else '#'
        html += f'<td><a href="{link}" target="_blank" class="link-icon">🔗</a></td>'
        
        html += '</tr>'
    
    html += '</tbody></table></div>'
    
    return html

# Função para gerar calendário
def gerar_calendario(df, ano, mes):
    df_mes = df[
        (df['DATA DO LEILÃO'].dt.year == ano) & 
        (df['DATA DO LEILÃO'].dt.month == mes)
    ].copy()
    
    cal = calendar.monthcalendar(ano, mes)
    dias_semana = ['dom.', 'seg.', 'ter.', 'qua.', 'qui.', 'sex.', 'sáb.']
    
    html = '<div class="calendar-container">'
    html += '<div class="calendar-grid">'
    
    for dia in dias_semana:
        html += f'<div class="calendar-day-header">{dia}</div>'
    
    for semana in cal:
        for dia in semana:
            if dia == 0:
                html += '<div class="calendar-day other-month"></div>'
            else:
                data_dia = datetime(ano, mes, dia).date()
                leiloes_dia = df_mes[df_mes['DATA DO LEILÃO'].dt.date == data_dia]
                
                html += f'<div class="calendar-day">'
                html += f'<div class="calendar-day-number">{dia}</div>'
                
                for idx, leilao in leiloes_dia.head(3).iterrows():
                    tipo = leilao['TIPO'].upper() if pd.notna(leilao['TIPO']) else 'IMÓVEL'
                    cidade = leilao['CIDADE/UF'].split('/')[0].strip().upper() if pd.notna(leilao['CIDADE/UF']) else ''
                    bairro = leilao['BAIRRO'].upper() if pd.notna(leilao['BAIRRO']) else ''
                    valor = formatar_moeda(leilao['LANCE INICIAL (R$)'])
                    
                    html += f'<div class="calendar-event">'
                    html += f'{tipo} - {cidade}/{bairro}<br>'
                    html += f'<span style="font-weight: 600;">{valor}</span>'
                    html += '</div>'
                
                if len(leiloes_dia) > 3:
                    html += f'<div class="calendar-event">+{len(leiloes_dia) - 3} mais</div>'
                
                html += '</div>'
    
    html += '</div></div>'
    
    return html

# Carregar dados
df = carregar_dados()

# Tabs
tab1, tab2 = st.tabs(["📋 Planilha", "📅 Calendário"])

with tab1:
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">▼ Filtros</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Extrair UF e MUNICIPIO
    # Extrair UF: pegar tudo após a barra, remover espaços, pegar primeiras 2 letras
    df['UF'] = df['CIDADE/UF'].str.split('/').str[-1].str.strip().str[:2].str.upper()
    # Corrigir RP para PR (Paraná)
    df['UF'] = df['UF'].replace('RP', 'PR')
    df['MUNICIPIO'] = df['CIDADE/UF'].str.split('/').str[0].str.strip()
    
    with col1:
        # Filtro de Estado (UF) - apenas UFs válidas (2 letras)
        ufs_validas = df['UF'].dropna().unique()
        # Filtrar apenas UFs com exatamente 2 letras maiúsculas
        ufs_validas = [uf for uf in ufs_validas if len(str(uf)) == 2 and str(uf).isalpha() and str(uf).isupper()]
        estados = ['Todos'] + sorted(ufs_validas)
        estado_selecionado = st.selectbox("Estado", estados, key="estado")
    
    with col2:
        # Filtrar municípios válidos
        municipios_unicos = df['MUNICIPIO'].dropna().unique().tolist()
        municipios_validos = [
            m for m in municipios_unicos 
            if not any(char.isdigit() or char in ['+', '-', '*', '/', '(', ')', '[', ']', ','] for char in str(m)) 
            and str(m) not in ['-', 'nan']
            and len(str(m).strip()) > 2
            and not str(m).lower().startswith('situado')
            and not str(m).lower().startswith('localidade')
        ]
        municipios = ['Todos'] + sorted(municipios_validos)
        municipio_selecionado = st.selectbox("Município", municipios, key="municipio")
    
    with col3:
        tipos_imovel = ['Todos os Tipos'] + sorted(df['TIPO'].dropna().unique().tolist())
        tipo_selecionado = st.selectbox("Tipo de Imóvel", tipos_imovel, key="tipo")
    
    with col4:
        # Filtrar apenas modalidades válidas (remover valores com m² ou números)
        modalidades_validas = [
            m for m in df['MODALIDADE'].dropna().unique().tolist()
            if not any(char in str(m) for char in ['m²', '²']) and not str(m).replace('-', '').replace('.', '').isdigit()
        ]
        modalidades = ['Todos'] + sorted(modalidades_validas)
        modalidade_selecionada = st.selectbox("Leilão", modalidades, key="modalidade")
    
    with col5:
        desconto_min = st.slider("Desconto Mínimo (%)", 0, 100, 0, key="desconto")
    
    col6, col7 = st.columns([6, 1])
    
    with col7:
        st.write("")
        st.write("")
        if st.button("Limpar"):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if estado_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['UF'] == estado_selecionado]
    
    if municipio_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['MUNICIPIO'] == municipio_selecionado]
    
    if tipo_selecionado != 'Todos os Tipos':
        df_filtrado = df_filtrado[df_filtrado['TIPO'] == tipo_selecionado]
    
    if modalidade_selecionada != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['MODALIDADE'] == modalidade_selecionada]
    
    if desconto_min > 0:
        df_filtrado = df_filtrado[df_filtrado['DESCONTO (%)'].abs() >= desconto_min]
    
    # Paginação
    per_page = 50
    total_pages = math.ceil(len(df_filtrado) / per_page)
    
    if 'page' not in st.session_state:
        st.session_state.page = 1
    
    if 'sort_column' not in st.session_state:
        st.session_state.sort_column = None
    
    if 'sort_order' not in st.session_state:
        st.session_state.sort_order = 'asc'
    
    st.markdown(f'<h3 style="color: #fff; font-weight: 400;">📋 Exibindo {len(df_filtrado)} leilões</h3>', unsafe_allow_html=True)
    
    tabela_html = gerar_tabela_html(df_filtrado, st.session_state.page, per_page, st.session_state.sort_column, st.session_state.sort_order)
    st.markdown(tabela_html, unsafe_allow_html=True)
    
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("⬅️ Anterior", disabled=(st.session_state.page == 1)):
            st.session_state.page -= 1
            st.rerun()
    
    with col_info:
        st.markdown(f"<p style='text-align: center; color: #999;'>Página {st.session_state.page} de {total_pages}</p>", unsafe_allow_html=True)
    
    with col_next:
        if st.button("Próxima ➡️", disabled=(st.session_state.page >= total_pages)):
            st.session_state.page += 1
            st.rerun()

with tab2:
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">▼ Filtros</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        # Filtro de Estado (UF)
        estado_cal = st.selectbox("Estado", estados, key="estado_cal")
    
    with col2:
        # Usar mesma lista de municípios válidos
        municipios_unicos_cal = df['MUNICIPIO'].dropna().unique().tolist()
        municipios_validos_cal = [
            m for m in municipios_unicos_cal 
            if not any(char.isdigit() or char in ['+', '-', '*', '/', '(', ')', '[', ']', ','] for char in str(m)) 
            and str(m) not in ['-', 'nan']
            and len(str(m).strip()) > 2
            and not str(m).lower().startswith('situado')
            and not str(m).lower().startswith('localidade')
        ]
        municipios_cal = ['Todos'] + sorted(municipios_validos_cal)
        municipio_cal = st.selectbox("Município", municipios_cal, key="municipio_cal")
    
    with col3:
        tipo_cal = st.selectbox("Tipo de Imóvel", tipos_imovel, key="tipo_cal")
    
    with col4:
        modalidade_cal = st.selectbox("Leilão", modalidades, key="modalidade_cal")
    
    with col5:
        desconto_min_cal = st.slider("Desconto Mínimo (%)", 0, 100, 0, key="desconto_cal")
    
    col6, col7 = st.columns([6, 1])
    
    with col7:
        st.write("")
        st.write("")
        if st.button("Limpar", key="limpar_cal"):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    df_cal_filtrado = df[df['DATA DO LEILÃO'].notna()].copy()
    
    if estado_cal != 'Todos':
        df_cal_filtrado = df_cal_filtrado[df_cal_filtrado['UF'] == estado_cal]
    
    if municipio_cal != 'Todos':
        df_cal_filtrado = df_cal_filtrado[df_cal_filtrado['MUNICIPIO'] == municipio_cal]
    
    if tipo_cal != 'Todos os Tipos':
        df_cal_filtrado = df_cal_filtrado[df_cal_filtrado['TIPO'] == tipo_cal]
    
    if modalidade_cal != 'Todos':
        df_cal_filtrado = df_cal_filtrado[df_cal_filtrado['MODALIDADE'] == modalidade_cal]
    
    if desconto_min_cal > 0:
        df_cal_filtrado = df_cal_filtrado[df_cal_filtrado['DESCONTO (%)'].abs() >= desconto_min_cal]
    
    # Navegação do calendário
    if 'cal_mes' not in st.session_state:
        st.session_state.cal_mes = datetime.now().month
    if 'cal_ano' not in st.session_state:
        st.session_state.cal_ano = datetime.now().year
    
    col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
    
    with col_nav1:
        col_prev_mes, col_hoje = st.columns(2)
        with col_prev_mes:
            if st.button("◀"):
                if st.session_state.cal_mes == 1:
                    st.session_state.cal_mes = 12
                    st.session_state.cal_ano -= 1
                else:
                    st.session_state.cal_mes -= 1
                st.rerun()
        with col_hoje:
            if st.button("Hoje"):
                st.session_state.cal_mes = datetime.now().month
                st.session_state.cal_ano = datetime.now().year
                st.rerun()
    
    with col_nav2:
        meses_pt = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 
                    'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
        mes_nome = meses_pt[st.session_state.cal_mes - 1]
        st.markdown(f"<h2 style='text-align: center; color: #fff;'>{mes_nome} de {st.session_state.cal_ano}</h2>", unsafe_allow_html=True)
    
    with col_nav3:
        col_prox_mes, col_views = st.columns([1, 2])
        with col_prox_mes:
            if st.button("▶"):
                if st.session_state.cal_mes == 12:
                    st.session_state.cal_mes = 1
                    st.session_state.cal_ano += 1
                else:
                    st.session_state.cal_mes += 1
                st.rerun()
        with col_views:
            st.markdown('<div style="display: flex; gap: 0.5rem; justify-content: flex-end;"><button style="background-color: #5bc0a5; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px;">Mês</button><button style="background-color: transparent; color: #999; border: 1px solid #333; padding: 0.5rem 1rem; border-radius: 6px;">Semana</button><button style="background-color: transparent; color: #999; border: 1px solid #333; padding: 0.5rem 1rem; border-radius: 6px;">Dia</button></div>', unsafe_allow_html=True)
    
    calendario_html = gerar_calendario(df_cal_filtrado, st.session_state.cal_ano, st.session_state.cal_mes)
    st.markdown(calendario_html, unsafe_allow_html=True)



