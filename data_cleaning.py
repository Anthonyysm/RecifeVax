import pandas as pd


def clean_vacinados_data(input_path: str, output_path: str):
    df = pd.read_csv(input_path)
    print(f'Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas')

    # remoção de colunas que contem dados sensiveis (por mais que estejam parcialmente anonimizados)
    df = df.drop(columns=['cpf', 'nome'], errors='ignore')

    # limpar espaços e padronizar o texto
    for col in ['sexo', 'grupo', 'vacina', 'lote', 'local_vacinação']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
            df[col] = df[col].replace(r"\s+", " ", regex=True)

    # converter data
    df['data_vacinacao'] = pd.to_datetime(
        df['data_vacinacao'], errors='coerce')

    # criar colunas de tempo
    df['ano'] = df['data_vacinacao'].dt.year
    df['mes'] = df['data_vacinacao'].dt.month
    df['dia'] = df['data_vacinacao'].dt.day

    # padronizar dose
    dose_map = {1: '1ª DOSE', 2: '2ª DOSE', 3: 'REFORÇO', 4: '4ª DOSE'}
    df["dose_tipo"] = df["dose"].map(dose_map).fillna(df["dose"].astype(str))

    # remover duplicatas
    df = df.drop_duplicates(subset=["_id"], keep="first")

    # salvando resultado
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Dados limpos salvos em: {output_path}")

    return df

if __name__ == '__main__':
    input_file = 'data/relacao-pessoas-vacinadas-covid19-recife.csv'
    output_file = 'data/relacao-pessoas-limpo.csv'
    df_clean = clean_vacinados_data(input_file, output_file)
    print(df_clean.head())