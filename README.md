# 💉 RecifeVax – Análise e Predição da Vacinação na Cidade do Recife

O **RecifeVax** é um projeto de análise e modelagem de dados que explora informações reais de vacinação aplicadas na cidade do Recife.  
O objetivo é gerar **insights visuais, previsões automáticas e agrupamentos inteligentes**, transformando dados brutos em conhecimento acessível e interativo.

---

## 🚀 Proposta

A ideia central é simples: entender **como a vacinação evolui ao longo do tempo** e identificar **padrões que podem apoiar decisões estratégicas**.  
O sistema utiliza:
- **Python e Pandas** para limpeza e processamento dos dados;
- **Plotly e Streamlit** para dashboards interativos;
- **Scikit-Learn** para previsão de doses aplicadas (Regressão Linear);
- **TF-IDF + KMeans (PLN)** para agrupamento semântico dos tipos de vacinas.

O resultado é uma aplicação web capaz de:
- Exibir o histórico mensal de vacinação;
- Comparar vacinas mais aplicadas;
- Gerar previsões automáticas de tendência;
- Agrupar vacinas por similaridade textual usando técnicas de PLN.

---

## 📂 Estrutura do Projeto
```
RecifeVax/
│
├── app.py                 # Arquivo principal da aplicação
├── data_cleaning.py       # Processamento e limpeza dos dados
├── ml_model.py            # Modelo(s) de Machine Learning
├── pln_model.py           # Modelo(s) de Processamento de Linguagem Natural
├── requirements.txt       # Dependências do projeto
├── LICENSE                # Licença
├── README.md              # Documentação principal
│
├── models/                # (Gerado automaticamente) Modelos treinados
├── content/               # Conteúdos gerados (gráficos, relatórios)
│
├── data/                  # Datasets usados no projeto
│   ├── relacao-pessoas-vacinadas-covid19-recife.csv
│   └── relacao-pessoas-limpo.csv
│
└── notebooks/             # Notebooks de análise
    └── eda_vacinacao.ipynb
```

---

## ⚙️ Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/Anthonyysm/RecifeVax.git
```

Acessar a pasta
```bash
cd RecifeVax
```

### 2. Crie e ative um ambiente virtual
#### Executar no Windows
```bash
python -m venv .venv
```
```bash
.venv\Scripts\activate
```
#### Executar no Linux
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```
### 4. Gere o dataset limpo
```bash
python data_cleaning.py
```
### 5. Treine os modelos
##### Machine Learning:
```bash
python ml_model.py
```
##### PLN:
```bash
python pln_model.py
```
### 6. Execute o dashboard
```bash
streamlit run app.py
```

O aplicativo será aberto automaticamente no navegador.  
Lá você poderá interagir com gráficos dinâmicos, previsões e análises semânticas.

---

## 📊 Tecnologias Utilizadas

- **Python 3.13**
- **Pandas / NumPy**
- **Plotly Express**
- **Streamlit**
- **Scikit-Learn**
- **TF-IDF / KMeans (NLP)**

---

## 💡 Principais Insights

- É possível prever a tendência mensal de doses aplicadas com base em séries históricas.
- A distribuição de vacinas por sexo, grupo e tipo revela padrões de cobertura e campanhas específicas.
- O uso de **PLN (Processamento de Linguagem Natural)** permite entender quais vacinas são semanticamente parecidas, ajudando a categorizar dados inconsistentes.
- O painel é 100% interativo e pode ser facilmente adaptado para qualquer outro município.

---

## 🌎 Impacto e Próximos Passos

O RecifeVax é um exemplo prático de como **dados públicos podem ser transformados em ferramentas de análise real**.  
Os próximos passos incluem:
- Adicionar previsão por grupo ou local de vacinação;
- Treinar modelos mais robustos (RandomForest, Prophet);
- Conectar o app a APIs reais de dados abertos.

---

## 🤝 Contribuição

Contribuições são muito bem-vindas!  
Sinta-se à vontade para:
- Abrir issues;
- Enviar pull requests;
- Sugerir melhorias de visualização, modelo ou interface.

---

⭐ Se este projeto te inspirou, deixe uma estrela no repositório e compartilhe — cada apoio ajuda o RecifeVax a crescer!
