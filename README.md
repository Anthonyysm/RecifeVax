# RecifeVax Dashboard - Análise de Vacinação COVID-19 em Recife

## Descrição

O **RecifeVax Dashboard** é um projeto de visualização de dados sobre a vacinação contra a COVID-19 na cidade de Recife. O objetivo deste projeto é fornecer insights sobre o progresso da vacinação, incluindo a distribuição de vacinas por tipo, sexo, grupo prioritário, local de vacinação, e outros aspectos importantes.

O dashboard é interativo e foi desenvolvido utilizando **Streamlit** para a interface e **Plotly** para os gráficos. O conjunto de dados utilizado neste projeto é referente à relação de pessoas vacinadas em Recife.

## Funcionalidades

- **Vacinação Mensal**: Exibe o total de vacinados por mês com uma previsão de vacinas para os próximos 3 meses.
- **Distribuição por Tipo de Vacina**: Mostra a distribuição de vacinas aplicadas (ex.: AstraZeneca, Pfizer, Coronavac, etc.).
- **Distribuição por Sexo**: Exibe a proporção de vacinados por sexo (masculino/feminino).
- **Top 10 Grupos Prioritários**: Exibe os 10 grupos prioritários mais vacinados.
- **Top 10 Locais de Vacinação**: Exibe os 10 locais mais frequentados para vacinação.
- **Predição de Vacinação por Grupo Prioritário (Gráfico Lollipop)**: Visualiza a previsão de vacinação futura por grupo prioritário.
- **Predição de Vacinação por Local de Vacinação (Mapa de Calor)**: Exibe as predições para os próximos 3 meses para cada local de vacinação.

## Pré-requisitos

Este projeto foi desenvolvido e testado em um ambiente com as seguintes dependências:

- Python 3.x
- Bibliotecas:
  - pandas
  - numpy
  - plotly
  - streamlit
  - scikit-learn

## Como Rodar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/RecifeVax.git
cd RecifeVax

### 2. Crie e ative um ambiente virtual