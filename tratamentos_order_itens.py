import pandas as pd
pd.set_option('display.width', None)

# Carregar os dados
orders_itens_df = pd.read_csv('order_itens1.csv')

print("Visão geral dos dados:")
print(orders_itens_df.head())
print("\nInformações do DataFrame:")
print(orders_itens_df.info())
print("\nEstatísticas descritivas de list_price:")
print(orders_itens_df['list_price'].describe())

# Verificar valores ausentes
print("\nValores nulos por coluna:")
print(orders_itens_df.isnull().sum())

# Verificar outliers em list_price
Q1 = orders_itens_df['list_price'].quantile(0.25)
Q3 = orders_itens_df['list_price'].quantile(0.75)
IQR = Q3 - Q1
limite_baixo = Q1 - 1.5 * IQR
limite_alto = Q3 + 1.5 * IQR

print(f"\nLimites para outliers: Menor = {limite_baixo}, Maior = {limite_alto}")
outliers_IQR = orders_itens_df[(orders_itens_df['list_price'] < limite_baixo) | (orders_itens_df['list_price'] > limite_alto)]
print(f"Número de outliers em list_price: {len(outliers_IQR)}")
print("Exemplo de outliers pelo IQR:")
print(outliers_IQR[['order_id', 'item_id', 'list_price']].head())

# Outliers não removidos porque seriam excluídos produtos apenas por ter um valor alto
# Novo Limite setado para incluir apenas produtos com valores incompatíveis
limite_baixo = 89
limite_alto = 13000

outliers = orders_itens_df[(orders_itens_df['list_price'] < limite_baixo) | (orders_itens_df['list_price'] > limite_alto)]
print("Exemplo de outliers:")
print(outliers[['order_id', 'item_id', 'list_price']].head())

# Criar DataFrame tratado com cópia
order_itens_tratados = orders_itens_df[(orders_itens_df['list_price'] >= limite_baixo) & (orders_itens_df['list_price'] <= limite_alto)].copy()

# Criar coluna de Valor Total sem desconto
order_itens_tratados.loc[:, 'preco_total'] = order_itens_tratados['list_price'] * order_itens_tratados['quantity']

# Criar coluna de Valor total com desconto
order_itens_tratados.loc[:, 'preco_final'] = (order_itens_tratados['list_price'] * order_itens_tratados['quantity']) * (1 - order_itens_tratados['discount'])

# Normalizar list_price
order_itens_tratados.loc[:, 'list_price_normalizado'] = (order_itens_tratados['list_price'] - order_itens_tratados['list_price'].min()) / (order_itens_tratados['list_price'].max() - order_itens_tratados['list_price'].min())

# Padronizar casas decimais
order_itens_tratados.loc[:, 'list_price'] = order_itens_tratados['list_price'].round(2)
order_itens_tratados.loc[:, 'preco_total'] = order_itens_tratados['preco_total'].round(2)
order_itens_tratados.loc[:, 'preco_final'] = order_itens_tratados['preco_final'].round(2)
order_itens_tratados.loc[:, 'list_price_normalizado'] = order_itens_tratados['list_price_normalizado'].round(4)

# Salvar os dados tratados
order_itens_tratados.to_csv('order_items_tratado.csv', index=False)

# Exibir o DataFrame tratado
print("\nDados tratados:")
print(order_itens_tratados.head())