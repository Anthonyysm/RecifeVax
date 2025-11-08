from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title='RecifeVax Dashboard', layout='wide')
st.title(
    '💉 RecifeVax - Relação de Pessoas Vacinadas contra Covid-19 em Recife'
)

# -------------------------------
# Carregar dados
# -------------------------------


@st.cache_data
def load_data():
    df = pd.read_csv(
        'data/relacao-pessoas-limpo.csv', parse_dates=['data_vacinacao']
    )
    return df


df = load_data()

# -------------------------------
# Vacinação mensal
# -------------------------------
df['ano_mes'] = df['data_vacinacao'].dt.to_period('M')
vacinacao_mensal = (
    df.groupby('ano_mes').size().reset_index(name='total_vacinados')
)
vacinacao_mensal['data'] = vacinacao_mensal['ano_mes'].dt.to_timestamp()

# -------------------------------
# Predição futura (3 meses)
# -------------------------------
vacinacao_mensal['mes_ordinal'] = np.arange(len(vacinacao_mensal)).reshape(
    -1, 1
)
X = vacinacao_mensal[['mes_ordinal']]
y = vacinacao_mensal['total_vacinados']
model = LinearRegression()
model.fit(X, y)

future_months = np.arange(
    len(vacinacao_mensal), len(vacinacao_mensal) + 3
).reshape(-1, 1)
predicoes = model.predict(future_months)
future_dates = pd.date_range(
    start=vacinacao_mensal['data'].max() + pd.offsets.MonthBegin(1),
    periods=3,
    freq='MS',
)
pred_df = pd.DataFrame({'data': future_dates, 'total_vacinados': predicoes})

# -------------------------------
# Gráfico: Vacinação Mensal + Predição
# -------------------------------
fig1 = px.line(
    vacinacao_mensal,
    x='data',
    y='total_vacinados',
    markers=True,
    title='Vacinação Mensal em Recife (com previsão)',
    labels={'total_vacinados': 'Total de vacinados', 'data': 'Mês/Ano'},
    color_discrete_sequence=['#1f77b4'],
)
fig1.add_scatter(
    x=pred_df['data'],
    y=pred_df['total_vacinados'],
    mode='lines+markers',
    line=dict(dash='dot', color='red'),
    name='Predição',
)
fig1.update_layout(
    template='plotly_white',
    hovermode='x unified',
    xaxis_title='Mês/Ano',
    yaxis_title='Total de Vacinação',
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# Distribuição por tipo de vacina
# -------------------------------
vacina_tipo = df['vacina'].value_counts().reset_index()
vacina_tipo.columns = ['vacina', 'total']

fig2 = px.bar(
    vacina_tipo,
    x='vacina',
    y='total',
    text='total',
    title='Distribuição por Tipo de Vacina',
    labels={'vacina': 'Vacina', 'total': 'Número de doses'},
    color='vacina',
    color_discrete_sequence=px.colors.qualitative.Set2,
    height=650,
)
fig2.update_traces(textposition='outside')
fig2.update_layout(
    template='plotly_white',
    xaxis_tickangle=-45,
    xaxis_title='Vacina',
    yaxis_title='Número de doses',
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Distribuição por sexo
# -------------------------------
sexo_dist = df['sexo'].value_counts().reset_index()
sexo_dist.columns = ['sexo', 'total']

fig3 = px.pie(
    sexo_dist,
    names='sexo',
    values='total',
    title='Distribuição por Sexo',
    color='sexo',
    color_discrete_map={'MASCULINO': '#1f77b4', 'FEMININO': '#ff7f0e'},
)
fig3.update_traces(textposition='outside', textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# Top 10 grupos prioritários
# -------------------------------
top_grupos = df['grupo'].value_counts().nlargest(10).reset_index()
top_grupos.columns = ['grupo', 'total']

fig4 = px.bar(
    top_grupos,
    x='grupo',
    y='total',
    text='total',
    title='Top 10 Grupos Prioritários',
    color='grupo',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    height=650,
)
fig4.update_traces(textposition='outside')
fig4.update_layout(
    template='plotly_white',
    xaxis_tickangle=-45,
    xaxis_title='Grupo',
    yaxis_title='Número de Pessoas',
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------
# Top 10 locais de vacinação
# -------------------------------
top_locais = df['local_vacinacao'].value_counts().nlargest(10).reset_index()
top_locais.columns = ['local_vacinacao', 'total']

fig5 = px.bar(
    top_locais,
    x='local_vacinacao',
    y='total',
    text='total',
    title='Top 10 Locais de Vacinação',
    color='local_vacinacao',
    color_discrete_sequence=px.colors.qualitative.Vivid,
    height=650,
)
fig5.update_traces(textposition='outside')
fig5.update_layout(
    template='plotly_white',
    xaxis_tickangle=-45,
    xaxis_title='Local de Vacinação',
    yaxis_title='Número de Pessoas',
)
st.plotly_chart(fig5, use_container_width=True)

# -------------------------------
# Gráfico Lollipop: Predição por grupo
# -------------------------------
grupo_prop = df.groupby('grupo').size() / len(df)
predicoes_grupo = grupo_prop * predicoes[-1]
pred_grupo_df = pd.DataFrame(
    {
        'grupo': grupo_prop.index,
        'total_previsto': predicoes_grupo.values,
        'historico': df.groupby('grupo').size().values,
    }
)
pred_grupo_df = pred_grupo_df.sort_values('total_previsto', ascending=True)

fig6 = go.Figure()

# Linhas do lollipop
fig6.add_trace(
    go.Scatter(
        x=pred_grupo_df['total_previsto'],
        y=pred_grupo_df['grupo'],
        mode='lines',
        line=dict(color='lightgray', width=2),
        showlegend=False,
    )
)

# Pontos do lollipop com hover customizado
fig6.add_trace(
    go.Scatter(
        x=pred_grupo_df['total_previsto'],
        y=pred_grupo_df['grupo'],
        mode='markers+text',
        marker=dict(color='#1f77b4', size=12),
        text=pred_grupo_df['total_previsto'].astype(int),
        textposition='middle right',
        name='Previsão',
        hovertemplate='Grupo: %{y}<br>Total Previsto: %{x}<extra></extra>',
    )
)

fig6.update_layout(
    title='Predição de Vacinação por Grupo Prioritário (Lollipop Chart)',
    xaxis_title='Total Previsto',
    yaxis_title='Grupo',
    template='plotly_white',
    height=700,
)

st.plotly_chart(fig6, use_container_width=True)

# -------------------------------
# Predição de locais de vacinação (Mapa de Calor)
# -------------------------------
df['ano_mes'] = df['data_vacinacao'].dt.to_period('M')
locais_mensal = (
    df.groupby(['local_vacinacao', 'ano_mes'])
    .size()
    .reset_index(name='total_vacinados')
)

predicoes_locais = []
future_dates = pd.date_range(
    start=df['data_vacinacao'].max() + pd.offsets.MonthBegin(1),
    periods=3,
    freq='MS',
)

for local in locais_mensal['local_vacinacao'].unique():
    df_local = locais_mensal[
        locais_mensal['local_vacinacao'] == local
    ].reset_index(drop=True)
    if len(df_local) < 2:
        continue
    X_local = np.arange(len(df_local)).reshape(-1, 1)
    y_local = df_local['total_vacinados']
    model_local = LinearRegression()
    model_local.fit(X_local, y_local)
    X_future = np.arange(len(df_local), len(df_local) + 3).reshape(-1, 1)
    y_pred_local = model_local.predict(X_future)
    predicoes_locais.append(
        pd.DataFrame(
            {
                'local_vacinacao': local,
                'mes': future_dates,
                'total_previsto': y_pred_local,
            }
        )
    )

heatmap_df = pd.concat(predicoes_locais)
heatmap_df['mes'] = heatmap_df['mes'].dt.strftime('%b %Y')

fig_heatmap = px.density_heatmap(
    heatmap_df,
    x='mes',
    y='local_vacinacao',
    z='total_previsto',
    labels={
        'local_vacinacao': 'Local de Vacinação',
        'total_previsto': 'Total Previsto',
    },
    color_continuous_scale='Viridis',
    title='Predição de Vacinação por Local nos Próximos 3 Meses',
)
fig_heatmap.update_layout(
    template='plotly_white',
    height=700,
    xaxis_title='Mês',
    yaxis_title='Local de Vacinação',
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# -------------------------------
# Análise de PLN: Agrupamento de Vacinas por Similaridade
# -------------------------------

st.subheader('🧠 Análise de Linguagem Natural (PLN) - Agrupamento de Vacinas')

# Preparar os textos de vacina
vacinas_texto = df['vacina'].dropna().astype(str)

# Vetorização TF-IDF (transforma texto em números)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(vacinas_texto)

# Agrupar por similaridade semântica (3 clusters)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster_vacina'] = kmeans.fit_predict(X)

# Agrupar e contar vacinas por cluster
vacina_clusters = (
    df.groupby('cluster_vacina')['vacina']
    .value_counts()
    .groupby(level=0)
    .head(10)
    .reset_index(name='contagem')
)

# Gráfico de barras mostrando os clusters
fig_pln = px.bar(
    vacina_clusters,
    x='vacina',
    y='contagem',
    color='cluster_vacina',
    title='Vacinas Agrupadas por Similaridade (PLN - TF-IDF + KMeans)',
    labels={'vacina': 'Vacina', 'contagem': 'Quantidade'},
    color_discrete_sequence=px.colors.qualitative.Safe,
    height=650,
)

fig_pln.update_layout(
    template='plotly_white',
    xaxis_tickangle=-45,
    xaxis_title='Vacina',
    yaxis_title='Quantidade',
)

st.plotly_chart(fig_pln, use_container_width=True)

# Insight rápido
top_vacina = df['vacina'].value_counts().idxmax()
st.info(
    f'💡 Insight: a vacina mais aplicada foi **{top_vacina}**, com destaque entre os clusters detectados.'
)
