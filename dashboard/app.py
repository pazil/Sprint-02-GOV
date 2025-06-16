import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json # Import json to load local file
import topojson

# Set page configuration
st.set_page_config(layout="wide", page_title="HP - Business Analytics Dashboard")

# --- Helper Functions ---
@st.cache_data
def load_data():
    """Loads the synthetic data."""
    data_path = os.path.join('data', 'synthetic_data.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df['call_date'] = pd.to_datetime(df['call_date'])
        return df
    else:
        st.error(f"Arquivo de dados não encontrado em '{data_path}'. Por favor, execute o script 'model/fraud_detection_rules.py' primeiro.")
        return pd.DataFrame()

@st.cache_data
def get_brazil_geojson():
    """Loads Brazil's states GeoJSON from a local file, handling TopoJSON as well."""
    geojson_path = os.path.abspath(os.path.join('data', 'uf.json'))
    try:
        with open(geojson_path, 'r', encoding='latin-1') as f:
            data = json.load(f)

        # Check if it's a TopoJSON file and convert it
        if data.get("type") == "Topology":
            obj_key = list(data['objects'].keys())[0]
            data = topojson.feature(data, data['objects'][obj_key])
            
        return data
    except FileNotFoundError:
        st.error(f"Arquivo do mapa não encontrado em '{geojson_path}'.")
        return None
    except Exception as e:
        st.error(f"Erro ao carregar ou converter o arquivo GeoJSON/TopoJSON: {e}")
        return None

@st.cache_data
def load_markdown(file_path):
    """Loads a markdown file."""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    return f"Arquivo não encontrado: {file_path}"

# --- Main App ---
def main():
    # --- Load Data ---
    df = load_data()
    if df.empty:
        return

    # --- Load GeoJSON ---
    geojson = get_brazil_geojson()

    # --- Sidebar Filters ---
    st.sidebar.image("https://logowik.com/content/uploads/images/hp-hewlett-packard2444.jpg", width=150)
    st.sidebar.title("Filtros do Dashboard")
    
    # Use selectbox for state selection
    states_options = ["Todos"] + sorted(df['state'].unique().tolist())
    selected_state = st.sidebar.selectbox(
        "Selecione o Estado",
        options=states_options,
    )

    # Use selectbox for cartridge type selection
    cartridge_options = ["Todos"] + df['cartridge_type'].unique().tolist()
    selected_cartridge_type = st.sidebar.selectbox(
        "Selecione o Tipo de Cartucho",
        options=cartridge_options,
    )

    # Filter data based on selection
    df_filtered = df.copy()
    if selected_state != "Todos":
        df_filtered = df_filtered[df_filtered['state'] == selected_state]

    if selected_cartridge_type != "Todos":
        df_filtered = df_filtered[df_filtered['cartridge_type'] == selected_cartridge_type]

    # --- Page Title ---
    st.title("Dashboard de Business Analytics & Governança de IA")
    st.markdown("Análise de chamados de suporte para combate a produtos falsificados.")
    st.markdown("---")

    # --- Entregável 1: Dashboard Interativo ---
    st.header("1. Análise de Chamados e NPS")

    # KPIs
    kpi1, kpi2, kpi3 = st.columns(3)
    
    nps_original_df = df_filtered[df_filtered['cartridge_type'] == 'original']['nps']
    nps_original = nps_original_df.mean() * 10 if not nps_original_df.empty else 0
    
    nps_generico_df = df_filtered[df_filtered['cartridge_type'] == 'generico']['nps']
    nps_generico = nps_generico_df.mean() * 10 if not nps_generico_df.empty else 0

    nps_falsificado_df = df_filtered[df_filtered['cartridge_type'] == 'falsificado']['nps']
    nps_falsificado = nps_falsificado_df.mean() * 10 if not nps_falsificado_df.empty else 0
    
    kpi1.metric("NPS Médio - Original", f"{nps_original:.1f}")
    kpi2.metric("NPS Médio - Genérico", f"{nps_generico:.1f}")
    kpi3.metric("NPS Médio - Falsificado", f"{nps_falsificado:.1f}", delta=f"{nps_falsificado - nps_original:.1f} vs Original", delta_color="inverse")

    st.markdown("#### Insights Rápidos:")

    # Insight 1: Region with most fake calls
    fakes_df = df[df['cartridge_type'] == 'falsificado']
    if not fakes_df.empty:
        top_region = fakes_df['region'].value_counts().idxmax()
        top_region_count = fakes_df['region'].value_counts().max()
        insight1_text = f"A região **{top_region}** lidera o número de chamados sobre produtos falsificados, com **{top_region_count}** casos registrados."
    else:
        insight1_text = "Nenhum chamado sobre produtos falsificados foi registrado."

    # Insight 2: NPS comparison (using the full dataset for a general insight)
    nps_insight_original_df = df[df['cartridge_type'] == 'original']['nps']
    nps_insight_original = nps_insight_original_df.mean() * 10 if not nps_insight_original_df.empty else 0

    nps_insight_generico_df = df[df['cartridge_type'] == 'generico']['nps']
    nps_insight_generico = nps_insight_generico_df.mean() * 10 if not nps_insight_generico_df.empty else 0

    insight2_text = f"O NPS médio para cartuchos **originais é {nps_insight_original:.1f}**, enquanto para **genéricos é {nps_insight_generico:.1f}**."

    st.info(f"""
    - {insight1_text}
    - {insight2_text}
    """)

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Volume de Chamados por Região e Tipo")
        chart_data = df_filtered.groupby(['region', 'cartridge_type']).size().reset_index(name='count')
        fig = px.bar(chart_data, x='region', y='count', color='cartridge_type', barmode='group',
                     title="Volume de Chamados por Região e Tipo de Cartucho",
                     labels={'region': 'Região', 'count': 'Número de Chamados', 'cartridge_type': 'Tipo de Cartucho'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Incidência de Falsificação por Estado")
        if geojson:
            falsificados_df = df_filtered[df_filtered['cartridge_type'] == 'falsificado']
            state_counts = falsificados_df['state'].value_counts().reset_index()
            state_counts.columns = ['state_abbr', 'count']

            # Map abbreviations to full names to match GeoJSON
            state_map = {
                'AC': 'Acre', 'AL': 'Alagoas', 'AP': 'Amapá', 'AM': 'Amazonas', 'BA': 'Bahia',
                'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
                'MA': 'Maranhão', 'MT': 'Mato Grosso', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
                'PA': 'Pará', 'PB': 'Paraíba', 'PR': 'Paraná', 'PE': 'Pernambuco', 'PI': 'Piauí',
                'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RS': 'Rio Grande do Sul',
                'RO': 'Rondônia', 'RR': 'Roraima', 'SC': 'Santa Catarina', 'SP': 'São Paulo',
                'SE': 'Sergipe', 'TO': 'Tocantins'
            }
            state_counts['state_full_name'] = state_counts['state_abbr'].map(state_map)
            
            # Create a complete list of states to avoid holes in the map
            all_states_df = pd.DataFrame(list(state_map.values()), columns=['state_full_name'])
            state_counts_full = pd.merge(all_states_df, state_counts, on='state_full_name', how='left')
            state_counts_full['count'] = state_counts_full['count'].fillna(0)

            fig_map = px.choropleth(
                state_counts_full,                  # Use the new complete dataframe
                geojson=geojson,
                locations='state_full_name',
                featureidkey="properties.NOME_UF",
                color='count',
                color_continuous_scale="Reds",
                scope="south america",
                title="Casos de Falsificação por Estado",
                labels={'count': 'Nº de Casos', 'state_full_name': 'Estado'}
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(height=600) # Increase map height
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.warning("Não foi possível carregar o mapa do Brasil.")

    st.subheader("Tendência de Devoluções e Suporte ao Longo do Tempo")
    df_filtered['year_month'] = df_filtered['call_date'].dt.to_period('M').astype(str)
    
    trend_data = df_filtered.groupby('year_month').agg(
        total_chamados=('id_chamado', 'count'),
        total_devolucoes=('returned', lambda x: x.sum())
    ).reset_index()
    trend_data.rename(columns={'total_chamados': 'Total de Chamados', 'total_devolucoes': 'Total de Devoluções'}, inplace=True)
    
    fig_trend = px.line(trend_data, x='year_month', y=['Total de Chamados', 'Total de Devoluções'],
                        title='Tendência Mensal de Chamados e Devoluções',
                        labels={'year_month': 'Mês/Ano', 'value': 'Quantidade', 'variable': 'Métrica'})
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("---")

    # --- Entregável 2: Modelo de Detecção ---
    st.header("2. Modelo de Detecção de Falsificação (Baseado em Regras)")
    st.markdown("A tabela abaixo mostra a **classificação de risco** aplicada pelo modelo de regras para os primeiros 10 chamados filtrados.")
    st.dataframe(df_filtered[['customer_id', 'frequencia_chamados_6_meses', 'tipo_erro_reportado', 'cartucho_registrado', 'classificacao_risco']].head(10))
    
    st.markdown("---")

    # --- Entregável 3 & 4: Planos ---
    st.header("3 & 4. Planos de Ação")
    tab1, tab2 = st.tabs(["Plano de Governança de IA", "Plano de Educação ao Cliente"])

    with tab1:
        st.markdown(load_markdown(os.path.join('reports', 'plano_governanca_ia.md')))

    with tab2:
        st.markdown(load_markdown(os.path.join('reports', 'plano_educacao_cliente.md')))

    st.markdown("---")
    
    # --- Entregável 5: Simulação de Impacto ---
    st.header("5. Simulação de Impacto Futuro")
    
    # Simulação de dados
    meses = pd.to_datetime([f"2024-{i}-01" for i in range(1, 13)])
    devolucoes_sem_acao = 100 * (1.02 ** np.arange(12)) * np.random.uniform(0.95, 1.05, 12) # 2% growth per month
    suporte_sem_acao = 150 * (1.015 ** np.arange(12)) * np.random.uniform(0.95, 1.05, 12) # 1.5% growth per month

    devolucoes_com_acao = devolucoes_sem_acao * (1 - 0.04 * np.arange(12)) # 4% reduction per month
    suporte_com_acao = suporte_sem_acao * (1 - 0.05 * np.arange(12)) # 5% reduction per month
    
    sim_df = pd.DataFrame({
        'Mês': meses,
        'Devoluções (Sem Ação)': devolucoes_sem_acao,
        'Suporte (Sem Ação)': suporte_sem_acao,
        'Devoluções (Com Ação)': np.clip(devolucoes_com_acao, 0, None),
        'Suporte (Com Ação)': np.clip(suporte_com_acao, 0, None),
    })

    col_sim1, col_sim2 = st.columns(2)

    with col_sim1:
        st.subheader("Projeção de Devoluções")
        fig_sim_dev = px.line(sim_df, x='Mês', y=['Devoluções (Sem Ação)', 'Devoluções (Com Ação)'],
                               title='Projeção de Devoluções: Com vs. Sem Ação', 
                               labels={'value': 'Número de Devoluções', 'variable': 'Cenário'})
        st.plotly_chart(fig_sim_dev, use_container_width=True)

    with col_sim2:
        st.subheader("Projeção de Chamados de Suporte")
        fig_sim_sup = px.line(sim_df, x='Mês', y=['Suporte (Sem Ação)', 'Suporte (Com Ação)'],
                               title='Projeção de Suporte Técnico: Com vs. Sem Ação', 
                               labels={'value': 'Número de Chamados', 'variable': 'Cenário'})
        st.plotly_chart(fig_sim_sup, use_container_width=True)

    st.success("""
    **Estimativas com Ação:**
    - **Redução Potencial em Suporte Técnico:** -35% após um ano com rastreamento via IA e ações de educação.
    - **Redução Potencial em Devoluções:** -20% em um ano com as medidas preventivas.
    """)

if __name__ == "__main__":
    main() 