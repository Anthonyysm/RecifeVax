import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import json

# === Caminhos base ===
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / 'data' / 'relacao-pessoas-limpo.csv'
MODELS_DIR = ROOT / 'models'
MODELS_DIR.mkdir(exist_ok=True)

# === Função principal ===


def load_local_data():
    """Carrega o CSV local limpo e retorna DataFrame."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f'Arquivo não encontrado: {DATA_PATH}')
    df = pd.read_csv(DATA_PATH, sep=',', encoding='utf-8', low_memory=False)
    return df


def prepare_monthly(df: pd.DataFrame):
    """Agrega o total de vacinações por mês e cria feature temporal."""
    if 'data_vacinacao' not in df.columns:
        raise RuntimeError("Coluna 'data_vacinacao' não encontrada no CSV.")

    df['data_vacinacao'] = pd.to_datetime(
        df['data_vacinacao'], errors='coerce'
    )
    df = df.dropna(subset=['data_vacinacao'])
    df['ano'] = df['data_vacinacao'].dt.year
    df['mes'] = df['data_vacinacao'].dt.month

    monthly = (
        df.groupby(['ano', 'mes']).size().reset_index(name='total_vacinados')
    )
    monthly = monthly.sort_values(['ano', 'mes']).reset_index(drop=True)
    monthly['mes_ordinal'] = np.arange(len(monthly))

    return monthly


def train_and_save():
    """Treina modelo RandomForest e salva artefatos e métricas."""
    print('Carregando dados...')
    df_raw = load_local_data()
    monthly = prepare_monthly(df_raw)
    print('Dados mensais preparados:', monthly.shape)

    X = monthly[['mes_ordinal', 'ano', 'mes']]
    y = monthly['total_vacinados'].values

    # Split temporal (mantém ordem)
    split_idx = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]

    pipeline = Pipeline(
        [
            ('scaler', StandardScaler()),
            (
                'rf',
                RandomForestRegressor(
                    n_estimators=200, random_state=42, n_jobs=-1
                ),
            ),
        ]
    )

    print('Treinando modelo...')
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)

    metrics = {
        'r2': float(r2_score(y_test, preds)),
        'rmse': float(mean_squared_error(y_test, preds) ** 0.5),
        'mae': float(mean_absolute_error(y_test, preds)),
        'n_train': int(len(X_train)),
        'n_test': int(len(X_test)),
    }

    joblib.dump(pipeline, MODELS_DIR / 'rf_pipeline.joblib')
    with open(MODELS_DIR / 'metrics.json', 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    print('\nTreinamento concluído com sucesso!')
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return metrics


if __name__ == '__main__':
    train_and_save()
