import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine, text

url_itens_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/itens_pedidos.csv'
url_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/pedidos.csv'
url_produto = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/produtos.csv'
url_vendedores = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/vendedores.csv'

dfIP = pd.read_csv(url_itens_pedidos)
dfPe = pd.read_csv(url_pedidos)
dfPr = pd.read_csv(url_produto)
dfVe = pd.read_csv(url_vendedores)

engine = create_engine('sqlite:///:memory:')

dfIP.to_sql('Itens', engine, index=False, if_exists='replace')
dfPe.to_sql('Pedidos', engine, index=False, if_exists='replace')
dfPr.to_sql('Produto', engine, index=False, if_exists='replace')
dfVe.to_sql('Vendedor', engine, index=False, if_exists='replace')

def sqlConDf(query):
    with engine.connect() as conexao:
        consulta = conexao.execute(text(query))
        dados = consulta.fetchall()
        return pd.DataFrame(dados, columns=consulta.keys())

query = '''SELECT condicao AS "Condicao", COUNT(*) AS quantidade 
    FROM Produto 
    GROUP BY condicao;'''
df_condicao = sqlConDf(query)

plt.figure(figsize=(10,5))
plt.bar(df_condicao["Condicao"], df_condicao["quantidade"], color="blue")
plt.title("Condição dos produtos")
plt.xlabel("Condição")
plt.ylabel("Quantidade")

query = '''
SELECT Produto.Produto, SUM(Itens.QUANTIDADE) AS Quantidade
FROM Itens
JOIN Produto ON Itens.PRODUTO_ID = Produto.PRODUTO_ID
GROUP BY Produto.Produto
ORDER BY Quantidade DESC
LIMIT 3;
'''
df_rank = sqlConDf(query)

plt.figure(figsize=(12,8))
plt.barh(df_rank['produto'], df_rank["Quantidade"], color="green")
plt.title("Rank Das 3 Peças Mais Vendidas (Usadas)")
plt.xlabel("Quantidade Vendida")
plt.yticks( fontsize=8)  


query = '''
    SELECT SUM(valor_total) AS Receita_Total
    FROM Itens;
'''
df_receita = sqlConDf(query)

receita_total = df_receita["Receita_Total"].iloc[0]

query = '''
    SELECT Vendedor.nome_vendedor, AVG(Pedidos.pedido_id) AS quantVendas2020
    FROM Pedidos
    JOIN Vendedor ON Vendedor.vendedor_id = Pedidos.vendedor_id
    WHERE strftime('%Y', data_compra) = '2020'
    GROUP BY Vendedor.nome_vendedor
    ORDER BY Vendedor.nome_vendedor desc
    LIMIT 10;
'''
df_2020 = sqlConDf(query)

plt.figure(figsize=(10,6))
plt.bar(df_2020["nome_vendedor"], df_2020["quantVendas2020"], color="red")
plt.title("Vendas em 2020")
plt.xlabel("Vendedores")
plt.ylabel("Quantidade")

query=''' SELECT PRODUTOS.PRODUTO, COUNT (PEDIDOS.PEDIDO_ID) AS TOTAL_PEDIDOS
FROM PEDIDOS, PRODUTOS
WHERE strftime('%Y', data_compra) = '2019' AND PEDIDOS.PRODUTO_ID = PRODUTOS.PRODUTO_ID
GROUP BY PRODUTOS.PRODUTO
ORDER BY TOTAL_PEDIDOS DESC
LIMIT 10;'''

query=''' SELECT Itens.Estado ,Count(*) AS Estados_Vendas
From itens
GROUP BY  Itens.Estado
ORDER BY  Estados_Vendas DESC 
LIMIT 3;'''
dfEstado=sqlConDf(query)

plt.figure(figsize=(10,4))
plt.bar(dfEstado["Estado"],dfEstado["Estados_Vendas"],color="brown")
plt.title("Os 3 Estados com mais vendas",fontsize=10)
plt.xlabel("Estados")
plt.ylabel("Quantidade de Vendas")


query=''' SELECT Vendedor.Nome_vendedor, COUNT(*) AS quantidade
FROM Pedidos
JOIN Vendedor ON Vendedor.Vendedor_id = Pedidos.Vendedor_id
JOIN Itens ON Itens.Pedido_id = Pedidos.Pedido_id
WHERE Itens.Estado = 'BR-SP'
GROUP BY Vendedor.Nome_vendedor
ORDER BY COUNT(*) DESC
LIMIT 3;
'''


dfSp=sqlConDf(query)
print(dfSp.head(3))