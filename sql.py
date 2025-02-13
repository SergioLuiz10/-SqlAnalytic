import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine, text

# URLs dos arquivos CSV
url_itens_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/itens_pedidos.csv'
url_pedidos = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/pedidos.csv'
url_produto = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/produtos.csv'
url_vendedores = 'https://github.com/alura-cursos/SQL-python-integracao/raw/main/TABELAS/vendedores.csv'

# Carrega os DataFrames
dfIP = pd.read_csv(url_itens_pedidos)
dfPe = pd.read_csv(url_pedidos)
dfPr = pd.read_csv(url_produto)
dfVe = pd.read_csv(url_vendedores)

# Cria um banco de dados SQLite em memória
engine = create_engine('sqlite:///:memory:')

# Salva os DataFrames como tabelas no banco
dfIP.to_sql('Itens', engine, index=False, if_exists='replace')
dfPe.to_sql('Pedidos', engine, index=False, if_exists='replace')
dfPr.to_sql('Produto', engine, index=False, if_exists='replace')
dfVe.to_sql('Vendedor', engine, index=False, if_exists='replace')

# Função para executar uma query SQL e retornar um DataFrame
def sqlConDf(query):
    with engine.connect() as conexao:
        consulta = conexao.execute(text(query))
        dados = consulta.fetchall()
        return pd.DataFrame(dados, columns=consulta.keys())

# Consulta 1: Quantidade de produtos por condição
query = '''
SELECT condicao AS "Condicao", COUNT(*) AS quantidade 
FROM Produto 
GROUP BY condicao;
'''
df_condicao = sqlConDf(query)
print(df_condicao)

plt.figure(figsize=(10,5))
plt.bar(df_condicao["Condicao"], df_condicao["quantidade"], color="blue")
plt.title("Condição dos produtos")
plt.xlabel("Condição")
plt.ylabel("Quantidade")
plt.show()

# Consulta 2: Ranking das 3 peças mais vendidas (usadas)
query = '''
SELECT Produto.Produto, SUM(Itens.QUANTIDADE) AS Quantidade
FROM Itens
JOIN Produto ON Itens.PRODUTO_ID = Produto.PRODUTO_ID
GROUP BY Produto.Produto
ORDER BY Quantidade DESC
LIMIT 3;
'''
df_rank = sqlConDf(query)
print(df_rank)

plt.figure(figsize=(10,5))
# Usando a coluna "produto" (minúsculo) conforme retornado no DataFrame
plt.bar(df_rank['produto'], df_rank["Quantidade"], color="green")
plt.title("Rank Das 3 Peças Mais Vendidas (Usadas)")
plt.ylabel("Quantidade Vendida")
plt.xticks( fontsize=8)  
plt.show()
