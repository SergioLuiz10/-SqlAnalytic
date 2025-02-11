import pandas as pd 
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine, inspect, text

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

inspector = inspect(engine)
query = 'SELECT Condicao FROM Produto'  


def sqlConect(query):
    with engine.connect() as conexao:
        consulta = conexao.execute(text(query))
        dados = consulta.fetchall()
        return pd.DataFrame(dados, columns=consulta.keys())  
       

sqlConect(query)