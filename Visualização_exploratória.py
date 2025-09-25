import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Configurações visuais
plt.style.use('seaborn-v0_8')
sns.set_color_codes(palette='dark')
plt.rcParams['figure.figsize'] = (10, 6)

# Carregamento de Dados
stocks_df = pd.read_csv('stocks.csv')
orders_df = pd.read_csv('orders.csv')
customers_df = pd.read_csv('customers.csv')
products_df = pd.read_csv('products.csv')
order_items_df = pd.read_csv('order_items_tratado.csv')

print("Dados carregados com sucesso!")
print(f"Stocks: {stocks_df.shape}, Orders: {orders_df.shape}, Customers: {customers_df.shape}")
print(f"Products: {products_df.shape}, Order Items: {order_items_df.shape}")


def analise_distribuicao_estoque():
    # Agrupar por loja
    estoque_por_loja = stocks_df.groupby('store_id')['quantity'].agg(
        ['count', 'mean', 'std', 'min', lambda x: x.quantile(0.25), 'median', lambda x: x.quantile(0.75), 'max']).round(
        2)
    estoque_por_loja.columns = ['Contagem', 'Média', 'Desvio Padrão', 'Mínimo', 'Q1 (25%)', 'Mediana (50%)', 'Q3 (75%)',
                                'Máximo']
    print("Tabela de Estatísticas Descritivas:")
    print(estoque_por_loja)

    # Histograma agrupado
    fig, ax = plt.subplots(1, 1)
    for store in stocks_df['store_id'].unique():
        data_loja = stocks_df[stocks_df['store_id'] == store]['quantity']
        ax.hist(data_loja, alpha=0.9, label=f'Loja {store}', bins=20)
    ax.set_xlabel('Quantidade')
    ax.set_ylabel('Nº de produtos na faixa (BIN)')
    ax.set_title('Distribuição de Quantidades em Estoque por Loja')
    ax.legend()
    plt.show()


analise_distribuicao_estoque()


def analise_outliers_estoque():
    outliers_summary = []
    for store in stocks_df['store_id'].unique():
        data = stocks_df[stocks_df['store_id'] == store]['quantity']
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        limite_inf = Q1 - 1.5 * IQR
        limite_sup = Q3 + 1.5 * IQR
        num_outliers = ((data < limite_inf) | (data > limite_sup)).sum()
        outliers_summary.append(
            {'Loja': store, 'Contagem de Outliers': num_outliers, 'Limite Inferior': round(limite_inf, 2),
             'Limite Superior': round(limite_sup, 2)})

    outliers_df = pd.DataFrame(outliers_summary)
    print("Tabela de Limites IQR e Outliers:")
    print(outliers_df)

    # Boxplot
    fig, ax = plt.subplots(1, 1)
    sns.boxplot(data=stocks_df, x='store_id', y='quantity', ax=ax)
    ax.set_title('Boxplot de Quantidades em Estoque por Loja (Sem Outliers)')
    plt.show()


analise_outliers_estoque()


def analise_media_mediana():
    tendencia_df = stocks_df.groupby('store_id')['quantity'].agg(['mean', 'median']).round(2)
    tendencia_df['Diferença (Média - Mediana)'] = (tendencia_df['mean'] - tendencia_df['median']).round(2)
    print("Tabela de Medidas de Tendência Central:")
    print(tendencia_df)

    # Barplot comparativo
    fig, ax = plt.subplots(1, 1)
    x = np.arange(len(tendencia_df))
    width = 0.35
    ax.bar(x - width / 2, tendencia_df['mean'], width, label='Média')
    ax.bar(x + width / 2, tendencia_df['median'], width, label='Mediana')
    ax.set_xlabel('Loja')
    ax.set_ylabel('Unidades em Estoque')
    ax.set_title('Comparação de Média e Mediana por Loja')
    ax.set_xticks(x)
    ax.set_xticklabels(tendencia_df.index)
    ax.legend()
    plt.show()


analise_media_mediana()


def analise_dispersao():
    dispersao_df = stocks_df.groupby('store_id')['quantity'].std().round(2).to_frame('Desvio Padrão')
    print("Tabela de Dispersão:")
    print(dispersao_df)

    # Barplot
    fig, ax = plt.subplots(1, 1)
    sns.barplot(data=dispersao_df.reset_index(), x='store_id', y='Desvio Padrão', ax=ax)
    ax.set_title('Desvio Padrão de Quantidades por Loja')
    plt.show()


analise_dispersao()


def analise_descontos():
    desc_stats = order_items_df['discount'].agg(
        ['count', 'mean', 'std', 'min', lambda x: x.quantile(0.25), 'median', lambda x: x.quantile(0.75), 'max']).round(
        3)
    desc_stats.index = ['Contagem', 'Média', 'Desvio Padrão', 'Mínimo', 'Q1 (25%)', 'Mediana', 'Q3 (75%)', 'Máximo']
    print("Tabela de Estatísticas Descritivas de Descontos:")
    print(desc_stats)

    # Histograma
    fig, ax = plt.subplots(1, 1)
    ax.hist(order_items_df['discount'] * 100, bins=10, alpha=0.7)
    ax.set_xlabel('Desconto (%)')
    ax.set_ylabel('Frequência')
    ax.set_title('Distribuição de Descontos em Itens de Pedidos')
    plt.show()

    # Frequência por faixa
    bins = [0, 0.05, 0.07, 0.10, 0.20, 1.0]
    labels = ['0-5%', '5-7%', '7-10%', '10-20%', '>20%']
    order_items_df['desconto_faixa'] = pd.cut(order_items_df['discount'], bins=bins, labels=labels)
    freq = order_items_df['desconto_faixa'].value_counts().sort_index()
    print("\nFrequência por Faixa de Desconto:")
    print(freq)


analise_descontos()


def analises_clientes_status_pedidos():
    # Status de Pedidos
    orders_clean = orders_df.dropna(subset=['order_status'])
    status_freq = orders_clean['order_status'].value_counts().sort_index().reset_index()
    status_freq.columns = ['Status', 'Frequência']
    status_freq['Porcentagem'] = (status_freq['Frequência'] / len(orders_clean) * 100).round(1)
    print("Tabela de Status de Pedidos (após remoção de NaN):")
    print(status_freq)

    # Mapeamento de Labels
    status_labels = {
        1: 'Pendente',
        2: 'Em Processamento',
        3: 'Rejeitado',
        4: 'Concluído'
    }
    status_freq['Status_Label'] = status_freq['Status'].map(status_labels)

    # Distribuição de Estados dos Clientes
    estados_freq = customers_df['state'].value_counts(normalize=True) * 100
    print("\nDistribuição de Estados (%):")
    print(estados_freq.round(1))

    # Gráficos
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Pie Chart de status
    wedges, texts, autotexts = axs[0].pie(status_freq['Frequência'],
                                          autopct='%1.1f%%',
                                          labels=None,  # Sem rótulos nas fatias
                                          colors=['lightcoral', 'orange', 'lightblue',
                                                  'green'])  # Cores pra cada status (1-4)
    axs[0].set_title('Distribuição de Status de Pedidos')
    axs[0].legend(wedges, status_freq['Status_Label'],
                  title="Status",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

    # Barplot de estados
    estados_freq.plot(kind='bar', ax=axs[1])
    axs[1].set_title('Distribuição de Clientes por Estado (%)')
    axs[1].set_ylabel('Porcentagem')
    plt.tight_layout()
    plt.show()

analises_clientes_status_pedidos()
