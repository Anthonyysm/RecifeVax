import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Carregar CSV
df = pd.read_csv(
    'data/relacao-pessoas-limpo.csv',
    sep=',',
    encoding='utf-8',
    low_memory=False,
)

texts = df['vacina'].dropna().astype(str)

# Vetorização TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Clustering para descobrir grupos de vacinas parecidas
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

df['cluster'] = kmeans.labels_

# Mostrar insight simples
print(df.groupby('cluster')['vacina'].value_counts().head(10))
