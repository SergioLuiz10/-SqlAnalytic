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

query = '''
SELECT condicao AS "Condicao", COUNT(*) AS quantidade 
FROM Produto 
GROUP BY condicao;
'''
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

plt.figure(figsize=(6, 4))
plt.bar(["Receita Total"], [receita_total], color="red")
plt.title("Receita Total das Vendas")
plt.ylabel("Valor (R$)")


print(dfPe.head(15))
print(dfIP.head(15))
print(dfPr.head(15))