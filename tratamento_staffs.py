import pandas as pd

staffs_df = pd.read_csv('staffs.csv')
print(staffs_df.head())

# Tratar Valores Nulos
staffs_df_tratado = staffs_df.fillna(0)
print("Dados após tratamento de valores nulos:\n", staffs_df_tratado.head())

staffs_df_tratado.to_csv('staffs_tratados.csv', index=False)
print(staffs_df_tratado.head())